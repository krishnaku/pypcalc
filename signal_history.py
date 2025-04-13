# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import List, Dict

from signal_history_metrics import SignalHistoryMetric, QueueLength


# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
@dataclass
class Signal:
    timestamp: float
    entity_id: str
    signal_type: str  # 'enter', 'exit', optionally 'start_service'


class SignalHistory:
    def __init__(self, node, measurement_window: int):
        self.node = node
        self.measurement_window = measurement_window
        self.signals: List[Signal] = []
        self.metrics: Dict[str, SignalHistoryMetric] = {
            "queue_length": QueueLength(node, measurement_window),
        }
        self.queue_length = self.metrics["queue_length"]


    def add(self, signal_type: str, timestamp: float, entity_id: str):
        self.signals.append(Signal(timestamp, entity_id, signal_type))
        self.queue_length.update(signal_type, timestamp, entity_id)

    def get_signals(self, signal_type: str = None) -> List[Signal]:
        if signal_type:
            return [s for s in self.signals if s.signal_type == signal_type]
        return self.signals

    def sort(self):
        self.signals.sort(key=lambda s: s.timestamp)

    def __str__(self):
        if not self.signals:
            return "SignalHistory: (no signals)"

        from collections import Counter

        types = Counter(s.signal_type for s in self.signals)
        times = [s.timestamp for s in self.signals]
        entities = set(s.entity_id for s in self.signals)

        summary = [
            f"SignalHistory for {self.node}:({len(self.signals)} signals)",
            f"  Types: " + ", ".join(f"{t}={n}" for t, n in types.items()),
            f"  Time range: {min(times):.2f} to {max(times):.2f}",
            f"  Unique entities: {len(entities)}",
        ]
        return "\n".join(summary)
