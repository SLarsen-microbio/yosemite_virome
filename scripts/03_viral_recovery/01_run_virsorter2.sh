#!/usr/bin/env bash
set -euo pipefail

# Identify viral sequences in assembled metagenomic contigs using VirSorter2.
#
# Software:
#   VirSorter2 v2.2.4
#
# Parameters:
#   minimum viral sequence length: 5,000 bp
#   viral groups: all
#   threads: 16
#
# Usage:
#   bash 01_run_virsorter2.sh <sample_id> <contigs.fasta>

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <sample_id> <contigs.fasta>"
    exit 1
fi

SAMPLE="$1"
CONTIGS="$2"

THREADS=16
OUTDIR="results/virsorter2/${SAMPLE}"

mkdir -p "results/virsorter2"

echo "[STEP] Running VirSorter2 for ${SAMPLE}"

virsorter run \
    -w "${OUTDIR}" \
    -i "${CONTIGS}" \
    --min-length 5000 \
    -j "${THREADS}" \
    all

echo "[DONE] VirSorter2 complete for ${SAMPLE}"
echo "[INFO] Output directory: ${OUTDIR}"
