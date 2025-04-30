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
from typing import Dict, Any, Optional, List, Literal, Union, Iterable



from .entity import Entity
from .node import Node
from .transaction import Transaction


@dataclass(frozen=True)
class Signal:
    source_id: str
    timestamp: float
    signal_type: str
    entity_id: str
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
    def entity(self) -> Entity:
        return self.signal_log.entity(self.entity_id)

    @property
    def transaction(self) -> Transaction:
        return self.signal_log.transaction(self.transaction_id)

    def as_dict(self: Signal) -> dict:
        # Necessary because Signal include non-serializable field (signal_log)
        return {
            "source_id": self.source_id,
            "timestamp": float(self.timestamp),
            "signal": self.signal_type,
            "transaction_id": self.transaction_id,
            "entity_id": self.entity_id,
            "target_id": self.target_id,
            "tags": self.tags,
        }


class SignalLog:
    def __init__(self):
        self._signals: List[Signal] = []
        self._transactions: Dict[str, Transaction] = {}
        self._entities: Dict[str, Entity] = {}
        self._nodes: Dict[str, Node] = {}

    @property
    def signals(self) -> List[Signal]:
        return self._signals

    def node(self, node_id) -> Node:
        return self._nodes.get(node_id)

    def entity(self, entity_id) -> Entity:
        return self._entities.get(entity_id)

    def transaction(self, transaction_id) -> Transaction:
        return self._transactions.get(transaction_id)

    def __len__(self):
        return len(self.signals)

    def record(self, source: Node, timestamp: float, signal_type: str, entity: Entity, transaction=None,
               target: Optional[Node] = None, tags: Optional[Dict[str, Any]] = None) -> Signal:
        self._nodes[source.id] = source
        self._entities[entity.id] = entity
        tx = transaction or entity.transaction
        if tx is not None:
            self._transactions[tx.id] = tx

        if target is not None:
            self._nodes[target.id] = target

        signal = Signal(
            source_id=source.id,
            timestamp=timestamp,
            signal_type=signal_type,
            transaction_id=tx.id if tx is not None else None,
            entity_id=entity.id,
            target_id=target.id if target is not None else None,
            tags=tags,
            signal_log=self
        )
        self._signals.append(signal)
        return signal

    def __iter__(self):
        return iter(self._signals)

    @property
    def transactions(self) -> Iterable[tuple[str, Transaction]]:
        return self._transactions.items()

    @property
    def entities(self) -> Iterable[tuple[str, Entity]]:
        return self._entities.items()

    @property
    def nodes(self) -> Iterable[tuple[str, Node]]:
        return self._nodes.items()

    # Transformations
    def as_polars(self):
        if not self._signals:
            return
        batch = [sig.as_dict() for sig in self._signals]
        df = pl.DataFrame(
            schema={
                "source_id": pl.Utf8,
                "timestamp": pl.Float64,
                "signal": pl.Utf8,
                "transaction_id": pl.Utf8,
                "entity_id": pl.Utf8,
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
                    "entity_types": 0,
                    "entities": 0,
                    "avg_transaction_duration": 0.0,
                    "avg_entity_span": 0.0,
                }
            return "📊 Signal Log Summary\n  • No signals recorded."

        num_entries: int = df.height
        tmin: float = df["timestamp"].min()
        tmax: float = df["timestamp"].max()
        timespan: float = tmax - tmin

        num_transactions: int = df["transaction_id"].drop_nulls().unique().len()

        num_nodes: int = df.select([
            df["source_id"],
            df["target_id"]
        ]).drop_nulls().unique().height

        num_entity_types = pl.Series([
            entity.entity_type for entity in self._entities.values()
        ]).unique().len()

        # 2. Count by entity_type
        entity_type_counts = pl.Series([
            entity.entity_type for entity in self._entities.values()
        ]).value_counts()

        entity_type_lines = "\n".join(
            f"    - {entity_type.ljust(10)}: {count}" for entity_type, count in entity_type_counts.rows()
        )

        num_entities: int = df["entity_id"].unique().len()

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
            df.group_by("entity_id")
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
            "start_time": tmin,
            "end_time": tmax,
            "transactions": num_transactions,
            "nodes": num_nodes,
            "entity_types": num_entity_types,
            "entity_type_count": entity_type_counts,
            "entities": num_entities,
            "avg_transaction_duration": avg_tx_duration,
            "avg_entity_span": avg_entity_duration,
        }

        if output == "dict":
            return summary_dict

        return (
            "📊 Signal Log Summary\n"
            f"  • Log entries       : {num_entries}\n"
            f"  • Time span         : {timespan:.3f} time units (from t={tmin:.3f} to t={tmax:.3f})\n"
            f"  • Transactions      : {num_transactions}\n"
            f"  • Avg Tx duration   : {avg_tx_duration:.3f}\n"
            f"  • Nodes             : {num_nodes}\n"
            f"  • Entity Types         : {num_entity_types}\n"
            f"{entity_type_lines}\n"
            f"  • Entities          : {num_entities}\n"
            f"  • Avg Entity span   : {avg_entity_duration:.3f}"
        )

    def display(self):
        summary = self.summarize()
        details = "\n".join([
            f"{sig.timestamp:.3f}: {sig.signal_type}: {sig.source.name} -> {sig.target.name if sig.target is not None else None} :: {sig.entity.name} ({sig.transaction.id[-8:] if sig.transaction else ' '})"
            for sig in self._signals
        ])
        return f"{summary}\n-------Detailed Log-----------\n{details}"

    def __str__(self):
        return self.summarize()

    def __repr__(self):
        return self.display()