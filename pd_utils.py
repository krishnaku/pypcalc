# Auto-generated module

import numpy as np
import pandas as pd
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