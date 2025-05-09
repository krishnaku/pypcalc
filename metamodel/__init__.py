# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

"""
This package defines a metamodel for modeling flow in a domain.

It provides the core constructs—Entities, Signals, Transactions, Timelines, DomainEvents, Boundaries,
Presences, and PresenceMatrices—that together form a causal-temporal metamodel for analyzing flow dynamics.

The metamodel provides a minimal abstract ontology required to measure and model flow in both simple and complex domains.
It is loosely inspired by John Hollands Signal/Boundary framework for modeling complex adaptive systems,
but is primarily focused on modeling the physics of flow in such systems: how information propagates,
how presence emerges, and how flow behaviors can be modeled, measured, bounded, and analyzed.

Modules in this package enable:

- Construction and identification of flow elements (entities, signals, transactions)
- Event-driven modeling of signal activity via domain events and timelines
- Boundary-based partitioning of domains for presence tracking and flow analysis

The metamodel provides a minimal abstraction of an underlying domain that allows us to model and measure flow using
the tools of The Presence Calculus (see package `pcalc`). The underlying domain may be implemented by a
simulation model (see package `sim`) or be sourced from real-time data from other sources.

This metamodel is intentionally decoupled from any specific domain model and serves as the analytic
backbone for reasoning about flow dynamics using The Presence Calculus, over any conforming model.
"""
from .element import Element
from .domain import DomainContext
from .entity import Entity
from .signal import Signal
from .transaction import Transaction
from .timeline import DomainEvent, Timeline
from .boundary import Boundary
from .presence import Presence
