#!/usr/bin/env bash
set -euo pipefail

# Generate circular genome maps from Pharokka annotations.
#
# Usage:
#   03_plot_complete_genomes.sh <pharokka_output_dir> <output_dir>
#
# Requires:
#   Pharokka plotter utility

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <pharokka_output_dir> <output_dir>"
    exit 1
fi

PHAROKKA_OUT="$1"
OUTDIR="$2"

mkdir -p "${OUTDIR}"

pharokka_plotter.py \
    -i "${PHAROKKA_OUT}" \
    -o "${OUTDIR}"

echo "[DONE] Circular genome plots written to ${OUTDIR}"
