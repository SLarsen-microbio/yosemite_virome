#!/usr/bin/env bash
set -euo pipefail

# Match CRISPR spacers against the viral genome catalog.
#
# Workflow:
#   1. Build a nucleotide BLAST database from viral genomes.
#   2. Search CRISPR spacers against the viral database.
#   3. Retain matches meeting:
#        >=95% nucleotide identity
#        >=95% query coverage
#        e-value <= 1e-5
#
# Requires:
#   NCBI BLAST+

if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <spacers.fna> <viral_genomes.fna> <output.tsv>"
    exit 1
fi

SPACERS="$1"
VIRUSES="$2"
OUT="$3"

DB_PREFIX="results/provirus_analysis/viral_spacer_db"

mkdir -p results/provirus_analysis

makeblastdb \
    -in "${VIRUSES}" \
    -dbtype nucl \
    -out "${DB_PREFIX}"

blastn \
    -query "${SPACERS}" \
    -db "${DB_PREFIX}" \
    -task blastn-short \
    -perc_identity 95 \
    -qcov_hsp_perc 95 \
    -evalue 1e-5 \
    -outfmt '6 qseqid sseqid pident length qlen qcovhsp evalue bitscore' \
    -out "${OUT}"

echo "[DONE] CRISPR spacer matches written to ${OUT}"
