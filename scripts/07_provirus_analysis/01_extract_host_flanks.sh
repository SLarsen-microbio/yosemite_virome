#!/usr/bin/env bash
set -euo pipefail

# Extract host flanking regions surrounding CheckV-identified proviruses.
#
# Inputs:
#   1. Host contig FASTA
#   2. TSV containing:
#        contig_id
#        provirus_start
#        provirus_end
#
# Output:
#   FASTA of non-proviral flanking regions for host assignment.
#
# Requires:
#   samtools 1.17

if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <contigs.fna> <provirus_coordinates.tsv> <output.fna>"
    exit 1
fi

CONTIGS="$1"
COORDS="$2"
OUT="$3"

samtools faidx "${CONTIGS}"

: > "${OUT}"

while IFS=$'\t' read -r CONTIG START END; do
    [[ "${CONTIG}" == "contig_id" ]] && continue

    CONTIG_LEN=$(samtools faidx "${CONTIGS}" "${CONTIG}" | \
        grep -v '^>' | tr -d '\n' | wc -c)

    if (( START > 1 )); then
        samtools faidx "${CONTIGS}" "${CONTIG}:1-$((START-1))" >> "${OUT}"
    fi

    if (( END < CONTIG_LEN )); then
        samtools faidx "${CONTIGS}" "${CONTIG}:$((END+1))-${CONTIG_LEN}" >> "${OUT}"
    fi

done < "${COORDS}"

echo "[DONE] Host flanking regions written to ${OUT}"
