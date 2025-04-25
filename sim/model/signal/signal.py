# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional, Dict, Any

import polars as pl


# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from core import Signal, Entity, Transaction, Node

class Enter(Signal):
    def __init__(self, source: Node, timestamp: float, entity: Entity, transaction: Transaction=None, **kwargs):
        self.signal_type = "enter"
        self.source = source
        self.transaction = transaction
        self.timestamp = timestamp
        self.entity = entity
        self.tags = kwargs


class Exit(Signal):
    def __init__(self, source: Node , timestamp: float, entity: Entity, transaction:Transaction = None, **kwargs):
        self.signal_type = "exit"
        self.source = source
        self.transaction = transaction
        self.timestamp = timestamp
        self.entity_id = entity
        self.tags = kwargs
