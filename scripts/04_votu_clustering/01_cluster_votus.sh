#!/usr/bin/env bash
set -euo pipefail

# Cluster Complete/HQ/MQ viral genomes into species-level vOTUs.
#
# Workflow:
#   1. Build a nucleotide BLAST database from the viral genome catalog.
#   2. Perform all-vs-all BLASTn.
#   3. Calculate pairwise ANI and alignment coverage with CheckV anicalc.py.
#   4. Cluster genomes with CheckV aniclust.py.
#
# Clustering thresholds:
#   ANI >= 95%
#   coverage of shorter genome >= 85%
#
# Software:
#   BLAST+
#   CheckV companion scripts: anicalc.py and aniclust.py
#
# Usage:
#   bash 01_cluster_votus.sh \
#       <all_genomes.fna> \
#       <anicalc.py> \
#       <aniclust.py>

if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <all_genomes.fna> <anicalc.py> <aniclust.py>"
    exit 1
fi

INPUT="$1"
ANICALC="$2"
ANICLUST="$3"

THREADS=16
OUTDIR="results/votu_clustering"

DB="${OUTDIR}/viral_genomes_db"
BLAST="${OUTDIR}/all_vs_all.blast.tsv"
ANI="${OUTDIR}/all_vs_all_ani.tsv"
CLUSTERS="${OUTDIR}/votu_clusters.tsv"

mkdir -p "${OUTDIR}"

echo "[STEP] Building BLAST database"

makeblastdb \
    -in "${INPUT}" \
    -dbtype nucl \
    -out "${DB}"

echo "[STEP] Running all-vs-all BLASTn"

blastn \
    -query "${INPUT}" \
    -db "${DB}" \
    -outfmt '6 std qlen slen' \
    -max_target_seqs 10000 \
    -num_threads "${THREADS}" \
    -out "${BLAST}"

echo "[STEP] Calculating ANI and alignment coverage"

python "${ANICALC}" \
    -i "${BLAST}" \
    -o "${ANI}"

echo "[STEP] Clustering genomes into vOTUs"

python "${ANICLUST}" \
    --fna "${INPUT}" \
    --ani "${ANI}" \
    --out "${CLUSTERS}" \
    --min_ani 95 \
    --min_tcov 85 \
    --min_qcov 0

echo "[DONE] vOTU clustering complete"
echo "[INFO] Cluster table: ${CLUSTERS}"
