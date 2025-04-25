# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
import uuid
from typing import Protocol, Optional

class Node(Protocol):
    """Marker protocol for a concrete system component."""
    @property
    def id(self) -> str:...

    @property
    def name(self) -> str:...

class NodeImpl(Node):
    """Marker implementation for a concrete system component."""
    def __init__(self, name, id:Optional[str]=None) -> None:
        self._id: str =str(uuid.uuid4()) if id is None else id
        self._name: str = name

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name
