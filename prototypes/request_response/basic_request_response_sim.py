# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

from __future__ import annotations

import simpy
import random
from dataclasses import dataclass

# ---------- Entity and Signal Log ----------

@dataclass
class Entity:
    id: str
    payload: dict = None
    sent: float = None
    received: float = None
    created_by: str = None

    def cycle_time(self):
        return self.received - self.sent

class SignalLog:
    def __init__(self):
        self.records = []

    def record(self, from_system, to_system, signal_id, timestamp):
        self.records.append({
            'from': from_system,
            'to': to_system,
            'signal_id': signal_id,
            'timestamp': timestamp
        })

    def dump(self):
        print("\n--- Signal Log ---")
        for r in self.records:
            print(f"[t={r['timestamp']:>2}] {r['from']} → {r['to']}: {r['signal_id']}")


# ---------- Base Class for A and B ----------

class SystemProcess:
    def __init__(self, env, name, sim: Simulation):
        self.env = env
        self.name = name
        self.sim = sim
        self.signal_log = sim.signal_log
        self.entities = sim.entities
        self.inbox = simpy.Store(env)
        self.peer = None

    def set_peer(self, peer):
        self.peer = peer

    def send(self, signal):
        self.signal_log.record(self.name, self.peer.name, signal.id, self.env.now)
        self.peer.inbox.put(signal)

    def receive_loop(self):
        while True:
            signal = yield self.inbox.get()
            self.env.process(self.on_receive(signal))

    def on_receive(self, signal):
        # Override in subclass
        pass

    def run(self):
        # Override in subclass
        pass


# ---------- System A: Generates and Responds ----------

class SystemA(SystemProcess):
    def __init__(self, env, name, sim: Simulation):
        super().__init__(env, name, sim)
        self.counter = 0

    def run(self):
        mean_delay = 2
        while True:
            signal = Entity(f"A-{self.counter}", created_by=self.name, payload=dict())
            self.entities.append(signal)
            self.counter += 1
            signal.sent = self.env.now
            self.send(signal)

            delay = random.expovariate(1 / mean_delay)
            yield self.env.timeout(delay)

    def on_receive(self, signal):
        signal.payload['responded_to_by_A'] = self.name
        signal.received = self.env.now
        print(f"[A @ t={self.env.now}] handled response: {signal.id}: cycle time: {signal.received - signal.sent}")
        yield self.env.timeout(0)

# ---------- System B: Reacts and Responds ----------

class SystemB(SystemProcess):
    def on_receive(self, signal):
        signal.payload['processed_by'] = self.name
        print(f"[B @ t={self.env.now}] processing: {signal.id}")
        mean_delay = 1.5
        delay = random.expovariate(1 / mean_delay)
        yield self.env.timeout(delay)

        self.send(signal)


# ---------- Simulation Orchestrator ----------

class Simulation:
    def __init__(self, until=20):
        self.env = simpy.Environment()
        self.signal_log = SignalLog()
        self.entities = []

        self.A = SystemA(self.env, "A", self)
        self.B = SystemB(self.env, "B", self)

        self.A.set_peer(self.B)
        self.B.set_peer(self.A)

        self.env.process(self.A.run())            # A generates entities
        self.env.process(self.A.receive_loop())   # A listens for responses
        self.env.process(self.B.receive_loop())   # B reacts to A

        self.until = until

    def run(self):
        self.env.run(until=self.until)
        self.signal_log.dump()
        if len(self.entities) > 0:
            print(f"Average cycle time: {sum(obj.cycle_time() for obj in self.entities) / len(self.entities)}")

# ---------- Run Simulation ----------

if __name__ == "__main__":
    sim = Simulation(until=20)
    sim.run()

