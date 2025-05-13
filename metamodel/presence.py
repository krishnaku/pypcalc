from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TYPE_CHECKING, Optional

from .element import T_Element

if TYPE_CHECKING:
    from .boundary import Boundary

@dataclass
class Presence(Generic[T_Element]):
    """
    A statement that a domain element was continuously present in a boundary
    during a specific time interval.

    Unlike a DomainEvent, which captures a point-in-time signal, a `Presence`
    represents a continuous interval in which the element was active or resident
    within a boundary.

    The assumption of continuity allows full reconstruction of element trajectories
    within the domain if all presences are known.

    Multiple distinct presences for the same element in the same boundary may occur over time.
    """

    element: T_Element
    """The element this Presence corresponds to."""

    boundary: Boundary
    """The boundary where this element was present."""

    start: float
    """Start time of the Presence interval."""

    end: float
    """
    End time of the Presence interval.

    A value of `np.inf` indicates an open-ended presence — i.e., the element has
    not yet exited the boundary or no end event has been observed.
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
        """
        if not self.overlaps(t0, t1):
            return None

        return Presence(
            element=self.element,
            boundary=self.boundary,
            start=max(self.start, t0),
            end=min(self.end, t1),
        )

    def duration(self) -> float:
        """
        Return the full duration of the presence.

        Returns `inf` if the presence is open-ended (`end = np.inf`).
        """
        return self.end - self.start
