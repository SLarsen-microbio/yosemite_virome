# Yosemite Alpine Lake Virome

Analysis scripts and metadata associated with the study of viral communities in alpine lakes in Yosemite National Park, California.

## Overview

This repository contains scripts and supporting metadata used to characterize viral communities from metagenomic samples collected from Yosemite alpine lakes. The study examines viral community composition, diversity, and abundance across lake systems and experimental conditions.

The repository provides the computational workflow used for metagenomic read processing, assembly, viral sequence identification and quality assessment, viral genome dereplication, read recruitment, abundance estimation, and downstream analyses and figure generation.

## Repository Structure

```text
yosemite_virome/
├── README.md
├── LICENSE
├── environment/
│   └── README.md
├── metadata/
│   └── sample_metadata.tsv
└── scripts/
    ├── README.md
    └── figures/
        └── README.md
```
## Analysis Workflow

The primary virome analysis workflow consisted of:

1. **Read quality assessment**  
   Raw metagenomic reads were assessed using FastQC.

2. **Read trimming and filtering**  
   Reads were processed using fastp with paired-end adapter detection.

3. **Metagenomic assembly**  
   Quality-filtered reads were assembled independently using MEGAHIT.

4. **Viral sequence identification**  
   Viral sequences were identified from assembled contigs using VirSorter2.

5. **Viral genome quality assessment**  
   Viral sequences were evaluated using CheckV.

6. **Viral genome dereplication**  
   Viral genomes were dereplicated to generate representative genome sets for downstream analyses.

7. **Read recruitment and viral abundance**  
   Metagenomic reads were mapped to viral reference genomes using Bowtie2. Viral abundance was calculated using RPKM with a 75% breadth-of-coverage threshold.

8. **Community analyses and visualization**  
   Viral richness, abundance, and community patterns were evaluated across samples and used to generate the figures presented in the manuscript.

## Software

Major software used in the virome workflow included:

- FastQC v0.11.8
- fastp v1.0.1
- MultiQC v1.30
- MEGAHIT v1.1.5
- VirSorter2 v2.2.4
- CheckV v1.0.3
- CD-HIT-EST v4.8.1
- Bowtie2 v2.5.1

Additional software and package information required for individual analyses are documented with the corresponding scripts.

## Data Availability

Raw metagenomic sequencing data analyzed in this study are available through the NCBI Sequence Read Archive (SRA). Sample accessions and associated lake, experiment, treatment, and sampling information are provided in `metadata/sample_metadata.tsv`.

Large sequencing files, intermediate assemblies, and database files are not included in this repository.

## Reproducibility

Scripts are organized approximately in the order in which analyses were performed. Paths to sequencing data, reference databases, and computational resources may need to be modified for use on other systems.

This repository contains the analysis code and metadata required to document and reproduce the computational workflow described in the associated manuscript.

## Citation

Citation information for the associated manuscript will be added upon publication.

## License

This repository is distributed under the MIT License. See `LICENSE` for details.
