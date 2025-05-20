# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Optional, Protocol

from pcalc.element import Element


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




