# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

"""
A Meta-Model for Flow Analysis in a domain

This package defines the foundational ontology and semantics for modeling flow in complex domains.
It provides the core constructs—Entities, Signals, Transactions, Timelines, DomainEvents, Boundaries,
Presences, and PresenceMatrices—that together form a causal-temporal metamodel for analyzing system dynamics.

Unlike traditional metamodels that focus solely on structural semantics, this framework encodes a
physics of flow: how information propagates, how presence emerges, and how flow behaviors can be
measured, bounded, and analyzed across temporal and topological boundaries.

Modules in this package enable:

- Construction and identification of flow elements (entities, signals, transactions)
- Event-driven modeling of signal activity via domain events and timelines
- Boundary-based partitioning of domains for presence tracking and flow analysis
- Transformation of event logs into scale-invariant presence matrices
- Support for simulations, empirical trace analysis, and higher-order metrics

This metamodel is intentionally decoupled from any specific execution model and serves as the analytic
backbone for reasoning about convergence, divergence, and causal relationships within signal-boundary domains.
"""

from .entity import Entity
from .signal import Signal
from .transaction import Transaction
from .affordances import Affordance
from .behaviors import Behavior
from .registry import Registry
from .timeline import DomainEvent
from .boundary import Boundary
