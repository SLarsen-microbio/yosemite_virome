#!/usr/bin/env python3

"""
Calculate the fraction of viral community RPKM attributable to
AMG-carrying vOTUs.

Inputs
------
1. VIBRANT_AMG_individuals TSV
2. Breadth-filtered 532-vOTU RPKM matrix

The RPKM matrix must contain:
    rows = vOTUs
    columns = samples
    values = breadth-filtered RPKM

Output columns
--------------
Sample
Total_viral_RPKM
AMG_vOTU_RPKM
Non_AMG_vOTU_RPKM
AMG_percent_of_viral_RPKM
AMG_vOTUs_detected
Total_vOTUs_detected
"""

import argparse
from pathlib import Path

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Calculate the contribution of AMG-carrying vOTUs "
            "to total viral RPKM."
        )
    )
    parser.add_argument(
        "amg_individuals",
        help="VIBRANT_AMG_individuals TSV.",
    )
    parser.add_argument(
        "rpkm_matrix",
        help=(
            "Breadth-filtered vOTU RPKM matrix "
            "(TSV; vOTUs rows, samples columns)."
        ),
    )
    parser.add_argument(
        "output",
        help="Output TSV containing AMG-vOTU abundance fractions.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    amgs = pd.read_csv(
        args.amg_individuals,
        sep="\t",
    )

    rpkm = pd.read_csv(
        args.rpkm_matrix,
        sep="\t",
        index_col=0,
    )

    if "scaffold" not in amgs.columns:
        raise ValueError(
            "AMG table must contain a 'scaffold' column."
        )

    if rpkm.empty:
        raise ValueError("RPKM matrix is empty.")

    if rpkm.isna().any().any():
        raise ValueError(
            "RPKM matrix contains missing values."
        )

    if (rpkm < 0).any().any():
        raise ValueError(
            "RPKM matrix contains negative values."
        )

    amg_votus = set(
        amgs["scaffold"]
        .dropna()
        .astype(str)
        .str.replace(r"_fragment_\d+$", "", regex=True)
        .unique()
    )

    missing_amg_votus = sorted(
        amg_votus - set(rpkm.index.astype(str))
    )

    if missing_amg_votus:
        raise ValueError(
            "AMG-carrying vOTUs not found in RPKM matrix: "
            + ", ".join(missing_amg_votus[:20])
            + (
                " ..."
                if len(missing_amg_votus) > 20
                else ""
            )
        )

    results = []

    for sample in rpkm.columns:
        sample_rpkm = rpkm[sample]

        detected = sample_rpkm > 0

        total_viral_rpkm = sample_rpkm.sum()

        amg_mask = rpkm.index.isin(amg_votus)

        amg_votu_rpkm = sample_rpkm.loc[
            amg_mask
        ].sum()

        non_amg_votu_rpkm = (
            total_viral_rpkm - amg_votu_rpkm
        )

        if total_viral_rpkm > 0:
            amg_percent = (
                amg_votu_rpkm
                / total_viral_rpkm
                * 100
            )
        else:
            amg_percent = 0.0

        amg_votus_detected = (
            (sample_rpkm.loc[amg_mask] > 0)
            .sum()
        )

        total_votus_detected = detected.sum()

        results.append(
            {
                "Sample": sample,
                "Total_viral_RPKM": total_viral_rpkm,
                "AMG_vOTU_RPKM": amg_votu_rpkm,
                "Non_AMG_vOTU_RPKM": non_amg_votu_rpkm,
                "AMG_percent_of_viral_RPKM": amg_percent,
                "AMG_vOTUs_detected": amg_votus_detected,
                "Total_vOTUs_detected": total_votus_detected,
            }
        )

    output = pd.DataFrame(results)

    Path(args.output).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.to_csv(
        args.output,
        sep="\t",
        index=False,
        float_format="%.4f",
    )


if __name__ == "__main__":
    main()
