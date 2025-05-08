# -*- coding: utf-8 -*-
from typing import Dict, Any

import simpy

from prototypes.queueing_network.base_node import NonBlockingService, BlockingService
from core.domain import DomainModel


# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
class PureDelay(NonBlockingService):
    def __init__(self, name: str, config: Dict[str, Any], sim_context: DomainModel) -> None:
        super().__init__(name, config, sim_context)
        self.delay_fn = config.get("delay")
        if self.delay_fn is None:
            raise ValueError(f"Pure delay node {self.name} did not specify a delay")
        if not callable(self.delay_fn):
            raise ValueError(f"Delay must be a callable in node {self.name}")

    def perform_service(self, signal_id: str, **kwargs):
        self.signal_start_service(signal_id, **kwargs)
        delay = self.delay_fn(signal_id, **kwargs)
        yield self.env.timeout(delay)
        self.signal_end_service(signal_id, **kwargs)


class BlockingDelay(BlockingService):
    def __init__(self, name: str, config: Dict[str, Any], sim_context: DomainModel) -> None:
        super().__init__(name, config, sim_context)
        self.delay_fn = config.get("delay")
        if self.delay_fn is None:
            raise ValueError(f"Pure delay node {self.name} did not specify a delay")
        if not callable(self.delay_fn):
            raise ValueError(f"Delay must be a callable in node {self.name}")

        self._init_concurrency_limit(self.env)

    def _init_concurrency_limit(self, env):
        self.concurrency = self.config.get("concurrency")
        if self.concurrency:
            self.resource = simpy.Resource(env, capacity=self.concurrency)
        else:
            self.resource = None

    def perform_service(self, signal_id: str, **kwargs):
        with self.resource.request() as req:
            yield req
            self.signal_start_service(signal_id, **kwargs)
            delay = self.delay_fn(signal_id, **kwargs)
            yield self.env.timeout(delay)
            self.signal_end_service(signal_id, **kwargs)
