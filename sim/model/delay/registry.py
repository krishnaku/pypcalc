# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT


"""
Registry for delay behaviors. See module behavior for examples of registered behaviors.
"""

from sim.model import Registry
from sim.model.delay.protocol import DelayBehavior


delay_behavior_registry: Registry[DelayBehavior]= Registry()
