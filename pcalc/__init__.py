# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

"""
#The Presence Calculus Toolkit
© 2025 Krishna Kumar
SPDX-License-Identifier: MIT


The Presence Calculus provides a mathematically rigorous formalism for reasoning about the relationship
between *things* and *places* over *time*.

It starts with [*Presence*](./pcalc/presence.html), an assertion that a certain  [*Element*](./pcalc/element.html) (thing) was present *continuously*
in a [*Boundary*](./pcalc/boundary.html) (place) over a *continuous* interval of *time*.

Starting with an arbitrary model of elements, boundaries and presences, the Presence Calculus builds
rigorous tools to reason about the relationship between flows, delays and accumulations across a wide range
of systems, including stochastic, non-linear, and complex adaptive systems.

<div style="text-align: center; margin:2em">
  <img src="./assets/pcalc/presence_calculus.svg" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em;margin-bottom: 1em;">
    Figure 1 Key constructs: presences, element paths, presence matrix, and co-presence topology
  </div>
</div>

Further, extending the notion of presences to *functions over presences* give us ways to reason about the *effects* of
presence, giving us a powerful new way to reason about time value and option value of presence.

The Presence Calculus lies at the intersection of stochastic process dynamics, queueing theory, topology, and
complex systems science—yet remains philosophically adjacent to all of them.
It draws from each field while re-framing their perspectives through the epistemic lens of presence.

 It provides an elementary and accessible entry point to some of the most abstract
 concepts in these domains, while supporting precise, computable formulations capable of powering real-time analysis
 and simulation of complex systems.

The Presence Calculus Toolkit—and the `pcalc` module in particular—is a minimal,
computationally efficient implementation of the core concepts and calculations
in Presence Calculus.

It is designed as a lightweight, easy-to-integrate analytical middleware library
that connects real-time event streams, simulation models, and static datasets
(from which presence assertions can be inferred) to rich visualization and
analysis tools.

While we provide several examples of end to end integrations, this open source library is MIT licensed and
you are encouraged to create models and applications, both commercial and non-commercial that
can apply the concepts of The Presence Calculus.

The concepts here are simple and elementary even though they are mathematically rigorous, and
I believe the space of potential applications of ths toolkit are vast.

I encourage you to explore and reach out if you have any questions, or wish to collaborate.

Dr. Krishna Kumar,

The Polaris Advisor Program

"""

from .element import Element
from .boundary import Boundary
from .presence import Presence
from .presence_matrix import PresenceMatrix
from .time_scale import Timescale
from .presence_map import PresenceMap
from .presence_invariant import PresenceInvariant
