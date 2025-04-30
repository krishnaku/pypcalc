# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

import random
from typing import Generator

import simpy
from .protocol import DelayBehavior
from .registry import delay_behavior_registry


class DelayBehaviorBase(DelayBehavior):
    def __init__(self, sim_context, avg_delay=None):
        self._sim_context = sim_context
        if avg_delay is not None:
            self._avg_delay = avg_delay
            self._rate = 1 / avg_delay if avg_delay > 0 else 0
        else:
            raise ValueError("Delay must specify a non null value for the parameter delay")

    def delay(self) -> Generator[simpy.Event, None, None]:
        yield self._sim_context.timeout(self._avg_delay)

@delay_behavior_registry.register("Deterministic")
class Deterministic(DelayBehaviorBase):...


@delay_behavior_registry.register("Exponential Delay")
class ExponentialDelay(DelayBehaviorBase):
    def __init__(self, sim_context, avg_delay=None):
        if avg_delay is None:
            raise ValueError("Exponential Delay must specify a non null value for the parameter delay")
        super().__init__(sim_context, avg_delay)

    def delay(self) -> Generator[simpy.Event, None, None]:
        delay = random.expovariate(self._avg_delay)
        yield self._sim_context.timeout(delay)


@delay_behavior_registry.register("Markov")
class Markov(ExponentialDelay):
    def __init__(self, sim_context, **kwargs):
        if 'mean_time_between_arrivals' in kwargs:
            avg_delay = kwargs['mean_time_between_arrivals']
        elif 'avg_processing_time' in kwargs:
            avg_delay = kwargs['avg_processing_time']
        elif 'mean_time_between_requests' in kwargs:
            avg_delay = kwargs['mean_time_between_requests']
        elif 'avg_delay' in kwargs:
            avg_delay = kwargs['avg_delay']
        else:
            raise ValueError("Markov Delays must specify a non null value for the delay parameter"
                             "you can pass it as any one of: mean_time_between_arrivals, avg_processing_time, "
                             "mean_time_between_requests or just as generic avg_delay")

        super().__init__(sim_context, avg_delay)
