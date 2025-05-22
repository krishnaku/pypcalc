# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT
"""
A *Presence* is the foundational assertion in the Presence Calculus. It states
that a specific element was continuously present within a specific boundary
over a defined time interval.

Formally, a presence is represented as a 4-tuple:

$$
p = (e, b, t_0, t_1)
$$

where:
- $e \in E$ is the element (thing),
- $b \in B$ is the boundary (place),
- $[t_0, t_1)$ is the half-open interval of presence in time.

Presence assertions define the structure from which all other constructs in
Presence Calculus are derived—such as element timelines, flow rates,
co-presence, accumulations, and topological structures.

A presence does not require knowledge of the internal state of elements or
boundaries—only that the element was known to be present in the boundary
during the specified time interval.

This module defines the data structure and associated methods for Presence, 
and serves as the canonical representation of presence assertions in the
presence calculus
"""

from __future__ import annotations
from typing import Optional, Protocol, runtime_checkable
import numpy as np
from .element import Element
from .boundary import Boundary


@runtime_checkable
class PresenceProtocol(Protocol):
    """
    A Presence is the foundational assertion in the Presence Calculus. It states
    that a specific element was continuously present within a specific boundary
    over a defined time interval.

    Formally, a presence is represented as a 4-tuple:

    $$
    p = (e, b, t_0, t_1)
    $$

    where:
    - $e \in E$ is the element (thing),
    - $b \in B$ is the boundary (place),
    - $[t_0, t_1)$ is the half-open interval of presence in time.
    """

    @property
    def element(self) -> Optional[Element]: ...

    @property
    def boundary(self) -> Optional[Boundary]: ...

    @property
    def start(self) -> float: ...

    @property
    def end(self) -> float: ...

    @property
    def provenance(self) -> str: ...

    def overlaps(self, t0: float, t1: float) -> bool: ...

    def clip(self, t0: float, t1: float) -> Optional[PresenceProtocol]: ...

    def duration(self) -> float: ...

    def residence_time(self, t0: float, t1: float) -> float: ...

    def __str__(self) -> str: ...


class PresenceMixin:
    """
    Common logic for all Presence implementations. Assumes consuming class
    defines `element`, `boundary`, `start`, `end`, and `provenance` properties.
    """

    def overlaps(self: PresenceProtocol, t0: float, t1: float) -> bool:
        return self.end > t0 and self.start < t1

    def clip(self: PresenceProtocol, t0: float, t1: float) -> Optional[Presence]:
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
                provenance=f"clipped from {self}",
            )
        else:
            return EMPTY_PRESENCE

    def duration(self: PresenceProtocol) -> float:
        return max(0.0, self.end - self.start)

    def residence_time(self: PresenceProtocol, t0: float, t1: float) -> float:
        if t0 >= t1 or not self.overlaps(t0, t1):
            return 0.0

        start = max(self.start, t0)
        end = min(self.end, t1)
        return max(0.0, end - start)

    def __str__(self: PresenceProtocol) -> str:
        element_str = str(self.element) if self.element is not None else "None"
        boundary_str = str(self.boundary) if self.boundary is not None else "None"
        interval_str = f"[{self.start}, {self.end})"
        return (
            f"Presence(element={element_str}, boundary={boundary_str}, "
            f"interval={interval_str}, provenance={self.provenance})"
        )


class Presence(PresenceMixin, PresenceProtocol):
    """
    Default implementation of PresenceProtocol.
    """
    __slots__ = ("_element", "_boundary", "_start", "_end", "_provenance")

    def __init__(
            self,
            element: Optional[Element],
            boundary: Optional[Boundary],
            start: float,
            end: float,
            provenance: str = "observed",
    ) -> None:
        self._element = element
        self._boundary = boundary
        self._start = start
        self._end = end
        self._provenance = provenance

    @property
    def element(self) -> Optional[Element]:
        return self._element

    @property
    def boundary(self) -> Optional[Boundary]:
        return self._boundary

    @property
    def start(self) -> float:
        return self._start

    @property
    def end(self) -> float:
        return self._end

    @property
    def provenance(self) -> str:
        return self._provenance


class PresenceView(PresenceMixin, PresenceProtocol):
    """
    Immutable view over a Presence-like object. Use this when exposing presence
    data from external sources or enforcing read-only access.
    """

    __slots__ = ("_element", "_boundary", "_start", "_end", "_provenance")

    _element: Optional[Element]
    _boundary: Optional[Boundary]
    _start: float
    _end: float
    _provenance: str

    def __init__(
            self,
            element: Optional[Element],
            boundary: Optional[Boundary],
            start: float,
            end: float,
            provenance: str = "observed",
    ) -> None:
        object.__setattr__(self, "_element", element)
        object.__setattr__(self, "_boundary", boundary)
        object.__setattr__(self, "_start", start)
        object.__setattr__(self, "_end", end)
        object.__setattr__(self, "_provenance", provenance)

    def __setattr__(self, key: str, value: object) -> None:
        raise AttributeError("PresenceView is immutable.")

    @property
    def element(self) -> Optional[Element]:
        return self._element

    @property
    def boundary(self) -> Optional[Boundary]:
        return self._boundary

    @property
    def start(self) -> float:
        return self._start

    @property
    def end(self) -> float:
        return self._end

    @property
    def provenance(self) -> str:
        return self._provenance


EMPTY_PRESENCE: Presence = Presence(
    element=None,
    boundary=None,
    start=0.0,
    end=0.0,
    provenance="empty",
)
