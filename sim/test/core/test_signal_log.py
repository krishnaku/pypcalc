import numpy as np
import pytest
from typing import Optional, Dict, Any
from dataclasses import dataclass
import polars as pl

from core import Entity, Signal, Transaction
from core.signal_log import Timeline
from sim.test.mocks import MockEntity, MockSimulation
from core import Transaction


def create_mock_signal_log():

    log = Timeline()
    sim = MockSimulation()
    e1 = MockEntity(id="E1", name="Source", sim_context=sim)
    e2 = MockEntity(id="E2", name="Target", sim_context=sim)

    tx = Transaction(id="TX1")
    sig1 = Signal(name="Sig1", signal_type="request", transaction=tx)
    sig2 = Signal(name="Sig2", signal_type="response", transaction=tx)

    log.record(e1, 1.0, "send", sig1, tx, e2)
    log.record(e2, 2.0, "receive", sig1, tx, e1)
    log.record(e1, 3.0, "send", sig2, tx, e2)
    log.record(e2, 4.0, "receive", sig2, tx, e1)

    return log

def test_record_and_length():
    log = create_mock_signal_log()
    assert len(log) == 4

def test_entities_and_signals_tracking():
    log = create_mock_signal_log()
    assert len(dict(log.entities)) == 2
    assert len(dict(log.signals)) == 2
    assert len(dict(log.transactions)) == 1

def test_signal_event_properties():
    log = create_mock_signal_log()
    event = log.signal_events[0]
    assert event.source.name == "Source"
    assert event.target.name == "Target"
    assert event.signal.name == "Sig1"
    assert event.transaction.id == "TX1"

def test_as_polars_basic():
    log = create_mock_signal_log()
    df = log.as_polars()
    assert df.shape[0] == 4
    assert df.columns == ['source_id', 'timestamp', 'event_type', 'transaction_id', 'signal_id', 'target_id', 'tags']

def test_as_polars_with_entity_and_signal_attrs():
    log = create_mock_signal_log()
    df = log.as_polars(with_entity_attributes=True, with_signal_attributes=True)
    for column in ['source_name', 'target_name', 'signal_name', 'signal_type']:
        assert column in df.columns

    assert set(df["source_name"].unique().to_list()) == {"Source", "Target"}

def test_summarize_str_output():
    log = create_mock_signal_log()
    summary = log.summarize()
    assert isinstance(summary, str)
    assert "Signal Log Summary" in summary

def test_summarize_dict_output():
    log = create_mock_signal_log()
    summary = log.summarize(output="dict")
    assert isinstance(summary, dict)
    assert summary["log_entries"] == 4
    assert summary["transactions"] == 1
    assert summary["entities"] == 2
    assert summary["signal_types"] == 2
    assert summary["signals"] == 2
    assert summary["avg_transaction_duration"] > 0
    assert summary["avg_signal_span"] > 0

def test_display_formatting():
    log = create_mock_signal_log()
    display = log.display()
    assert display == """📊 Signal Log Summary
  • Log entries       : 4
  • Time span         : 3.000 time units (from t=1.000 to t=4.000)
  • Transactions      : 1
  • Avg Tx duration   : 3.000
  • Entities             : 2
  • Signal Types         : 2
    - request   : 1
    - response  : 1
  • Signals          : 2
  • Avg Signal duration   : 1.000
-------Detailed Log-----------
1.000: send: Source , Target :: request Sig1 (TX1)
2.000: receive: Target , Source :: request Sig1 (TX1)
3.000: send: Source , Target :: response Sig2 (TX1)
4.000: receive: Target , Source :: response Sig2 (TX1)"""

def test_empty_log_summary_and_display():

    log = Timeline()
    assert log.summarize(output="dict")["log_entries"] == 0
    assert "No signals recorded" in log.summarize()
    assert "No signals recorded" in log.display()
