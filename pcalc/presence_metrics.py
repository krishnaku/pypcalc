# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved
# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from typing import Generic, Optional
import numpy as np

from metamodel import Presence, T_Element
from pcalc import PresenceMatrix, PresenceMap

class PresenceMetrics(Generic[T_Element]):
    """
    Metrics for Presence over a finite interval of a timescale in a PresenceMatrix.

    All metrics operate over a sub-interval [start_time, end_time) of
    end points (t0, t1] of the timescale for the underlying PresenceMatrix,
    unless otherwise documented.

    These metrics are the primitive building blocks for the colloquially familiar Flow Metrics, and provide
    a more precise set of measurements that allow us to reason causally about flow metrics.
    """

    def __init__(self, matrix: PresenceMatrix[T_Element]):
        self.matrix = matrix
        """"""
        self.presences: list[Presence] = matrix.presences
        """Only presences that overlap the interval [t0, t1) are included in Presence Metrics.
        Note however that this may include presences that started before the interval or ended after the interval."""

        self.presence_map: list[PresenceMap] = matrix.presence_map
        """Only presences that overlap the interval [t0, t1) are included in Presence Metrics.
        Note however that this may include presences that started before the interval or ended after the interval."""

        self.ts = matrix.time_scale
        """The timescale of the presence matrix. This is the default 'window' over which all metrics are computed."""

    def _resolve_range(self, start_time: Optional[float], end_time: Optional[float]) -> tuple[float, float]:
        start = start_time if start_time is not None else self.ts.t0
        end = end_time if end_time is not None else self.ts.t1
        if start_time < self.ts.t0 or end_time > self.ts.t1:
            raise ValueError(
                f"Presence metrics are not defined outside the time scale of the presence matrix."
                f"Time scale = [{self.ts.t0}, {self.ts.t1})."
                f"Provided: [{start_time}, {end_time})"
            )
        return start, end



    def average_presence_per_bin(self, start_time: float = None, end_time: float = None) -> float:
        start, end = self._resolve_range(start_time, end_time)
        matrix = self.matrix
        col_start, col_end = self.ts.bin_slice(start, end)

        if col_end <= col_start:
            return 0.0

        slice_matrix = matrix[:, col_start:col_end]
        total = np.sum(slice_matrix)
        duration = end - start
        return total / duration

    def average_residence_time_per_presence(self, start_time: float = None, end_time: float = None) -> float:
        start, end = self._resolve_range(start_time, end_time)

        total_overlap = 0.0
        for p in self.presences:
            overlap = max(0.0, min(p.end, end) - max(p.start, start))
            total_overlap += overlap

        if not self.presences:
            return 0.0
        return total_overlap / len(self.presences)

    def flow_rate(self, start_time: float = None, end_time: float = None) -> float:
        """
        The average flow rate (arrival/throughput) for the Presence Matrix
        over the time interval [start_time, end_time).

        The flow rate is defined as:
            number of active presences in the matrix slice [:start_bin:end_bin] /
            number of time bins in the slice (end_bin - start_bin)

        Conceptually:
            Let N be the number of presences (rows) that are active (non-zero)
            in the matrix between start_time and end_time.

            Let T be the number of discrete time bins (columns) in that interval.

            Then:
                flow_rate = N / T

        Examples:
            - If 4 presences span a 6-bin window, flow_rate = 4 / 6 = 0.666...
            - If only one open-ended presence remains active over a 4-bin window, flow_rate = 1 / 4 = 0.25

        The flow rate is a finite-window estimate of both long-run arrival rate and departure rate.
        The precise relationship between flow rate, arrival rate, and departure rate is as follows:

            N = number of presences that started *before* start_time (see `starting_presence_count`)
                + number that started *in* the interval [start_time, end_time) (see `arrival_count`)

              — this is also called the cumulative arrivals into the window

            or equivalently:

            N = number of presences that *ended* in [start_time, end_time) (see `departure_count`)
                + number that ended *after* end_time (see `ending_presence_count`)

              — this is the departure contribution from the window

            These two decompositions of N are always equal; they just reflect different
            ways of expressing the same set of active presences.

        Intuitively, over a long enough window, if flow converges, most presences
        will start and end within the window, with fewer presences that partially overlap
        the interval at the beginning and end.

        This makes N a good estimator of true arrivals or departures over that interval.

        In other words, if flow through the boundary is asymptotically convergent over [start_time, end_time),
        then:
            flow_rate → arrival_rate → departure_rate

        When flow is fully convergent over the interval, then:
            flow_rate = arrival_rate = departure_rate

        This equality is one of the key conditions for *stable* flow through the boundary.

        On the other hand, if flow is not convergent over the interval, the delta between
        flow rate, arrival rate, and departure rate will be large — either increasing (divergent)
        or decreasing (convergent) over time.
        """
        start, end = self._resolve_range(start_time, end_time)
        start_bin, end_bin = self.ts.bin_slice(start, end)

        num_bins = end_bin - start_bin
        if num_bins <= 0:
            return 0.0

        count = sum(1 for pm in self.presence_map if pm.is_active(start_bin, end_bin))
        return count / num_bins

    def starting_presence_count(self, start_time: float = None, end_time: float = None) -> int:
        start, end = self._resolve_range(start_time, end_time)
        start_bin, end_bin = self.ts.bin_slice(start, end)

        return sum(
            1 for pm in self.presence_map
            if pm.is_active(start_bin, end_bin)
            #Note: here we must explicitly check the un-clipped
            # bin indices, since we are looking for end indices that fall outside the
            # window and even the matrix. So pm.end_bin is not the right test here.
            and self.ts.bin_index(pm.presence.start) < start_bin
        )

    def ending_presence_count(self, start_time: float = None, end_time: float = None) -> int:
        start, end = self._resolve_range(start_time, end_time)
        start_bin, end_bin = self.ts.bin_slice(start, end)

        return sum(
            1 for pm in self.presence_map
            if pm.is_active(start_bin, end_bin)
            and (np.isinf(pm.presence.end) or
                 # Note: here we must explicitly check the un-clipped
                 # bin indices, since we are looking for end indices that fall outside the
                 # window and even the matrix. So pm.end_bin is not the right test here.
                 self.ts.bin_index(pm.presence.end) >= end_bin)
        )

    def arrival_count(self, start_time: float = None, end_time: float = None) -> int:
        """The number of presences that started within the window"""
        start, end = self._resolve_range(start_time, end_time)
        start_bin, end_bin = self.ts.bin_slice(start, end)

        return sum(
            1 for pm in self.presence_map
            if start_bin <= self.ts.bin_index(pm.presence.start) < end_bin
        )

    def departure_count(self, start_time: float = None, end_time: float = None) -> int:
        start, end = self._resolve_range(start_time, end_time)
        start_bin, end_bin = self.ts.bin_slice(start, end)

        return sum(
            1 for pm in self.presence_map
            if np.isfinite(pm.presence.end)
            and pm.is_active(start_bin, end_bin)
            and self.ts.bin_index(pm.presence.end) in range(start_bin, end_bin)
        )