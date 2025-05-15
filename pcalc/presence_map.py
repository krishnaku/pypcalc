# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT


from __future__ import annotations

from dataclasses import dataclass

from metamodel import Presence
from .time_scale import Timescale


@dataclass
class PresenceMap:
    """
        A PresenceMap maps a continuous presence interval [start, end)
        onto a discrete time grid defined by a Timescale.

        The result is a bin-aligned representation:
        - `start_bin` is the index of the first bin touched
        - `end_bin` is the exclusive upper bound (i.e., first bin not touched)
        - `start_value` and `end_value` represent fractional presence at the edges
        - Bins between `start_bin` and `end_bin` are fully or partially covered

        Contract:
        - A presence is considered "mapped" if it overlaps the timescale [t0, t1)
        - Mapped presences always produce:
            start_bin ∈ [0, num_bins)
            end_bin   ∈ (start_bin, num_bins]
        - The bin range [start_bin, end_bin) contains all and only the bins the presence overlaps
        - start_value ∈ (0.0, 1.0] if partially covers `start_bin`
        - end_value   ∈ (0.0, 1.0] if partially covers `end_bin - 1`
    """

    presence: Presence
    """The presence entry"""
    time_scale: Timescale
    """The time scale that the presence is mapped to"""

    is_mapped: bool
    """True if the presence has a valid mapping. Unmapped presences have value=-1
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
    """A presence value 0 < p < 1.0 that represents a potentially partial presence at the end of the mapping"""

    @property
    def bin_range(self) -> range:
        return range(self.start_bin, self.end_bin) if self.is_mapped else range(0)

    @property
    def duration(self) -> float:
        return self.presence.end - self.presence.start


    def __init__(self, presence: Presence, time_scale: Timescale):
        """
        Map a presence interval to matrix slice indices and edge fractional values
        using the provided Timescale object.
         """
        self.presence = presence
        self.time_scale = time_scale
        ts = self.time_scale
        is_mapped = False
        start_bin = -1
        end_bin = -1
        start_value = -1.0
        end_value = -1.0

        if presence.overlaps(ts.t0, ts.t1):
            is_mapped = True
            start_bin, end_bin = ts.bin_slice(presence.start, presence.end)
            start_value, end_value = self._compute_fractional_values(presence.start, start_bin, presence.end, end_bin)

        self.is_mapped = is_mapped
        self.start_bin = start_bin
        self.end_bin = end_bin
        self.start_value = start_value
        self.end_value = end_value

    def _compute_fractional_values(self, start_time: float, start_bin: int, end_time: float, end_bin: int):
        ts = self.time_scale
        # Compute partial overlap at start bin
        start_value = ts.fractional_overlap(start_time, end_time, start_bin)

        # Compute partial overlap at end bin, if not same as start
        if end_bin - 1 > start_bin:
            end_value = ts.fractional_overlap(start_time, end_time, end_bin - 1)
        else:
            end_value = 0.0

        return start_value, end_value


    def is_active(self, start_bin: int, end_bin: int):
        return end_bin > self.start_bin and start_bin < self.end_bin

    def presence_value_in(self, start_time: float, end_time: float) -> float:
        """
        Computes total presence value (in time) within [start_time, end_time),
        using bin-based approximation logic, clipped to the given interval.
        """
        ts = self.time_scale
        bin_width = ts.bin_width

        start_bin, end_bin = ts.bin_slice(start_time, end_time)
        if self.is_mapped and self.is_active(start_bin, end_bin):
            #  Clip window to actual presence bounds
            effective_start = max(self.presence.start, start_time)
            effective_end = min(self.presence.end, end_time)

            effective_start_bin, effective_end_bin = ts.bin_slice(effective_start, effective_end)

            if start_time == ts.t0 and end_time == ts.t1:
                start_value = self.start_value
                end_value = self.end_value
            else:
                start_value, end_value = self._compute_fractional_values(effective_start, effective_start_bin, effective_end, effective_end_bin)

            full_bin_value = max(0, effective_end_bin - effective_start_bin - 2)

            fractional_value = start_value + end_value

            return (full_bin_value + fractional_value) * bin_width
        else:
            return 0.0

    @property
    def presence_value(self) -> float:
        return self.presence_value_in(self.time_scale.t0, self.time_scale.t1)