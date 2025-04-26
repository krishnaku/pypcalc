# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from __future__ import annotations

import logging
import random
import threading
from collections import deque
import time
from typing import Callable

from IPython.core.display_functions import display
from matplotlib import pyplot as plt, animation


from sim.runtime.request_response.collaborator import Collaborator, Request, Response
from sim.runtime.simulation import Simulation

log = logging.getLogger(__name__)

class Requestor(Collaborator):
    def __init__(self, name:str, sim_context: Simulation,  mean_time_between_requests=2):
        super().__init__(name, sim_context,  processing_time=0, capacity=None)
        self.counter = 0
        self.mean_time_between_requests = mean_time_between_requests


    def run(self):
        while True:
            request = Request(
                name=f"A-{self.counter}",
                metadata={"created_by": self.name}
            )
            self.counter += 1
            self.send(request)


            delay = random.expovariate(1 / self.mean_time_between_requests)
            yield self.env.timeout(delay)


class Responder(Collaborator):
    def on_receive(self, request):
        mean_delay = self.processing_time or 1
        delay = random.expovariate(1 / mean_delay)
        log.debug(f"[{self.name} @ t={self.env.now}] processing {request.name} with processing time {delay}")
        yield self.env.timeout(delay)


class RequestResponseSimulation(Simulation):
    def __init__(self, requestor: Callable[[Simulation], Requestor], responder: Callable[[Simulation], Responder], until=20, metrics_poll_interval=0.2, realtime_factor=None):
        super().__init__(realtime_factor)
        self.queue_samples = deque()
        self.sample_lock = threading.Lock()
        self.metrics_poll_interval = metrics_poll_interval
        self.until = until

        self.requestor = requestor(self)
        self.responder = responder(self)


        self.requestor.set_peer(self.responder)




    def queue_monitor(self, interval=0.1):
        """Push (sim_time, queue_len) into queue_samples every *interval*."""
        while True:
            with self.sample_lock:
                self.queue_samples.append((self.env.now, self.responder.entity_count))
            yield self.env.timeout(interval)

    def plot(self, interval=30, arrival_rate=None, service_rate=None):
        fig, ax = plt.subplots(figsize=(8, 4))
        (ax_line,) = ax.plot([], [], lw=2)
        (avg_line,) = ax.plot([], [], lw=1, linestyle='--', label="Cumulative Avg")
        (target_line,) = ax.plot([], [], lw=1, color='red', linestyle=':', label="Theoretical Avg")

        ax.set_xlabel("simulation‑time")
        ax.set_ylabel("queue length")
        ax.legend()

        utilization = arrival_rate/service_rate
        target_average = (utilization*utilization)/(1-utilization)

        def init():
            ax.set_xlim(0, self.until)
            ax.set_ylim(0, target_average*2)
            return ax_line, avg_line, target_line

        def update(frame):
            with self.sample_lock:
                if not self.queue_samples:
                    print(f"Nothing to plot")
                    return ax_line,avg_line,target_line

                xs, ys = zip(*self.queue_samples)

            # main queue length line
            ax_line.set_data(xs, ys)
            # cumulative average
            cumulative_avg = [sum(ys[:i + 1]) / (i + 1) for i in range(len(ys))]
            avg_line.set_data(xs, cumulative_avg)

            # Theoretical average line
            target_line.set_data([xs[0], xs[-1]], [target_average, target_average])

            ax.set_ylim(0, max(5, max(list(ys) + cumulative_avg + [target_average]) + 1))
            return ax_line, avg_line, target_line

        ani = animation.FuncAnimation(fig, update, init_func=init,
                                      interval=interval, blit=False, cache_frame_data=False)
        fig._ani = ani


        return ani

    def init_processes(self):
        self.env.process(self.requestor.run())
        self.env.process(self.requestor.receive())
        self.env.process(self.responder.receive())
        self.env.process(self.queue_monitor(self.metrics_poll_interval))

    def run(self):
        print(f"Simulation started at {self.env.now}")
        self.init_processes()
        self.env.run(until=self.until)
        print(f"simulation ended at {self.env.now}")
        print(str(self.signal_log))




if __name__ == "__main__":
    import matplotlib

    matplotlib.use('MacOSX')

    logging.basicConfig(level=logging.INFO)
    sim = RequestResponseSimulation(
        requestor=lambda sim: Requestor(name="A", sim_context=sim, mean_time_between_requests=2),
        responder =  lambda sim: Responder(name="B", sim_context=sim, processing_time=1.5, capacity=1),
        until=3000,
        realtime_factor=None
    )

    ani = sim.plot(interval=10, arrival_rate=0.5, service_rate=1/1.5)
    threading.Thread(target=sim.run, daemon=True).start()
    plt.show()

