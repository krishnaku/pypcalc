# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from typing import Protocol, Dict, Any, Optional


from .node import Node
class Signal(Protocol):
    """Marker protocol for a concrete Signals."""

    """The node sending the signal"""
    def source(self) -> Node: ...
    """The target of the signal (optional)"""
    def target(self) -> Optional[Node]: ...
    """The name of the signal"""
    def name(self) -> str: ...
    """The timestamp of the signal"""
    def timestamp(self) -> float: ...
    """The id of the entity attached to the signal"""
    def subject(self)->Optional[str]: ...

    """Any additional metadata attached to the signal"""
    def tags(self) -> Optional[Dict[str, Any]]: ...

