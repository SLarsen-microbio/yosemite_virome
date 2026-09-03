# Provirus and Host Analysis

This module documents host-assignment analyses for CheckV-identified proviruses.

## Workflow

1. **Extract host flanking regions**
   - `01_extract_host_flanks.sh`
   - Uses CheckV provirus coordinates and `samtools faidx` to recover non-proviral sequence flanking each provirus.

2. **Search host flanks**
   - `02_search_host_flanks.sh`
   - Searches extracted host regions against NCBI databases.
   - BLASTn/megablast is used first for close nucleotide matches.
   - BLASTx against `nr` can be used when nucleotide searches are not informative.

3. **CRISPR spacer matching**
   - `03_match_crispr_spacers.sh`
   - Searches CRISPR spacers against the viral genome catalog.
   - Matches are retained at:
     - >=95% nucleotide identity
     - >=95% query coverage
     - e-value <=1e-5

CRISPR arrays were identified with MinCED. tRNA-based host linkage was also evaluated during the study, but neither CRISPR spacer matching nor tRNA matching produced significant host assignments for the reported dataset.

## Requirements

- SAMtools 1.17
- NCBI BLAST+
- MinCED
