# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

from __future__ import annotations

from typing import Generator, Dict, Any, Optional

import simpy

from sim.model.collaborator.base import CollaboratorBase, Request, Response
from sim.model.delay import DelayBehavior, delay_behavior_registry
from sim.runtime.simulation import Simulation
from misc.collection_utils import without_keys
from .registry import collaborator_registry

@collaborator_registry.register("Requestor")
class Requestor(CollaboratorBase):
    def __init__(self, name: str, sim_context: Simulation, delay_behavior: Dict[str,Any]=None,  **kwargs):
        super().__init__(name, sim_context, delay_behavior=delay_behavior, **kwargs)
        self.counter: int = 0
        self.delay_behavior: Optional[DelayBehavior] = None
        if delay_behavior is not None:
            self.delay_behavior = delay_behavior_registry.create(sim_context=sim_context, **delay_behavior)
        else:
            raise ValueError(f"Request behavior not specified for Requestor {name}")


    def start_processes(self):
        if self.sim_context is None:
            raise RuntimeError(f"Simulation Context for Requestor {self.name} has not been initialized")
        self.sim_context.process(self.send_requests())
        self.sim_context.process(self.receive())


    def send_requests(self):
        while True:
            request = Request(
                name=f"A-{self.counter}",
                metadata={"created_by": self.name}
            )
            self.transactions_in_process.add(request.transaction.id)
            self.send(request)
            self.counter += 1
            yield from self.delay_behavior.delay()


    def on_receive_response(self, response: Response) -> Generator[simpy.events.Event, None, None]:
        self.transactions_in_process.remove(response.transaction.id)
        yield self.sim_context.timeout(0)


@collaborator_registry.register("Responder")
class Responder(CollaboratorBase):
    def __init__(self, name: str, sim_context: Simulation, concurrency=None, delay_behavior:Dict[str,Any] = None, **kwargs):
        super().__init__(name, sim_context, concurrency=concurrency, delay_behavior=delay_behavior, **kwargs)
        self.counter: int = 0
        self.delay_behavior: Optional[DelayBehavior] = None
        if delay_behavior is not None:
            self.delay_behavior = delay_behavior_registry.create(sim_context=sim_context, **delay_behavior)
        else:
            raise ValueError(f"Response behavior not specified for Responder {name}")

    def start_processes(self):
        if self.sim_context is None:
            raise RuntimeError(f"Simulation Context for Responder {self.name} has not been initialized")
        self.sim_context.process(self.receive())

    def on_receive_request(self, request) -> Generator[simpy.events.Event, None, None]:
        yield from self.delay_behavior.delay()

