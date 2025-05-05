# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from typing import Protocol, Dict, Any

class Entity(Protocol):
    """Marker protocol for a concrete system component."""
    @property
    def id(self) -> str:...

    @property
    def name(self) -> str:...


    @property
    def metadata(self) -> Dict[str, Any]: ...