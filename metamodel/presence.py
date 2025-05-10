from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TYPE_CHECKING

from .element import T_Element
if TYPE_CHECKING:
    from .boundary import Boundary

@dataclass
class Presence(Generic[T_Element]):
    """
    A statement that a domain element was continuously present in a  boundary
    for a time interval.

    In contrast to a domain event which locates a domain element in time, a `Presence` captures time and location
    of a domain element within the domain.

    The requirement of continuity of presence, in a boundary means that, in principle, one
    can recover the entire trajectory of the domain element in the domain given a complete
    history of the presences of the element within boundaries.

    Note that an element may be present in many boundaries at the same time, ie presences, can overlap.
    """

    element: T_Element
    """The element this Presence corresponds to."""

    boundary: Boundary
    """The boundary where this element was present."""
    start: float
    """Start time of the Presence interval."""

    end: float
    """End time of the Presence interval."""

    presence_row: int = -1
    """The row index assigned to this Presence in the `PresenceMatrix`."""

    start_bin: int = -1
    """The index of the first time bin where the Presence is active."""

    end_bin: int = -1
    """The index of the last time bin where the Presence is active."""

    def overlaps(self, t0: int, t1: int) -> bool:
        """
        Check whether this Presence overlaps with the given time interval.

        Args:
            t0: Start of the comparison window.
            t1: End of the comparison window.

        Returns:
            True if the Presence overlaps any part of [t0, t1), False otherwise.
        """
        return self.start < t1 and self.end > t0

    def duration(self) -> float:
        """
        Return the duration of the Presence.

        Returns:
            The length of the interval in time units.
        """
        return self.end - self.start


