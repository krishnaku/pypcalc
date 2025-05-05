# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from __future__ import annotations
from typing import Optional
import polars as pl
from core import Entity

from core.signal_log import SignalLog, SignalEvent
from sim.runtime.simulation import Simulation


def sim_log(self: Simulation) -> SimulationLogAssertion:
    return SimulationLogAssertion(self)


class SimulationLogAssertion:
    def __init__(self, sim: Simulation):
        self.sim = sim
        self.all_logs = sim.all_logs

    def log_at(self, index):
        n = len(self.all_logs)
        assert -n <= index < n, f"index {index} out of range for simulation logs of length {n}"
        return SignalLogAssertion(self.all_logs[index])

    def latest_log(self) -> SignalLogAssertion:
        return self.log_at(-1)

    def __bool__(self) -> bool:
        return True  # all prior assertions passed, object is valid


def signal_log(log: SignalLog) -> SignalLogAssertion:
    return SignalLogAssertion(log)


class SignalLogAssertion:
    def __init__(self, log: SignalLog):
        self.log = log
        self.df: Optional[pl.DataFrame] = None

    def _lookup_node_id(self, source_name: str) -> Optional[str]:
        for id, node in self.log.nodes:
            if node.name == source_name:
                return id

    def has_length(self, expected: int) -> SignalLogAssertion:
        actual = len(self.log.signals)
        assert actual == expected, f"Expected {expected} signals, got {actual}"
        return self

    # note: tests look up everything by name of the nodes, enitities etc.
    def contains_signal(self, signal_type: str, source: str = None, target: str = None, count: int = None) -> SignalLogAssertion:
        if self.df is None:
            self.df = self.log.as_polars()

        filtered = self.df.filter(pl.col("signal") == signal_type)

        if source is not None:
            filtered = filtered.filter(pl.col("source_id") == self._lookup_node_id(source))

        if target is not None:
            filtered = filtered.filter(pl.col("target_id") == self._lookup_node_id(target))

        if count is not None:
            assert filtered.height == count, \
                f"Expected {count} '{signal_type}' signals (source={source}, target={target}), got {filtered.height}"
        else:
            assert filtered.height > 0, \
                f"No signals of type '{signal_type}' (source={source}, target={target}) found"

        return self

    def with_filter(self, **kwargs) -> SignalLogAssertion:
        if self.df is None:
            self.df = self.log.as_polars()

        for col, pattern in kwargs.items():
            self.df = self.df.filter(pl.col(col).cast(str).str.contains(pattern))
        return self

    # chain to signal assertions
    def signal_at(self, index: int) -> SignalAssertion:
        n = len(self.log.signals)
        assert -n <= index < n, f"index {index} out of range for signal of length {n}"
        return SignalAssertion(self.log.signals[index])

    def __bool__(self) -> bool:
        return True  # all prior assertions passed, object is valid


class SignalAssertion:
    def __init__(self, signal: SignalEvent):
        self.signal = signal

    def has_type(self, expected: str) -> SignalAssertion:
        assert self.signal.signal_type == expected, \
            f"Expected signal_type '{expected}', got '{self.signal.signal_type}'"
        return self

    def has_source(self, expected: str) -> SignalAssertion:
        assert self.signal.source.name == expected, \
            f"Expected source_id '{expected}', got '{self.signal.source.name}'"
        return self

    def has_target(self, expected: str) -> SignalAssertion:
        assert self.signal.target.name == expected, \
            f"Expected target_id '{expected}', got '{self.signal.target.name}'"
        return self

    def has_transaction(self, expected: str) -> SignalAssertion:
        assert self.signal.transaction_id == expected, \
            f"Expected transaction_id '{expected}', got '{self.signal.transaction_id}'"
        return self

    def has_signal(self, expected: str) -> SignalAssertion:
        assert self.signal.signal.name == expected, \
            f"Expected signal_id '{expected}', got '{self.signal.signal.name}'"
        return self

    def has_tag(self, key: str, value: str) -> SignalAssertion:
        tags = self.signal.tags or {}
        assert key in tags, f"Missing tag key '{key}'"
        actual_value = str(tags[key])
        assert actual_value == value, \
            f"Expected tag '{key}' to be '{value}', got '{actual_value}'"
        return self

    def has_timestamp_between(self, after: float, before: float) -> SignalAssertion:
        ts = self.signal.timestamp
        assert after < ts < before, \
            f"Expected timestamp between {after} and {before}, got {ts}"
        return self

    def describe(self):
        return {
            "type": self.signal.signal_type,
            "source": self.signal.source_id,
            "target": self.signal.target_id,
            "signal": self.signal.signal_id,
            "transaction": self.signal.transaction_id,
            "tags": self.signal.tags,
            "timestamp": self.signal.timestamp,
        }

    def __bool__(self) -> bool:
        return True  # all prior assertions passed, object is valid
