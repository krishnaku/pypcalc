# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm
import numpy as np

# Reconstructing the full triangular matrix of presence density values
# Each entry is (density, incidence)
presence_data = [
    [(1.34, 1), (0.98, 2), (1.70, 3), (1.99, 4), (2.27, 5), (2.55, 4), (2.43, 3), (2.60, 2), (2.74, 2), (2.80, 1)],
    [None, (1.29, 1), (1.67, 2), (1.90, 3), (2.18, 4), (2.47, 3), (2.36, 2), (2.54, 2), (2.68, 2), (2.74, 1)],
    [None, None, (1.57, 1), (1.61, 2), (1.90, 3), (2.24, 2), (2.19, 2), (2.38, 2), (2.53, 2), (2.60, 1)],
    [None, None, None, (1.21, 1), (1.35, 2), (1.81, 3), (1.87, 2), (2.11, 2), (2.29, 2), (2.36, 1)],
    [None, None, None, None, (1.28, 1), (1.55, 2), (1.68, 2), (1.93, 2), (2.12, 2), (2.20, 1)],
    [None, None, None, None, None, (1.43, 1), (1.50, 2), (1.72, 2), (1.92, 2), (1.99, 1)],
    [None, None, None, None, None, None, (1.53, 1), (1.44, 2), (1.62, 2), (1.68, 1)],
    [None, None, None, None, None, None, None, (1.35, 1), (1.45, 2), (1.53, 1)],
    [None, None, None, None, None, None, None, None, (1.23, 1), (1.28, 1)],
    [None, None, None, None, None, None, None, None, None, (0.71, 1)]
]

n = len(presence_data)

# Prepare color map for different diagonals
colors = cm.get_cmap('tab10', n)

fig, ax = plt.subplots(figsize=(10, 7))

# Plot each diagonal as a trajectory on its own horizontal line
for diag in range(n):
    trajectories = []
    for start in range(n - diag):
        i, j = start, start + diag
        if presence_data[i][j] is not None:
            trajectories.append((presence_data[i][j][0], presence_data[i][j][1]))  # (density, incidence)

    if len(trajectories) < 2:
        continue

    color = colors(diag)
    ys = np.full(len(trajectories), diag)
    xs = [pt[0] for pt in trajectories]
    sizes = [pt[1]*20 for pt in trajectories]

    # Plot points
    ax.scatter(xs, ys, s=sizes, marker='o', color=color, zorder=3)

    # Draw curved paths (quadratic Bézier approximations)
    for k in range(len(xs) - 1):
        x0, y0 = xs[k], ys[k]
        x1, y1 = xs[k+1], ys[k+1]
        xm, ym = (x0 + x1)/2, y0 + 0.2 + 0.05 * diag  # slight vertical curve

        path = patches.FancyArrowPatch((x0, y0), (x1, y1),
                                       connectionstyle=f"arc3,rad=0.25",
                                       arrowstyle='-|>',
                                       color=color,
                                       mutation_scale=10,
                                       lw=1)
        ax.add_patch(path)

ax.set_xlabel("Presence Density")
ax.set_ylabel("Interval Length (Diagonal Index)")
ax.set_title("Signal Trajectories by Interval Length")
ax.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()

