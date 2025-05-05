# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

from abc import abstractmethod
from typing import Dict, Any, Set, Protocol

from .signal_log import SignalLog, SignalListener, SignalEvent

from .node import Node

class Boundary(Node, SignalListener, Protocol):

    @property
    def signal_history(self) -> SignalLog:...

    @property
    def population(self) -> int: ...

    @property
    def tenants(self) -> Set[str]:...


    def on_signal_event(self, event: SignalEvent) -> None:
        pass


