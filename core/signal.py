# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from .transaction import Transaction
from .element import Element

@dataclass
class Signal(Element):
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

    # Element implementation
    _id: str = field(default_factory=lambda: str(uuid.uuid4()))


    @property
    def id(self) -> str:
        """The unique ID of the signal (auto-assigned)."""
        return self._id


