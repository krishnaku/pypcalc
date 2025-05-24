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

Note that P maps into ℝ (real numbers), rather than into the Boolean set {0, 1}.
This is because applying a time scale to presences—for example, by binning time into discrete intervals —
can yield fractional values for presence. These fractional values represent partial overlap with a bin
and enable presence to be interpreted as a continuous, additive quantity. See class [TimeScale](./time_scale.html) for
more details.

This real-valued interpretation supports robust aggregation, smoothing, and rate-based calculations
within the calculus even as we apply scaling factors to the input timeline.

### Presence onset and reset

$t_0$ is called the <em>onset time</em> of the presence—the instant at which the
presence transitions from zero to non-zero. $t_1$ is called the *reset time* —
the instant at which the presence transitions back to zero.

We will say the presence is *active*
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

### The Time Model

Time in the presence calculus is modeled as a continuous quantity over $\mathbb{R}$.
When interfacing with external systems that operate in wallclock time you will need to
convert between timestamps and dates and floating point numbers when constructing presence assertions.

The [TimeModel](./time_model.html) class (`pcalc.time_model.TimeModel`) is provided for this purpose.

---
### Validity of Presence Assertions

It is crucial to note that the Presence Calculus treats presence assertions
as **axiomatic**: it does not question or make inferences about their validity.

If a presence assertion is derived from point-in-time events, the meaning of
that derivation must be defined within the domain itself.

For example, suppose in a traffic domain we observe that a vehicle (the element) crossed the
1-mile marker at 11:00 AM and the 2-mile marker at 11:10 AM. If we assert that
the vehicle was continuously present (i.e., within the boundary between those
markers) during the interval [11:00, 11:11), that assertion depends on
domain-level assumptions—such as continuity of motion, absence of detours,
or the nonexistence of teleportation.

In a different domain—for example, one in which a wormhole allows instantaneous
travel between Mars and mile 1.6—such an assertion might be invalid.

The Presence Calculus does **not** attempt to resolve or validate such
assumptions. It simply assumes that all presence assertions are valid according
to domain semantics and proceeds to compute their consequences.


### Topology

This brings us to a fundamental distinction between a presence assertion and a
point-in-time event: a presence assertion introduces a natural way to define a
**topology** on the space of entities, boundaries, and time intervals
\( E \times B \times \mathbb{R} \times \mathbb{R} \).

This means that presence assertions allow us to reason about concepts such as
**nearness**, **overlap**, **continuity**, and **structure**—that is, how
things relate across elements, boundaries, and time.

The consequences of presence assertions are not logical in the classical sense,
but **topological**: they give rise to notions of proximity, flow, and
co-presence that reveal the shape, connectedness and dynamics of the domain.

With presence, we can detect patterns such as:
- elements that tend to be present together (co-presence),
- transitions between boundaries, and
- regions of concentrated or evolving presence.

Presence thus provides the foundational structure for understanding the **dynamics
of entities** in a domain.

---

## Presence API

This module defines the data structure and associated methods for Presence, 
and serves as the canonical representation of presence assertions and their topological
 primitives in the
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
