# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
import numpy as np
import numpy.typing as npt

@dataclass
class Timescale:
    """
    Timescale represents a partitioning of a continuous time interval [t0, t1)
    into N = ceil((t1 - t0) / bin_width) contiguous, left-aligned, non-overlapping bins.

    Each bin has width `bin_width` and covers a half-open interval:
        Bin k = [t0 + k * bin_width, t0 + (k + 1) * bin_width)

    This class provides methods for:
    - Mapping real-valued timestamps to discrete bin indices
    - Extracting the time boundaries of any bin
    - Computing which bins an interval [start, end) overlaps
    - Estimating how much of a bin is covered by a given interval

    **Boundary Behavior**:
    - All bins lie strictly within [t0, t1)
    - Any time `t` where t < t0 or t >= t1 is considered **outside** the defined timescale
    - bin_index(t) may return an out-of-range index if `t < t0` or `t >= t1`

    This class does not perform clipping: it assumes all inputs are in-range unless explicitly clipped by the caller.
"""

    t0: float
    """start time of the interval [t0, t1)"""
    t1: float
    """end time of the interval [t0, t1)"""

    bin_width: float
    """Width of each bin"""

    @property
    def num_bins(self) -> int:
        """Return number of bins between t0 and t1."""
        return int(np.ceil((self.t1 - self.t0) / self.bin_width))

    # Mapping from continuous time to discrete bins.
    def bin_index(self, time: float) -> int:
        """Purpose:
            Map a real-valued timestamp to the index of the bin that contains it.

        Contract:
            Returns k such that bin_start(k) ≤ time < bin_end(k)
            Uses floor() logic — i.e., left-aligned binning
            No bounds check: time < t0 may yield negative indices; time ≥ t1 may return out-of-bounds indices
            Caller is responsible for ensuring t0 ≤ time < t1 if range enforcement is needed
        """
        return int(np.floor((time - self.t0) / self.bin_width))

    def bin_slice(self, start: float, end: float) -> Tuple[int, int]:
        """Return the bin indices [start_bin, end_bin) that overlap the interval [start, end).
        Contract:
            - Clips the interval [start, end) to [t0, t1) before binning
            - Computes:
                start_bin = floor((clipped_start - t0) / bin_width)
                end_bin   = ceil((clipped_end   - t0) / bin_width)
            - Resulting slice [start_bin, end_bin) may be empty if the interval does not overlap the timescale
            - start_bin ∈ [0, num_bins)
            - end_bin   ∈ [0, num_bins]

        """
        effective_start = max(start, self.t0)
        effective_end = min(end, self.t1)
        if effective_start >= effective_end:
            return 0, 0
        start_bin = int(np.floor((effective_start - self.t0) / self.bin_width))
        end_bin = int(np.ceil((effective_end - self.t0) / self.bin_width))
        return start_bin, end_bin

    def fractional_overlap(self, start: float, end: float, bin_idx: int) -> float:
        """Return the fraction of the bin at index `bin_idx` that is covered by the interval [start, end).
        Contract:
            - Computes how much of bin_idx's interval is covered by [start, end)
            - Returns value in [0.0, 1.0] based on normalized overlap over bin width
            - Clipped to bin extent: overlaps outside the bin are ignored
            - Used to compute partial presence contribution within a bin
        """
        # Clip to timescale
        start = max(start, self.t0)
        end = min(end, self.t1)

        bin_start = self.bin_start(bin_idx)
        bin_end = self.bin_end(bin_idx)

        overlap_start = max(start, bin_start)
        overlap_end = min(end, bin_end)

        return max(0.0, overlap_end - overlap_start) / self.bin_width

    # Mapping from discrete bins back to continuous time.
    def bin_start(self, bin_idx: int) -> float:
        """Return the start time of a bin given its index.
        Contract:
            bin_start(k) = t0 + k * bin_width
        """
        return self.t0 + bin_idx * self.bin_width

    def bin_end(self, bin_idx: int) -> float:
        """Return the end time of a bin given its index.
        Contract:
            bin_end(k) = t0 + (k + 1) * bin_width
        """
        return self.t0 + (bin_idx + 1) * self.bin_width

    def bin_edges(self) -> np.ndarray:
        """
        Return an array of bin edge times from t0 to t1, spaced by bin_width.

        The result has length `num_bins + 1` and is safe against floating-point rounding
        by capping the range to include exactly the number of bins implied by `num_bins()`.

        Contract:
        - Returns `num_bins + 1` edge values such that:
            edges = [t0, t0 + bin_width, ..., t1]

        - Guarantees:
            bin_start(k) == edges[k]
            bin_end(k)   == edges[k + 1]

        - Handles floating-point rounding safely:
            If np.arange overproduces due to rounding, result is trimmed
            to ensure exactly `num_bins + 1` entries.

        This method defines the canonical bin boundaries used across
        the presence matrix and all derived metrics.

        Example:
            Timescale(t0=0.0, t1=10.0, bin_width=2.0).bin_edges()
            => array([0.0, 2.0, 4.0, 6.0, 8.0, 10.0])
        """
        num_edges = self.num_bins + 1
        edges = np.arange(self.t0, self.t0 + num_edges * self.bin_width, self.bin_width)

        # Ensure exactly num_edges (for safety in rare floating-point cases)
        if len(edges) > num_edges:
            edges = edges[:num_edges]
        return edges


    def time_range(self, bin_idx: int) -> Tuple[float, float]:
        """
            Return the (start, end) time of a bin.
            Contract:
                Returns tuple (bin_start(k), bin_end(k))
                Matches exactly the continuous interval spanned by the bin
        """
        return self.bin_start(bin_idx), self.bin_end(bin_idx)


