#!/usr/bin/env bash
set -euo pipefail

# Assess viral genome quality using CheckV.
#
# Software:
#   CheckV v1.0.3
#   CheckV database v1.5
#
# Parameters:
#   workflow: end_to_end
#   threads: 16
#
# Usage:
#   bash 02_run_checkv.sh <sample_id> <viral_fasta> <checkv_database>
#
# Example:
#   bash 02_run_checkv.sh sample1 final-viral-combined.fa /path/to/checkv-db-v1.5

if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <sample_id> <viral_fasta> <checkv_database>"
    exit 1
fi

SAMPLE="$1"
VIRAL_FASTA="$2"
CHECKVDB="$3"

THREADS=16
OUTDIR="results/checkv/${SAMPLE}"

mkdir -p "results/checkv"

if [[ -e "${OUTDIR}" ]]; then
    echo "[ERROR] Output directory already exists: ${OUTDIR}"
    echo "[ERROR] Remove it or move it before rerunning CheckV."
    exit 1
fi

echo "[STEP] Running CheckV for ${SAMPLE}"

checkv end_to_end \
    "${VIRAL_FASTA}" \
    "${OUTDIR}" \
    -d "${CHECKVDB}" \
    -t "${THREADS}"

echo "[DONE] CheckV complete for ${SAMPLE}"
echo "[INFO] Output directory: ${OUTDIR}"
