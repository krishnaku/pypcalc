from __future__ import annotations

from dataclasses import dataclass
from typing import Generic

from .element import T_Element


@dataclass
class Presence(Generic[T_Element]):
    """
    A continuous interval during which a domain element is considered present within a boundary.

    A `Presence` captures a presence interval for a single `element`, including start and end times,

    A `core.boundary.Boundary` is responsible for mapping a set of point in time `core.timeline.DomainEvents` into
    Presences.
    """

    element: T_Element
    """The element this Presence corresponds to."""

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


