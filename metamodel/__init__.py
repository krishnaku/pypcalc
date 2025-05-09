# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

"""
##A domain metamodel for The Presence Calculus

This package defines a metamodel for modeling a domain for the purposes of analyzing flow using The Presence Calculus.

It provides the minimal abstract ontology: Entities, Signals, Transactions, Timelines, DomainEvents, Boundaries,
and Presence that are required  for analyzing flow in any domain.

It is inspired by and compatible with John Hollands Signal/Boundary framework for modeling complex adaptive systems,
but is primarily focused on modeling the physics of flow in such systems: how signals propagate across boundaries,
how presence emerges, and how flow behaviors can be modeled, measured, bounded, and analyzed. For a more detailed
comparison please see [Holland's Signal/Boundary framework](https://github.com/krishnaku/p-calculus-tools/blob/main/docs/holland.md).

Modules in this package enable:

- Construction and identification of domain elements that can flow (entities, signals, transactions)
- Event-driven modeling of signal activity via domain events and timelines
- Defining domain topology using boundaries for determining presence of flow elements in boundaries over time and
thus enabling flow analysis using The Presence Calculus (see package `pcalc`),

This metamodel is intentionally decoupled from any specific domain model. Given any conforming model, it serves as the
bridge for reasoning about flow dynamics using The Presence Calculus (see package `pcalc`),

The first concrete implementation is a simulation framework which can be found in the `sim` package. This allows us to
model and simulate a wide variety of complex adaptive systems: value networks, agent network, queueing systems, value streams etc.
and analyze flow in these systems uniformly via The Presence Calculus.
"""
from .element import Element
from .domain import DomainContext
from .entity import Entity
from .signal import Signal
from .transaction import Transaction
from .timeline import DomainEvent, Timeline
from .boundary import Boundary
from .presence import Presence
