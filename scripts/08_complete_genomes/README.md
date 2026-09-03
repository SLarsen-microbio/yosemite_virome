# Complete Viral Genome Analysis

This module documents the workflow used for complete viral genomes supported by direct terminal repeat (DTR) evidence from CheckV.

## Workflow

1. **Reorient complete genomes**
   - `01_reorient_complete_genomes.sh`
   - Uses Dnaapler to reorient circular viral genomes prior to annotation.

2. **Annotate complete genomes**
   - `02_annotate_complete_genomes.sh`
   - Uses Pharokka v1.9.1 for functional annotation of reoriented genomes.

3. **Generate circular genome maps**
   - `03_plot_complete_genomes.sh`
   - Uses the Pharokka plotter utility to generate circular genome visualizations from annotation outputs.

Seven complete viral genomes were identified by CheckV based on terminal-repeat evidence and subjected to detailed annotation and visualization.

## Requirements

- Dnaapler
- Pharokka v1.9.1
- Pharokka plotter
