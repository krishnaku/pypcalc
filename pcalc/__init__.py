# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

"""
#The Presence Calculus Toolkit
© 2025 Krishna Kumar
SPDX-License-Identifier: MIT

The Presence Calculus provides a mathematical formalism for reasoning about
the relationship between *things* and *places* over *time*.

It begins with a [*Presence*](./pcalc/presence.html)—an assertion that a
particular [*Element*](./pcalc/element.html) (thing) was continuously present
within a [*Boundary*](./pcalc/boundary.html) (place) over a continuous interval
of time.

Given a set of presence assertions over a defined domain of elements and
boundaries, the presence calculus constructs rigorous tools for analyzing
element timelines and trajectories, presence-induced boundary topologies, and the
effects of co-presence - simultaneous element presence within and across
boundaries.

Further, by extending the notion of presences to *functions over presences*, we introduce
a powerful mechanism for reasoning about the *effects* of presence—enabling
reasoning about concepts such as the time value and option value of presence.

These techniques apply consistently across a wide range of systems, including
stochastic, non-linear, adaptive, and complex systems.

<div style="text-align: center; margin:2em">
  <img src="./assets/pcalc/presence_calculus.svg" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 1: Key constructs—presences, element paths, presence matrix, and co-presence topology
  </div>
</div>

The presence calculus lies at the intersection of stochastic process dynamics,
queueing theory, topology, and complex systems science—yet remains
philosophically distinct from each of them. It allows to connect these fields while
re-framing their perspectives through the common epistemic lens of presence.

The foundational concepts of the presence calculus allow us to precisely *define*  derived
concepts like flow, stability, equilibrium, and coherence in these domains—and
relate them to practically useful measures such as delay, cost, revenue, and
user experience when mapped back into the semantics of the underlying domain being modeled.

Our main goal in developing the presence calculus is to provide better tools
for rigorous modeling and principled decision-making using messy, real-world data.

We are less concerned with what decisions to make or prescribing *how* to make decisions.
Rather, our focus is on ensuring that the way data is used in those decisions rests on a
linguistically precise, logically sound and mathematically defensible foundation.



## The Toolkit

The Presence Calculus Toolkit is a
minimal, computationally efficient implementation of the core concepts and
calculations in Presence Calculus.

This `pcalc` module in particular, is an elementary and accessible entry point to some of the more abstract
concepts in the presence calculus. It is a precise, computational formulation of the calculus
capable of powering real-time analysis and simulation of complex systems. If you are more comfortable
reading code rather than mathematical notation, this is a better entry point for you.

The module is designed as a lightweight, easy-to-integrate analytical
middleware library that connects real-time event streams, simulation models,
and static datasets (from which presence assertions can be inferred) to rich
visualization and analysis tools.

While we provide several examples of end-to-end integrations, the library is
open source under the MIT license, and you are encouraged to create models and
applications—both commercial and non-commercial—that apply the concepts of
the presence calculus.

The presence calculus builds on an intuitive and elementary foundation, even as
it remains mathematically rigorous. I believe the space of potential
applications is vast, and I invite you to explore it—and to reach out if you
have questions or would like to collaborate.

[Dr. Krishna Kumar](https://www.linkedin.com/in/krishnaku1/),
<br> [The Polaris Advisor Program](https://github.com/polarisadvisor)


"""

from .element import Element
from .boundary import Boundary
from .presence import Presence
from .presence_matrix import PresenceMatrix
from .time_scale import Timescale
from .presence_map import PresenceMap
from .presence_invariant import PresenceInvariant
