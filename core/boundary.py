# -*- coding: utf-8 -*-
# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from __future__ import annotations

from typing import List, Protocol, TYPE_CHECKING

from .presence_matrix import Visit, PresenceMatrix

if TYPE_CHECKING:
    pass

from .signal_log import SignalLog
from .entity import Entity

class Boundary(Entity, Protocol):

    @property
    def signal_log(self) -> SignalLog:...

    def get_presence_matrix(self, start_time: float, end_time: float, bin_width: float) -> PresenceMatrix:...



