# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT
"""
## Introduction

`TimeModel` is a calendar-aware utility that maps external `datetime` values
to continuous float time relative to a chosen origin and unit of measure.

The presence calculus operates over real time axis, and time is therefore
represented as a floating point value in all calculations.

To avoid working with arbitrarily large floating point numbers unnecessarily—which can
introduce interpretability or numerical precision issues—it is recommended
that you define an explicit origin for your time axis and express all time values
relative to this origin.

This model supports both fixed-duration units (e.g., 'seconds', 'minutes',
'days') and calendar-relative units (e.g., 'months', 'quarters', 'years').

`TimeModel` is most useful when interfacing with external timestamped data
sources—such as logs, CRM systems, or real-time feeds—where time is expressed
as absolute wall-clock timestamps.

In contrast, when working with synthetic or simulated data (e.g., from a
simulation engine), such translation is typically unnecessary, as the
simulation clock already provides floating point time relative to the start
of the simulation.

Parameters:
- origin: the reference `datetime` from which time is measured
- unit: one of 'seconds', 'minutes', 'hours', 'days', 'months', 'quarters', 'years'

### Examples

```python
from datetime import datetime
from pc.entity import Entity
from pc.presence import Presence
from pc.time import TimeModel

# Define a time model using seconds since midnight
time_model = TimeModel(origin=datetime(2025, 5, 1), unit="seconds")

# External datetime timestamps
start_time = datetime(2025, 5, 1, 9, 30)
end_time = datetime(2025, 5, 1, 10, 45)

# Convert to float using the time model
start = time_model.to_float(start_time)  # 34200.0
end = time_model.to_float(end_time)      # 38700.0

# Define domain entities
element = Entity(id="cust-001", name="Alice Chen", metadata={"type": "customer"})
boundary = Entity(id="seg-enterprise", name="Enterprise Segment")

# Create the presence assertion
presence = Presence(
    element=element,
    boundary=boundary,
    start=start,
    end=end,
    provenance="crm"
)

print(presence)
```
"""
from datetime import datetime, timedelta
from typing import Literal, Union
from dateutil.relativedelta import relativedelta

CalendarUnit = Literal["seconds", "minutes", "hours", "days", "months", "quarters", "years"]

class TimeModel:


    def __init__(self, origin: datetime, unit: CalendarUnit = "seconds"):
        self.origin = origin
        self.unit = unit

    def to_float(self, t: datetime) -> float:
        delta = t - self.origin
        seconds = delta.total_seconds()

        if self.unit == "seconds":
            return seconds
        if self.unit == "minutes":
            return seconds / 60.0
        if self.unit == "hours":
            return seconds / 3600.0
        if self.unit == "days":
            return delta.days + (delta.seconds / 86400.0)
        if self.unit == "months":
            return self._months_between(self.origin, t)
        if self.unit == "quarters":
            return self._months_between(self.origin, t) / 3.0
        if self.unit == "years":
            return self._months_between(self.origin, t) / 12.0

        raise ValueError(f"Unsupported time unit: {self.unit}")

    def from_float(self, t: float) -> datetime:
        if self.unit == "seconds":
            return self.origin + timedelta(seconds=t)
        if self.unit == "minutes":
            return self.origin + timedelta(minutes=t)
        if self.unit == "hours":
            return self.origin + timedelta(hours=t)
        if self.unit == "days":
            return self.origin + timedelta(days=t)
        if self.unit in {"months", "quarters", "years"}:
            months = {
                "months": int(round(t)),
                "quarters": int(round(t * 3)),
                "years": int(round(t * 12)),
            }[self.unit]
            return self.origin + relativedelta(months=+months)

        raise ValueError(f"Unsupported time unit: {self.unit}")

    @staticmethod
    def _months_between(d1: datetime, d2: datetime) -> float:
        """Return the number of calendar months between two dates, fractional."""
        rd = relativedelta(d2, d1)
        return rd.years * 12 + rd.months + (rd.days / 30.0)
