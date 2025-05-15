# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from typing import Any, Optional, Dict

import numpy as np
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt
from IPython.display import display, Markdown

def pd_display(df, **kwargs):
    text = df.to_string(**kwargs)
    display(Markdown(f'```\n{text}\n```'))

def estimate_limits(df, tail_frac=0.2):
    tail = df.tail(int(len(df) * tail_frac))
    return {
        "lambda_limit": tail["lambda"].mean(),
        "W_limit": tail["W"].mean(),
        "L_limit": tail["L"].mean(),
        "L_estimated": tail["lambda"].mean() * tail["W"].mean()
    }

# Convert Python types to Polars types
def map_polars_schema(annotations):
    type_map = {
        float: pl.Float64,
        str: pl.Utf8,
        dict: pl.Object,
        Any: pl.Object,
        Optional[str]: pl.Utf8,
        Optional[Dict[str, Any]]: pl.Object,
        Optional[dict]: pl.Object,
    }
    return {field: type_map.get(t, pl.Object) for field, t in annotations.items()}