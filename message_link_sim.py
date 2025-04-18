# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from __future__ import annotations

import threading
from collections import deque

import simpy
import random
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from matplotlib import pyplot as plt, animation
from IPython.display import display

@dataclass
class Entity:
    id: str
    payload: dict


class SignalLog:
    def __init__(self):
        self.records = []

    def record(self, from_system, to_system, entity_id, timestamp):
        self.records.append({
            'from': from_system,
            'to': to_system,
            'entity_id': entity_id,
            'timestamp': timestamp
        })

    def dump(self):
        print("\n--- Signal Log ---")
        for r in self.records:
            print(f"[t={r['timestamp']:>2}] {r['from']} → {r['to']}: {r['entity_id']}")


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



class SystemA(MessageLink):
    def __init__(self, env, name, signal_log, generation_rate=2):
        super().__init__(env, name, signal_log, processing_time=0, capacity=None)
        self.counter = 0
        self.generation_rate = generation_rate  # mean interarrival time

    def run(self):
        while True:
            entity = Entity(f"A-{self.counter}", {"created_by": self.name})
            self.counter += 1
            self.send(entity)

            mean_delay = 1.5
            delay = random.expovariate(1 / mean_delay)
            yield self.env.timeout(delay)




class Simulation:
    def __init__(self, until=20, metrics_poll_interval=0.2, realtime_factor=1):
        self.env = simpy.rt.RealtimeEnvironment(factor=realtime_factor)
        self.signal_log = SignalLog()
        self.queue_samples = deque(maxlen=2_000)
        self.sample_lock = threading.Lock()
        self.metrics_poll_interval = metrics_poll_interval
        self.until = until

        self.A = SystemA(self.env, "A", self.signal_log, generation_rate=2)
        self.B = MessageLink(self.env, "B", self.signal_log, processing_time=1.5, capacity=1)

        self.A.set_peer(self.B)
        self.B.set_peer(self.A)



    def queue_monitor(self, interval=0.2):
        """Push (sim_time, queue_len) into queue_samples every *interval*."""
        while True:
            with self.sample_lock:
                self.queue_samples.append((self.env.now, self.B.entity_count))
            yield self.env.timeout(interval)

    def plot(self, interval=100):
        fig, ax = plt.subplots(figsize=(8, 4))
        (ax_line,) = ax.plot([], [], lw=2)
        ax.set_xlabel("simulation‑time")
        ax.set_ylabel("queue length")

        def init():
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 5)
            return (ax_line,)

        def update(frame):
            with self.sample_lock:
                if not self.queue_samples:
                    return (ax_line,)
                xs, ys = zip(*self.queue_samples)
            ax_line.set_data(xs, ys)
            ax.set_xlim(max(0, xs[-1] - 10), xs[-1] + 1)  # 10‑time‑unit window
            ax.set_ylim(0, max(5, max(ys) + 1))
            return (ax_line,)

        ani = animation.FuncAnimation(fig, update, init_func=init,
                                      interval=100, blit=True, cache_frame_data=False)
        fig._ani = ani

        # show the live figure right now
        display(fig)
        return None


    def run(self):
        self.env.process(self.A.run())
        self.env.process(self.A.receive())
        self.env.process(self.B.receive())
        self.env.process(self.queue_monitor(self.metrics_poll_interval))
        self.env.run(until=self.until)
        self.signal_log.dump()


if __name__ == "__main__":
    sim = Simulation(until=20)
    sim.run()
