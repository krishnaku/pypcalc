# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import List, Optional, Generic

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from numpy import typing as npt

from .element import T_Element
from .presence import Presence
from .presence_map import PresenceMap
from .time_scale import Timescale


class PresenceMatrix(Generic[T_Element]):
    """
    A scale-invariant, optionally lazy matrix representation of element presences over time.

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

    def __init__(self, presences: List[Presence[T_Element]], time_scale: Timescale, materialize=False):
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

    def init_presence_map(self, presences: List[Presence[T_Element]]) -> None:
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
    def presences(self) -> List[Presence[T_Element]]:
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


def get_entry_exit_times(presence, signal_index, queue_name):
    arrivals = []
    departures = []
    mat = presence[queue_name]
    for i in range(mat.shape[0]):
        times = np.where(mat[i])[0]
        if times.size > 0:
            arrivals.append(times[0])
            departures.append(times[-1] + 1)
    return (arrivals, departures)


def compute_cumulative_arrival_rate(arrival_index, presence, t0, t1):
    """Cumulative arrival rate over [t0, t1): arrivals + number in system at t0, divided by window length."""
    in_system_at_t0 = np.sum(presence[:, t0 - 1]) if t0 > 0 else 0
    arrivals_during_window = np.sum(arrival_index[t0:t1])
    total_signals = in_system_at_t0 + arrivals_during_window
    return total_signals / (t1 - t0) if t1 > t0 else 0.0


def compute_average_residence_time(visit_index, presence, t0, t1):
    """Average time in system for signals present during [t0, t1)."""
    window = presence[:, t0:t1]
    total_time = np.sum(window)
    total_presences = 0
    for row_presences in visit_index:
        total_presences += sum((t0 <= t < t1 for t in row_presences))
    return total_time / total_presences if total_presences > 0 else 0.0


def compute_average_number_in_queue(presence, t0, t1):
    """Average number of signals present during [t0, t1)."""
    window = presence[:, t0:t1]
    count_per_time = np.sum(window, axis=0)
    return np.mean(count_per_time)


def compute_operator_flow_metrics(presence, arrival_index, visit_index, t0, t1):
    return {'lambda': compute_cumulative_arrival_rate(arrival_index, presence, t0, t1),
            'L': compute_average_number_in_queue(presence, t0, t1),
            'W': compute_average_residence_time(visit_index, presence, t0, t1), 'window': (t0, t1)}


def compute_signal_flow_metrics(presence, arrival_index, visit_index, t0, t1):
    active_signals = np.any(presence[:, t0:t1], axis=1)
    signal_rows = presence[active_signals]
    time_presence = np.any(signal_rows, axis=0)
    t_indices = np.where(time_presence)[0]
    if len(t_indices) == 0:
        return {'lambda': 0, 'L': 0, 'W': 0, 'span': (t0, t1)}
    t_prime_0 = t_indices[0]
    t_prime_1 = t_indices[-1] + 1
    return compute_operator_flow_metrics(presence, arrival_index, visit_index, t_prime_0, t_prime_1)


def estimate_limits(df, tail_frac=0.2):
    tail = df.tail(int(len(df) * tail_frac))
    return {'lambda_limit': tail['lambda'].mean(), 'W_limit': tail['W'].mean(), 'L_limit': tail['L'].mean(),
            'L_estimated': tail['lambda'].mean() * tail['W'].mean()}


def detect_stability_by_tail_convergence(df, tail_frac=0.2, epsilon=0.005):
    deltas = []
    window_ends = df['window_end'].values
    for i in range(1, len(df)):
        tail_size = max(1, int(tail_frac * i))
        tail = df.iloc[i - tail_size + 1:i + 1]
        lam_tail = tail['lambda'].mean()
        W_tail = tail['W'].mean()
        L_tail = tail['L'].mean()
        L_estimated = lam_tail * W_tail
        delta = abs(L_tail - L_estimated)
        deltas.append({'window_end': window_ends[i], 'delta': delta, 'L_tail': L_tail, 'L_estimated': L_estimated,
                       'lambda_tail': lam_tail, 'W_tail': W_tail, 'stable': delta < epsilon})
    delta_df = pd.DataFrame(deltas)
    plt.figure(figsize=(10, 6))
    plt.plot(delta_df['window_end'], delta_df['delta'], label='|L - λ×W|')
    plt.axhline(epsilon, color='red', linestyle='--', label=f'ε = {epsilon}')
    plt.xlabel('Window End Time')
    plt.ylabel('Delta: |L - λ×W|')
    plt.title('Convergence of L = λ × W (Tail-Averaged)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return delta_df


def detect_tail_convergence(delta_df, tail_frac=0.2, epsilon=0.05):
    """
    Annotates chart with the first window_end where convergence occurs.
    """
    delta_df = delta_df.copy()
    delta_df['tail_size_days'] = (tail_frac * delta_df['window_end']).astype(int)
    delta_df['converged'] = delta_df['delta'] < epsilon
    tail_size_annotation = int(tail_frac * delta_df['window_end'].max())
    first_converged = delta_df[delta_df['converged']].head(1)
    convergence_point = first_converged['window_end'].values[0] if not first_converged.empty else None
    plt.figure(figsize=(10, 6))
    plt.plot(delta_df['window_end'], delta_df['delta'], label=f'|W_op - W_ent| (tail avg, {tail_size_annotation} days)',
             linewidth=2)
    plt.axhline(epsilon, color='red', linestyle='--', label=f'ε = {epsilon}')
    if convergence_point:
        plt.axvline(convergence_point, color='green', linestyle=':', linewidth=1.5,
                    label=f'Converged at t = {convergence_point}')
        plt.text(convergence_point + 1, epsilon + 0.02, f't = {convergence_point}', color='green', fontsize=10)
    plt.xlabel('Window End Time')
    plt.ylabel('Tail Delta')
    plt.title('Tail Convergence of Residence Time (Entity vs Operator Perspective)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return delta_df[['window_end', 'tail_size_days', 'delta', 'converged']]
