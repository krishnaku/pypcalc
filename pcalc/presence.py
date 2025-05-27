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



from dataclasses import dataclass
from typing import Optional
import numpy as np
from .entity import EntityProtocol


@dataclass(frozen=True)
class Presence:
    """
    A presence assertion in the Presence Calculus.

    This is a fundamental, immutable construct representing the presence of an
    element at a boundary over a continuous interval of time.

    A presence is defined over a half-open interval $[t_0, t_1)$ on the real
    line, where $t_0$ is the onset time and $t_1$ is the reset time.

    The
    following constraints must hold:

    - $t_0 < t_1$
    - $t_0 \\in \\mathbb{R} \\cup \\{-\\infty\\}$
    - $t_1 \\in \\mathbb{R} \\cup \\{+\\infty\\}$
    - $t_0 \\ne +\\infty$
    - $t_1 \\ne -\\infty$

    These rules ensure that the interval is well-formed, bounded on the left,
    and open on the right. Intervals such as $[2.0, 5.0)$, $[-\\infty, 4.2)$,
    and $[1.0, +\\infty)$ are allowed, as are the special case $[-\\infty,
    +\\infty)$ and $[0,0),$ the empty presence.

    With the empty presence as the only exception, intervals with zero or negative duration, or with reversed or
    undefined bounds, are disallowed.
    """
    element: Optional[EntityProtocol]
    boundary: Optional[EntityProtocol]
    onset_time: float
    reset_time: float
    provenance: str = "observed"

    def __post_init__(self):
        """
        Validates the temporal bounds of the presence interval
        """
        if self.onset_time >= self.reset_time:
            if not (self.onset_time == self.reset_time == 0):
                raise ValueError(
                    f"Invalid interval: onset_time ({self.onset_time}) must be less than reset_time ({self.reset_time})")

        if self.onset_time == float("inf"):
            raise ValueError("Presence cannot begin at +inf")

        if self.reset_time == float("-inf"):
            raise ValueError("Presence cannot end at -inf")

    def overlaps(self, t0: float, t1: float) -> bool:
        return self.reset_time > t0 and self.onset_time < t1

    def duration(self) -> float:
        """
        Returns the duration of the presence, interpreted as the total length
        of time the element is asserted to have been present.

        If the onset time is finite, the duration is simply:

            duration = max(0, reset_time - onset_time)

        If the onset time is -∞, the presence is treated as beginning at the
        start of observation time (t = 0) for the purpose of duration
        calculation. This bounds the duration to a finite value when
        reset_time is known.

        Thus, for onset_time = -∞ and reset_time = t₁ < ∞, we compute:

            duration = max(0, t₁ - 0) = t₁

        If the reset time is ∞, the duration is ∞, regardless of onset time.

        This behavior ensures that durations remain meaningful and converge
        within systems where observation windows begin at t = 0, while still
        preserving the semantic intent of presences that began before the
        observable history.
        """
        onset = max(0.0, self.onset_time)
        return max(0.0, self.reset_time - onset)

    def residence_time(self, t0: float, t1: float) -> float:
        if t0 >= t1 or not self.overlaps(t0, t1):
            return 0.0
        start = max(self.onset_time, t0)
        end = min(self.reset_time, t1)
        return max(0.0, end - start)


    def __str__(self) -> str:
        element_str = str(self.element) if self.element is not None else "None"
        boundary_str = str(self.boundary) if self.boundary is not None else "None"
        interval_str = f"[{self.onset_time}, {self.reset_time})"
        return (
            f"Presence(element={element_str}, boundary={boundary_str}, "
            f"interval={interval_str}, provenance={self.provenance})"
        )

EMPTY_PRESENCE: Presence = Presence(
    element=None,
    boundary=None,
    onset_time=0.0,
    reset_time=0.0,
    provenance="empty",
)

