# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

from __future__ import annotations

from typing import List, Dict, Optional, Protocol, Any


from .signal import Signal
from .transaction import Transaction
from .boundary import Boundary
from .timeline import DomainEvent, Timeline, SignalEventListener
from .entity import Entity

class DomainModel(Protocol):
    """
    Abstract interface for domain model.

    A `SimulationContext` provides all entities in the system with access to simulation-wide state including other
    entities, signals, transactions, and boundaries. It also exposes methods for recording signal events and
    subscribing to changes in the system's execution history. All entities in the simulation use the global signal logs
    in the SimulationContext to record :class: `SignalEvents`.

    Other classes such as boundaries also maintain signal logs, but they are expected to register for SignalEvents with
    the global signal log.

    Concrete simulation classes are expected to implement this interface to support analysis,
    monitoring, and coordination across subsystems. See :class:`sim.runtime.Simulation` for a concrete
    implementation.

    ### Example

    ```python
    class MySim(SimulationContext):
        def entities(self, name: str) -> List[Entity]:
            return self.entity_registry.get(name, [])

        def record_signal(self, source, timestamp, signal_type, signal, transaction=None, target=None, tags=None):
            return self.timeline.record(source, timestamp, signal_type, signal, transaction, target, tags)

        @property
        def all_logs(self) -> List[SignalLog]:
            return [self.timeline]
    ```
    """



    # -------- Accessors -------------------------

    def entities(self, name: str) -> List[Entity]:
        """Return a list of `Entity` objects with the given name (or matching key)."""
        ...

    def signals(self, name: str) -> List[Signal]:
        """Return a list of `Signal` instances with the given name (or type label)."""
        ...

    def transactions(self, name: str) -> List[Transaction]:
        """Return a list of `Transaction` objects with the given ID or tag."""
        ...

    def boundaries(self, name: str) -> List[Boundary]:
        """Return a list of `Boundary` instances matching the provided name or identifier."""
        ...

    # -------- Signal Interface ------------------

    def record_signal(
        self,
        source: Entity,
        timestamp: float,
        signal_type: str,
        signal: Signal,
        transaction: Optional[Transaction] = None,
        target: Optional[Entity] = None,
        tags: Optional[Dict[str, Any]] = None
    ) -> DomainEvent:
        """
        Record a signal event in the simulation.

        Args:
            source: The entity emitting or processing the signal.
            timestamp: The time at which the event occurred.
            signal_type: The type of event (e.g., 'send', 'receive').
            signal: The signal being recorded.
            transaction: Optional transaction context.
            target: Optional receiving entity.
            tags: Optional metadata tags.

        Returns:
            The created `SignalEvent` instance.
        """
        ...

    def register_listener(self, listener: SignalEventListener) -> None:
        """
        Register a listener that will be notified when a new signal event is recorded.

        Args:
            listener: An object implementing the `SignalEventListener` protocol.
        """
        ...

    @property
    def all_logs(self) -> List[Timeline]:
        """
        Access the complete set of `SignalLog` instances tracked by the simulation.

        This includes logs from all boundaries or subsystems that emit signals.
        """
        ...
