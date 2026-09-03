#!/usr/bin/env python3

"""
Build lake-level ambient vOTU presence/absence from a breadth-filtered
vOTU RPKM matrix.

Input RPKM values are expected to have already been set to zero for
sample-vOTU combinations with <75% breadth of coverage.

Inputs
------
1. Breadth-filtered vOTU RPKM matrix
   - rows: vOTU IDs
   - columns: sample IDs

2. Sample metadata TSV containing:
   - sample_id
   - lake
   - ambient

The `ambient` column should identify samples included in the ambient
biogeography analysis using TRUE/FALSE values.

Output
------
TSV with one row per vOTU and one binary presence/absence column per lake.
A vOTU is present in a lake if it has RPKM > 0 in at least one ambient
sample from that lake.
"""

import argparse
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("rpkm_matrix")
    parser.add_argument("metadata_tsv")
    parser.add_argument("output_tsv")
    return parser.parse_args()


def main():
    args = parse_args()

    rpkm = pd.read_csv(args.rpkm_matrix, sep="\t", index_col=0)
    metadata = pd.read_csv(args.metadata_tsv, sep="\t")

    required = {"sample_id", "lake", "ambient"}
    missing = required - set(metadata.columns)
    if missing:
        raise ValueError(
            f"Metadata is missing required columns: {', '.join(sorted(missing))}"
        )

    metadata["sample_id"] = metadata["sample_id"].astype(str)
    metadata["lake"] = metadata["lake"].astype(str)

    ambient_mask = (
        metadata["ambient"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin({"true", "t", "1", "yes", "y"})
    )
    ambient_meta = metadata.loc[ambient_mask].copy()

    if ambient_meta.empty:
        raise ValueError("No ambient samples were identified in metadata.")

    missing_samples = [
        sample
        for sample in ambient_meta["sample_id"]
        if sample not in rpkm.columns
    ]
    if missing_samples:
        raise ValueError(
            "Ambient samples missing from RPKM matrix: "
            + ", ".join(missing_samples)
        )

    lake_presence = {}

    for lake, group in ambient_meta.groupby("lake", sort=True):
        samples = group["sample_id"].tolist()
        lake_presence[lake] = (rpkm[samples] > 0).any(axis=1).astype(int)

    presence = pd.DataFrame(lake_presence, index=rpkm.index)
    presence.index.name = rpkm.index.name or "votu_id"

    presence["n_lakes"] = presence.sum(axis=1)

    presence.to_csv(args.output_tsv, sep="\t")

    print(
        f"[DONE] Wrote ambient lake-level presence for "
        f"{presence.shape[0]} vOTUs across {len(lake_presence)} lakes."
    )


if __name__ == "__main__":
    main()
