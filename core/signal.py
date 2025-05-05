# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from .transaction import Transaction

@dataclass
class Signal:
    id: str
    name: str
    signal_type: Optional[str] = None
    transaction: Optional[Transaction] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, name: str, entity_type: Optional[str], metadata: Dict[str, Any] = None, transaction: Optional[Transaction]=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.signal_type = entity_type
        self.metadata = metadata
        self.transaction = transaction
