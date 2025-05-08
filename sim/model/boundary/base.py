# -*- coding: utf-8 -*-

# Copyright: © Exathink, LLC 2016-2015-${today.year} All Rights Reserved

# Unauthorized use or copying of this file and its contents, via any medium
# is strictly prohibited. The work product in this file is proprietary and
# confidential.

# Author: Krishna Kumar

from typing import Dict, Any, Optional, Set, List, Callable, Tuple

from abc import ABC, abstractmethod
from collections import defaultdict

import numpy as np

from core import Boundary, SignalEvent, Signal
from core.signal_log import  Timeline, SignalEventListener
from core.presence import Presence, PresenceMatrix
from sim.runtime.simulation import Simulation

class BoundaryBase(Boundary, SignalEventListener, ABC):
    def __init__(self, kind, name, enter_event: str, exit_event: str, config: Dict[str,Any], sim_context: Simulation, id:Optional[str]=None ):
        super().__init__(kind, name, config, sim_context, id)

        self._signal_log: Timeline = Timeline()
        self._sim_context = sim_context
        self._enter_event = enter_event
        self._exit_event = exit_event

        self._sim_context.register_listener(self)

    @property
    def signal_log(self) -> Timeline:
        return self._signal_log

    def get_presence_matrix(self, start_time: float, end_time: float, bin_width: float, match: Optional[Callable[[SignalEvent], bool]] = None) -> PresenceMatrix:
        presences = self.extract_presences(start_time, end_time, match)
        return PresenceMatrix(presences=presences,t0=start_time, t1=end_time, bin_width=bin_width)

    def extract_presences(self, t0, t1, match: Optional[Callable[[SignalEvent], bool]] = None) -> List[Presence]:
        signal_events = self.signal_log.signal_events
        enter_event = self._enter_event
        exit_event = self._exit_event

        if match is not None:
             signal_events = filter(match, signal_events)

        signal_events = sorted(signal_events, key=lambda s: s.timestamp)

        presences: List[Presence] = []
        open_presences: Dict[str, Presence] = {}

        for e in signal_events:
            # Once we hit t1, we don't care about later events
            if e.timestamp > t1:
                break

            if e.event_type == enter_event:
                # clip the presence so that it never starts before t0.
                presence = Presence(signal=e.signal, start=max(e.timestamp, t0), end=np.inf)
                open_presences[e.signal_id] = presence

            elif e.event_type == exit_event:
                presence = open_presences.pop(e.signal_id, None)
                if presence:
                    presence.end = e.timestamp
                    # If it ends within window, include it
                    if presence.end >= t0:
                        presences.append(presence)
                else:
                    # Exit without entry: assume it was open from time t0
                    presence = Presence(signal=e.signal, start=t0, end=e.timestamp)
                    presences.append(presence)

        # After scan, extract presences open at t0 but not exited
        for sid, presence in open_presences.items():
            # clip the presence to end at t1.
            presence.end = t1
            presences.append(presence)

        return presences



    @abstractmethod
    def on_signal_event(self, event: SignalEvent) -> None:...