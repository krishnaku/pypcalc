# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from sim.metamodel import Transaction


@dataclass
class DefaultTransaction(Transaction):
    """
    Represents a transactional context for a signal or series of signal exchanges.

    Transactions allow related signals to be grouped under a shared identifier.
    This is useful for correlating causally linked events (e.g., a request and its response),
    or tracking nested operations in more complex protocols.

    Transactions can be nested via the `parent` field to support hierarchical relationships.


    ```
    """

    parent: Optional["Transaction"] = None  # Optional parent transaction for nesting

    def __init__(self, parent: Optional["Transaction"] = None):
        """
        Create a new transaction.

        Args:
            id: Optional explicit transaction ID (e.g., UUID or hash). If not provided, one is generated.
            parent: Optional parent transaction to support nesting or chaining.
        """
        self._id = str(uuid.uuid4())
        self._parent = parent

    @property
    def id(self) -> str:
        return self._id