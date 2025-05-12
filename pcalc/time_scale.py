# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
import numpy as np
import numpy.typing as npt

@dataclass
class Timescale:
    """
    Timescale represents a partition of a continuous time interval [t0, t1)
    into a fixed number of equal-width bins, where each bin spans `bin_width` time units.

    This class provides utility methods for:
    - Mapping continuous time values to discrete bin indices
    - Retrieving the time boundaries of bins
    - Determining which bins are touched by a time interval
    - Computing the fractional overlap of an interval with a specific bin

    It is the foundational object used in constructing presence matrices, allowing
    continuous presence intervals to be consistently and accurately projected onto
    a discrete time grid for analysis or visualization.
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

    def bin_edges(self) -> np.ndarray:
        """
        Return an array of bin edge times from t0 to t1, spaced by bin_width.

        The result has length `num_bins + 1` and is safe against floating-point rounding
        by capping the range to include exactly the number of bins implied by `num_bins()`.

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


    def bin_index(self, time: float) -> int:
        """Return the bin index for a given time (floor)."""
        return int(np.floor((time - self.t0) / self.bin_width))

    def bin_start(self, bin_idx: int) -> float:
        """Return the start time of a bin given its index."""
        return self.t0 + bin_idx * self.bin_width

    def bin_end(self, bin_idx: int) -> float:
        """Return the end time of a bin given its index."""
        return self.t0 + (bin_idx + 1) * self.bin_width

    def time_range(self, bin_idx: int) -> Tuple[float, float]:
        """Return the (start, end) time of a bin."""
        return self.bin_start(bin_idx), self.bin_end(bin_idx)

    def bin_slice(self, start: float, end: float) -> Tuple[int, int]:
        """Return the slice of bin indices [start_bin, end_bin) that a time interval overlaps."""
        effective_start = max(start, self.t0)
        effective_end = min(end, self.t1)
        start_bin = int(np.floor((effective_start - self.t0) / self.bin_width))
        end_bin = int(np.ceil((effective_end - self.t0) / self.bin_width))
        return start_bin, end_bin

    def fractional_overlap(self, start: float, end: float, bin_idx: int) -> float:
        """Return the fraction of the bin at index `bin_idx` that is covered by the interval [start, end)."""
        bin_start = self.bin_start(bin_idx)
        bin_end = self.bin_end(bin_idx)
        overlap_start = max(start, bin_start)
        overlap_end = min(end, bin_end)
        return max(0.0, overlap_end - overlap_start) / self.bin_width

