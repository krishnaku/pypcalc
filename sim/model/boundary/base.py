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
from core.signal_log import  SignalLog, SignalEventListener
from core.presence import Visit, PresenceMatrix
from sim.runtime.simulation import Simulation

class BoundaryBase(Boundary, SignalEventListener, ABC):
    def __init__(self, kind, name, enter_event: str, exit_event: str, config: Dict[str,Any], sim_context: Simulation, id:Optional[str]=None ):
        super().__init__(kind, name, config, sim_context, id)

        self._signal_log: SignalLog = SignalLog()
        self._sim_context = sim_context
        self._enter_event = enter_event
        self._exit_event = exit_event

        self._sim_context.register_listener(self)

    @property
    def signal_log(self) -> SignalLog:
        return self._signal_log

    def get_presence_matrix(self, start_time: float, end_time: float, bin_width: float, match: Optional[Callable[[SignalEvent], bool]] = None) -> PresenceMatrix:
        visits = self.extract_visits(start_time, end_time, match)
        return PresenceMatrix(visits=visits,t0=start_time, t1=end_time, bin_width=bin_width)

    def extract_visits(self, t0, t1, match: Optional[Callable[[SignalEvent], bool]] = None) -> List[Visit]:
        signals = self.signal_log.signal_events
        enter_event = self._enter_event
        exit_event = self._exit_event

        if match is not None:
             signals = filter(match, signals)

        signals = sorted(signals, key=lambda s: s.timestamp)

        visits: List[Visit] = []
        signal_visits: Dict[str, List[Visit]] = defaultdict(list)
        open_visits: Dict[str, Visit] = {}


        for s in signals:
            if s.event_type == enter_event:
                visit = Visit(signal_id=s.signal_id, start=s.timestamp, end=np.inf)
                open_visits[s.signal_id] = visit

                # Track visit if it starts within window
                if t0 <= s.timestamp <= t1:
                    visits.append(visit)
                    signal_visits[s.signal_id].append(visit)

            elif s.event_type == exit_event:
                visit = open_visits.pop(s.signal_id, None)
                if visit:
                    visit.end = s.timestamp

                    # If it ends within window, include it
                    if visit.start < t1 and s.timestamp >= t0:
                        visits.append(visit)
                        signal_visits[s.signal_id].append(visit)
                else:
                    # Exit without entry: assume it was open from time 0
                    visit = Visit(signal_id=s.signal_id, start=0, end=s.timestamp)
                    if s.timestamp >= t0:
                        visits.append(visit)
                        signal_visits[s.signal_id].append(visit)

            # Once we hit t1, we don't care about later events
            if s.timestamp > t1:
                break

        # After scan, extract visits open at t0 (entered before t0, not exited)
        for sid, visit in open_visits.items():
            if visit.start < t0:
                # Also record the open visit for presence accounting
                visits.append(visit)
                signal_visits[sid].append(visit)

        return visits



    @abstractmethod
    def on_signal_event(self, event: SignalEvent) -> None:...