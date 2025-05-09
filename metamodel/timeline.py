# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

"""
This module defines the `Timeline`, a runtime record of lifecycle events of elements in a domain.
The timeline captures event history for a domain including signals, timestamps,
source/target entities, and any associated transaction.

The `DomainModel` is the canonical source of truth for the Timeline of a domain.
However, every `Boundary` in the domain has its own timeline that may observe only a
subset of events that occur in the domain.

Analyzing how events propagate across timelines is a first class analysis concern for us.
"""
from __future__ import annotations
import polars as pl
import uuid

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Literal, Union, Iterable, Protocol



from .entity import Entity
from .signal import Signal
from .transaction import Transaction
from .element import Element

class DomainEvent(Element, Protocol):
    """A timestamped event representing the lifecycle events of a domain element as recorded on a timeline."""

    source_id: str
    """The ID of the entity that emitted or handled the signal."""

    timestamp: float
    """The time at which the event occurred."""

    event_type: str
    """A label describing the type of event (e.g., 'send', 'receive', 'process')."""

    signal_id: str
    """The ID of the signal involved in the event."""

    transaction_id: Optional[str] = None
    """Optional transaction ID if the signal is part of a transaction."""

    target_id: Optional[str] = None
    """The ID of the receiving entity, if any."""

    tags: Optional[Dict[str, Any]] = None
    """Optional dictionary of additional metadata tags."""

    timeline: Timeline = None
    """Back-reference to the timeline where this event was recorded (used for resolving IDs)."""

    @property
    def id(self) -> str:
        """The unique ID of the signal (auto-assigned)."""
        ...

    @property
    def source(self) -> Entity:
        """Returns the `Entity` corresponding to the source ID."""
        ...

    @property
    def target(self) -> Entity:
        """Returns the `Entity` corresponding to the target ID, if present."""
        ...

    @property
    def signal(self) -> Signal:
        """Returns the full `Signal` object referenced by this event."""
        ...

    @property
    def transaction(self) -> Transaction:
        """Returns the `Transaction` this signal is part of, if any."""
        ...

    def as_dict(self) -> dict:
        """Convert the event into a serializable dictionary (excluding timeline)."""
        ...


class DomainEventListener(Protocol):
    """Protocol for subscribers that react to new signal events."""

    def on_domain_event(self, event: DomainEvent) -> None:
        """Called when a new `SignalEvent` is recorded."""
        ...


class Timeline(Element, Protocol):
    """Captures and manages all signal events emitted during simulation or execution."""

    @property
    def domain_events(self) -> List[DomainEvent]:
        """Return the full list of recorded signal events."""
        ...


    def record(self, source: Entity, timestamp: float, event_type: str, signal: Signal, transaction=None,
               target: Optional[Entity] = None, tags: Optional[Dict[str, Any]] = None) -> DomainEvent:
        """
        Add a new domain event to the timeline and return it. This is the canonical factory method for DomainEvents
        """
        ...

    @property
    def transactions(self) -> Iterable[tuple[str, Transaction]]:
        """All known transactions referenced in the timeline."""
        ...

    @property
    def signals(self) -> Iterable[tuple[str, Signal]]:
        """All known signals referenced in the timeline."""
        ...

    @property
    def entities(self) -> Iterable[tuple[str, Entity]]:
        """All known entities that emitted or received signals."""
        ...

    def entity(self, entity_id) -> Entity:
        """Look up an entity  in the timeline by ID."""
        ...

    def signal(self, signal_id) -> Signal:
        """Look up a signal in the timeline by ID."""
        ...

    def transaction(self, transaction_id) -> Transaction:
        """Look up a transaction in the timeline by ID."""
        ...

