# Auto-generated module
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Generic, Tuple
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from numpy import typing as npt

from metamodel.element import T_Element
from metamodel.presence import Presence




@dataclass
class PresenceMap:
    """A presence map is a mapping of a presence, which has
    a start and end time on a continuous timescale, to a
    discrete timescale where a continuous interval from t0 to t1 is
    divided into equal-sized bins of width `bin_width`.

    A presence map is a piecewise constant function over the bin indices,
    where the presence is assumed to be:

    - zero outside the mapped bin range,
    - possibly fractional (0 < p < 1) in the first and last bins due to partial overlap, and
    - equal to 1.0 in all interior bins that fall entirely within the presence interval.

    This representation allows the continuous duration of a presence
    to be projected onto a discrete matrix without loss of precision
    at the boundaries, while enabling efficient matrix-based analytics and transformations.
    """

    presence: Presence
    """The presence entry"""

    is_mapped: bool
    """True if the presence has a valid mapping. Unmapped presences have value=None
    for start_slice, end_slice, start_value and end_value. 
    """
    start_bin: int
    """The starting bin in the discrete mapping"""
    end_bin: int
    """The ending bin in the discrete mapping` 
    of row `row`. 
    """
    start_value: float
    """A presence value 0 < p < 1.0 that represents a potentially partial presence at the start of the mapping"""
    end_value: float
    """A presence value 0 < p < 1.0 that represents a partially partial presence at the end of the mapping"""


class PresenceMatrix(Generic[T_Element]):
    """
    A scale invariant matrix representation of element presences on a timeline.

    Each row corresponds to a single `Presence`, and each column represents a unit of time on a timescale.
    The matrix is binary: a value of 1 indicates the signal was present in the boundary
    during that time bin, while 0 indicates absence.

    Note that the same element may be present in a  given matrix multiple times, but they will
    be recorded as separate Presences and be represented as separate rows in the matrix.

    The `PresenceMatrix` is the core data structure used to analyze how elements
    propagate through boundaries over time, and to support calculations of flow metrics like
    arrivals, departures, residence times of elements in boundaries.

    ### Dimensions

    - Rows: `len(Presences)`
    - Columns: `(t1 - t0) / timescale`

    ### Example

    ```python
    matrix = PresenceMatrix(Presences, t0=0.0, t1=10.0, time_scale=1.0)
    matrix.presence_matrix  # shape: (num_Presences, num_time_bins)
    ```
    """

    def __init__(self, presences: List[Presence[T_Element]], start_time: float, end_time: float,
                 time_scale: float = 1.0):
        """
        Construct a presence matrix from a list of Presences and time window configuration.

        Args:
            presences: A list of `Presence` instances, one per element of interest.
            start_time: Start of the observation window.
            end_time: End of the observation window.
            time_scale: Multiple of some base time unit in which all timelines are recorded in the system.
        """

        self.presence_matrix: Optional[npt.NDArray[np.float64]] = None
        """
        A real valued matrix with shape (num_Presences, num_bins).
        When every presence.start and presence.end are whole numbers every value
        in the matrix is either 0.0 or 1.0. If they are not whole numbers, the presence
        is mapped to a number between 0.0 and 1.0 at the start and end (or both), with any
        intermediate value being 1.0. 
        """

        self.start_time = start_time
        """The start of the observation window."""

        self.end_time = end_time
        """The end of the observation window."""

        self.time_scale = time_scale
        """
        The width of each column in the presence matrix, measured in base time units.
    
        All time in the domain (e.g. start/end of presence intervals) is assumed to be recorded 
        in a normalized base unit (such as milliseconds, epoch seconds, or simulation ticks).
        
        The time_scale defines how many base units are aggregated into a single matrix column. 
        A value of 1 means each column represents exactly one unit of time. Larger values 
        aggregate more coarsely, reducing resolution but improving efficiency. 
        
        Must be >= 1.0. Values less than 1 imply sub-unit precision, which is invalid unless
        the domain supports continuous time (which we dont model at the moment).
        """

        self.time_bins: int = 0
        """The number of bins used across the observation window."""

        self.presence_map: List[PresenceMap] = []
        self.shape = None
        self.init_matrix(presences)

    def init_matrix(self, presences: List[Presence[T_Element]]) -> None:
        """
        Initialize the internal presence matrix based on the Presence intervals and binning scheme.
        """

        t0 = self.start_time
        t1 = self.end_time
        bin_width = self.time_scale

        time_bins = np.arange(t0, t1 + bin_width, bin_width)
        num_bins = len(time_bins) - 1
        num_rows = len(presences)
        self.shape = (num_rows, num_bins)

        # the matrix is an array of floats.
        matrix = np.zeros(self.shape, dtype=float)
        for row, presence in enumerate(presences):
            presence_map = self.map_presence(presence, t0, t1, bin_width)
            if presence_map.is_mapped:
                self.map_matrix_row(matrix, row, presence_map)

            self.presence_map.append(presence_map)

        self.presence_matrix = matrix
        self.time_bins = time_bins

    @staticmethod
    def map_matrix_row(matrix: npt.NDArray, row: int, presence_map: PresenceMap) -> None:
        matrix[row, presence_map.start_bin] = presence_map.start_value
        matrix[row, presence_map.start_bin + 1: presence_map.end_bin - 1] = 1.0
        if presence_map.end_bin - 1 > presence_map.start_bin:
            matrix[row, presence_map.end_bin - 1] = presence_map.end_value

    @staticmethod
    def map_presence(presence: Presence, t0: float, t1: float, bin_width: float) -> PresenceMap:
        """Map a presence interval to matrix slice indices and edge fractional values."""

        effective_start = max(presence.start, t0)
        effective_end = min(presence.end, t1)

        # If there is no mapping, then these are the values in the presence map.
        is_mapped = False
        start_slice = -1
        end_slice = -1
        start_value = -1
        end_value = -1

        if effective_end > effective_start:
            is_mapped = True
            start_slice = int(np.floor((effective_start - t0) / bin_width))
            end_slice = int(np.ceil((effective_end - t0) / bin_width))

            # Compute partial overlap at start
            bin_start_time = t0 + start_slice * bin_width
            bin_end_time = bin_start_time + bin_width
            start_overlap = (min(effective_end, bin_end_time) - effective_start) / bin_width
            start_value = max(0.0, min(1.0, start_overlap))

            # Compute partial overlap at end
            if end_slice - 1 > start_slice:
                bin_start_time = t0 + (end_slice - 1) * bin_width
                end_overlap = (effective_end - max(effective_start, bin_start_time)) / bin_width
                end_value = max(0.0, min(1.0, end_overlap))
            else:
                end_value = start_value  # same bin

        return PresenceMap(
            presence=presence,
            is_mapped=is_mapped,
            start_bin=start_slice,
            end_bin=end_slice,
            start_value=start_value,
            end_value=end_value,
        )


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
