# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

from typing import Dict, Any, Optional, Set

from abc import ABC, abstractmethod

from core import Boundary
from core.signal_log import SignalEvent, SignalLog
from sim.model.node import NodeBase
from sim.runtime.simulation import Simulation

class BoundaryBase(NodeBase, Boundary, ABC):

    def __init__(self, kind, name, config: Dict[str,Any], sim_context: Simulation, id:Optional[str]=None ):
        super().__init__(kind, name, config, sim_context, id)

        self._signal_history: SignalLog = SignalLog()
        self._sim_context = sim_context
        self._tenants: Set[str] = set()

        self._sim_context.register_listener(self)

    @property
    def signal_history(self) -> SignalLog:
        return self._signal_history

    @property
    def population(self) -> int:
        return len(self._tenants)

    @property
    def tenants(self) -> Set[str]:
        return self._tenants

    @abstractmethod
    def on_signal_event(self, event: SignalEvent) -> None:...