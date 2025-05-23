# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

"""
#The Presence Calculus Toolkit
© 2025 Dr. Krishna Kumar
SPDX-License-Identifier: MIT

## Introduction

The Presence Calculus provides a mathematical formalism for reasoning about
the relationship between *things* and *places* over *time*.

It begins with a [*Presence*](./pcalc/presence.html)—an *assertion* that a
particular *Element* (thing) was *continuously* present
within a *Boundary* (place) over an interval
of *time*. Both Elements and Boundaries come from some underlying domain $D$
that we are studying.

Given a set of presence assertions over a domain $D$, the presence calculus provides
rigorously defined  primitives and constructs for analyzing element timelines and trajectories,
presence-induced topologies on $D$, and the
effects of co-presence - simultaneous element presence - within and across
boundaries.

Further, by extending the notion of presences to *functions over presences*, it gives
a general mechanism for representing the *effects* of presence, This helps
model concepts such value, impact, delays, cost, revenues, user experience etc, as well
as reason rigorously about concepts like time value, delayed value and option value of presence.

These techniques can be applied consistently across a wide range of domains, including
stochastic, non-linear, adaptive, and complex systems.

<div style="text-align: center; margin:2em">
  <img src="./assets/pcalc/presence_calculus.svg" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 1: Key constructs—presences, element paths, presence matrix, and co-presence topology
  </div>
</div>

## Motivation
Our main goal in developing the presence calculus is to provide better tools
for rigorous modeling and principled decision-making in messy, real-world domains.
Our focus is on ensuring that the way data is used in those decisions rests on a
linguistically precise, logically sound and mathematically grounded foundation.

The world of measurement, particularly in messy, complex, real-world domains, is sorely lacking in all these
three areas, and the presence calculus evolved from a search for better solutions here.

The presence calculus builds on ideas from stochastic process dynamics,
queueing theory, topology, and complex systems science—yet remains
philosophically distinct from each of them. It allows us to connect these fields while
re-framing their perspectives through the common epistemic lens of presence.

The foundational concepts of Presence Calculus allow us to *define*
derived notions such as flow, stability, equilibrium, and coherence precisely, and to
relate them to practically useful measures like delay, cost, revenue, and user
experience when interpreted within the semantics of the domain being modeled.

In messy real-world domains, relationships between elements, boundaries, flows, and
effects often emerge from complex, higher-dimensional interactions among
many parameters. These patterns are often more amenable to machine analysis
in high-dimensional representations than through the simplified, low-dimensional
models we typically use to make decisions. The presence calculus provides a precise and structured way to
build such representations starting from simple, declarative models of presence.

Although we will motivate most ideas we introduce with real-world decision
problems, we are less focused on *what* decisions to make or prescribing *how* to make decisions. This is the
 application domain for the presence calculus.

 We believe it is vast and hope to make it accessible for more people to build applications without requiring a deep
understanding of the underlying mathematics.

## The Toolkit

The Presence Calculus Toolkit is a computationally efficient implementation of the core concepts and
calculations in Presence Calculus.

This `pcalc` module in particular, is an elementary and accessible entry point to some of the more abstract
concepts in the presence calculus. It is a computational model for the calculus
capable of powering real-time analysis and simulation of complex systems.

If you are more comfortable learning by
reading code and implementing models rather than reading mathematical notation or prose, this is a better entry point
to the presence calculus for you.

The module is designed as a lightweight, easy-to-integrate analytical
middleware library that connects real-time event streams, simulation models,
and static datasets from a domain to rich
visualization and analysis tools.

While we provide several examples of end-to-end integrations, the library is
open source under the MIT license, and you are encouraged to create models and
applications—both commercial and non-commercial—that build on the concepts.

The presence calculus builds on an intuitive and elementary foundation, even as
it remains mathematically rigorous. We believe the space of potential
applications is vast, and invite you to explore it—and to reach out if you
have questions or would like to collaborate.

[Dr. Krishna Kumar](https://www.linkedin.com/in/krishnaku1/),
<br> [The Polaris Advisor Program](https://github.com/polarisadvisor)


"""

from .entity import Entity
from .presence import Presence
from .presence_matrix import PresenceMatrix
from .time_scale import Timescale
from .presence_map import PresenceMap
from .presence_invariant import PresenceInvariant

__all__ = [
    "entity",
    "presence",
    "time_scale",
    "presence_map",
    "presence_matrix",
    "presence_invariant",
]
