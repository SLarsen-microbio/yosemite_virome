#!/usr/bin/env python3

"""
Calculate breadth-filtered viral genome or vOTU RPKM values.

Workflow:
1. Read each sample BAM.
2. Calculate breadth of coverage for each reference sequence:
       breadth = covered bases / reference length
3. Retain detections with breadth >= 0.75.
4. Sum mapped reads across only references passing that threshold.
5. Calculate RPKM for each passing reference:
       RPKM = mapped_reads * 1e9 /
              (reference_length * passing_mapped_reads)
6. Set failing reference/sample combinations to 0.

Software:
    Python 3
    pandas
    SAMtools v1.17

Usage:
    python 03_calculate_rpkm_breadth.py \
        <bam_directory> \
        <sample_metadata.tsv> \
        <output_directory>
"""

from pathlib import Path
import subprocess
import sys

import pandas as pd


BREADTH_THRESHOLD = 0.75


def run_command(command):
    result = subprocess.run(
        command,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout


def get_idxstats(bam_path):
    output = run_command(
        ["samtools", "idxstats", str(bam_path)]
    )

    records = []

    for line in output.strip().splitlines():
        reference, length, mapped, unmapped = line.split("\t")

        if reference == "*":
            continue

        records.append(
            {
                "reference": reference,
                "length": int(length),
                "mapped": int(mapped),
            }
        )

    return pd.DataFrame(records).set_index("reference")


def get_breadth(bam_path, reference, reference_length):
    output = run_command(
        [
            "samtools",
            "depth",
            "-aa",
            "-r",
            reference,
            str(bam_path),
        ]
    )

    covered = 0
    positions = 0

    for line in output.splitlines():
        fields = line.split("\t")

        if len(fields) < 3:
            continue

        depth = int(fields[2])
        positions += 1

        if depth > 0:
            covered += 1

    if positions == 0:
        return 0.0

    return covered / reference_length


def process_sample(sample, bam_dir):
    bam_path = bam_dir / f"{sample}.bam"

    if not bam_path.exists():
        raise FileNotFoundError(
            f"BAM file not found for sample {sample}: {bam_path}"
        )

    print(f"Processing {sample}")

    stats = get_idxstats(bam_path)
    breadth_values = {}

    for reference, row in stats.iterrows():
        if row["mapped"] == 0:
            breadth_values[reference] = 0.0
            continue

        breadth_values[reference] = get_breadth(
            bam_path,
            reference,
            row["length"],
        )

    stats["breadth"] = pd.Series(breadth_values)

    stats["passes_breadth"] = (
        stats["breadth"] >= BREADTH_THRESHOLD
    )

    passing_read_total = stats.loc[
        stats["passes_breadth"],
        "mapped",
    ].sum()

    print(
        f"  References passing breadth filter: "
        f"{stats['passes_breadth'].sum()}"
    )

    print(
        f"  Mapped reads on passing references: "
        f"{passing_read_total}"
    )

    stats["rpkm"] = 0.0

    if passing_read_total > 0:
        passing = stats["passes_breadth"]

        stats.loc[passing, "rpkm"] = (
            stats.loc[passing, "mapped"]
            * 1e9
            / (
                stats.loc[passing, "length"]
                * passing_read_total
            )
        )

    return stats["rpkm"]


def main():
    if len(sys.argv) != 4:
        sys.exit(
            "Usage: python 03_calculate_rpkm_breadth.py "
            "<bam_directory> <sample_metadata.tsv> <output_directory>"
        )

    bam_dir = Path(sys.argv[1])
    metadata_file = Path(sys.argv[2])
    output_dir = Path(sys.argv[3])

    output_dir.mkdir(parents=True, exist_ok=True)

    metadata = pd.read_csv(metadata_file, sep="\t")

    if "sample_id" not in metadata.columns:
        raise ValueError(
            "Metadata file must contain a 'sample_id' column."
        )

    samples = metadata["sample_id"].tolist()
    matrix = {}

    for sample in samples:
        matrix[sample] = process_sample(
            sample,
            bam_dir,
        )

    rpkm_matrix = pd.DataFrame(matrix)
    rpkm_matrix.index.name = "reference"

    output_path = output_dir / "rpkm_matrix_breadth75.tsv"

    rpkm_matrix.to_csv(
        output_path,
        sep="\t",
        float_format="%.4f",
    )

    print(f"\nSaved: {output_path}")


if __name__ == "__main__":
    main()
