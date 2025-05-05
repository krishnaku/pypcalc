# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from __future__ import annotations
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Set, Generator
import simpy
from core import Signal, Transaction, Registry
from sim.model.entity.base import EntityBase
from sim.runtime.simulation import Simulation

log = logging.getLogger(__name__)

class Request(Signal):
    def __init__(self, name:str, metadata: Dict[str, Any]=None, transaction: Optional[Transaction]=None) -> None:
        super().__init__(
            name, 
            signal_type="request",
            metadata=metadata,
            transaction=transaction or Transaction()
        )

class Response(Signal):
    def __init__(self, signal):
        super().__init__(
            signal.name,
            signal_type="response",
            metadata=signal.payload,
            transaction=signal.transaction
        )
        
class Collaborator(EntityBase, ABC):
    def __init__(self, kind:str, name:str, sim_context: Simulation, concurrency=None):
        super().__init__(kind, name, sim_context)
        self.inbox = sim_context.get_store()
        self.resource = sim_context.get_resource(capacity=concurrency) if concurrency else None
        self.entities_in_process: int = 0
        self.transactions_in_process: Set = set()
        self.concurrency = concurrency
        self.peer = None


    def set_peer(self, peer: Collaborator):
        self.peer = peer
        peer.peer = self

    @property
    def signal_count(self):
        return self.entities_in_process + len(self.inbox.items)

    def send(self, signal: Request|Response) -> None:
        log.debug(f"[{self.name} @ t={self.sim_context.now}] send → {self.peer.name}: {signal.name}")
        self.sim_context.record_signal(
            signal_type="request",
            source=self,
            target=self.peer,
            signal=signal,
            timestamp=self.sim_context.now,
            transaction=signal.transaction
        )
        self.peer.inbox.put(signal)

    def receive(self) -> Generator[simpy.events.Event, None, None]:
        while True:
            signal: Request|Response = yield self.inbox.get()  # type: ignore
            self.inbox.items.insert(0, signal)  # put it back to drain queue
            log.debug(f"[{self.name} @ t={self.sim_context.now}] signal count: {self.signal_count}")
            while self.inbox.items:
                log.debug(f"[{self.name} @ t={self.sim_context.now}] draining inbox (size={len(self.inbox.items)})")
                signal = self.inbox.items.pop(0)

                if signal.signal_type == "request":
                    self.entities_in_process += 1
                    log.debug(f"[{self.name} @ t={self.sim_context.now}] scheduling process for {signal.name}")
                    self.sim_context.process(self.dispatch(signal))
                    yield self.sim_context.timeout(0)
                else:
                    log.debug(f"[{self.name} @ t={self.sim_context.now}] received response for {signal.name}")
                    yield from self.on_receive_response(signal)

    def dispatch(self, signal) -> Generator[simpy.events.Event, None, None]:
        try:
            if self.resource:
                log.debug(f"[{self.name} @ t={self.sim_context.now}] acquiring resource for {signal.name}")
                with self.resource.request() as req:
                    yield req
                    yield from self.respond(signal)
            else:
                yield from self.respond(signal)
        finally:
            self.entities_in_process -= 1
            log.debug(f"[{self.name} @ t={self.sim_context.now}] signal count: {self.signal_count}")

    def respond(self, signal: Request) -> Generator[simpy.events.Event, None, None]:
        yield from self.on_receive_request(signal)
        log.debug(f"[{self.name} @ t={self.sim_context.now}] finished processing {signal.name}")
        yield from self.send_response(signal)

    def send_response(self, signal) -> Generator[simpy.events.Event, None, None]:
        yield self.sim_context.timeout(0)
        response = Response(signal)
        self.sim_context.record_signal(
            signal_type="response",
            source=self,
            target=self.peer,
            signal=response,
            timestamp=self.sim_context.now
        )
        self.peer.inbox.put(response)

    @abstractmethod
    def start_processes(self):...

    def on_receive_request(self, request: Request) -> Generator[simpy.events.Event, None, None]:
        yield self.sim_context.timeout(0)

    def on_receive_response(self, response: Response) -> Generator[simpy.events.Event, None, None]:
        yield self.sim_context.timeout(0)

