#!/usr/bin/env bash
set -euo pipefail

# Annotate auxiliary metabolic genes (AMGs) in the corrected
# 532-vOTU representative catalog using VIBRANT.
#
# Usage:
#   ./01_run_vibrant.sh <votu_representatives.fna> <output_directory> [threads]
#
# Final analysis:
#   VIBRANT v1.2.1
#   Input: 532-vOTU representative catalog
#   Mode: virome
#   Threads: 8

if [[ $# -lt 2 || $# -gt 3 ]]; then
    echo "Usage: $0 <votu_representatives.fna> <output_directory> [threads]" >&2
    exit 1
fi

INPUT="$1"
OUTDIR="$2"
THREADS="${3:-8}"

if [[ ! -f "${INPUT}" ]]; then
    echo "ERROR: Input FASTA not found: ${INPUT}" >&2
    exit 1
fi

mkdir -p "${OUTDIR}"

VIBRANT_run.py \
    -i "${INPUT}" \
    -folder "${OUTDIR}" \
    -t "${THREADS}" \
    -virome
