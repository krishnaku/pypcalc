# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved
# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from __future__ import annotations
import uuid
from typing import Optional
from dataclasses import dataclass


from dataclasses import dataclass
from typing import Optional
import uuid

@dataclass
class Transaction:
    """
    Represents a transactional context for a signal or series of signal exchanges.

    Transactions allow related signals to be grouped under a shared identifier.
    This is useful for correlating causally linked events (e.g., a request and its response),
    or tracking nested operations in more complex protocols.

    Transactions can be nested via the `parent` field to support hierarchical relationships.

    Signal flow metrics at the transaction level are often the bridge between operational flow metrics
    and business outcomes.

    ### Example

    ```python
    tx = Transaction()
    sig1 = Signal(name="Sig1", signal_type="request", transaction=tx)
    sig2 = Signal(name="Sig2", signal_type="response", transaction=tx)

    ```
    """

    id: str  # UUID or hash identifying the transaction
    parent: Optional["Transaction"] = None  # Optional parent transaction for nesting

    def __init__(self, id: Optional[str] = None, parent: Optional["Transaction"] = None):
        """
        Create a new transaction.

        Args:
            id: Optional explicit transaction ID (e.g., UUID or hash). If not provided, one is generated.
            parent: Optional parent transaction to support nesting or chaining.
        """
        self.id = id or str(uuid.uuid4())
        self.parent = parent
