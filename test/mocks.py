# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from typing import List, Callable, Optional

import simpy

from metamodel import Boundary, Timeline, Presence, Signal, DomainEvent, Entity
from sim.model.element import ElementBase
from sim.runtime.simulation import Simulation
from sim.model.entity import EntityBase
from sim.model.signal import SignalBase
from sim.model.timeline import DefaultTimeline, DefaultEvent


class MockSimulation(Simulation):
    def start_processes(self) -> List[simpy.events.Process]:
        pass

    def bind_environment(self):
        pass



# Default implementations of model base classes.

class TestEntity(EntityBase): ...


class TestSignal(SignalBase): ...


@dataclass
class  MockElement(ElementBase):
    ...


class MockBoundary(Boundary):
    @property
    def timeline(self) -> Timeline:
       return DefaultTimeline()

    def get_signal_presences(self, start_time: float, end_time: float, match: Callable[[DomainEvent], bool] = None) -> \
    List[Presence[Signal]]:
        return []

    def get_entity_presences(self, start_time: float, end_time: float,
                             match: Optional[Callable[[DomainEvent], bool]] = None) -> List[Presence[Entity]]:
        return []

