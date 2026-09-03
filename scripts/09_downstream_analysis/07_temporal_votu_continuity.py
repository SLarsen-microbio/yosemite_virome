#!/usr/bin/env python3

"""
Calculate temporal continuity of vOTU communities between sample pairs.

The input is a breadth-filtered vOTU RPKM matrix with vOTUs as rows and
samples as columns. RPKM > 0 indicates detection after application of the
breadth-of-coverage threshold upstream.

For each requested sample pair, the script reports:
    - vOTUs detected in sample A
    - vOTUs detected in sample B
    - shared vOTUs
    - fraction of sample A vOTUs detected in sample B
    - fraction of sample B vOTUs detected in sample A
    - symmetric Jaccard similarity

An optional minimum RPKM threshold can be applied for abundance-restricted
comparisons.
"""

import argparse
from pathlib import Path

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(
        description="Calculate temporal vOTU continuity between sample pairs."
    )
    parser.add_argument(
        "rpkm_matrix",
        help="Breadth-filtered vOTU RPKM matrix (TSV; vOTUs rows, samples columns).",
    )
    parser.add_argument(
        "pairs",
        help=(
            "TSV containing comparison_name, sample_a, and sample_b columns."
        ),
    )
    parser.add_argument(
        "output",
        help="Output TSV containing temporal continuity statistics.",
    )
    parser.add_argument(
        "--min-rpkm",
        type=float,
        default=0.0,
        help=(
            "Minimum RPKM required for detection. Default: 0, so any "
            "breadth-filtered RPKM > 0 is considered detected."
        ),
    )
    return parser.parse_args()


def main():
    args = parse_args()

    matrix = pd.read_csv(args.rpkm_matrix, sep="\t", index_col=0)
    pairs = pd.read_csv(args.pairs, sep="\t")

    required = {"comparison_name", "sample_a", "sample_b"}
    missing = required - set(pairs.columns)
    if missing:
        raise ValueError(
            "Pairs table is missing required columns: "
            + ", ".join(sorted(missing))
        )

    results = []

    for row in pairs.itertuples(index=False):
        comparison = row.comparison_name
        sample_a = row.sample_a
        sample_b = row.sample_b

        for sample in (sample_a, sample_b):
            if sample not in matrix.columns:
                raise ValueError(
                    f"Sample '{sample}' not found in RPKM matrix."
                )

        detected_a = set(
            matrix.index[matrix[sample_a] > args.min_rpkm]
        )
        detected_b = set(
            matrix.index[matrix[sample_b] > args.min_rpkm]
        )

        shared = detected_a & detected_b
        union = detected_a | detected_b

        n_a = len(detected_a)
        n_b = len(detected_b)
        n_shared = len(shared)

        persistence_a_to_b = n_shared / n_a if n_a else 0.0
        persistence_b_to_a = n_shared / n_b if n_b else 0.0
        jaccard = n_shared / len(union) if union else 0.0

        results.append(
            {
                "comparison_name": comparison,
                "sample_a": sample_a,
                "sample_b": sample_b,
                "min_rpkm": args.min_rpkm,
                "sample_a_detected_votus": n_a,
                "sample_b_detected_votus": n_b,
                "shared_votus": n_shared,
                "sample_a_persistence_fraction": persistence_a_to_b,
                "sample_b_persistence_fraction": persistence_b_to_a,
                "jaccard_similarity": jaccard,
            }
        )

    output = pd.DataFrame(results)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(args.output, sep="\t", index=False)


if __name__ == "__main__":
    main()
