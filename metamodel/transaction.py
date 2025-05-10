# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved
# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from __future__ import annotations

import uuid
from typing import Optional, Protocol

from .element import Element


class Transaction(Element, Protocol):
    """
    Represents a transactional context for a signal or series of signal exchanges.

    Transactions allow related elements to be grouped under a shared identifier.
    This is useful for correlating causally linked signals (e.g., a request and its response),
    or tracking nested operations in more complex protocols.

    Transactions can be nested via the `parent` field to support hierarchical relationships

    ```
    """

    parent: Optional["Transaction"] = None  # Optional parent transaction for nesting




