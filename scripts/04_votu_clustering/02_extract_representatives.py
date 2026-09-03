#!/usr/bin/env python3

"""
Extract representative viral genomes from an aniclust cluster table.

The aniclust output is expected to be headerless, with the representative
genome ID in the first tab-delimited column.

Usage:
    python 02_extract_representatives.py \
        <votu_clusters.tsv> \
        <all_genomes.fna> \
        <representatives.fna>
"""

import sys


def read_representatives(cluster_file):
    representatives = []

    with open(cluster_file) as handle:
        for line in handle:
            line = line.rstrip("\n")

            if not line:
                continue

            representative = line.split("\t", 1)[0]
            representatives.append(representative)

    if not representatives:
        raise ValueError("No representative genome IDs found in cluster table.")

    if len(representatives) != len(set(representatives)):
        raise ValueError("Duplicate representative IDs found in cluster table.")

    return representatives


def read_fasta(fasta_file):
    sequences = {}
    current_id = None
    current_header = None
    current_sequence = []

    with open(fasta_file) as handle:
        for line in handle:
            line = line.rstrip("\n")

            if line.startswith(">"):
                if current_id is not None:
                    sequences[current_id] = (
                        current_header,
                        "".join(current_sequence),
                    )

                current_header = line
                current_id = line[1:].split()[0]
                current_sequence = []
            else:
                current_sequence.append(line)

        if current_id is not None:
            sequences[current_id] = (
                current_header,
                "".join(current_sequence),
            )

    return sequences


def main():
    if len(sys.argv) != 4:
        sys.exit(
            "Usage: python 02_extract_representatives.py "
            "<votu_clusters.tsv> <all_genomes.fna> <representatives.fna>"
        )

    cluster_file = sys.argv[1]
    fasta_file = sys.argv[2]
    output_file = sys.argv[3]

    representatives = read_representatives(cluster_file)
    sequences = read_fasta(fasta_file)

    missing = [seq_id for seq_id in representatives if seq_id not in sequences]

    if missing:
        raise RuntimeError(
            f"{len(missing)} representative genome(s) were not found "
            f"in the input FASTA. First missing ID: {missing[0]}"
        )

    with open(output_file, "w") as outfile:
        for seq_id in representatives:
            header, sequence = sequences[seq_id]
            outfile.write(f"{header}\n{sequence}\n")

    print(f"[DONE] Extracted {len(representatives)} representative genomes")
    print(f"[INFO] Output: {output_file}")


if __name__ == "__main__":
    main()
