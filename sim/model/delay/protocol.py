# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT


from typing import Generator

import simpy

from sim.model import Behavior

class DelayBehavior(Behavior):
    def delay(self) -> Generator[simpy.Event, None, None]:...
