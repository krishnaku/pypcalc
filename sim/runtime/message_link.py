# -*- coding: utf-8 -*-
from __future__ import annotations

import random

import simpy

from sim.examples.message_link_sim import Simulation


# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
class MessageLink:
    def __init__(self, env, name, signal_log, processing_time=0.0, capacity=None, sim_context: Simulation=None):
        self.env = env
        self.name = name
        self.signal_log = signal_log
        self.processing_time = processing_time
        self.capacity = capacity
        self.inbox = simpy.Store(env)
        self.peer = None
        self.sim_context = sim_context

        self.resource = simpy.Resource(env, capacity) if capacity else None
        self.entities_in_process: int = 0

    def set_peer(self, peer):
        self.peer = peer

    @property
    def entity_count(self):
        return self.entities_in_process + len(self.inbox.items)

    def send(self, entity):
        print(f"[{self.name} @ t={self.env.now}] send → {self.peer.name}: {entity.id}")
        self.signal_log.record(self.name, self.peer.name, entity.id, self.env.now)
        self.peer.inbox.put(entity)

    def receive(self):
        while True:
            entity = yield self.inbox.get()  # wait for 1 message
            self.inbox.items.insert(0, entity)  # put it back to drain queue
            print(f"[{self.name} @ t={self.env.now}] entity count: {self.entity_count}")
            while self.inbox.items:
                    print(f"[{self.name} @ t={self.env.now}] draining inbox (size={len(self.inbox.items)})")
                    entity = self.inbox.items.pop(0)

                    if entity.payload['created_by'] != self.name:
                        self.entities_in_process += 1
                        print(f"[{self.name} @ t={self.env.now}] scheduling process for {entity.id}")
                        self.env.process(self.on_receive(entity))
                        yield self.env.timeout(0)
                    else:
                        print(f"[{self.name} @ t={self.env.now}] received response for {entity.id}")

    def on_receive(self, entity):
        try:
            if self.resource:
                print(f"[{self.name} @ t={self.env.now}] acquiring resource for {entity.id}")
                with self.resource.request() as req:
                    yield req
                    yield from self.delay(entity)
                    print(f"[{self.name} @ t={self.env.now}] finished processing {entity.id}")
                    yield from self.respond(entity)
            else:
                yield from self.delay(entity)
                print(f"[{self.name} @ t={self.env.now}] finished processing {entity.id}")
                yield from self.respond(entity)
        finally:
            self.entities_in_process -= 1
            print(f"[{self.name} @ t={self.env.now}] entity count: {self.entity_count}")

    def respond(self, entity):
        yield self.env.timeout(0)
        self.send(entity)

    def delay(self, entity):
        mean_delay = self.processing_time or 1
        delay = random.expovariate(1 / mean_delay)
        print(f"[{self.name} @ t={self.env.now}] processing {entity.id} with processing time {delay}")
        yield self.env.timeout(delay)
