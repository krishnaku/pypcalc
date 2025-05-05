# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from __future__ import annotations
import polars as pl
import fnmatch

from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Literal, Union, Iterable, Protocol

from .signal import Signal
from .node import Node
from .transaction import Transaction


@dataclass(frozen=True)
class SignalEvent:
    source_id: str
    timestamp: float
    signal_type: str
    signal_id: str
    transaction_id: Optional[str] = None
    target_id: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None
    signal_log: SignalLog = None

    @property
    def source(self) -> Node:
        return self.signal_log.node(self.source_id)

    @property
    def target(self) -> Node:
        return self.signal_log.node(self.target_id)

    @property
    def signal(self) -> Signal:
        return self.signal_log.entity(self.signal_id)

    @property
    def transaction(self) -> Transaction:
        return self.signal_log.transaction(self.transaction_id)

    def as_dict(self: SignalEvent) -> dict:
        # Necessary because Signal include non-serializable field (signal_log)
        return {
            "source_id": self.source_id,
            "timestamp": float(self.timestamp),
            "signal": self.signal_type,
            "transaction_id": self.transaction_id,
            "signal_id": self.signal_id,
            "target_id": self.target_id,
            "tags": self.tags,
        }

class SignalListener(Protocol):

    def on_signal_event(self, event: SignalEvent) -> None:...

class SignalLog:
    def __init__(self):
        self._signal_events: List[SignalEvent] = []
        self._transactions: Dict[str, Transaction] = {}
        self._entities: Dict[str, Signal] = {}
        self._nodes: Dict[str, Node] = {}

    @property
    def signals(self) -> List[SignalEvent]:
        return self._signal_events

    def node(self, node_id) -> Node:
        return self._nodes.get(node_id)

    def entity(self, signal_id) -> Signal:
        return self._entities.get(signal_id)

    def transaction(self, transaction_id) -> Transaction:
        return self._transactions.get(transaction_id)

    def __len__(self):
        return len(self.signals)

    def record(self, source: Node, timestamp: float, signal_type: str, entity: Signal, transaction=None,
               target: Optional[Node] = None, tags: Optional[Dict[str, Any]] = None) -> SignalEvent:
        self._nodes[source.id] = source
        self._entities[entity.id] = entity
        tx = transaction or entity.transaction
        if tx is not None:
            self._transactions[tx.id] = tx

        if target is not None:
            self._nodes[target.id] = target

        signal = SignalEvent(
            source_id=source.id,
            timestamp=timestamp,
            signal_type=signal_type,
            transaction_id=tx.id if tx is not None else None,
            signal_id=entity.id,
            target_id=target.id if target is not None else None,
            tags=tags,
            signal_log=self
        )
        self._signal_events.append(signal)
        return signal

    def __iter__(self):
        return iter(self._signal_events)

    @property
    def transactions(self) -> Iterable[tuple[str, Transaction]]:
        return self._transactions.items()

    @property
    def entities(self) -> Iterable[tuple[str, Signal]]:
        return self._entities.items()

    @property
    def nodes(self) -> Iterable[tuple[str, Node]]:
        return self._nodes.items()

    # Transformations
    def as_polars(self):
        if not self._signal_events:
            return
        batch = [sig.as_dict() for sig in self._signal_events]
        df = pl.DataFrame(
            schema={
                "source_id": pl.Utf8,
                "timestamp": pl.Float64,
                "signal": pl.Utf8,
                "transaction_id": pl.Utf8,
                "signal_id": pl.Utf8,
                "target_id": pl.Utf8,
                "tags": pl.Object,
            })
        return df.vstack(pl.DataFrame(batch))

    def summarize(self, output: Literal["str", "dict"] = "str") -> Union[str, Dict[str, Union[int, float, str]]]:
        df = self.as_polars()
        if df is None or df.is_empty():
            if output == "dict":
                return {
                    "log_entries": 0,
                    "time_span": 0.0,
                    "transactions": 0,
                    "nodes": 0,
                    "signal_types": 0,
                    "entities": 0,
                    "avg_transaction_duration": 0.0,
                    "avg_entity_span": 0.0,
                }
            return "📊 Signal Log Summary\n  • No signals recorded."

        num_entries: int = df.height
        t_min: float = df["timestamp"].min()
        t_max: float = df["timestamp"].max()
        timespan: float = t_max - t_min

        num_transactions: int = df["transaction_id"].drop_nulls().unique().len()

        num_nodes: int = df.select([
            df["source_id"],
            df["target_id"]
        ]).drop_nulls().unique().height

        num_signal_types = pl.Series([
            entity.signal_type for entity in self._entities.values()
        ]).unique().len()

        # 2. Count by signal_type
        signal_type_counts = pl.Series([
            entity.signal_type for entity in self._entities.values()
        ]).value_counts()

        signal_type_lines = "\n".join(
            f"    - {signal_type.ljust(10)}: {count}" for signal_type, count in signal_type_counts.rows()
        )

        num_entities: int = df["signal_id"].unique().len()

        tx_span = (
            df.filter(pl.col("transaction_id").is_not_null())
            .group_by("transaction_id")
            .agg([
                pl.col("timestamp").min().alias("t_start"),
                pl.col("timestamp").max().alias("t_end")
            ])
            .with_columns((pl.col("t_end") - pl.col("t_start")).alias("tx_duration"))
        )
        avg_tx_duration: float = tx_span["tx_duration"].mean()

        entity_span = (
            df.group_by("signal_id")
            .agg([
                pl.col("timestamp").min().alias("t_start"),
                pl.col("timestamp").max().alias("t_end")
            ])
            .with_columns((pl.col("t_end") - pl.col("t_start")).alias("entity_duration"))
        )
        avg_entity_duration: float = entity_span["entity_duration"].mean()

        summary_dict: Dict[str, Union[int, float, str]] = {
            "log_entries": num_entries,
            "time_span": timespan,
            "start_time": t_min,
            "end_time": t_max,
            "transactions": num_transactions,
            "nodes": num_nodes,
            "signal_types": num_signal_types,
            "signal_type_count": signal_type_counts,
            "entities": num_entities,
            "avg_transaction_duration": avg_tx_duration,
            "avg_entity_span": avg_entity_duration,
        }

        if output == "dict":
            return summary_dict

        return (
            "📊 Signal Log Summary\n"
            f"  • Log entries       : {num_entries}\n"
            f"  • Time span         : {timespan:.3f} time units (from t={t_min:.3f} to t={t_max:.3f})\n"
            f"  • Transactions      : {num_transactions}\n"
            f"  • Avg Tx duration   : {avg_tx_duration:.3f}\n"
            f"  • Nodes             : {num_nodes}\n"
            f"  • Entity Types         : {num_signal_types}\n"
            f"{signal_type_lines}\n"
            f"  • Entities          : {num_entities}\n"
            f"  • Avg Entity span   : {avg_entity_duration:.3f}"
        )

    def display(self):
        summary = self.summarize()
        details = "\n".join([
            f"{sig.timestamp:.3f}: {sig.signal_type}: {sig.source.name} -> {sig.target.name if sig.target is not None else None} :: {sig.signal.name} ({sig.transaction.id[-8:] if sig.transaction else ' '})"
            for sig in self._signal_events
        ])
        return f"{summary}\n-------Detailed Log-----------\n{details}"

    def __str__(self):
        return self.summarize()

    def __repr__(self):
        return self.display()