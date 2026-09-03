#!/usr/bin/env bash
set -euo pipefail

# Identify CRISPR arrays and extract spacer sequences with MinCED.
#
# Usage:
#   ./03_run_minced.sh <bacterial_contigs.fna> <output_prefix>
#
# Produces:
#   <output_prefix>.gff
#   <output_prefix>_spacers.fna

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <bacterial_contigs.fna> <output_prefix>" >&2
    exit 1
fi

CONTIGS="$1"
PREFIX="$2"

if [[ ! -f "${CONTIGS}" ]]; then
    echo "ERROR: Input FASTA not found: ${CONTIGS}" >&2
    exit 1
fi

mkdir -p "$(dirname "${PREFIX}")"

minced \
    -gff "${PREFIX}.gff" \
    -spacers "${PREFIX}_spacers.fna" \
    "${CONTIGS}"
