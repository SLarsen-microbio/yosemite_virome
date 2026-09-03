#!/usr/bin/env bash
set -euo pipefail

# Map paired-end metagenomic reads to the representative vOTU catalog.
#
# Software:
#   Bowtie2 v2.5.1
#   SAMtools v1.17
#
# Bowtie2 was run with default paired-end mapping settings and --no-unal.
#
# Usage:
#   bash 02_map_reads_votu_catalog.sh \
#       <sample_id> \
#       <read1.fastq.gz> \
#       <read2.fastq.gz> \
#       <votu_catalog.fna>

if [[ $# -ne 4 ]]; then
    echo "Usage: $0 <sample_id> <read1.fastq.gz> <read2.fastq.gz> <votu_catalog.fna>"
    exit 1
fi

SAMPLE="$1"
READ1="$2"
READ2="$3"
VOTUS="$4"

THREADS=8
OUTDIR="results/read_recruitment/votu_catalog/bam"
DB_PREFIX="results/read_recruitment/votu_catalog/votu_db"

mkdir -p "${OUTDIR}"

if [[ ! -f "${DB_PREFIX}.1.bt2" && ! -f "${DB_PREFIX}.1.bt2l" ]]; then
    echo "[STEP] Building Bowtie2 index"
    bowtie2-build "${VOTUS}" "${DB_PREFIX}"
fi

echo "[STEP] Mapping ${SAMPLE}"

bowtie2 \
    -x "${DB_PREFIX}" \
    -1 "${READ1}" \
    -2 "${READ2}" \
    --no-unal \
    -p "${THREADS}" \
    2> "${OUTDIR}/${SAMPLE}.log" \
    | samtools sort \
        -@ "${THREADS}" \
        -o "${OUTDIR}/${SAMPLE}.bam"

samtools index "${OUTDIR}/${SAMPLE}.bam"

echo "[DONE] Mapping complete for ${SAMPLE}"
