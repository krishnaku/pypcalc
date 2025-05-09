# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved
# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.
# Author: Krishna Kumar

from typing import Protocol, TypeVar

T_Element = TypeVar('T_Element', bound='Element')

class Element(Protocol):
    """Identifiable members of a domain."""

    @property
    def id(self) -> str:
        """A stable unique identifier for the element (used for indexing and lookup)."""
        ...
