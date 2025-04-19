# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional, Dict, Any

import polars as pl


# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
@dataclass
class Signal:
    source: str
    timestamp: float
    signal: str
    entity_id: str
    target: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None


SIGNAL_SCHEMA_PL = {
    "source": pl.Utf8,
    "timestamp": pl.Float64,
    "signal": pl.Utf8,
    "entity_id": pl.Utf8,
    "target": pl.Utf8,
    "tags": pl.Object,
}

class Enter(Signal):
    def __init__(self, source: str, timestamp: float, entity_id: str, **kwargs):
        self.signal_type = "enter"
        self.source = source
        self.timestamp = timestamp
        self.entity_id = entity_id
        self.tags = kwargs


class Exit(Signal):
    def __init__(self, source: str, timestamp: float, entity_id: str, **kwargs):
        self.signal_type = "exit"
        self.source = source
        self.timestamp = timestamp
        self.entity_id = entity_id
        self.tags = kwargs
