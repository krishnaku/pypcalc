# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass

from metamodel import Presence


# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

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
