#!/usr/bin/env bash
set -euo pipefail

# Assemble paired-end metagenomic reads and retain contigs >=1,000 bp.
#
# Software:
#   MEGAHIT v1.1.5
#
# MEGAHIT was run with 16 threads and otherwise default parameters.
#
# Usage:
#   bash 01_assemble_megahit.sh <sample_id> <read1.fastq.gz> <read2.fastq.gz>

if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <sample_id> <read1.fastq.gz> <read2.fastq.gz>"
    exit 1
fi

SAMPLE="$1"
READ1="$2"
READ2="$3"

THREADS=16
OUTDIR="results/megahit/${SAMPLE}"
FILTERED_DIR="results/contigs_ge1000"

mkdir -p \
    "results/megahit" \
    "${FILTERED_DIR}"

echo "[STEP] Assembling ${SAMPLE}"

megahit \
    -1 "${READ1}" \
    -2 "${READ2}" \
    -o "${OUTDIR}" \
    -t "${THREADS}"

echo "[STEP] Retaining contigs >=1,000 bp"

awk '
    /^>/ {
        if (seq != "" && length(seq) >= 1000) {
            print header
            print seq
        }
        header=$0
        seq=""
        next
    }
    {
        seq=seq $0
    }
    END {
        if (seq != "" && length(seq) >= 1000) {
            print header
            print seq
        }
    }
' "${OUTDIR}/final.contigs.fa" \
    > "${FILTERED_DIR}/${SAMPLE}.contigs_ge1000.fa"

echo "[DONE] Assembly complete for ${SAMPLE}"
echo "[INFO] Filtered contigs: ${FILTERED_DIR}/${SAMPLE}.contigs_ge1000.fa"
