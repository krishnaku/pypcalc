from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
from core import SignalEvent


@dataclass
class Visit:
    entity_id: str
    start: float
    end: float
    presence_row: int = -1
    start_bin: int = -1
    end_bin: int = -1

    def overlaps(self, t0: int, t1: int) -> bool:
        return self.start < t1 and self.end > t0

    def duration(self) -> float:
        return self.end - self.start


class PresenceMatrix:
    def __init__(
        self,
        queue_name: str,
        t0: float,
        t1: float,
        enter_event: str,
        exit_event: str,
        presence: np.ndarray,
        entity_visits: Dict[str, List[Visit]],
        visits: List[Visit],
        time_bins: np.ndarray,
        bin_width: float
    ):
        self.queue_name = queue_name
        self.t0 = t0
        self.t1 = t1
        self.enter_event = enter_event
        self.exit_event = exit_event
        self.entity_visits = entity_visits
        self.visits = visits
        self.presence = presence
        self.time_bins = time_bins
        self.bin_width = bin_width

    @classmethod
    def from_signals(
        cls,
        signals: List[SignalEvent],
        source: str,
        t0: float,
        t1: float,
        bin_width: float = 1.0,
        enter_event: str = "enter",
        exit_event: str = "exit",
        initial_population: Optional[List[str]] = None,
    ):


        # Filter for 'enter' and 'exit' events for the specified source
        entity_visits, visits = cls.extract_visits(signals, source, t0, t1, enter_event, exit_event, initial_population)

        presence, time_bins = cls.map_presence(visits, t0, t1, bin_width)

        return cls(
            queue_name=source,
            t0=t0,
            t1=t1,
            enter_event=enter_event,
            exit_event=exit_event,
            presence=presence,
            entity_visits=entity_visits,
            visits=visits,
            time_bins=time_bins,
            bin_width=bin_width,
        )

    @classmethod
    def extract_visits(cls, signals, source, t0, t1, enter_event, exit_event, initial_population ):
        filtered = [s for s in signals if
                    s.signal_type in {enter_event, exit_event} and s.source == source and t0 <= s.timestamp <= t1]
        visits: List[Visit] = []
        entity_visits: Dict[str, List[Visit]] = defaultdict(list)
        for entity_id in initial_population or []:
            visit = Visit(entity_id=entity_id, start=0, end=np.inf)
            visits.append(visit)
            entity_visits[entity_id].append(visit)
        for s in sorted(filtered, key=lambda s: s.timestamp):
            if s.signal_type == enter_event:
                visit = Visit(entity_id=s.entity_id, start=s.timestamp, end=np.inf)
                visits.append(visit)
                entity_visits[s.entity_id].append(visit)
            if s.signal_type == exit_event:
                visit_list = entity_visits[s.entity_id]
                latest: Visit = visit_list[-1] if len(visit_list) > 0 else None
                if latest is not None:
                    latest.end = s.timestamp
                else:
                    visit = Visit(entity_id=s.entity_id, start=0, end=s.timestamp)
                    visits.append(visit)
                    entity_visits[s.entity_id].append(visit)
        return entity_visits, visits

    @classmethod
    def map_presence(cls, visits, t0, t1, bin_width):
        time_bins = np.arange(t0, t1 + bin_width, bin_width)
        num_bins = len(time_bins) - 1
        num_rows = len(visits)
        # Initialize presence matrix
        presence = np.zeros((num_rows, num_bins), dtype=int)
        for i, visit in enumerate(visits):
            visit.presence_row = i

            # Clip start and end to t0 and t1 bounds
            effective_start = max(visit.start, t0)
            effective_end = min(visit.end, t1)

            # Convert to bin indices
            start_bin = int((effective_start - t0) // bin_width)
            end_bin = int((effective_end - t0) // bin_width)

            # Clamp to matrix bounds
            if end_bin > start_bin:
                presence[i, start_bin:end_bin] = 1
            visit.start_bin = start_bin
            visit.end_bin = end_bin

            # Fill presence matrix and update visit metadata
            presence[i, start_bin:end_bin] = 1
            visit.start_bin = start_bin
            visit.end_bin = end_bin
        return presence, time_bins
