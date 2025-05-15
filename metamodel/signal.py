# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Protocol

from .transaction import Transaction
from .element import Element


class Signal(Element, Protocol):
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




