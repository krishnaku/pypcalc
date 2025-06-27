# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT
import numpy as np
import pandas as pd
from flow_field_viz import compute_presence_invariant, compute_polar_representation, plot_flow_field
from attractors import plot_accumulation_trajectories
# Logistic map definition
def logistic_map(r, x0, n):
    x = np.zeros(n)
    x[0] = x0
    for t in range(1, n):
        x[t] = r * x[t - 1] * (1 - x[t - 1])
    return x

# Parameters for intermittent regime
r = 3.4
x0 = 0.5
n = 20

# Generate time series
x = logistic_map(r, x0, n)

# Construct presence matrix for intervals of length 1
interval_starts = np.arange(n - 1)
interval_ends = interval_starts + 1
presence_mass = x[interval_starts]  # f(j, j+1) = x[j]

presence_matrix = np.array([presence_mass])
delta, iota, avg_mass = compute_presence_invariant(presence_matrix)
magnitude, theta = compute_polar_representation(iota, avg_mass)

plot_flow_field(magnitude,theta)
plot_accumulation_trajectories(delta)