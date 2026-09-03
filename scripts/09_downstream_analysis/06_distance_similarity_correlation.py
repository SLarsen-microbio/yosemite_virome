#!/usr/bin/env python3

"""
Test the relationship between geographic distance and ambient viral
community similarity.

Input
-----
Pairwise lake-comparison table produced by:
05_pairwise_lake_similarity.py

Required columns:
- lake_a
- lake_b
- jaccard
- distance_km

The analysis reports both:
- Spearman rank correlation
- Pearson correlation

One or more lakes may optionally be excluded from the analysis.
"""

import argparse
import pandas as pd
from scipy.stats import pearsonr, spearmanr


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "pairwise_tsv",
        help="Pairwise lake similarity table"
    )

    parser.add_argument(
        "output_tsv",
        help="Output table of correlation statistics"
    )

    parser.add_argument(
        "--exclude-lake",
        action="append",
        default=[],
        help=(
            "Exclude pairwise comparisons containing this lake. "
            "May be supplied more than once."
        )
    )

    return parser.parse_args()


def main():
    args = parse_args()

    df = pd.read_csv(args.pairwise_tsv, sep="\t")

    required = {
        "lake_a",
        "lake_b",
        "jaccard",
        "distance_km"
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            "Input table missing columns: "
            + ", ".join(sorted(missing))
        )

    analysis = df.copy()

    for lake in args.exclude_lake:
        analysis = analysis.loc[
            (analysis["lake_a"] != lake)
            & (analysis["lake_b"] != lake)
        ]

    analysis = analysis.dropna(
        subset=["jaccard", "distance_km"]
    )

    if len(analysis) < 3:
        raise ValueError(
            "At least three pairwise comparisons are required."
        )

    spearman_rho, spearman_p = spearmanr(
        analysis["distance_km"],
        analysis["jaccard"]
    )

    pearson_r, pearson_p = pearsonr(
        analysis["distance_km"],
        analysis["jaccard"]
    )

    results = pd.DataFrame([
        {
            "test": "Spearman",
            "correlation": spearman_rho,
            "p_value": spearman_p,
            "n_pairs": len(analysis)
        },
        {
            "test": "Pearson",
            "correlation": pearson_r,
            "p_value": pearson_p,
            "n_pairs": len(analysis)
        }
    ])

    results.to_csv(
        args.output_tsv,
        sep="\t",
        index=False
    )

    print(f"[DONE] Pairwise comparisons analyzed: {len(analysis)}")
    print(
        f"[DONE] Spearman rho = {spearman_rho:.4f}, "
        f"p = {spearman_p:.4g}"
    )
    print(
        f"[DONE] Pearson r = {pearson_r:.4f}, "
        f"p = {pearson_p:.4g}"
    )


if __name__ == "__main__":
    main()
