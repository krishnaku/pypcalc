# -*- coding: utf-8 -*-
from core.signal import SignalLog

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
import simpy

from typing import List
class Simulation:
    def __init__(self, until=30, runs=1, realtime_factor: float = None):
        self._env = None
        self._signal_log = None
        # preserve separate signal logs per simulation run
        self._all_logs: List[SignalLog] = []

        self.realtime_factor = realtime_factor
        self.until = until
        self.runs = runs
        self.current_run = 0



    def init_sim(self):
        if self.realtime_factor is not None:
            self._env = simpy.rt.RealtimeEnvironment(factor=self.realtime_factor)
        else:
            self._env = simpy.Environment()

        self.reset_signal_log()

        self.bind_environment(self._env)

    def reset_signal_log(self):
        if self._signal_log is not None:
            self._all_logs.append(self._signal_log)

        self._signal_log = SignalLog()

    def bind_environment(self, env):
        pass

    def run(self):
        print(f"Simulation started")
        for self.current_run in range(self.runs):
            self.init_sim()
            self.env.run(until=self.until)
            self.post_run()

        print(f"simulation ended")
        print(str(self.signal_log))

    def post_run(self):
        pass

    @property
    def env(self):
        return self._env

    @property
    def signal_log(self):
        return self._signal_log

    @property
    def all_logs(self) -> List[SignalLog]:
        return self._all_logs + ([self._signal_log] if self._signal_log else [])