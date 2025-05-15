# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT


from typing import Dict

import polars as pl
from metamodel import Signal, Entity
from metamodel.timeline import Timeline


from prototypes.queueing_network.signal_history_metrics import SignalHistoryMetric, QueueLength


class SignalHistory:
    def __init__(self, node, measurement_window: int):
        self.node = node
        self.measurement_window = measurement_window
        self._signals = Timeline()

        self.metrics: Dict[str, SignalHistoryMetric] = {
            "queue_length": QueueLength(node, measurement_window),
        }
        self.queue_length = self.metrics["queue_length"]

    @property
    def signals(self) -> Timeline:
        return self._signals

    def add(self, source: Entity, timestamp: float, signal_type: str, signal: Signal, transaction=None, target=None, **kwargs):
        self._signals.record(
            source=source,
            timestamp=timestamp,
            event_type=signal_type,
            signal=signal,
            transaction=transaction,
            target=target,
            tags=kwargs
        )
        self.queue_length.update(signal_type, timestamp, signal.id)

    def get_signals(self, signal_type: str = None) -> pl.DataFrame:
        df = self._signals.as_polars()
        if signal_type:
            return df.filter(pl.col("signal") == signal_type)
        return df

    def sort(self):
        # Sorting is not necessary in Polars until explicitly needed during query
        pass

    def __str__(self):
        df = self.get_signals()
        if df.is_empty():
            return "SignalHistory: (no signals)"

        types = df.group_by("signal").count()
        times = df["timestamp"].to_list()
        signals = df["signal_id"].unique()

        summary = [
            f"SignalHistory for {self.node}:({len(df)} signals)",
            f"  Types: " + ", ".join(f"{row['signal']}={row['count']}" for row in types.iter_rows()),
            f"  Time range: {min(times):.2f} to {max(times):.2f}",
            f"  Unique signals: {len(signals)}",
        ]
        return "\n".join(summary)



