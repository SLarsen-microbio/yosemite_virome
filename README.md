# Yosemite Lake Virome

Analysis scripts and supporting metadata associated with the study of viral communities in lakes in Yosemite National Park, California.

## Overview

This repository documents the computational workflow used to characterize viral communities from metagenomic samples collected from Yosemite lakes.

The workflow includes metagenomic read processing, assembly, viral genome recovery and quality assessment, vOTU clustering, read recruitment and abundance estimation, auxiliary metabolic gene (AMG) analysis, provirus and host-linkage analysis, complete viral genome characterization, and downstream community and biogeographic analyses.

Large sequencing files, intermediate analysis files, and reference databases are not included. The repository is intended to provide the analysis framework, scripts, parameters, and supporting metadata needed to reproduce the computational approach.

## Repository Structure

```text
yosemite_virome/
├── README.md
├── LICENSE
├── metadata/
│   └── amg/
└── scripts/
    ├── README.md
    ├── 01_qc/
    ├── 02_assembly/
    ├── 03_viral_recovery/
    ├── 04_votu_clustering/
    ├── 05_read_recruitment/
    ├── 06_amg_analysis/
    ├── 07_provirus_analysis/
    ├── 08_complete_genomes/
    └── 09_downstream_analysis/
```

## Analysis Workflow

The primary analysis framework consists of:

1. **Read quality control**
   - Raw metagenomic reads are assessed with FastQC.
   - Reads are trimmed and filtered with fastp using paired-end adapter detection.
   - Post-trimming quality is assessed with FastQC and summarized with MultiQC.

2. **Metagenomic assembly**
   - Quality-filtered reads are assembled independently with MEGAHIT.
   - Contigs shorter than 1,000 bp are removed before viral sequence identification.

3. **Viral genome recovery**
   - VirSorter2 identifies putative viral sequences.
   - CheckV evaluates viral genome quality.
   - Complete, High-quality, and Medium-quality viral genomes are retained.
   - geNomad is used for viral taxonomic assignment.

4. **vOTU clustering**
   - Retained viral genomes are compared with all-vs-all BLASTn.
   - CheckV `anicalc.py` and `aniclust.py` are used to cluster genomes at >=95% ANI across >=85% of the shorter sequence.
   - Representative sequences are selected to construct the vOTU catalog.

5. **Read recruitment and abundance**
   - Trimmed reads are mapped with Bowtie2 to retained viral genomes for genome-level analyses and to the representative vOTU catalog for community analyses.
   - SAMtools is used for BAM processing and coverage calculations.
   - RPKM values are retained when reference sequences meet a 75% breadth-of-coverage detection threshold.

6. **Auxiliary metabolic gene analysis**
   - VIBRANT is used to identify AMGs in the representative vOTU catalog.
   - AMG annotations are summarized by KO, vOTU, and broad metabolic category.
   - AMG-carrying vOTU abundance is integrated with breadth-filtered read-recruitment results.

7. **Provirus and host-linkage analysis**
   - CheckV-identified proviral regions are used to recover flanking host sequence.
   - Host regions are evaluated using sequence-similarity searches.
   - MinCED-derived CRISPR spacers are compared with viral sequences.
   - tRNA-based host linkage is evaluated through viral genome annotation.

8. **Complete viral genome characterization**
   - Complete viral genomes are reoriented with Dnaapler and annotated with Pharokka.
   - Genome maps are generated with the Pharokka plotting workflow.

9. **Community and biogeographic analyses**
   - Breadth-filtered vOTU detections are summarized across lakes.
   - Lake occupancy, shared-vOTU patterns, watershed relationships, and geographic distances are evaluated.
   - Community structure is assessed using Bray-Curtis dissimilarity and principal coordinates analysis.
   - Temporal continuity is evaluated between selected sample pairs.

## Software

Major software represented in the workflow includes:

- FastQC v0.11.8
- fastp v1.0.1
- MultiQC v1.30
- MEGAHIT v1.1.5
- VirSorter2 v2.2.4
- CheckV v1.0.3
- BLAST+
- Bowtie2 v2.5.1
- SAMtools v1.17
- VIBRANT v1.2.1
- MinCED v0.4.2
- Pharokka v1.9.1
- Dnaapler
- Python 3
- pandas
- scipy

Additional software, databases, dependencies, and analysis-specific requirements are documented with the corresponding scripts.

## Data Availability

Raw metagenomic sequencing data analyzed in this study are publicly available through the NCBI Sequence Read Archive (SRA). Accession information and study metadata are reported with the associated study.

Large sequencing files, assemblies, read-mapping files, intermediate analysis outputs, and reference databases are not included in this repository.

## Reproducibility

Scripts are organized in the order of the major computational stages described above. Individual scripts accept input and output paths as arguments where appropriate so that the workflow can be adapted to different computing environments.

The repository documents the analysis framework used for the study rather than reproducing the complete computational working directory. Intermediate files and large datasets generated during analysis are therefore intentionally excluded.

## Citation

Citation information for the associated manuscript will be added upon publication.

## License

This repository is distributed under the MIT License. See `LICENSE` for details.
