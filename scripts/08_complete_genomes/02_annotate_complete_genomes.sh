#!/usr/bin/env bash
set -euo pipefail

# Annotate reoriented complete viral genomes with Pharokka.
#
# Complete genomes were reoriented with Dnaapler prior to annotation.
# Pharokka v1.9.1 was used for functional annotation.
#
# Usage:
#   02_annotate_complete_genomes.sh <reoriented_genomes.fna> <pharokka_database>
#
# Requires:
#   Pharokka v1.9.1

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <reoriented_genomes.fna> <pharokka_database>"
    exit 1
fi

GENOMES="$1"
PHAROKKA_DB="$2"
OUTDIR="results/complete_genomes/pharokka"

mkdir -p "${OUTDIR}"

pharokka.py \
    -i "${GENOMES}" \
    -o "${OUTDIR}" \
    -d "${PHAROKKA_DB}" \
    -t 16 \
    --force

echo "[DONE] Pharokka annotation written to ${OUTDIR}"
