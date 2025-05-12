# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

from __future__ import annotations

from dataclasses import dataclass

from metamodel import Presence
from .time_scale import Timescale


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

        effective_start = max(presence.start, ts.t0)
        effective_end = min(presence.end, ts.t1)

        is_mapped = False
        start_bin = -1
        end_bin = -1
        start_value = -1.0
        end_value = -1.0

        if effective_end > effective_start:
            is_mapped = True
            start_bin, end_bin = ts.bin_slice(effective_start, effective_end)

            # Compute partial overlap at start bin
            start_value = ts.fractional_overlap(effective_start, effective_end, start_bin)

            # Compute partial overlap at end bin, if not same as start
            if end_bin - 1 > start_bin:
                end_value = ts.fractional_overlap(effective_start, effective_end, end_bin - 1)
            else:
                end_value = start_value

        self.is_mapped = is_mapped
        self.start_bin = start_bin
        self.end_bin = end_bin
        self.start_value = start_value
        self.end_value = end_value
