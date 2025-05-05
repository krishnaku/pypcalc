# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar
from typing import Protocol, runtime_checkable, Generator

@runtime_checkable
class Affordance(Protocol):
    """Base protocol for any signal-handling capability"""
    ...

@runtime_checkable
class Enter(Affordance, Protocol):
    """Accepts enter signals"""
    def enter(self, signal_id: str, **kwargs) -> Generator:...


@runtime_checkable
class Exit(Affordance, Protocol):
    """Accepts exit signals"""
    def exit(self, signal_id: str, **kwargs) -> Generator: ...

@runtime_checkable
class Perform(Affordance, Protocol):
    """Performs actions"""
    def perform(self, signal_id: str, **kwargs) -> Generator: ...

