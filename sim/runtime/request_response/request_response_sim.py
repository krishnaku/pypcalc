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
from typing import Callable, List, Tuple

import simpy
import numpy as np

from IPython.core.display_functions import display
from matplotlib import pyplot as plt, animation

from sim.runtime.request_response.collaborator import Collaborator, Request, Response
from sim.runtime.simulation import Simulation

log = logging.getLogger(__name__)


class Requestor(Collaborator):
    def __init__(self, name: str, sim_context: Simulation, mean_time_between_requests=2):
        super().__init__(name, sim_context, processing_time=0, capacity=None)
        self.counter: int = 0
        self.mean_time_between_requests = mean_time_between_requests

    def run(self):
        while True:
            request = Request(
                name=f"A-{self.counter}",
                metadata={"created_by": self.name}
            )
            self.transactions_in_process.add(request.transaction.id)
            self.send(request)
            self.counter += 1
            delay = random.expovariate(1 / self.mean_time_between_requests)
            yield self.env.timeout(delay)

    def on_receive_response(self, response: Response):
        self.transactions_in_process.remove(response.transaction.id)
        yield self.env.timeout(0)



class Responder(Collaborator):
    def on_receive_request(self, request):
        mean_delay = self.processing_time or 1
        delay = random.expovariate(1 / mean_delay)
        log.debug(f"[{self.name} @ t={self.env.now}] processing {request.name} with processing time {delay}")
        yield self.env.timeout(delay)


class RequestResponseSimulation(Simulation):
    def __init__(
            self,
            requestor: Callable[[Simulation], Requestor],
            responder: Callable[[Simulation], Responder],
            runs=1,
            until=20,
            metrics_poll_interval=1.0,
            realtime_factor=None):
        self.queue_samples: List[List[Tuple[float, int]]] = [[] for run in range(runs)]
        self.sample_lock = threading.Lock()
        self.metrics_poll_interval = metrics_poll_interval
        self.requestor_factory = requestor
        self.responder_factory = responder
        self.requestor = None
        self.responder = None
        # animation support
        self._ani = None
        self._needs_update = False


        # init the simulation parameters and model
        super().__init__(
            until,
            runs,
            realtime_factor
        )

    def bind_environment(self, env: simpy.Environment):
        # this is called every time the simulation environment is reset
        self.requestor = self.requestor_factory(self)
        self.responder = self.responder_factory(self)
        self.requestor.set_peer(self.responder)

        env.process(self.requestor.run())
        env.process(self.requestor.receive())
        env.process(self.responder.receive())
        env.process(self.queue_monitor())

    def post_run(self):
        super().post_run()
        self._needs_update = True



    def queue_monitor(self):
        while True:
            with self.sample_lock:
                self.queue_samples[self.current_run].append((self.env.now, len(self.requestor.transactions_in_process)))
            yield self.env.timeout(self.metrics_poll_interval)

    def plot(self):
        import matplotlib.pyplot as plt
        import numpy as np

        log.info(f"plotting {len(self.queue_samples[self.current_run])} samples")

        fig, (ax_avg, ax_current) = plt.subplots(
            2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [2, 1]}
        )

        # --- Theoretical average ---
        rho=0
        target_average = None
        arrival_rate  = 1 / self.requestor.mean_time_between_requests if self.requestor.mean_time_between_requests is not None else None
        service_rate = 1 / self.responder.processing_time if self.responder.processing_time is not None else None

        if arrival_rate and service_rate:
            rho = arrival_rate / service_rate
            if rho < 1:
                target_average = rho / (1 - rho)

        # --- Lower plot: last run ---
        last_run = self.queue_samples[-1] if self.queue_samples else []
        if len(last_run) >= 2:
            t, q = zip(*last_run)
            cumulative_avg = [sum(q[:j + 1]) / (j + 1) for j in range(len(q))]
            ax_current.plot(t, q, lw=1.5, label="Queue Length")
            ax_current.plot(t, cumulative_avg, lw=1, linestyle='--', label="Cumulative Avg")

            if target_average is not None:
                ax_current.axhline(y=target_average, color='red', linestyle=':', label="Theoretical Avg")

            ax_current.set_ylim(0, max(5, max(list(q) + cumulative_avg + (
                [target_average] if target_average else [])) + 1))

        ax_current.set_ylabel("Queue Length (Last Run)")
        ax_current.legend()

        ax_current.set_title("Last Run Detail")
        ax_current.set_xlabel("Simulation Time")

        # --- Upper plot: cumulative avg curves + confidence band ---
        time_grid = np.linspace(0, self.until, 3000)
        interpolated_curves = []
        max_y = 0

        for i, run in enumerate(self.queue_samples):
            if len(run) < 2:
                continue
            t, q = zip(*run)
            cumulative_avg = np.cumsum(q) / np.arange(1, len(q) + 1)
            interp = np.interp(time_grid, t, cumulative_avg)
            interpolated_curves.append(interp)

            # Only show legend label for last 5 runs
            label = f"Run {i + 1}" if i >= len(self.queue_samples) - 5 else None
            ax_avg.plot(t, cumulative_avg, alpha=0.4, linewidth=0.75, color='gray', label=label)
            max_y = max(max_y, max(cumulative_avg))

        if interpolated_curves:
            arr = np.array(interpolated_curves)
            lower = np.percentile(arr, 5, axis=0)
            upper = np.percentile(arr, 95, axis=0)
            mean = np.mean(arr, axis=0)

            ax_avg.fill_between(time_grid, lower, upper, color='cornflowerblue', alpha=0.6,  label='90% Confidence Band')
            ax_avg.plot(time_grid, mean, color='navy', linestyle='--', linewidth=1.5, label='Ensemble Mean (All Runs)')

            max_y = max(max_y, np.max(upper))

        if target_average is not None:
            ax_avg.axhline(y=target_average, color='red', linestyle=':', label="Theoretical Avg")
            max_y = max(max_y, target_average)

        ax_avg.set_title(f"Utilization {rho:.2f}: Cumulative Averages Across {self.runs} Runs")
        ax_avg.set_ylim(0, max(5, max_y + 1))
        ax_avg.set_ylabel("Queue Length (Cumulative Averages)")
        ax_avg.legend(loc="upper right")

        plt.tight_layout()
        log.info(f"plotted {len(self.queue_samples[self.current_run])} samples")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    sim = RequestResponseSimulation(
        requestor=lambda sim: Requestor(name="A", sim_context=sim, mean_time_between_requests=1.4),
        responder=lambda sim: Responder(name="B", sim_context=sim, processing_time=1.5, capacity=1),
        until=20000,
        runs=5,
        realtime_factor=None
    )
    sim.run()

    sim.plot()

    plt.show()
