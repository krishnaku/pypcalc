# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import List, Optional

import numpy as np
from numpy import typing as npt

from .presence import Presence
from .presence_map import PresenceMap
from .time_scale import Timescale


class PresenceMatrix:
    """
    A scale-invariant, optionally lazy matrix representation of element presences over discrete time bins.

    Each row corresponds to a single `Presence`, and each column represents a discrete time bin defined by a `Timescale`.
    The matrix records the degree of presence of each element within a given boundary over time, where each value is a real number in [0.0, 1.0]:
    - 1.0 = full presence for the duration of the time bin
    - 0.0 = no presence
    - values in between represent partial presence due to overlap

    The matrix can be computed eagerly via `materialize()` or accessed lazily through NumPy-style slicing.

    ### Structure

    - **Rows:** Each row corresponds to one `Presence` instance.
    - **Columns:** Each column represents a discrete bin of time defined by the `Timescale` (from `t0` to `t1` using `bin_width`).
    - The matrix shape is therefore `(len(presences), timescale.num_bins)`.

    ### Usage

    ```python
    from pcalc import PresenceMatrix
    from metamodel.timescale import Timescale

    # Define a time window with bin width of 1.0
    ts = Timescale(t0=0.0, t1=5.0, bin_width=1.0)

    # Construct lazily
    matrix = PresenceMatrix(presences, time_scale=ts)

    # Access entire row
    row = matrix[0]  # row 0 as 1D array

    # Access single value
    value = matrix[2, 3]  # presence at row 2, column 3

    # Access slice of row
    window = matrix[1, 1:4]  # row 1, columns 1–3

    # Access slice of rows
    rows = matrix[0:2]  # rows 0 and 1

    # Access single column
    col = matrix[:, 2]  # all rows at column 2

    # Access column block
    col_block = matrix[:, 1:4]  # all rows, columns 1–3

    # Materialize full matrix (optional)
    dense = matrix.materialize()
    ```

    Features
    --------
    - Lazy evaluation by default; full matrix computed only if needed
    - NumPy-style indexing: supports full rows, row/column slicing, and scalar access
    - Precision-preserving: partial bin overlaps are retained in the matrix
    - Compatible with matrix operations and flow metric calculations
    - Backed by a sparse `PresenceMap`, which stores slice indices and fractional overlaps

    Notes
    -----
    - Use `materialize()` if you want to extract or operate on the full dense matrix
    - Use `matrix[i, j]`, `matrix[i, j:k]`, or `matrix[:, j]` for lightweight slicing without allocating the full matrix
    - Stepped slicing (e.g., `matrix[::2]`) is not currently supported

"""

    def __init__(self, presences: List[Presence], time_scale: Timescale, materialize=False):
        """
        Construct a presence matrix from a list of Presences and time window configuration.

        Args:
            presences: A list of `Presence` instances, one per element of interest.
            time_scale: The discrete `Timescale` that the matrix will be normalized to.
            materialize: If True, immediately constructs the full backing matrix.
                     Otherwise, matrix values will be computed on demand using the sparse presence map.
        """

        self.presence_matrix: Optional[npt.NDArray[np.float64]] = None
        """
        A real valued matrix with shape (num_Presences, num_bins).
        When every presence.start and presence.end are whole numbers every value
        in the matrix is either 0.0 or 1.0. If they are not whole numbers, the presence
        is mapped to a number between 0.0 and 1.0 at the start and end (or both), with any
        intermediate value being 1.0. 
        """

        self.time_scale = time_scale
        """
        The time scale of the presence matrix.
        """

        self.presence_map: List[PresenceMap] = []
        self.shape = None
        self.init_presence_map(presences)

        if materialize:
            self.materialize()

    def init_presence_map(self, presences: List[Presence]) -> None:
        """
        Initialize the internal presence matrix based on the Presence intervals and binning scheme.
        Only presences that overlap the timescale endpoints [t0, t1) are mapped.
        """
        ts = self.time_scale  # Timescale object: includes t0, t1, bin_width

        for row, presence in enumerate(presences):
            presence_map = PresenceMap(presence, ts)
            if presence_map.is_mapped:
                self.presence_map.append(presence_map)

        num_bins = ts.num_bins
        num_rows = len(self.presence_map)
        self.shape = (num_rows, num_bins)

    def is_materialized(self) -> bool:
        """Return True if the backing matrix has been materialized."""
        return self.presence_matrix is not None

    def materialize(self) -> npt.NDArray[np.float64]:
        """
        Materialize and return the full presence matrix from presence maps.
        If already materialized, this is a no-op and returns the cached matrix.

        Use this only if want the full matrix to operate on. For most cases, you should
        be able to work with the sparse representation with the presence map and using
        array slicing on the matrix object. So think twice about why you are materializing
        a matrix.

        Returns:
            The dense presence matrix of shape (num_presences, num_bins).
        """
        if self.is_materialized():
            return self.presence_matrix

        num_rows, num_cols = self.shape
        matrix = np.zeros((num_rows, num_cols), dtype=float)

        for row, pm in enumerate(self.presence_map):
            if not pm.is_mapped:
                continue
            start = pm.start_bin
            end = pm.end_bin
            matrix[row, start] = pm.start_value
            if end - 1 > start:
                matrix[row, end - 1] = pm.end_value
            if end - start > 2:
                matrix[row, start + 1: end - 1] = 1.0

        self.presence_matrix = matrix
        return self.presence_matrix

    def drop_materialization(self) -> None:
        """Discard the cached matrix, returning to sparse-only mode."""
        self.presence_matrix = None

    def _compute_row_slice(self, row: int, start: int, stop: int) -> np.ndarray:
        """
        On-demand computation of a row slice from presence map.
        If the presence is not mapped or out of bounds, returns zeroes.
        """
        pm = self.presence_map[row]
        width = stop - start
        output = np.zeros(width, dtype=float)

        if not pm.is_mapped:
            return output

        # Slice and overlap window
        for col in range(start, stop):
            if col < pm.start_bin or col >= pm.end_bin:
                continue
            elif col == pm.start_bin:
                output[col - start] = pm.start_value
            elif col == pm.end_bin - 1:
                output[col - start] = pm.end_value
            else:
                output[col - start] = 1.0

        return output

    @property
    def presences(self) -> List[Presence]:
        return [pm.presence for pm in self.presence_map]

    def __getitem__(self, index):
        """
        Support NumPy-style indexing:
        - matrix[i]           → row i
        - matrix[i:j]         → row slice (returns 2D array)
        - matrix[i, j]        → scalar
        - matrix[i, j:k]      → row[i], column slice
        - matrix[:, j]        → column j (all rows)
        - matrix[:, j:k]      → column block j:k (all rows)
        """
        # matrix[i:j] → top-level row slicing
        if isinstance(index, slice):
            if index.step is not None:
                raise ValueError("PresenceMatrix does not support slicing with a step.")
            start = index.start if index.start is not None else 0
            stop = index.stop if index.stop is not None else self.shape[0]
            if self.presence_matrix is not None:
                return self.presence_matrix[start:stop]
            return np.array([self[row] for row in range(start, stop)])

        # matrix[i, j], matrix[i, j:k], matrix[:, j]
        if isinstance(index, tuple):
            row_idx, col_idx = index

            # matrix[:, j] or matrix[:, j:k]
            if isinstance(row_idx, slice):
                if row_idx.step is not None:
                    raise ValueError("PresenceMatrix does not support stepped row slicing.")
                row_start = row_idx.start if row_idx.start is not None else 0
                row_stop = row_idx.stop if row_idx.stop is not None else self.shape[0]

                if isinstance(col_idx, int):
                    return np.array([self[row, col_idx] for row in range(row_start, row_stop)])

                elif isinstance(col_idx, slice):
                    if col_idx.step is not None:
                        raise ValueError("PresenceMatrix does not support stepped column slicing.")
                    col_start = col_idx.start if col_idx.start is not None else 0
                    col_stop = col_idx.stop if col_idx.stop is not None else self.shape[1]
                    return np.array([self[row, col_start:col_stop] for row in range(row_start, row_stop)])

            # matrix[i, j] or matrix[i, j:k]
            elif isinstance(row_idx, int):
                if isinstance(col_idx, int):
                    return self.presence_matrix[row_idx, col_idx] if self.presence_matrix is not None \
                        else self._compute_row_slice(row_idx, col_idx, col_idx + 1)[0]

                elif isinstance(col_idx, slice):
                    if col_idx.step is not None:
                        raise ValueError("PresenceMatrix does not support stepped column slicing.")
                    start = col_idx.start if col_idx.start is not None else 0
                    stop = col_idx.stop if col_idx.stop is not None else self.shape[1]
                    return self.presence_matrix[row_idx, start:stop] if self.presence_matrix is not None \
                        else self._compute_row_slice(row_idx, start, stop)

        # matrix[i] → single row
        if isinstance(index, int):
            return self.presence_matrix[index] if self.presence_matrix is not None \
                else self._compute_row_slice(index, 0, self.shape[1])

        raise TypeError(f"Invalid index for PresenceMatrix: {index}")



