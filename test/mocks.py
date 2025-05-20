# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from typing import List, Callable, Optional

import simpy

from sim.metamodel import Timeline, Signal, DomainEvent, Entity
from pcalc import Boundary, Presence
from sim.model.element import ElementBase
from sim.runtime.simulation import Simulation
from sim.model.entity import EntityBase
from sim.model.signal import SignalBase
from sim.model.timeline import DefaultTimeline


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
    List[Presence]:
        return []

    def get_entity_presences(self, start_time: float, end_time: float,
                             match: Optional[Callable[[DomainEvent], bool]] = None) -> List[Presence]:
        return []

    def __init__(self, name=None):
        self._name: str = name



    @property
    def name(self) -> str:
        return self._name


    def __str__(self) -> str:
        return self._name if self._name is not None else 'None'