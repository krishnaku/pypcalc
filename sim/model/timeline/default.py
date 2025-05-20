# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

import uuid
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Iterable, Literal, Union

import polars as pl

from sim.metamodel import Entity, Signal, Transaction, Timeline, DomainEvent


@dataclass
class DefaultEvent(DomainEvent):
    """A timestamped event representing the lifecycle events of a domain element as recorded on a timeline."""

    source_id: str
    """The ID of the entity that emitted or handled the signal."""

    timestamp: float
    """The time at which the event occurred."""

    event_type: str
    """A label describing the type of event (e.g., 'send', 'receive', 'process')."""

    signal_id: str
    """The ID of the signal involved in the event."""

    transaction_id: Optional[str] = None
    """Optional transaction ID if the signal is part of a transaction."""

    target_id: Optional[str] = None
    """The ID of the receiving entity, if any."""

    tags: Optional[Dict[str, Any]] = None
    """Optional dictionary of additional metadata tags."""

    timeline: Timeline = None
    """Back-reference to the timeline where this event was recorded (used for resolving IDs)."""

    # Element implementation
    _id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @property
    def id(self) -> str:
        """The unique ID of the signal (auto-assigned)."""
        return self._id

    @property
    def source(self) -> Entity:
        """Returns the `Entity` corresponding to the source ID."""
        return self.timeline.entity(self.source_id)

    @property
    def target(self) -> Entity:
        """Returns the `Entity` corresponding to the target ID, if present."""
        return self.timeline.entity(self.target_id)

    @property
    def signal(self) -> Signal:
        """Returns the full `Signal` object referenced by this event."""
        return self.timeline.signal(self.signal_id)

    @property
    def transaction(self) -> Transaction:
        """Returns the `Transaction` this signal is part of, if any."""
        return self.timeline.transaction(self.transaction_id)

    def as_dict(self) -> dict:
        """Convert the event into a serializable dictionary (excluding timeline)."""
        return {
            "source_id": self.source_id,
            "timestamp": float(self.timestamp),
            "event_type": self.event_type,
            "transaction_id": self.transaction_id,
            "signal_id": self.signal_id,
            "target_id": self.target_id,
            "tags": self.tags,
        }


class DefaultTimeline(Timeline):
    """Captures and manages all signal events emitted during simulation or execution."""

    def __init__(self):
        """Initialize an empty timeline"""
        self._id = str(uuid.uuid4())
        self._domain_events: List[DomainEvent] = []
        self._transactions: Dict[str, Transaction] = {}
        self._signals: Dict[str, Signal] = {}
        self._entities: Dict[str, Entity] = {}

    @property
    def id(self) -> str:
        return self._id

    @property
    def domain_events(self) -> List[DomainEvent]:
        """Return the full list of recorded signal events."""
        return self._domain_events

    def entity(self, entity_id) -> Entity:
        """Look up an entity by ID."""
        return self._entities.get(entity_id)

    def signal(self, signal_id) -> Signal:
        """Look up a signal by ID."""
        return self._signals.get(signal_id)

    def transaction(self, transaction_id) -> Transaction:
        """Look up a transaction by ID."""
        return self._transactions.get(transaction_id)

    def __len__(self):
        """Return the number of recorded signal events."""
        return len(self.domain_events)

    def record(self, source: Entity, timestamp: float, event_type: str, signal: Signal, transaction=None,
               target: Optional[Entity] = None, tags: Optional[Dict[str, Any]] = None) -> DomainEvent:
        """Add a new signal event to the log and return it."""
        self._entities[source.id] = source
        self._signals[signal.id] = signal
        tx = transaction or signal.transaction
        if tx is not None:
            self._transactions[tx.id] = tx
        if target is not None:
            self._entities[target.id] = target

        domain_event = DefaultEvent(
            source_id=source.id,
            timestamp=timestamp,
            event_type=event_type,
            transaction_id=tx.id if tx else None,
            signal_id=signal.id,
            target_id=target.id if target else None,
            tags=tags,
            timeline=self
        )
        self._domain_events.append(domain_event)
        return domain_event

    def __iter__(self):
        """Iterate over all signal events in the log."""
        return iter(self._domain_events)

    @property
    def transactions(self) -> Iterable[tuple[str, Transaction]]:
        """All known transactions referenced in the log."""
        return self._transactions.items()

    @property
    def signals(self) -> Iterable[tuple[str, Signal]]:
        """All known signals referenced in the log."""
        return self._signals.items()

    @property
    def entities(self) -> Iterable[tuple[str, Entity]]:
        """All known entities that emitted or received signals."""
        return self._entities.items()

    def as_polars(self, with_entity_attributes=False, with_signal_attributes=False):
        """Convert the log into a Polars dataframe. Schema in source"""
        if not self._domain_events:
            return
        batch = [sig.as_dict() for sig in self._domain_events]
        df = pl.DataFrame(batch).cast(
            dtypes={
                "source_id": pl.Utf8,
                "timestamp": pl.Float64,
                "event_type": pl.Utf8,
                "transaction_id": pl.Utf8,
                "signal_id": pl.Utf8,
                "target_id": pl.Utf8,
                "tags": pl.Object,
            }
        )

        columns = []

        if with_entity_attributes:
            columns += [
                pl.col("source_id").map_elements(
                    lambda sid: self.entity(sid).name
                ).alias("source_name"),
                pl.col("target_id").map_elements(
                    lambda tid: self.entity(tid).name
                ).alias("target_name"),
            ]

        if with_signal_attributes:
            columns += [
                pl.col("signal_id").map_elements(
                    lambda sid: self.signal(sid).name
                ).alias("signal_name"),
                pl.col("signal_id").map_elements(
                    lambda sid: self.signal(sid).signal_type
                ).alias("signal_type"),
            ]

        if columns:
            df = df.with_columns(columns)

        return df

    def summarize(self, output: Literal["str", "dict"] = "str") -> Union[str, Dict[str, Union[int, float, str]]]:
        """Summary stats for the signal log."""
        df = self.as_polars()
        if df is None or df.is_empty():
            if output == "dict":
                return {
                    "log_entries": 0,
                    "time_span": 0.0,
                    "transactions": 0,
                    "entities": 0,
                    "signal_types": 0,
                    "signals": 0,
                    "avg_transaction_duration": 0.0,
                    "avg_signal_span": 0.0,
                }
            return "📊 Signal Log Summary\n  • No signals recorded."

        num_entries: int = df.height
        t_min: float = df["timestamp"].min()
        t_max: float = df["timestamp"].max()
        timespan: float = t_max - t_min

        num_transactions: int = df["transaction_id"].drop_nulls().unique().len()

        num_entities: int = df.select([
            df["source_id"],
            df["target_id"]
        ]).drop_nulls().unique().height

        num_signal_types = pl.Series([
            signal.signal_type for signal in self._signals.values()
        ]).unique().len()

        # 2. Count by signal_type
        signal_type_counts = pl.Series("signal_type", [
            signal.signal_type for signal in self._signals.values()
        ]).value_counts().sort("signal_type")

        signal_type_lines = "\n".join(
            f"    - {signal_type.ljust(10)}: {count}" for signal_type, count in signal_type_counts.rows()
        )

        num_signals: int = df["signal_id"].unique().len()

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

        signal_span = (
            df.group_by("signal_id")
            .agg([
                pl.col("timestamp").min().alias("t_start"),
                pl.col("timestamp").max().alias("t_end")
            ])
            .with_columns((pl.col("t_end") - pl.col("t_start")).alias("signal_duration"))
        )
        avg_signal_duration: float = signal_span["signal_duration"].mean()

        summary_dict: Dict[str, Union[int, float, str]] = {
            "log_entries": num_entries,
            "time_span": timespan,
            "start_time": t_min,
            "end_time": t_max,
            "transactions": num_transactions,
            "entities": num_entities,
            "signal_types": num_signal_types,
            "signal_type_count": signal_type_counts,
            "signals": num_signals,
            "avg_transaction_duration": avg_tx_duration,
            "avg_signal_span": avg_signal_duration,
        }

        if output == "dict":
            return summary_dict

        return (
            "📊 Signal Log Summary\n"
            f"  • Log entries       : {num_entries}\n"
            f"  • Time span         : {timespan:.3f} time units (from t={t_min:.3f} to t={t_max:.3f})\n"
            f"  • Transactions      : {num_transactions}\n"
            f"  • Avg Tx duration   : {avg_tx_duration:.3f}\n"
            f"  • Entities             : {num_entities}\n"
            f"  • Signal Types         : {num_signal_types}\n"
            f"{signal_type_lines}\n"
            f"  • Signals          : {num_signals}\n"
            f"  • Avg Signal duration   : {avg_signal_duration:.3f}"
        )

    def display(self):
        """Friendly display of the log, summary and detailed line entries."""
        summary = self.summarize()
        details = "\n".join([
            f"{sig.timestamp:.3f}: {sig.event_type}: {sig.source.name} , {sig.target.name if sig.target is not None else None} :: {sig.signal.signal_type} {sig.signal.name} ({sig.transaction.id[-8:] if sig.transaction else ' '})"
            for sig in self._domain_events
        ])
        return f"{summary}\n-------Detailed Log-----------\n{details}"

    def __str__(self):
        """Alias for `summarize()`."""
        return self.summarize()

    def __repr__(self):
        """Alias for `display()`."""
        return self.display()
