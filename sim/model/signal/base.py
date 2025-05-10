# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

from metamodel import Signal, Transaction

from sim.model.element import ElementBase
from sim.model.transaction import DefaultTransaction

@dataclass
class SignalBase(ElementBase, Signal):
    """
    Signals represent information flows between entities in a domain.

    A signal is a named message or unit of communication, optionally tied to a transaction
    and carrying a payload of metadata. Each signal has a unique ID, a type (e.g., request, response),
    and optional metadata that may be acted on by entities in the domain.
    """
    name: str
    """The name of the signal (e.g., "GET", "ACK", "CommitRequest")."""

    signal_type: str
    """A label categorizing the signal (e.g., "request", "response")"""

    payload: Dict[str, Any] = field(default_factory=dict)
    """Optional key-value data payload carried with the signal."""

    transaction: Optional[Transaction] = None
    """An optional reference to a transaction object that this signal is part of."""

    def __init__(self, name:str, signal_type:str, payload: Dict[str, Any]=None, transaction: Optional[Transaction]=None) -> None:
        super().__init__()
        self.name = name
        self.signal_type = signal_type
        self.payload = payload
        self.transaction = transaction if transaction is not None else DefaultTransaction()

