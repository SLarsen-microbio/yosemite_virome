#!/usr/bin/env bash
set -euo pipefail

# Assign taxonomy and annotate retained viral genomes with geNomad.
#
# This step is run on the Complete/High-quality/Medium-quality viral
# genome set retained after CheckV filtering.
#
# Software:
#   geNomad v1.12.0
#   geNomad database v1.9
#
# Parameters from the final analysis:
#   sensitivity = 4.2
#   e-value = 0.001
#
# Usage:
#   bash 04_run_genomad_taxonomy.sh \
#       <viral_genomes.fna> \
#       <genomad_database>

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <viral_genomes.fna> <genomad_database>"
    exit 1
fi

GENOMES="$1"
GENOMAD_DB="$2"

OUTDIR="results/genomad"
THREADS=32

mkdir -p "${OUTDIR}"

genomad annotate \
    "${GENOMES}" \
    "${OUTDIR}" \
    "${GENOMAD_DB}" \
    --threads "${THREADS}" \
    --sensitivity 4.2 \
    --evalue 0.001

echo "[DONE] geNomad annotation and taxonomy complete"
