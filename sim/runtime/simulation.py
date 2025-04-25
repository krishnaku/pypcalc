# -*- coding: utf-8 -*-
from core.signal import SignalLog

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
import simpy

class Simulation:
    def __init__(self, realtime_factor: float = None):
        self._env = simpy.rt.RealtimeEnvironment(factor=realtime_factor) if realtime_factor is not None else simpy.Environment()
        self._signal_log = SignalLog()

    @property
    def env(self):
        return self._env

    @property
    def signal_log(self):
        return self._signal_log


