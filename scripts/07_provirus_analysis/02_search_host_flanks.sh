#!/usr/bin/env bash
set -euo pipefail

# Search provirus flanking regions against NCBI databases for host assignment.
#
# Workflow:
#   1. BLASTn using megablast for close nucleotide matches.
#   2. BLASTx against nr for cases without informative nucleotide matches.
#
# Inputs:
#   1. FASTA of host flanking regions
#   2. Output prefix
#
# Requires:
#   NCBI BLAST+
#
# Note:
#   This script assumes remote NCBI searches. Large jobs may be rate-limited
#   or fail because of remote resource limits.

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <host_flanks.fna> <output_prefix>"
    exit 1
fi

FLANKS="$1"
PREFIX="$2"

blastn \
    -query "${FLANKS}" \
    -db nt \
    -remote \
    -task megablast \
    -max_target_seqs 10 \
    -outfmt '6 qseqid sacc pident length qcovs evalue bitscore staxids sscinames' \
    -out "${PREFIX}.blastn.tsv"

blastx \
    -query "${FLANKS}" \
    -db nr \
    -remote \
    -max_target_seqs 10 \
    -outfmt '6 qseqid sacc pident length qcovs evalue bitscore staxids sscinames' \
    -out "${PREFIX}.blastx.tsv"

echo "[DONE] Host-search results written to:"
echo "  ${PREFIX}.blastn.tsv"
echo "  ${PREFIX}.blastx.tsv"
