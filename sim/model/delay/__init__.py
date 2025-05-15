# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from .protocol import DelayBehavior
from .registry import delay_behavior_registry

#trigger registration of concrete behaviors
import sim.model.delay.behavior



