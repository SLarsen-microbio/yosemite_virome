#!/usr/bin/env python3

"""
Perform Bray-Curtis principal coordinates analysis (PCoA) on the
breadth-filtered vOTU RPKM abundance matrix.

Input matrix:
    rows = vOTUs
    columns = samples
    values = breadth-filtered RPKM

The script calculates Bray-Curtis dissimilarities among samples and then
performs classical principal coordinates analysis.

Outputs:
    1. Sample PCoA coordinates
    2. Axis eigenvalues and percent variance explained
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform


def parse_args():
    parser = argparse.ArgumentParser(
        description="Bray-Curtis PCoA of breadth-filtered vOTU RPKM profiles."
    )
    parser.add_argument(
        "rpkm_matrix",
        help="TSV matrix with vOTUs as rows and samples as columns.",
    )
    parser.add_argument(
        "coordinates_output",
        help="Output TSV for sample PCoA coordinates.",
    )
    parser.add_argument(
        "eigenvalues_output",
        help="Output TSV for eigenvalues and variance explained.",
    )
    return parser.parse_args()


def classical_pcoa(distance_matrix):
    """
    Classical principal coordinates analysis from a square distance matrix.
    """
    n = distance_matrix.shape[0]

    d2 = distance_matrix ** 2

    centering = np.eye(n) - np.ones((n, n)) / n

    b_matrix = -0.5 * centering @ d2 @ centering

    eigenvalues, eigenvectors = np.linalg.eigh(b_matrix)

    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    positive = eigenvalues > 0

    positive_eigenvalues = eigenvalues[positive]
    positive_eigenvectors = eigenvectors[:, positive]

    coordinates = (
        positive_eigenvectors
        * np.sqrt(positive_eigenvalues)
    )

    return eigenvalues, coordinates


def main():
    args = parse_args()

    rpkm = pd.read_csv(args.rpkm_matrix, sep="\t", index_col=0)

    if rpkm.empty:
        raise ValueError("RPKM matrix is empty.")

    if rpkm.isna().any().any():
        raise ValueError("RPKM matrix contains missing values.")

    if (rpkm < 0).any().any():
        raise ValueError("RPKM matrix contains negative abundance values.")

    # Bray-Curtis is calculated among samples, so transpose the
    # vOTU-by-sample matrix to sample-by-vOTU.
    sample_matrix = rpkm.T

    distances = pdist(
        sample_matrix.values,
        metric="braycurtis",
    )

    distance_matrix = squareform(distances)

    eigenvalues, coordinates = classical_pcoa(distance_matrix)

    coordinate_columns = [
        f"PCoA{i + 1}"
        for i in range(coordinates.shape[1])
    ]

    coordinate_df = pd.DataFrame(
        coordinates,
        index=sample_matrix.index,
        columns=coordinate_columns,
    )

    coordinate_df.index.name = "Sample"

    positive_eigenvalues = eigenvalues[eigenvalues > 0]

    total_positive = positive_eigenvalues.sum()

    variance_explained = np.where(
        eigenvalues > 0,
        eigenvalues / total_positive * 100,
        0.0,
    )

    eigen_df = pd.DataFrame(
        {
            "axis": [
                f"PCoA{i + 1}"
                for i in range(len(eigenvalues))
            ],
            "eigenvalue": eigenvalues,
            "variance_explained_percent": variance_explained,
        }
    )

    Path(args.coordinates_output).parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    Path(args.eigenvalues_output).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    coordinate_df.to_csv(
        args.coordinates_output,
        sep="\t",
    )

    eigen_df.to_csv(
        args.eigenvalues_output,
        sep="\t",
        index=False,
    )


if __name__ == "__main__":
    main()
