# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from matplotlib import cm
from collections import Counter

def plot_accumulation_trajectories(accum_matrix,filename='trajectories.png'):
    """
    Plot presence‐density trajectories along each diagonal of an upper‐triangular matrix.
    - Includes every diagonal d=0…n-1 as valid sample paths (even single‐point).
    - For d>0, splits into non‐overlapping trajectories by stepping in strides of d.
    - Assigns each trajectory its own color (colors reset per diagonal).
    """
    n = accum_matrix.shape[0]
    fig, ax = plt.subplots(figsize=(10, 7))

    for d in range(n):
        # 1) Gather all values on diagonal d for incidence
        diag_vals = [
            accum_matrix[i, i + d]
            for i in range(n - d)
            if np.isfinite(accum_matrix[i, i + d])
        ]
        if len(diag_vals) == 0:
            continue

        # 2) Incidence count per distinct density
        freq = Counter(diag_vals)

        # 3) Build trajectory list
        traj_list = []
        if d == 0:
            # main diagonal is one trajectory
            traj_list = [diag_vals]
        else:
            # non‐overlapping sliding windows of width d
            for start in range(d):
                traj = []
                idx = start
                while idx + d < n:
                    val = accum_matrix[idx, idx + d]
                    if np.isfinite(val):
                        traj.append(val)
                    idx += d
                if len(traj) >= 1:
                    traj_list.append(traj)

        # 4) Plot each trajectory with its own color
        cmap = cm.get_cmap('tab10', len(traj_list))
        for t_idx, traj in enumerate(traj_list):
            color = cmap(t_idx)
            y = np.full(len(traj), d)
            x = traj
            sizes = [freq[v] * 20 for v in traj]

            # plot the points
            ax.scatter(x, y, s=sizes, color=color, marker='o', zorder=3)

            # if more than one point, connect with arrows
            if len(x) > 1:
                for k in range(len(x) - 1):
                    arrow = FancyArrowPatch(
                        (x[k],   d),
                        (x[k+1], d),
                        connectionstyle="arc3,rad=0.25",
                        arrowstyle='-|>',
                        color=color,
                        mutation_scale=10,
                        lw=1.5,
                        alpha=0.8
                    )
                    with np.errstate(over='ignore', invalid='ignore'):
                        ax.add_patch(arrow)


    ax.set_xlabel("Presence Density (δ)")
    ax.set_ylabel("Interval Length (Diagonal Index)")
    ax.set_title("Signal Trajectories by Interval Length")
    ax.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()






