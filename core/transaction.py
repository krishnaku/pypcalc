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


@dataclass
class Transaction:
    id: str  # UUID or hash
    parent: Optional[Transaction] = None

    def __init__(self, id: Optional[str]=None, parent: Optional[Transaction]=None):
        self.id = id or str(uuid.uuid4())
        self.parent = parent

