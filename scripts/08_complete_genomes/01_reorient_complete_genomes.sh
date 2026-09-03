#!/usr/bin/env bash
set -euo pipefail

# Reorient CheckV-complete viral genomes prior to annotation.
#
# Complete genomes supported by terminal-repeat evidence were reoriented
# using Dnaapler before Pharokka annotation.
#
# Usage:
#   01_reorient_complete_genomes.sh <complete_genomes.fna>
#
# Requires:
#   Dnaapler

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <complete_genomes.fna>"
    exit 1
fi

GENOMES="$1"
OUTDIR="results/complete_genomes/dnaapler"

mkdir -p "${OUTDIR}"

dnaapler all \
    -i "${GENOMES}" \
    -o "${OUTDIR}" \
    -f

echo "[DONE] Reoriented genomes written to ${OUTDIR}"
