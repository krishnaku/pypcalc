# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT



from abc import ABC, abstractmethod
import simpy
import logging
import time
from typing import List, Generator, Optional, Any, Protocol, Dict
from simpy.events import Timeout

from sim.metamodel import Entity, Signal
from sim.metamodel import DomainEvent, Timeline, DomainEventListener
from sim.metamodel import DomainContext

from sim.model.timeline import DefaultTimeline

log = logging.getLogger(__name__)

class SimpyProxy(Protocol):
    @property
    def now(self) -> float:...
    """Get the current simulation time."""

    def timeout(self, delay: float, value: Optional[Any] = None) -> Timeout:...
    """Yield a timeout event after a delay."""

    def process(self, generator: Generator) -> simpy.events.Process:...
    """Start a new process from a generator."""


    def event(self) -> DomainEvent:...
    """Create a new, untriggered event."""


    def schedule(self, event: DomainEvent, delay: float = 0) -> None:...
    """Manually schedule an event after a delay."""

    def get_store(self) -> simpy.Store:...
    """An inbox for messages etc"""

    def get_resource(self, capacity=None) -> simpy.Resource :...
    """Concurrency constrained resources etc"""

# Simulation class is the proxy for the simpy environment.
# We create fresh simpy environments between runs, so it is unsafe to hand out explicit references to anything
# in the simpy environment outside this class
# Route all calls to simpy.env through the simulation class and hand only this context
# to all other parts of the code.
class Simulation(SimpyProxy, DomainContext, ABC):
    def __init__(self, until=30, runs=1, realtime_factor: float = None):

        # Signal management parameters
        self._timeline = None
        # preserve separate signal logs per simulation run
        self._all_logs: List[Timeline] = []
        self._signal_listeners: List[DomainEventListener] = []

        # simpy proxy parameters
        # NOTE: _env is intentionally private — do NOT expose or pass it around.
        # All access to the environment must go through this context.
        self._env = None
        self.realtime_factor = realtime_factor
        self.until = until
        self.runs = runs
        self.current_run = 0
        self.simulation_start = None

        # initialize an environment and signal logs
        self.init_sim()


    # Simulation Lifecycle
    def init_sim(self):
        if self.realtime_factor is not None:
            self._env = simpy.rt.RealtimeEnvironment(factor=self.realtime_factor)
        else:
            self._env = simpy.Environment()

        self.reset_timeline()

    def reset_timeline(self):
        if self._timeline is not None:
            self._all_logs.append(self._timeline)

        self._timeline = DefaultTimeline()

    @abstractmethod
    def bind_environment(self):
        ...

    """Subclasses initialize all the simulation objects that require access to the simulation environment"""

    @abstractmethod
    def start_processes(self) -> List[simpy.events.Process]:
        ...

    """Nodes call self.process to create all the running processes in the simulation"""

    def post_run(self):
        log.info(f"Simulation run: {self.current_run} completed @ {time.time() - self.simulation_start}")

    def run_simulation(self, until=None):
        """Single run of the simulation """
        self.until = until
        self.bind_environment()
        self.start_processes()
        # kick off the simulation
        self._env.run(until=self.until)
        # post hooks for subclasses to cache metrics etc.
        self.post_run()

    def run(self, until, runs=1) -> None:
        """Outer loop - multiple runs"""
        self.current_run = 0
        self._all_logs = []
        self.simulation_start = time.time()
        log.info(f"Simulation started at 0 seconds")
        self.runs = runs
        for self.current_run in range(self.runs):
            self.run_simulation(until=until)
            self.init_sim()

        log.info(f"simulation ended at {(time.time() - self.simulation_start)} seconds")

    # ------------- Signal Management Interface -------------------------------------
    def register_listener(self, listener: DomainEventListener) -> None:
        self._signal_listeners.append(listener)

    def record_signal(self, source: Entity, timestamp: float, event_type: str, signal: Signal, transaction=None,
                      target: Optional[Entity] = None, tags: Optional[Dict[str, Any]] = None) -> DomainEvent:
        """Write access to the global signal log is via this method."""
        signal:DomainEvent =  self._timeline.record(
            source=source,
            timestamp=timestamp,
            event_type=event_type,
            signal=signal,
            transaction=transaction,
            target=target,
            tags=tags
        )
        self.notify_listeners(signal)
        return signal

    def notify_listeners(self, signal: DomainEvent) -> None:
        for listener in self._signal_listeners:
            if signal.source != listener:
                listener.on_domain_event(signal)


    @property
    def all_timelines(self) -> List[Timeline]:
        """Read access to signal logs is via the all_logs property."""
        return self._all_logs + ([self._timeline] if self._timeline and self.current_run < self.runs  else [])

    @property
    def latest_log(self) -> Timeline:
        """Access the latest signal log across runs."""
        return self.all_timelines[-1] if len(self.all_timelines) > 0 else None


    # ----- SimpyProxy implementation - concrete binding to simulation infra.
    @property
    def now(self) -> float:
        """Get the current simulation time."""
        return self._env.now

    def timeout(self, delay: float, value: Optional[Any] = None) -> Timeout:
        """Yield a timeout event after a delay."""
        return self._env.timeout(delay, value=value)

    def process(self, generator: Generator) -> simpy.events.Process:
        """Start a new process from a generator."""
        return self._env.process(generator)

    def event(self) -> DomainEvent:
        """Create a new, un-triggered event."""
        return self._env.event()

    def schedule(self, event: DomainEvent, delay: float = 0) -> None:
        """Manually schedule an event after a delay."""
        self._env.schedule(event, delay=delay)

    # additional Simpy infrastructure exposed via the context
    def get_store(self) -> simpy.Store:
        return simpy.Store(self._env)

    def get_resource(self, capacity=None) -> simpy.Resource:
        return simpy.Resource(self._env, capacity)