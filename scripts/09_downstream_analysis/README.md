# Downstream Community and Biogeography Analysis

This module documents downstream analyses performed using the corrected
532-vOTU catalog and breadth-filtered read-recruitment results.

## Ambient vOTU Biogeography

1. `01_build_ambient_votu_presence.py`
   - Converts the breadth-filtered vOTU RPKM matrix into lake-level
     presence/absence for samples included in the ambient analysis.
   - A vOTU is considered present when its filtered RPKM is >0.

2. `02_summarize_votu_occupancy.py`
   - Classifies ambient vOTUs as not detected, lake-specific, or shared.
   - Summarizes the number of lakes occupied by each vOTU.

3. `03_summarize_shared_votu_combinations.py`
   - Identifies exact lake combinations represented by shared vOTUs.

4. `04_add_shared_votu_biogeography.py`
   - Adds HUC8 watershed context and maximum geographic distance to
     shared-vOTU records.

5. `05_pairwise_lake_similarity.py`
   - Calculates pairwise Jaccard similarity between lake-level ambient
     vOTU communities.
   - Adds geographic distance and HUC8 relationship for each lake pair.

6. `06_distance_similarity_correlation.py`
   - Tests the relationship between geographic distance and Jaccard
     similarity using Spearman and Pearson correlations.
   - Supports optional exclusion of individual lakes from the analysis.

## Input assumptions

Community analyses use the 532-vOTU representative catalog generated
using >=95% ANI and >=85% alignment coverage of the shorter genome.

Presence/absence is derived from RPKM values after application of the
75% breadth-of-coverage detection threshold during read recruitment.

Sample-to-lake assignments and geographic/watershed information are
provided through metadata files rather than hard-coded in the scripts.

## Requirements

- Python 3
- pandas
- scipy

## Community Structure and Temporal Continuity

7. `07_pcoa_votu_community.py`
   - Calculates Bray-Curtis dissimilarity among samples from the
     breadth-filtered 532-vOTU RPKM matrix.
   - Performs principal coordinates analysis (PCoA) and reports sample
     coordinates, eigenvalues, and percent variance explained.

8. `08_temporal_votu_continuity.py`
   - Compares vOTU detections between specified sample pairs.
   - Reports directional persistence and symmetric Jaccard similarity.
   - Supports an optional minimum-RPKM threshold for abundance-restricted
     sensitivity comparisons.
