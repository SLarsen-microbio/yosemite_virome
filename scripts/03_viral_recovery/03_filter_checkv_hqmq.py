#!/usr/bin/env python3

"""
Retain viral genomes classified by CheckV as Complete, High-quality,
or Medium-quality.

Usage:
    python 03_filter_checkv_hqmq.py \
        <quality_summary.tsv> \
        <viral_fasta> \
        <output_fasta>
"""

import csv
import sys


KEEP_QUALITIES = {
    "Complete",
    "High-quality",
    "Medium-quality",
}


def read_retained_ids(summary_file):
    retained = set()

    with open(summary_file, newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")

        required = {"contig_id", "checkv_quality"}
        missing = required - set(reader.fieldnames or [])

        if missing:
            raise ValueError(
                "Missing required column(s) in CheckV quality summary: "
                + ", ".join(sorted(missing))
            )

        for row in reader:
            if row["checkv_quality"] in KEEP_QUALITIES:
                retained.add(row["contig_id"])

    return retained


def filter_fasta(input_fasta, output_fasta, retained_ids):
    kept = 0
    write_sequence = False

    with open(input_fasta) as infile, open(output_fasta, "w") as outfile:
        for line in infile:
            if line.startswith(">"):
                seq_id = line[1:].split()[0]
                write_sequence = seq_id in retained_ids

                if write_sequence:
                    kept += 1
                    outfile.write(line)
            elif write_sequence:
                outfile.write(line)

    return kept


def main():
    if len(sys.argv) != 4:
        sys.exit(
            "Usage: python 03_filter_checkv_hqmq.py "
            "<quality_summary.tsv> <viral_fasta> <output_fasta>"
        )

    summary_file = sys.argv[1]
    viral_fasta = sys.argv[2]
    output_fasta = sys.argv[3]

    retained_ids = read_retained_ids(summary_file)

    kept = filter_fasta(
        viral_fasta,
        output_fasta,
        retained_ids,
    )

    if kept != len(retained_ids):
        raise RuntimeError(
            f"CheckV summary contained {len(retained_ids)} retained genomes, "
            f"but only {kept} were found in the FASTA."
        )

    print(f"[DONE] Retained {kept} Complete/HQ/MQ viral genomes")
    print(f"[INFO] Output: {output_fasta}")


if __name__ == "__main__":
    main()
