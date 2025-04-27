# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar


from __future__ import annotations
import logging
from abc import ABC
from typing import Any, Dict, Optional, Set
import simpy
from core import Entity, Transaction
from core.node import NodeImpl
from sim.runtime.simulation import Simulation

log = logging.getLogger(__name__)

class Request(Entity):
    def __init__(self, name:str, metadata: Dict[str, Any]=None, transaction: Optional[Transaction]=None) -> None:
        super().__init__(
            name, 
            entity_type="request", 
            metadata=metadata,
            transaction=transaction or Transaction()
        )

class Response(Entity):
    def __init__(self, entity):
        super().__init__(
            entity.name, 
            entity_type="response", 
            metadata=entity.metadata,
            transaction=entity.transaction
        )
        
class Collaborator(NodeImpl, ABC):
    def __init__(self, name, sim_context: Simulation, processing_time=0.0, capacity=None):
        super().__init__(name)
        self.processing_time = processing_time
        self.capacity = capacity

        self.sim_context = sim_context
        self._env = self.sim_context.env
        self.signal_log = self.sim_context.signal_log

        self.inbox = simpy.Store(self._env)
        self.resource = simpy.Resource(self._env, capacity) if capacity else None
        self.entities_in_process: int = 0
        self.transactions_in_process: Set = set()

        self.peer = None

    @property
    def env(self):
        return self._env

    def set_peer(self, peer: Collaborator):
        self.peer = peer
        peer.peer = self

    @property
    def entity_count(self):
        return self.entities_in_process + len(self.inbox.items)

    def send(self, entity: Request|Response):
        log.debug(f"[{self.name} @ t={self.env.now}] send → {self.peer.name}: {entity.name}")
        self.signal_log.record(
            signal_type="request",
            source=self,
            target=self.peer,
            entity=entity,
            timestamp=self.env.now,
            transaction=entity.transaction
        )
        self.peer.inbox.put(entity)

    def receive(self):
        while True:
            entity: Request|Response = yield self.inbox.get()  # wait for 1 message
            self.inbox.items.insert(0, entity)  # put it back to drain queue
            log.debug(f"[{self.name} @ t={self.env.now}] entity count: {self.entity_count}")
            while self.inbox.items:
                log.debug(f"[{self.name} @ t={self.env.now}] draining inbox (size={len(self.inbox.items)})")
                entity = self.inbox.items.pop(0)

                if entity.entity_type == "request":
                    self.entities_in_process += 1
                    log.debug(f"[{self.name} @ t={self.env.now}] scheduling process for {entity.name}")
                    self.env.process(self.dispatch(entity))
                    yield self.env.timeout(0)
                else:
                    log.debug(f"[{self.name} @ t={self.env.now}] received response for {entity.name}")
                    yield from self.on_receive_response(entity)

    def dispatch(self, entity):
        try:
            if self.resource:
                log.debug(f"[{self.name} @ t={self.env.now}] acquiring resource for {entity.name}")
                with self.resource.request() as req:
                    yield req
                    yield from self.respond(entity)
            else:
                yield from self.respond(entity)
        finally:
            self.entities_in_process -= 1
            log.debug(f"[{self.name} @ t={self.env.now}] entity count: {self.entity_count}")

    def respond(self, entity: Request):
        yield from self.on_receive_request(entity)
        log.debug(f"[{self.name} @ t={self.env.now}] finished processing {entity.name}")
        yield from self.send_response(entity)

    def send_response(self, entity):
        yield self.env.timeout(0)
        response = Response(entity)
        self.signal_log.record(
            signal_type="response",
            source=self,
            target=self.peer,
            entity=response,
            timestamp=self.env.now
        )
        self.peer.inbox.put(response)

    def on_receive_request(self, request: Request):
        yield self.env.timeout(0)

    def on_receive_response(self, response: Response):
        yield self.env.timeout(0)