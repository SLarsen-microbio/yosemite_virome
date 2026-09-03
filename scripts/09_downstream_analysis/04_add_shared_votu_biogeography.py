#!/usr/bin/env python3

"""
Add watershed and geographic context to shared ambient vOTUs.

Inputs
------
1. Shared-vOTU table produced by:
   03_summarize_shared_votu_combinations.py

   Required columns:
   - n_lakes
   - lake_combination

2. Lake metadata TSV with one row per lake and columns:
   - lake
   - huc8
   - latitude
   - longitude

Output
------
One row per shared vOTU containing:
- n_lakes
- lake_combination
- watershed_class
- max_distance_km

watershed_class is:
- within_huc8: all occupied lakes are in the same HUC8
- cross_huc8: occupied lakes span more than one HUC8

Maximum geographic distance is the greatest pairwise haversine
distance among lakes occupied by that vOTU.
"""

import argparse
from itertools import combinations
from math import asin, cos, radians, sin, sqrt

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("shared_votus_tsv")
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

    shared = pd.read_csv(
        args.shared_votus_tsv,
        sep="\t",
        index_col=0
    )

    lakes = pd.read_csv(args.lake_metadata_tsv, sep="\t")

    required_shared = {"n_lakes", "lake_combination"}
    required_lakes = {"lake", "huc8", "latitude", "longitude"}

    missing_shared = required_shared - set(shared.columns)
    missing_lakes = required_lakes - set(lakes.columns)

    if missing_shared:
        raise ValueError(
            "Shared-vOTU table missing columns: "
            + ", ".join(sorted(missing_shared))
        )

    if missing_lakes:
        raise ValueError(
            "Lake metadata missing columns: "
            + ", ".join(sorted(missing_lakes))
        )

    if lakes["lake"].duplicated().any():
        duplicates = lakes.loc[
            lakes["lake"].duplicated(),
            "lake"
        ].tolist()

        raise ValueError(
            "Duplicate lake names in metadata: "
            + ", ".join(duplicates)
        )

    lake_info = lakes.set_index("lake")

    watershed_classes = []
    max_distances = []

    for _, row in shared.iterrows():
        occupied = [
            x.strip()
            for x in str(row["lake_combination"]).split(";")
            if x.strip()
        ]

        missing = [
            lake for lake in occupied
            if lake not in lake_info.index
        ]

        if missing:
            raise ValueError(
                "Lakes missing from metadata: "
                + ", ".join(missing)
            )

        if len(occupied) != int(row["n_lakes"]):
            raise ValueError(
                f"n_lakes does not match lake_combination: "
                f"{row['lake_combination']}"
            )

        huc8_values = {
            str(lake_info.loc[lake, "huc8"])
            for lake in occupied
        }

        watershed_classes.append(
            "within_huc8"
            if len(huc8_values) == 1
            else "cross_huc8"
        )

        distances = []

        for lake_a, lake_b in combinations(occupied, 2):
            a = lake_info.loc[lake_a]
            b = lake_info.loc[lake_b]

            distances.append(
                haversine_km(
                    float(a["latitude"]),
                    float(a["longitude"]),
                    float(b["latitude"]),
                    float(b["longitude"])
                )
            )

        max_distances.append(
            max(distances) if distances else 0.0
        )

    result = shared.copy()
    result["watershed_class"] = watershed_classes
    result["max_distance_km"] = [
        round(x, 2) for x in max_distances
    ]

    result.to_csv(args.output_tsv, sep="\t")

    print(f"[DONE] Shared vOTUs: {len(result)}")
    print(
        "[DONE] Within-HUC8:",
        (result["watershed_class"] == "within_huc8").sum()
    )
    print(
        "[DONE] Cross-HUC8:",
        (result["watershed_class"] == "cross_huc8").sum()
    )


if __name__ == "__main__":
    main()
