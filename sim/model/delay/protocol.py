# -*- coding: utf-8 -*-
from typing import Generator

import simpy

from core import Behavior


# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
class DelayBehavior(Behavior):
    def delay(self) -> Generator[simpy.Event, None, None]:...
