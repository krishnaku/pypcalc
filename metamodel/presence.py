# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from .boundary import Boundary

T_Element = TypeVar("T_Element")


@dataclass
class Presence(Generic[T_Element]):
    """
    An assertion that a domain element was continuously present in a boundary
    during a specific time interval [start, end).

    Presences reflect observations or inferences, not
    guarantees about reality, and thus are epistemic in nature.

    An element can have multiple presences over time.
    If those intervals overlap, we treat them as part of the same underlying presence—
    fragments of the same thing - regardless of the boundary.

    Similarly, an element may overlap in time across presences in multiple boundaries.
    We will use this as the definition that the boundaries intersect. In other words,
    boundary topology is dynamic and emerges from element presence.
    
    """

    element: Optional[T_Element]
    """The element this Presence corresponds to. May be None in EmptyPresence."""

    boundary: Optional[Boundary]
    """The boundary where this element was present. None for EmptyPresence."""

    start: float
    """Start time of the Presence interval."""

    end: float
    """
    End time of the Presence interval.

    A value of `np.inf` indicates an open-ended presence — i.e., the element has
    not yet exited the boundary or no end event has been observed.
    """

    provenance: str = "observed"
    """
    The epistemic status of this presence. Could be 'observed', 'inferred',
    'imputed', etc. Not used in algebraic operations yet, but important for
    future modeling of epistemic certainty. 
    """

    def overlaps(self, t0: float, t1: float) -> bool:
        """
        Return True if this presence overlaps the time interval [t0, t1).

        Overlap means there exists a nonzero-duration intersection between
        [self.start, self.end) and [t0, t1).
        """
        return self.end > t0 and self.start < t1

    def clip(self, t0: float, t1: float) -> Optional["Presence[T_Element]"]:
        """
        Return a new Presence representing the clipped overlap with [t0, t1),
        or None if there is no overlap.

        The resulting presence inherits element and boundary of the original.
        """
        if not self.overlaps(t0, t1):
            return None

        start = max(self.start, t0)
        end = min(self.end, t1)

        if start < end:
            return Presence(
                element=self.element,
                boundary=self.boundary,
                start=start,
                end=end,
                provenance=f"clipped from {self}"
            )
        else:
            return EMPTY_PRESENCE

    def duration(self) -> float:
        """
        Return the full duration of the presence.

        Returns `inf` if the presence is open-ended (`end = np.inf`).
        Returns 0.0 if the interval is empty.
        """
        return max(0.0, self.end - self.start)

    def residence_time(self, t0: float, t1: float) -> float:
        """
        Returns the duration of this presence when clipped to the interval [t0, t1).

        Always returns a finite value ≥ 0.
        """
        if t0 >= t1 or not self.overlaps(t0, t1):
            return 0.0

        start = max(self.start, t0)
        end = min(self.end, t1)
        return max(0.0, end - start)

    def __str__(self) -> str:
        """
        Return a human-readable summary of this presence for logging or provenance tracking.
        Format: 'Presence(element=E, boundary=B, [start, end), provenance=...)'
        """
        element_str = str(self.element) if self.element is not None else "None"
        boundary_str = str(self.boundary) if self.boundary is not None else "None"
        interval_str = f"[{self.start}, {self.end})"
        return f"Presence(element={element_str}, boundary={boundary_str}, interval={interval_str}, provenance={self.provenance})"


# Define a canonical EmptyPresence constant for algebraic identity
EMPTY_PRESENCE: Presence = Presence(
    element=None,
    boundary=None,
    start=0.0,
    end=0.0,
    provenance="empty"
)
