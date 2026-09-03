#!/usr/bin/env python3

"""
Calculate pairwise ambient vOTU Jaccard similarity between lakes and
relate it to geographic distance.

Inputs
------
1. Lake-level ambient vOTU presence/absence table produced by:
   01_build_ambient_votu_presence.py

   Expected columns:
   - one binary column per lake
   - n_lakes

2. Lake metadata TSV with columns:
   - lake
   - latitude
   - longitude
   - huc8

Output
------
Pairwise lake table containing:
- lake_a
- lake_b
- shared_votus
- union_votus
- jaccard
- distance_km
- watershed_class
"""

import argparse
from itertools import combinations
from math import asin, cos, radians, sin, sqrt

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("presence_tsv")
    parser.add_argument("lake_metadata_tsv")
    parser.add_argument("output_tsv")
    return parser.parse_args()


def haversine_km(lat1, lon1, lat2, lon2):
    radius_km = 6371.0088

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    return 2 * radius_km * asin(sqrt(a))


def main():
    args = parse_args()

    presence = pd.read_csv(
        args.presence_tsv,
        sep="\t",
        index_col=0
    )

    metadata = pd.read_csv(
        args.lake_metadata_tsv,
        sep="\t"
    )

    required_meta = {"lake", "latitude", "longitude", "huc8"}
    missing = required_meta - set(metadata.columns)

    if missing:
        raise ValueError(
            "Lake metadata missing columns: "
            + ", ".join(sorted(missing))
        )

    lake_columns = [
        col for col in presence.columns
        if col != "n_lakes"
    ]

    meta_lakes = set(metadata["lake"].astype(str))

    missing_meta = [
        lake for lake in lake_columns
        if lake not in meta_lakes
    ]

    if missing_meta:
        raise ValueError(
            "Presence-table lakes missing from metadata: "
            + ", ".join(missing_meta)
        )

    info = metadata.set_index("lake")

    rows = []

    for lake_a, lake_b in combinations(lake_columns, 2):
        a = presence[lake_a].astype(bool)
        b = presence[lake_b].astype(bool)

        shared = int((a & b).sum())
        union = int((a | b).sum())

        jaccard = shared / union if union else 0.0

        meta_a = info.loc[lake_a]
        meta_b = info.loc[lake_b]

        distance = haversine_km(
            float(meta_a["latitude"]),
            float(meta_a["longitude"]),
            float(meta_b["latitude"]),
            float(meta_b["longitude"])
        )

        watershed_class = (
            "same_huc8"
            if str(meta_a["huc8"]) == str(meta_b["huc8"])
            else "cross_huc8"
        )

        rows.append({
            "lake_a": lake_a,
            "lake_b": lake_b,
            "shared_votus": shared,
            "union_votus": union,
            "jaccard": jaccard,
            "distance_km": round(distance, 2),
            "watershed_class": watershed_class
        })

    result = pd.DataFrame(rows)

    result.to_csv(
        args.output_tsv,
        sep="\t",
        index=False
    )

    print(
        f"[DONE] Wrote {len(result)} pairwise lake comparisons."
    )


if __name__ == "__main__":
    main()
