# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT
"""
A *Presence* is a foundational concept in the presence calculus and this modules
includes all the concepts for modeling presence and the API to work with them.

Formally, a presence may represented as a 5-tuple:

$$
p = (e, b, t_0, t_1, m)
$$

where:
- $e \in E \subseteq D$ is an element (thing) in the domain $D$,
- $b \in B \subseteq D$ is the boundary (place) in the domain $D$,
- $[t_0, t_1)$ is the half-open interval of presence in time.
- $m \in R$ is called the
<em>mass</em> (or value/weight) of the presence.

A presence can be viewed as a function:

$$
P: E \\times B \\times \\overline{\\mathbb{R}} \\times \\overline{\\mathbb{R}} \\to \\mathbb{R}
$$


where


- $P(e, b, t_0, t_1) = m \gt 0 $  if $e$ is present in $b$ during $[t_0, t_1)$
- $P(e, b, t_0, t_1) = 0 $    otherwise


When $m \in
\\\\{ 0,1 \\\\} $ this corresponds to the base notion of a boolean presence, a statement that an element was
present or not during that interval.

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



### The Open World Assumption

The time interval $[t_0, t_1)$ is defined over the <em>extended</em> reals
$\overline{\mathbb{R}}$: the real line $\mathbb{R}$ extended with the symbols
$-\infty$ and $+\infty$.

This reflects the presence calculus's open world assumption, which permits
intervals that extend indefinitely into the past or future. A presence with
$t_0 = -\infty$ represents a presence whose beginning is unknown, and
$t_1 = +\infty$ represents a presence whose end is unknown.

Presences with both start and end unknown are valid and represent eternal
presences. Many of the most interesting questions in the presence calculus
involve reasoning about the dynamics of a domain under the epistemic
uncertainty introduced by such presences.

---
### Presence Assertions

A Presence Assertion is an assertion about the existence of a presence from
the standpoint of a specific observer at a specific time.

A presence assertion is thus a seven-tuple
$(e, b, t_0, t_1, m, o, t_2)$ where:

- $(e, b, t_0, t_1, m)$ is the presence being asserted,
- $o \in O \subseteq D$ is the observer (a domain entity), and
- $t_2 \in \overline{\mathbb{R}}$ is the assertion time.

Both observer and assertion time may themselves be unknown, and together
they reflect the epistemic *provenance* of the assertion.

Given our open world assumptions, we assume by default that we are reasoning
about *dynamic* sets of presences that reflect observations by various observers
on the underlying domain. Presence assertions may be added or removed
from this set, which in turn changes what we can say about the
state of the domain. We assume (by construction, if necessary) that observers
are part of the domain $D$.

For example, learning the reset time of a presence—when it was previously
unknown—allows us to replace the old assertion with a new one that reflects
greater epistemic certainty about the domain state. A new assertion may update
the onset or reset time based on new information from different observers
(e.g., sensor disagreements), reflecting the evolving nature of knowledge in
an open world.

At any point in time, we are reasoning about a known subset of the domain's
history, and potentially even making assertions about the *future*
(estimates, forecasts, etc., which can also be modeled as presence assertions),
each with its own epistemic status.

It is crucial to note that the presence calculus treats presence assertions as
*axiomatic*: it does not question or infer their validity, nor does it make
decisions based on provenance. However, the provenance of assertions may be
used to reason about the reliability or implications of the conclusions reached
via the machinery of the calculus.

For example, suppose in a traffic domain we observe that a vehicle (the
element) crossed the 1-mile marker at 11:00 AM and the 2-mile marker at
11:10 AM. If we assert that the vehicle was continuously present (i.e.,
within the boundary between those markers) during the interval [11:00, 11:11),
that assertion depends on domain-level assumptions—such as continuity of
motion, absence of detours, or the nonexistence of teleportation.

In a different domain—for example, one in which a wormhole allows
instantaneous travel between Mars and mile 1.6—such an assertion might be
invalid.

The presence calculus does *not* attempt to resolve or validate such
assumptions. It simply assumes that all presence assertions are logically
valid according to domain semantics and proceeds to compute their
consequences using the machinery of the calculus.

### Time as Topology

This brings us to a fundamental property of presences—and the key distinction
between presences and point-in-time events: the continuity of presence gives us
a natural and mathematically precise way to define a *topology* of presence
over the time dimension $\overline{\mathbb{R}}$.

Each presence defines a basic open set in the topology, corresponding to its
half-open interval $[t_0, t_1) \subset \overline{\mathbb{R}}$. The collection of
all such intervals forms a basis for a topology over time, using the standard
technique from point-set topology of generating a topology from a basis of
open sets. See [BasisTopology](./basis_topology.html) for details.

This means that presence assertions allow us to reason about concepts such as
*nearness*, *overlap*, *continuity*, and *structure* of presence in time—
that is, how domain entities relate across time with mathematical precision.

Thus, the consequences of presence assertions are not logical in the classical
sense, but *temporal* and *topological*: they give rise to notions of proximity, flow, and
co-presence in time that reveal the shape, connectedness, and dynamics of the domain
in mathematically precise ways.

With presence, we can reason about patterns such as:
- elements that tend to be present together (co-presence),
- transitions between boundaries,
- regions of concentrated or evolving presence, and
- causal relationships between presences.

Furthermore, the presence calculus introduces certain topological invariants
see [PresenceInvariant](./presence_invariant_discrete.html) that *constrain* the behavior of *sets* of
presence assertions.

This provides the foundational structure for reasoning about the *dynamics*
and *causality* of presences in a domain.

---

## Presence API

This module defines the data structure and associated methods for Presence, 
and serves as the canonical representation of presence assertions and their topological
 primitives in the
presence calculus

Note: When interfacing with external systems that operate in wallclock time you will need to
convert between timestamps and dates and floating point numbers when constructing presence assertions.

The [TimeModel](./time_model.html) class (`pcalc.time_model.TimeModel`) is provided for this purpose.

---
"""

from __future__ import annotations
from typing import Optional, Protocol, runtime_checkable

from dataclasses import dataclass
from typing import Optional, Callable

from .entity import EntityProtocol


PresenceFunction = Callable[[EntityProtocol, EntityProtocol, float], float]
# Presence functions and Presence Protocols
"""
A `PresenceFunction` $f$ is a time-varying function represented as a callable of the form:

```python
(e: EntityProtocol, b: EntityProtocol, t: float) -> float
```

It returns a real-valued signal that is non-zero only when $t$ falls within some half open 
interval $[t_s, t_e)$

Presence functions must satisfy the following property:

- For some half-open interval $[t_s, t_e) in \overline{\mathbb{R}}$, the function is non-zero only within that interval:

    - $f(e, b, t) \\\\ne 0$ only if $t \in [t_s, t_e)$
    - $f(e, b, t) = 0$ elsewhere

The returned value for $f$ in $\mathbb{R}$ can represent any time-varying quantity that has meaning in the domain—
such as revenue, attention, sensor signal strength, or value accrual. Note that since the function domain is over
the extended reals, we do allow these presences to extend infinitely into the past and the future. 

For example, in a sales domain, if the element `e` is a customer and `b` is a customer segment,
the presence function might represent revenue from that customer at time `t`. If $[t_s, t_e)$
represents the customer lifetime, then customer revenue is zero outside that interval. 

<div style="text-align: center; margin:2em">
  <img src="../assets/pcalc/presence_function.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 1: A presence function for customer revenues in the sales domain. 
  </div>
</div>

Note that Inside the interval, the value may still drop to zero — presence does not
require that every value for the presence function remain greater than zero during the interval.


Here are more examples of presence functions in python. 
Note that `constant_presence` corresponds to the most commonly assumed form of
presence in classical models. It represents entities with uniform presence
over a finite interval—from the start of the event to its end—with constant
instantaneous mass.

Much of queueing theory and flow analysis is based solely on this simple
model, where presence is modeled as a rectangular pulse with finite duration
and constant density.

The presence calculus generalizes this by allowing arbitrary real-valued
functions with compact support over the extended real line
$\\overline{\\mathbb{R}}$, enabling richer modeling of non-uniform, delayed,
forecasted, or probabilistic presences.


```python
# Boolean presence: returns 1.0 within [start, end), 0.0 elsewhere
def constant_presence(start: float, end: float) -> PresenceFunction:
    def f(e, b, t):
        return 1.0 if start <= t < end else 0.0
    return f

# Ramped presence: increases linearly from 0.0 to 1.0 over [start, end)
def ramp_presence(start: float, end: float) -> PresenceFunction:
    def f(e, b, t):
        if start <= t < end:
            return (t - start) / (end - start)
        return 0.0
    return f

# Delayed pulse: returns fixed value only after a delay from start
def delayed_presence(start: float, end: float, delay: float = 1.0) -> PresenceFunction:
    def f(e, b, t):
        if start + delay <= t < end:
            return 1.0
        return 0.0
    return f
```

These functions form the foundation of presence semantics.

Presence functions are defined *in the domain* and serve as the bridge between discrete
domain events and continuous presence intervals used in the presence calculus. 
They are exposed to the presence calculus via the `PresenceProtocol`.

"""


@runtime_checkable
class PresenceProtocol(Protocol):
    """
    The PresenceProtocol represents the  contract between an arbitrary presence function
    and the foo
    """

    def __call__(self, t0: float, t1: float) -> float: ...



    def overlaps(self, t0: float, t1: float) -> bool: ...

    @property
    def onset_time(self) -> float: ...

    @property
    def reset_time(self) -> float: ...


@dataclass(frozen=True)
class PresenceAssertion:
    """

    This is the fundamental, immutable construct of The presence calculus,
    and asserts the presence of an element at a boundary over a continuous interval of time.

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
    presence: Optional[PresenceProtocol] = None
    observer: Optional[EntityProtocol] | str = "observed"
    assert_time: Optional[float] = 0.0

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

    def mass(self) -> float:
        """
        Returns the mass of the presence.


        
        """
        onset = max(0.0, self.onset_time)
        return max(0.0, self.reset_time - onset)

    def mass_contribution(self, t0: float, t1: float) -> float:
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
            f"interval={interval_str}, provenance={self.observer})"
        )


EMPTY_PRESENCE: PresenceAssertion = PresenceAssertion(
    element=None,
    boundary=None,
    presence=None,
    onset_time=0.0,
    reset_time=0.0,
    observer="empty",
)
