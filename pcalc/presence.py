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

A presence can be viewed as a function:

$$
P: E \\times B \\times \\mathbb{R} \\times \\mathbb{R} \\to \\mathbb{R}
$$


where


- $P(e, b, t_0, t_1) = 1$  if $e$ is present in $b$ during $[t_0, t_1)$
- $P(e, b, t_0, t_1) = 0$  otherwise

### Presence onset and reset

$t_0$ is called the onset time of the presence—the instant at which the
presence transitions from zero to non-zero. $t_1$ is called the reset time—
the instant at which the presence transitions back to zero. The presence is *active*
over the half-open interval $[t_0, t_1)$, meaning it
includes $t_0$ but excludes $t_1$.

<div style="text-align: center; margin: 2em 0;">
  <img src="../assets/pcalc/half_open_presence.png" width="400px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 0.5em;">
    Figure: A presence interval $[t_0, t_1)$ with $t_0$ included (●) and
    $t_1$ excluded (○).
  </div>
</div>

This diagram illustrates a presence assertion over a half-open interval
$[t_0, t_1)$, where element $e$ is continuously present in boundary $b$
starting at $t_0$ (included) and ending just before $t_1$ (excluded).
Time is modeled as a continuous quantity over $\mathbb{R}$.

## Structure

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
from .entity import EntityProtocol



@runtime_checkable
class PresenceProtocol(Protocol):
    """The structural and behavioral contract for a Presence."""
    __init__ = None  # type: ignore

    @property
    def element(self) -> Optional[EntityProtocol]: ...

    @property
    def boundary(self) -> Optional[EntityProtocol]: ...

    @property
    def onset_time(self) -> float: ...

    @property
    def reset_time(self) -> float: ...

    @property
    def provenance(self) -> str: ...

    def overlaps(self, t0: float, t1: float) -> bool: ...



    def duration(self) -> float: ...

    def residence_time(self, t0: float, t1: float) -> float: ...

    def __str__(self) -> str: ...


class PresenceMixin:
    """
    Common logic for all Presence implementations. Assumes consuming class
    defines `element`, `boundary`, `start`, `end`, and `provenance` properties.
    """

    def overlaps(self: PresenceProtocol, t0: float, t1: float) -> bool:
        return self.reset_time > t0 and self.onset_time < t1


    def duration(self: PresenceProtocol) -> float:
        return max(0.0, self.reset_time - self.onset_time)

    def residence_time(self: PresenceProtocol, t0: float, t1: float) -> float:
        if t0 >= t1 or not self.overlaps(t0, t1):
            return 0.0

        start = max(self.onset_time, t0)
        end = min(self.reset_time, t1)
        return max(0.0, end - start)

    def __str__(self: PresenceProtocol) -> str:
        element_str = str(self.element) if self.element is not None else "None"
        boundary_str = str(self.boundary) if self.boundary is not None else "None"
        interval_str = f"[{self.onset_time}, {self.reset_time})"
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
            element: Optional[EntityProtocol],
            boundary: Optional[EntityProtocol],
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
    def element(self) -> Optional[EntityProtocol]:
        return self._element

    @property
    def boundary(self) -> Optional[EntityProtocol]:
        return self._boundary

    @property
    def onset_time(self) -> float:
        return self._start

    @property
    def reset_time(self) -> float:
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

    _element: Optional[EntityProtocol]
    _boundary: Optional[EntityProtocol]
    _start: float
    _end: float
    _provenance: str

    def __init__(
            self,
            element: Optional[EntityProtocol],
            boundary: Optional[EntityProtocol],
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
    def element(self) -> Optional[EntityProtocol]:
        return self._element

    @property
    def boundary(self) -> Optional[EntityProtocol]:
        return self._boundary

    @property
    def onset_time(self) -> float:
        return self._start

    @property
    def reset_time(self) -> float:
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
