#!/usr/bin/env python3

"""
Summarize VIBRANT auxiliary metabolic gene (AMG) annotations.

Inputs
------
1. VIBRANT_AMG_individuals TSV
2. Curated KO-to-primary-category mapping TSV

Outputs
-------
1. AMG counts per KO
2. AMG counts per vOTU
3. AMG counts per broad metabolic category
"""

import argparse
from pathlib import Path

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(
        description="Summarize VIBRANT AMG annotations."
    )
    parser.add_argument(
        "amg_individuals",
        help="VIBRANT_AMG_individuals TSV.",
    )
    parser.add_argument(
        "ko_category_mapping",
        help=(
            "TSV containing AMG KO, AMG KO name, and one primary "
            "metabolic Category per KO."
        ),
    )
    parser.add_argument(
        "ko_counts_output",
        help="Output TSV for AMG counts per KO.",
    )
    parser.add_argument(
        "votu_counts_output",
        help="Output TSV for AMG counts per vOTU.",
    )
    parser.add_argument(
        "category_counts_output",
        help="Output TSV for AMG counts per broad category.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    amgs = pd.read_csv(args.amg_individuals, sep="\t")
    mapping = pd.read_csv(args.ko_category_mapping, sep="\t")

    required_amg = {
        "protein",
        "scaffold",
        "AMG KO",
        "AMG KO name",
    }
    missing_amg = required_amg - set(amgs.columns)

    if missing_amg:
        raise ValueError(
            "AMG table is missing required columns: "
            + ", ".join(sorted(missing_amg))
        )

    required_mapping = {
        "AMG KO",
        "AMG KO name",
        "Category",
    }
    missing_mapping = required_mapping - set(mapping.columns)

    if missing_mapping:
        raise ValueError(
            "KO-category mapping is missing required columns: "
            + ", ".join(sorted(missing_mapping))
        )

    # ------------------------------------------------------------
    # AMG counts per KO
    # ------------------------------------------------------------

    ko_counts = (
        amgs.groupby(
            ["AMG KO", "AMG KO name"],
            as_index=False
        )
        .size()
        .rename(columns={"size": "AMG_instances"})
        .sort_values(
            ["AMG_instances", "AMG KO"],
            ascending=[False, True],
        )
    )

    # ------------------------------------------------------------
    # AMG counts per vOTU
    # ------------------------------------------------------------

    votu_counts = (
        amgs.groupby("scaffold")
        .agg(
            AMG_instances=("AMG KO", "size"),
            Unique_KOs=("AMG KO", "nunique"),
        )
        .reset_index()
        .sort_values("scaffold")
    )

    # ------------------------------------------------------------
    # Broad metabolic category counts
    # ------------------------------------------------------------

    duplicate_mapping = mapping["AMG KO"].duplicated(keep=False)

    if duplicate_mapping.any():
        duplicates = sorted(
            mapping.loc[duplicate_mapping, "AMG KO"].unique()
        )
        raise ValueError(
            "KO-category mapping contains duplicate KO entries: "
            + ", ".join(duplicates)
        )

    category_lookup = mapping[
        ["AMG KO", "Category"]
    ].drop_duplicates()

    annotated = amgs.merge(
        category_lookup,
        on="AMG KO",
        how="left",
        validate="many_to_one",
    )

    missing_categories = sorted(
        annotated.loc[
            annotated["Category"].isna(),
            "AMG KO"
        ].dropna().unique()
    )

    if missing_categories:
        raise ValueError(
            "No primary category assigned for AMG KOs: "
            + ", ".join(missing_categories)
        )

    category_counts = (
        annotated.groupby("Category")
        .size()
        .reset_index(name="N_AMG_instances")
        .sort_values(
            ["N_AMG_instances", "Category"],
            ascending=[False, True],
        )
    )

    for path in (
        args.ko_counts_output,
        args.votu_counts_output,
        args.category_counts_output,
    ):
        Path(path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    ko_counts.to_csv(
        args.ko_counts_output,
        sep="\t",
        index=False,
    )

    votu_counts.to_csv(
        args.votu_counts_output,
        sep="\t",
        index=False,
    )

    category_counts.to_csv(
        args.category_counts_output,
        sep="\t",
        index=False,
    )


if __name__ == "__main__":
    main()
