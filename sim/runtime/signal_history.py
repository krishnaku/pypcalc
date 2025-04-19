# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

from dataclasses import asdict
from typing import List, Dict, Optional, Any
import polars as pl

from sim.model.signal.signal import Signal, SIGNAL_SCHEMA_PL
from signal_history_metrics import SignalHistoryMetric, QueueLength


class SignalLog:
    def __init__(self):
        self._signal_buffer: List[Signal] = []
        self.signals = pl.DataFrame(
            schema=SIGNAL_SCHEMA_PL
        )

    def record(self, source: str, timestamp: float, signal_type: str, entity_id: str, target: Optional[str] = None, tags: Optional[Dict[str, Any]] = None) -> Signal:
        signal = Signal(source, timestamp, signal_type, entity_id, target, tags)
        return self.signal(signal)

    def signal(self, signal: Signal) -> Signal:
        self._signal_buffer.append(signal)
        return signal

    def flush(self):
        if not self._signal_buffer:
            return
        batch = [asdict(sig) for sig in self._signal_buffer]
        self.signals = self.signals.vstack(pl.DataFrame(batch))
        self._signal_buffer.clear()

    def get_signals(self) -> pl.DataFrame:
        self.flush()
        return self.signals

    def __len__(self):
        return len(self.signals) + len(self._signal_buffer)



class SignalHistory:
    def __init__(self, node, measurement_window: int):
        self.node = node
        self.measurement_window = measurement_window
        self.signals = SignalLog()

        self.metrics: Dict[str, SignalHistoryMetric] = {
            "queue_length": QueueLength(node, measurement_window),
        }
        self.queue_length = self.metrics["queue_length"]



    def add(self, source: str, timestamp: float, signal_type: str, entity_id: str, target=None, **kwargs):
        signal = Signal(
            source=source,
            timestamp=timestamp,
            signal=signal_type,
            entity_id=entity_id,
            target=target,
            tags=kwargs
        )
        self.signals.record(signal)
        self.queue_length.update(signal_type, timestamp, entity_id)

    def get_signals(self, signal_type: str = None) -> pl.DataFrame:
        df = self.signals.get_signals()
        if signal_type:
            return df.filter(pl.col("signal") == signal_type)
        return df

    def sort(self):
        # Sorting is not necessary in Polars until explicitly needed during query
        pass

    def __str__(self):
        df = self.signals.get_signals()
        if df.is_empty():
            return "SignalHistory: (no signals)"

        types = df.group_by("signal").count()
        times = df["timestamp"].to_list()
        entities = df["entity_id"].unique()

        summary = [
            f"SignalHistory for {self.node}:({len(df)} signals)",
            f"  Types: " + ", ".join(f"{row['signal']}={row['count']}" for row in types.iter_rows()),
            f"  Time range: {min(times):.2f} to {max(times):.2f}",
            f"  Unique entities: {len(entities)}",
        ]
        return "\n".join(summary)
