# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
# Re-defining the minimal test scaffold after reset

from dataclasses import dataclass
from typing import Optional, List
import numpy as np
# Minimal Signal class for test
@dataclass
class Signal:
    source: str
    timestamp: float
    signal: str
    entity_id: str
    target: Optional[str] = None

# Factory to simplify signal creation
def make_signal(source, signal_type, timestamp, entity_id, target=None):
    return Signal(source=source, signal=signal_type, timestamp=timestamp, entity_id=entity_id, target=target)

# Placeholder for setup_presence_matrix (would call PresenceMatrix.from_signals in real use)
def setup_presence_matrix(signals: List[Signal], t0=0.0, t1=10.0, bin_width=1.0, enter_event="enter", exit_event="exit", initial_population=None):
    return {
        "signals": signals,
        "t0": t0,
        "t1": t1,
        "bin_width": bin_width,
        "initial_population": initial_population
    }

# Example test for pytest
def test_empty_signal_list():
    matrix = setup_presence_matrix(signals=[])
    assert matrix["signals"] == []
    assert matrix["t0"] == 0.0
    assert matrix["t1"] == 10.0
    assert matrix["bin_width"] == 1.0
    assert matrix["initial_population"] is None

test_empty_signal_list()
