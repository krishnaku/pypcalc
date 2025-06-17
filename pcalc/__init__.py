# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

"""
#The Presence Calculus Toolkit
© 2025 Dr. Krishna Kumar
SPDX-License-Identifier: MIT

## Introduction

The Presence Calculus provides a mathematical formalism for reasoning about
the relationship between measures on *elements* and *boundaries* in a domain over *time*.

It begins with the concept of a Presence—a measure over the real numbers, associated with
a particular *Element* (thing) in a domain, observed within a *Boundary* (place),
over a continuous interval of time.

Both Elements and Boundaries belong
to an underlying domain $D$ under analysis.

Measure theory offers a general mechanism for representing
both presence and its effects. This lets us model concepts such as value,
impact, delay, cost, revenue, and user experience as forms of presence.
It also enables rigorous reasoning about temporal constructs like time value,
delayed value, and the option value of presence.

The Presence Calculus is built on rigorous mathematical foundations—
measure theory and topology—anchored by presence as an epistemic primitive.

This frames each presence as an observation made by a specific observer
at a specific time, within an open-world setting across an infinite timeline.
It enables meaningful reasoning about complex systems where
noise, delay, ambiguity, and the provenance of observations play a critical role.

Given a set of presence assertions over a domain $D$, the calculus provides
rigorously defined primitives and constructs for analyzing element timelines
and trajectories, presence-induced topologies on $D$, and the effects of
co-presence—simultaneous element presence—within and across boundaries.#233


These techniques apply consistently across a wide range of domains, including
stochastic, non-linear, adaptive, and complex systems.

<div style="text-align: center; margin:2em">
  <img src="../assets/pcalc/presence_calculus.svg" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 1: Key constructs—presences, element paths, presence matrix, and co-presence topology
  </div>
</div>

## Motivation
Our primary goal in developing the Presence Calculus is to support rigorous
modeling and principled decision-making in complex, real-world domains. We aim
to ensure that the use of data in such decisions rests on a foundation that is
mathematically precise, logically coherent, and epistemically grounded.

The current state of measurement—particularly in messy, complex domains—is often
deficient in all three of these areas. The Presence Calculus emerged from a
search for better structural tools in contexts where traditional statistical or
causal methods fall short.

Presence Calculus builds on ideas from measure theory and topology, and
connects it stochastic process dynamics, queueing
theory, and complex systems science—yet remains philosophically
distinct from each of them in its focus. This allows it to connect disparate fields while
re-framing their perspectives through the common epistemic lens of presence.

The foundational constructs of Presence Calculus allow us to define derived
notions such as flow, stability, equilibrium, and coherence precisely, and to
relate them to practically useful measures like delay, cost, revenue, and user
experience—once interpreted within the semantics of the domain being modeled.

In messy, real-world domains, relationships between elements, boundaries, flows,
and effects often emerge from complex, higher-dimensional interactions among
many parameters. These patterns are often more amenable to machine analysis in
high-dimensional representations than through the simplified, low-dimensional
models we typically use to make decisions. The Presence Calculus lets us
build such representations, starting from simple, declarative models of presence.

While we illustrate our ideas using real-world decision problems, our focus is
not on prescribing what decisions to make or how to make them. That belongs to
the application domain of Presence Calculus—a domain we believe is vast.

Our goal is to make this framework accessible enough for others to build powerful
applications on top of it, without requiring a deep background in the
underlying mathematics (though it will help in following some of the more technical
arguments)

## The Toolkit

The Presence Calculus Toolkit is a computationally efficient implementation of the core concepts and
calculations in presence calculus.

This `pcalc` module in particular, is an elementary and accessible entry point to some of the more abstract
concepts in the presence calculus. It is a computational model for the calculus
capable of powering real-time analysis and simulation of complex systems. The module is designed as a lightweight,
easy-to-integrate analytical middleware library that connects real-time event streams, simulation models,
and static datasets from a domain to rich visualization and analysis tools.

While we'll provide several examples of end-to-end integrations, the library is
open source under the MIT license, and you are encouraged to create models and
applications—both commercial and non-commercial—that build on the concepts.

If you are comfortable learning by
reading code and implementing models and don't mind just a tiny bit of
formal mathematical notation, this is a better entry point to the presence calculus for you.

More background and general, informal discussion around these topics
can be found on [The Polaris Flow Dispatch.](https://wwww.polaris-flow-dispatch.com)

## Reading these docs

The documentation is organized so that you can get a very good idea of the
scope of the presence calculus and it's implementation by reading the
topics listed on the "submodules" left hand menu, in order.

Each module
links to detailed API documentation that is also directly accessible from this page.
The index is also searchable once you get familiar with the concepts.

We believe the space of potential
applications is vast, and invite you to explore it—and to reach out if you
have questions or would like to collaborate with me on helping develop it further.


[Dr. Krishna Kumar](https://www.linkedin.com/in/krishnaku1/),
<br> [The Polaris Advisor Program](https://github.com/polarisadvisor)


"""

from .entity import Entity, EntityProtocol
from .presence import PresenceAssertion
from .time_model import TimeModel
from .basis_topology import BasisTopology
from .presence_invariant import PresenceInvariant
from .presence_matrix import PresenceMatrix
from .time_scale import Timescale
from .presence_map import PresenceMap
from .presence_invariant_discrete import PresenceInvariantDiscrete

__all__ = [
    # Domain API
    "entity",
    Entity, EntityProtocol,

    "presence",
    PresenceAssertion,

    # Continuous Time Models
    "time_model",
    TimeModel,
    "basis_topology",
    BasisTopology,
    "presence_invariant",
    PresenceInvariant,

    # Discrete Time Models
    "time_scale",
    Timescale,
    "presence_map",
    PresenceMap,
    "presence_matrix",
    PresenceMatrix,
    "presence_invariant_discrete",
    PresenceInvariantDiscrete,
]
