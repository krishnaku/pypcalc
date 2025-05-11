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

    Note that an element may have many associated presences over time in the same boundary, and each one is considered
    distinct.
    """

    element: T_Element
    """The element this Presence corresponds to."""

    boundary: Boundary
    """The boundary where this element was present."""

    start: float
    """Start time of the Presence interval."""

    end: float
    """End time of the Presence interval."""




