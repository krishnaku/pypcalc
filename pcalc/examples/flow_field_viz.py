# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

import numpy as np
import matplotlib
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.cm as cm

from matplotlib.colors import ListedColormap, BoundaryNorm
from attractors import plot_accumulation_trajectories

def plot_flow_field(magnitude, theta, filename='flow_field.png'):
    rows, cols = magnitude.shape
    # Step 1: Find max magnitude to normalize arrow length
    max_r = np.nanmax([
        magnitude[i, j]
        for i in range(cols)
        for j in range(i, cols)
        if not np.isnan(magnitude[i, j])
    ])

    # Step 2: Generate scaled arrows centered in bands
    band_height = 1.0
    max_arrow_length = band_height * 0.9  # max arrow length in y-direction
    arrows = []
    for i in range(cols):
        for j in range(i, cols):
            r = magnitude[i, j]
            a = theta[i, j]
            if not np.isnan(r) and not np.isnan(a):
                duration = j - i
                y = duration + 0.5  # center of band
                x = i + duration / 2  # center horizontally

                scale = max_arrow_length / max_r
                dx = r * np.cos(a) * scale
                dy = r * np.sin(a) * scale

                arrows.append((x, y, dx, dy))




    fig, ax = plt.subplots(figsize=(8, 10))
    for x, y, dx, dy in arrows:
        ax.arrow(x, y, dx, dy, head_width=0.1, head_length=0.15, fc='black', ec='black', length_includes_head=True)

    # Determine number of rows (interval lengths)
    max_y = int(max(y for (_, y, _, _) in arrows)) + 1

    cmap = plt.colormaps.get_cmap('viridis')
    alpha=0.25
    # 1. Discretize the colormap into max_y + 1 bins
    colors_list = cmap(np.linspace(0, 1, max_y + 1))
    colors_list[:, -1] = alpha  # set alpha for all entries
    discrete_cmap = ListedColormap(colors_list)
    bounds = np.arange(max_y + 2) - 0.5  # e.g., [-0.5, 0.5, ..., 9.5]
    discrete_norm = BoundaryNorm(bounds, discrete_cmap.N)

    # 2. Draw bands using the discrete colormap
    for y_band in range(max_y + 1):
        color = discrete_cmap(y_band)
        ax.axhspan(y_band - 0.5, y_band + 0.5, facecolor=color, alpha=alpha, zorder=0)

    # 3. Colorbar using the same cmap and norm
    sm = cm.ScalarMappable(cmap=discrete_cmap, norm=discrete_norm)
    sm.set_array([])

    cbar = plt.colorbar(sm, ax=ax, pad=0.01, aspect=10, shrink=0.4)
    cbar.set_label('Observation Window Length', rotation=270, labelpad=10)
    cbar.set_ticks(np.arange(0, max_y + 1))
    # Layout
    ax.set_aspect('equal')
    ax.hlines(y=np.arange(max_y + 1), xmin=-0.5, xmax=cols - 0.5, color='white', linewidth=0.5, alpha=0.4)
    ax.set_xlim(-0.5, cols)
    ax.set_ylim(-0.5, max_y + 0.5)
    ax.set_xticklabels([])
    ax.tick_params(axis='x', which='both', length=0)
    ax.set_xlabel("Observation windows")
    ax.yaxis.set_visible(False)
    ax.set_title("Flow Field Visualization")

    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()




def compute_presence_invariant(presence_matrix):
    rows, cols = presence_matrix.shape
    accumulation_matrix = np.zeros((cols, cols))

    for i in range(cols):
        for j in range(i, cols):
            accumulation_matrix[i, j] = presence_matrix[:, i:j+1].sum()

    # SECTION 3: Compute Incidence Count Matrix
    incidence_matrix = np.zeros((cols, cols))
    for i in range(cols):
        for j in range(i, cols):
            submatrix = presence_matrix[:, i:j+1]
            incidence_matrix[i, j] = np.count_nonzero(np.any(submatrix > 0, axis=1))

    # SECTION 4: Compute iota, bar_m, and presence density delta
    iota = np.zeros_like(incidence_matrix)
    avg_mass = np.zeros_like(accumulation_matrix)
    delta = np.zeros_like(accumulation_matrix)

    # Loop to compute iota (incidence rate)
    for i in range(cols):
        for j in range(i, cols):
            T = j - i + 1  # window length
            if T > 0:
                iota[i, j] = incidence_matrix[i, j] / T

    # Loop to compute avg_mass (average mass per incidence)
    for i in range(cols):
        for j in range(i, cols):
            if incidence_matrix[i, j] > 0:
                avg_mass[i, j] = accumulation_matrix[i, j] / incidence_matrix[i, j]

    # Loop to compute delta (presence density)
    for i in range(cols):
        for j in range(i, cols):
            T = j - i + 1
            if T > 0:
                delta[i, j] = accumulation_matrix[i, j] / T

    return delta, iota, avg_mass

def compute_polar_representation(iota, avg_mass):
    # SECTION 5: Compute log values, magnitude and angle
    log_iota = np.log(iota, where=iota > 0, out=np.full_like(iota, np.nan))
    log_avg_mass = np.log(avg_mass, where=avg_mass > 0, out=np.full_like(avg_mass, np.nan))

    magnitude = np.sqrt(log_iota**2 + log_avg_mass**2)
    theta = np.arctan2(log_avg_mass, log_iota)

    return magnitude, theta

def show_html_table(magnitude, theta, digits=2, filename="polar_matrix.html"):
    cols = magnitude.shape[1]

    data = []
    for i in range(cols):
        row = []
        for j in range(cols):
            if i <= j:
                val = f"{magnitude[i,j]:.{digits}f} ∠ {theta[i,j]:.{digits}f}"
                diag_index = j - i
                diag_color = '#eef' if diag_index % 2 == 0 else '#ddf'
                style = f'style="background-color: {diag_color};"'
                cell = f'<td {style}>{val}</td>'
            else:
                cell = '<td></td>'
            row.append(cell)
        data.append(row)

    col_headers = ''.join([f'<th>{j+1}</th>' for j in range(cols)])

    html = f'''
    <div style="text-align: center; margin: 2em">
      <table style="border-collapse: collapse; margin: auto; font-family: serif; font-size: 0.95em;">
        <thead>
          <tr><th>i\\j</th>{col_headers}</tr>
        </thead>
        <tbody>
    '''

    for i, row in enumerate(data):
        html += f'<tr><td><b>{i+1}</b></td>' + ''.join(row) + '</tr>\n'

    html += '''
        </tbody>
      </table>
    </div>
    '''

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)




if __name__ == '__main__':
    # SECTION 1: Presence Matrix (given)
    presence_matrix_a = np.array([
        [0.3, 2.3, 3.4, 1.1, 2.9, 3.2, 1.1, 0.0, 0.0, 0.0],  # e1_b1
        [0.3, 2.3, 3.4, 1.1, 0.0, 1.1, 2.2, 2.4, 2.3, 0.8],  # e1_b2
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 1.8, 3.2, 0.9],  # e2_b2
        [0.8, 1.3, 2.4, 2.8, 3.0, 3.2, 3.4, 2.4, 0.0, 0.0],  # e2_b1
    ])

    presence_matrix_b = np.array([
        [0.3, 2.3, 3.4, 1.1, 2.9, 3.2, 1.1, 0.0, 0.0, 0.0],  # e1_b1
        [0.3, 2.3, 3.4, 1.1, 0.0, 1.1, 2.2, 2.4, 2.3, 0.8],  # e1_b2
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 1.8, 3.2, 0.9],  # e2_b2
        [0.8, 1.3, 2.4, 2.8, 3.0, 3.2, 3.4, 2.4, 0.0, 0.0],  # e2_b1
    ])

    presence_matrix = presence_matrix_a

    delta, iota, avg_mass = compute_presence_invariant(presence_matrix)
    magnitude, theta = compute_polar_representation(iota, avg_mass)

    show_html_table(magnitude, theta)

    plot_flow_field(magnitude,theta)

    # plot_accumulation_trajectories(delta)