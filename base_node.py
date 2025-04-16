# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Dict, Any, Generator, TypeVar, Callable, Generic, Set

from signal import Signal
from signal_history import SignalLog
from simulation import Simulation
from registry import Registry

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
class Node(ABC):
    def __init__(self, name: str, config: Dict[str, Any], sim_context: Simulation) -> None:
        self._name: str = name
        self._config: Dict[str, Any] = config
        self._sim_context = sim_context
        self.env = sim_context.env


    @property
    def name(self) -> str:
        return self._name

    @property
    def config(self) -> Dict[str, Any]:
        return self._config

    @property
    def sim_context(self) -> Simulation:
        return self._sim_context


class Boundary(Node):

    def __init__(self, name: str, config: Dict[str, Any], sim_context: Simulation) -> None:
        super().__init__(name, config, sim_context)
        self._signal_history: SignalLog = SignalLog()
        self._tenants: Set[str] = set()

    @property
    def signal_history(self) -> SignalLog:
        return self._signal_history

    @property
    def population(self) -> int:
        return len(self._tenants)

    @property
    def tenants(self) -> Set[str]:
        return self._tenants

    def enter(self, entity_id: str, **kwargs) -> Generator:
        self._tenants.add(entity_id)
        self.signal_enter(entity_id, **kwargs)
        yield from self.on_enter(entity_id, **kwargs)

    def signal_enter(self, entity_id: str, **kwargs) -> Signal:
        timestamp = self.env.now
        return self.signal_history.signal(
            Signal(
                signal="enter",
                source=self.name,
                timestamp=timestamp,
                entity_id=entity_id,
                tags=kwargs
            )
        )



    def exit(self,entity_id: str, **kwargs) -> Generator:
        self._tenants.remove(entity_id)
        self.signal_exit(entity_id, **kwargs)
        yield from self.on_exit(entity_id, **kwargs)

    def signal_exit(self, entity_id:str, **kwargs) -> Signal:

        timestamp = self.env.now
        return self.signal_history.signal(
            Signal(
                signal="exit",
                source=self.name,
                timestamp=timestamp,
                entity_id=entity_id,
                tags=kwargs
            )
        )

    @abstractmethod
    def on_enter(self, entity_id: str, **kwargs) -> Generator:
        pass

    @abstractmethod
    def on_exit(self, entity_id: str, **kwargs) -> None:
        pass


class Service(Boundary):
    def on_enter(self, entity_id: str, **kwargs) -> Generator:
        yield from self.perform_service(entity_id, **kwargs)
        yield from self.exit(entity_id, **kwargs)

    def on_exit(self, entity_id: str, **kwargs) -> Generator:
        yield from ()

    def signal_start_service(self, entity_id:str, **kwargs) -> Signal:
        timestamp = self.env.now
        return self.signal_history.signal(
            Signal(
                signal="start_service",
                source=self.name,
                timestamp=timestamp,
                entity_id=entity_id,
                **kwargs
            )
        )

    def signal_end_service(self, entity_id:str, **kwargs) -> Signal:
        timestamp = self.env.now
        return self.signal_history.signal(
            Signal(
                signal="end_service",
                source=self.name,
                timestamp=timestamp,
                entity_id=entity_id,
                **kwargs
            )
        )



    @abstractmethod
    def perform_service(self, entity_id: str, **kwargs) -> Generator:
       pass


class BlockingService(Service, ABC):
    pass


class NonBlockingService(Service, ABC):
    pass




