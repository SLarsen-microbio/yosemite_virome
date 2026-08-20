# Analysis Scripts

This directory contains scripts used for the computational analysis of viral communities in Yosemite alpine lake metagenomes.

Scripts are organized approximately in the order of the analysis workflow. Individual scripts contain additional information on required inputs, outputs, software, and parameters.

## Workflow

### 00. Read quality control and assembly

- `00a_fastqc_multiqc.sh` — assess raw read quality with FastQC and summarize results with MultiQC.
- `00b_fastp.sh` — trim and quality-filter paired-end reads with fastp.
- `00c_megahit.sh` — assemble quality-filtered metagenomic reads with MEGAHIT.

### 01. Viral sequence identification

- `01_virsorter2.sh` — identify viral sequences in metagenomic assemblies using VirSorter2.

### 02. Viral genome quality assessment

- `02_checkv.sh` — assess viral genome quality and completeness using CheckV.

### 03. Viral genome dereplication

Scripts in this step generate the dereplicated viral genome set used for downstream community analyses.

### 04. Read recruitment and abundance

Scripts in this step map metagenomic reads against the viral reference genome set and calculate viral abundance.

A 75% breadth-of-coverage threshold was applied before RPKM values were retained for downstream analyses.

### 05. Community analyses

Scripts in this step calculate and summarize viral community metrics used in the manuscript.

### Figures

Figure-generation scripts are located in:

`figures/`

See `figures/README.md` for figure-specific information.

## Usage

Scripts are intended to document the computational workflow used for the associated study. File paths and computational resource parameters may need to be modified for use on other systems.

Unless otherwise indicated, shell scripts should be run from the command line using Bash.

## Software

Major command-line software used by these scripts includes:

- FastQC v0.11.8
- fastp v1.0.1
- MultiQC v1.30
- MEGAHIT v1.1.5
- VirSorter2 v2.2.4
- CheckV v1.0.3
- CD-HIT-EST v4.8.1
- Bowtie2 v2.5.1

Additional dependencies are documented with the corresponding scripts.
