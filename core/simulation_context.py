# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

from __future__ import annotations

from typing import List, Dict, Optional, Protocol, Any


from .entity import Entity
from .transaction import Transaction
from .boundary import Boundary
from .signal import SignalEvent, SignalLog, SignalListener


class SimulationContext(Protocol):
    from .node import Node

    # -------- Accessors-------------------------
    def nodes(self, name: str) -> List[Node]:...

    def entities(self, name: str) -> List[Entity]:...

    def transactions(self, name: str) -> List[Transaction]:...

    def boundaries(self, name: str) -> List[Boundary]:...

    # --------Signal Interface ------------------
    def record_signal(self, source: Node, timestamp: float, signal_type: str, entity: Entity, transaction=None,
                      target: Optional[Node] = None, tags: Optional[Dict[str, Any]] = None) -> SignalEvent:...

    def register_listener(self, listener: SignalListener) -> None:...

    @property
    def all_logs(self) -> List[SignalLog]:...
    """Read access to signal logs is via the all_logs property."""
