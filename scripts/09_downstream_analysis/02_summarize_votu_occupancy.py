#!/usr/bin/env python3

"""
Summarize ambient vOTU occupancy across lakes.

Input
-----
Lake-level ambient vOTU presence/absence table produced by
01_build_ambient_votu_presence.py.

Expected columns:
- one binary column per lake
- n_lakes

Outputs
-------
1. Per-vOTU occupancy table including:
   - n_lakes
   - occupancy_class
   - lake_combination

2. Occupancy summary table with counts of vOTUs detected in:
   - 1 lake
   - 2 lakes
   - 3 lakes
   - 4 lakes
   - 5 lakes
"""

import argparse
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("presence_tsv")
    parser.add_argument("occupancy_output_tsv")
    parser.add_argument("summary_output_tsv")
    return parser.parse_args()


def main():
    args = parse_args()

    df = pd.read_csv(args.presence_tsv, sep="\t", index_col=0)

    if "n_lakes" not in df.columns:
        raise ValueError("Input table must contain an 'n_lakes' column.")

    lake_columns = [c for c in df.columns if c != "n_lakes"]

    if not lake_columns:
        raise ValueError("No lake presence columns were found.")

    for col in lake_columns:
        values = set(df[col].dropna().unique())
        if not values.issubset({0, 1}):
            raise ValueError(
                f"Lake column '{col}' contains values other than 0/1."
            )

    calculated_n_lakes = df[lake_columns].sum(axis=1)

    if not calculated_n_lakes.equals(df["n_lakes"]):
        raise ValueError(
            "Existing n_lakes values do not match the lake presence columns."
        )

    def lake_combination(row):
        lakes = [lake for lake in lake_columns if row[lake] == 1]
        return ";".join(lakes)

    occupancy = pd.DataFrame(index=df.index)
    occupancy.index.name = df.index.name or "votu_id"
    occupancy["n_lakes"] = df["n_lakes"]
    occupancy["occupancy_class"] = occupancy["n_lakes"].apply(
        lambda n: (
            "not_detected" if n == 0
            else "lake_specific" if n == 1
            else "shared"
        )
    )
    occupancy["lake_combination"] = df.apply(lake_combination, axis=1)

    occupancy.to_csv(args.occupancy_output_tsv, sep="\t")

    summary = (
        occupancy["n_lakes"]
        .value_counts()
        .sort_index()
        .rename_axis("n_lakes")
        .reset_index(name="n_votus")
    )

    summary.to_csv(args.summary_output_tsv, sep="\t", index=False)

    n_total = len(occupancy)
    n_specific = (occupancy["n_lakes"] == 1).sum()
    n_shared = (occupancy["n_lakes"] >= 2).sum()

    print(f"[DONE] Total ambient vOTUs: {n_total}")
    print(f"[DONE] Lake-specific vOTUs: {n_specific}")
    print(f"[DONE] Shared vOTUs: {n_shared}")


if __name__ == "__main__":
    main()
