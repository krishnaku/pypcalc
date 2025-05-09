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

from metamodel import Transaction
from sim.model.entity.base import EntityBase
from sim.model.signal import SignalBase
from sim.runtime.simulation import Simulation

log = logging.getLogger(__name__)

class Request(SignalBase):
    def __init__(self, name:str, payload: Dict[str, Any]=None, transaction: Optional[Transaction]=None) -> None:
        super().__init__(
            name,
            signal_type="request",
            payload=payload,
            transaction=transaction or Transaction()
        )

class Response(SignalBase):
    def __init__(self, signal):
        super().__init__(
            signal.name,
            signal_type="response",
            payload=signal.payload,
            transaction=signal.transaction
        )
        
class CollaboratorBase(EntityBase, ABC):
    def __init__(self, name:str, domain_context: Simulation, concurrency=None, **kwargs):
        super().__init__(name, domain_context, concurrency=concurrency, **kwargs)
        self.inbox = domain_context.get_store()
        self.resource = domain_context.get_resource(capacity=concurrency) if concurrency else None
        self.signals_in_process: int = 0
        self.transactions_in_process: Set = set()
        self.concurrency = concurrency
        self.peer = None


    def set_peer(self, peer: CollaboratorBase):
        self.peer = peer
        peer.peer = self

    @property
    def signal_count(self):
        return self.signals_in_process + len(self.inbox.items)

    def send(self, signal: Request|Response) -> None:
        log.debug(f"[{self.name} @ t={self.domain_context.now}] send → {self.peer.name}: {signal.name}")
        self.domain_context.record_signal(
            event_type="send",
            source=self,
            target=self.peer,
            signal=signal,
            timestamp=self.domain_context.now,
            transaction=signal.transaction
        )
        self.peer.inbox.put(signal)

    def receive(self) -> Generator[simpy.events.Event, None, None]:
        while True:
            signal: Request|Response = yield self.inbox.get()  # type: ignore
            self.inbox.items.insert(0, signal)  # put it back to drain queue
            log.debug(f"[{self.name} @ t={self.domain_context.now}] signal count: {self.signal_count}")
            while self.inbox.items:
                log.debug(f"[{self.name} @ t={self.domain_context.now}] draining inbox (size={len(self.inbox.items)})")
                signal = self.inbox.items.pop(0)

                self.domain_context.record_signal(
                    event_type="receive",
                    source=self,
                    target=self.peer,
                    signal=signal,
                    timestamp=self.domain_context.now
                )

                if signal.signal_type == "request":
                    self.signals_in_process += 1
                    log.debug(f"[{self.name} @ t={self.domain_context.now}] scheduling process for {signal.name}")
                    self.domain_context.process(self.dispatch(signal))
                    yield self.domain_context.timeout(0)
                else:
                    log.debug(f"[{self.name} @ t={self.domain_context.now}] received response for {signal.name}")
                    yield from self.on_receive_response(signal)

    def dispatch(self, signal) -> Generator[simpy.events.Event, None, None]:
        try:
            if self.resource:
                log.debug(f"[{self.name} @ t={self.domain_context.now}] acquiring resource for {signal.name}")
                with self.resource.request() as req:
                    yield req
                    yield from self.respond(signal)
            else:
                yield from self.respond(signal)
        finally:
            self.signals_in_process -= 1
            log.debug(f"[{self.name} @ t={self.domain_context.now}] signal count: {self.signal_count}")

    def respond(self, signal: Request) -> Generator[simpy.events.Event, None, None]:
        yield from self.on_receive_request(signal)
        log.debug(f"[{self.name} @ t={self.domain_context.now}] finished processing {signal.name}")
        yield from self.send_response(signal)

    def send_response(self, signal) -> Generator[simpy.events.Event, None, None]:
        yield self.domain_context.timeout(0)
        response = Response(signal)
        self.domain_context.record_signal(
            event_type="send",
            source=self,
            target=self.peer,
            signal=response,
            timestamp=self.domain_context.now
        )
        self.peer.inbox.put(response)

    @abstractmethod
    def start_processes(self):...

    def on_receive_request(self, request: Request) -> Generator[simpy.events.Event, None, None]:
        yield self.domain_context.timeout(0)

    def on_receive_response(self, response: Response) -> Generator[simpy.events.Event, None, None]:
        yield self.domain_context.timeout(0)

