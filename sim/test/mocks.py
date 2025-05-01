# -*- coding: utf-8 -*-
from typing import List

import simpy

from sim.runtime.simulation import Simulation


# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
class MockSimulation(Simulation):
    def start_processes(self) -> List[simpy.events.Process]:
        pass

    def bind_environment(self):
        pass
