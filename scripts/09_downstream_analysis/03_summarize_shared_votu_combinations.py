#!/usr/bin/env python3

"""
Summarize exact lake combinations for shared ambient vOTUs.

Input
-----
Per-vOTU occupancy table produced by:
02_summarize_votu_occupancy.py

Expected columns:
- n_lakes
- occupancy_class
- lake_combination

Outputs
-------
1. Shared-vOTU table containing only vOTUs present in >=2 lakes.
2. Exact lake-combination summary with:
   - lake_combination
   - n_lakes
   - n_votus
"""

import argparse
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("occupancy_tsv")
    parser.add_argument("shared_votus_output_tsv")
    parser.add_argument("combination_summary_output_tsv")
    return parser.parse_args()


def main():
    args = parse_args()

    occupancy = pd.read_csv(
        args.occupancy_tsv,
        sep="\t",
        index_col=0
    )

    required = {"n_lakes", "occupancy_class", "lake_combination"}
    missing = required - set(occupancy.columns)

    if missing:
        raise ValueError(
            "Input table is missing required columns: "
            + ", ".join(sorted(missing))
        )

    shared = occupancy.loc[
        occupancy["n_lakes"] >= 2
    ].copy()

    shared.to_csv(
        args.shared_votus_output_tsv,
        sep="\t"
    )

    summary = (
        shared
        .groupby(
            ["lake_combination", "n_lakes"],
            as_index=False
        )
        .size()
        .rename(columns={"size": "n_votus"})
        .sort_values(
            ["n_lakes", "n_votus", "lake_combination"],
            ascending=[True, False, True]
        )
    )

    summary.to_csv(
        args.combination_summary_output_tsv,
        sep="\t",
        index=False
    )

    print(f"[DONE] Shared vOTUs: {len(shared)}")
    print(f"[DONE] Exact lake combinations: {len(summary)}")


if __name__ == "__main__":
    main()
