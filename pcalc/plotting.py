# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from .pd_utils import estimate_limits


def plot_residence_time_convergence(presence, arrival_index, visit_index):
    T = presence.shape[1]
    data = []
    for t in range(1, T):
        op_metrics = compute_operator_flow_metrics(presence, arrival_index, visit_index, 0, t)
        ent_metrics = compute_signal_flow_metrics(presence, arrival_index, visit_index, 0, t)
        data.append({'window_end': t, 'W_operator': op_metrics['W'], 'W_signal': ent_metrics['W']})
    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))
    plt.plot(df['window_end'], df['W_operator'], label='Operator Perspective W', linewidth=2)
    plt.plot(df['window_end'], df['W_signal'], label='Entity Perspective W', linewidth=2, linestyle='--')
    plt.xlabel('Window End Time')
    plt.ylabel('Average Residence Time (W)')
    plt.title('Convergence of Residence Time from Operator and Entity Perspectives')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return df


def plot_tail_convergence_of_residence_time(presence, arrival_index, visit_index, tail_frac=0.2):
    T = presence.shape[1]
    data = []
    for t in range(1, T):
        op_metrics = compute_operator_flow_metrics(presence, arrival_index, visit_index, 0, t)
        ent_metrics = compute_signal_flow_metrics(presence, arrival_index, visit_index, 0, t)
        data.append({'window_end': t, 'W_operator': op_metrics['W'], 'W_signal': ent_metrics['W']})
    df = pd.DataFrame(data)
    tail_deltas = []
    for i in range(1, len(df)):
        tail_size = max(1, int(tail_frac * i))
        tail = df.iloc[i - tail_size + 1:i + 1]
        W_op_tail = tail['W_operator'].mean()
        W_ent_tail = tail['W_signal'].mean()
        delta = abs(W_op_tail - W_ent_tail)
        tail_deltas.append(
            {'window_end': df['window_end'].iloc[i], 'W_operator_tail': W_op_tail, 'W_signal_tail': W_ent_tail,
             'delta': delta})
    delta_df = pd.DataFrame(tail_deltas)
    plt.figure(figsize=(10, 6))
    plt.plot(delta_df['window_end'], delta_df['W_operator_tail'], label='W_operator (tail avg)', linewidth=2)
    plt.plot(delta_df['window_end'], delta_df['W_signal_tail'], label='W_signal (tail avg)', linewidth=2,
             linestyle='--')
    plt.xlabel('Window End Time')
    plt.ylabel('Tail-Averaged Residence Time (W)')
    plt.title(f'Tail Convergence of Residence Time (Tail = {int(tail_frac * 100)}%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return delta_df


def plot_cumulative_flow(queue_name, presence, signal_index, T=200):
    entry_times, exit_times = get_entry_exit_times(presence, signal_index, queue_name)
    arrivals = np.zeros(T)
    departures = np.zeros(T)
    for t in entry_times:
        if t < T:
            arrivals[t] += 1
    for t in exit_times:
        if t < T:
            departures[t] += 1
    cumulative_arrivals = np.cumsum(arrivals)
    cumulative_departures = np.cumsum(departures)
    plt.figure(figsize=(10, 5))
    plt.plot(range(T), cumulative_arrivals, label='Cumulative Arrivals')
    plt.plot(range(T), cumulative_departures, label='Cumulative Departures')
    plt.title(f'Cumulative Flow Diagram (Queue {queue_name})')
    plt.xlabel('Time')
    plt.ylabel('Cumulative Count')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return pd.DataFrame({'Time': np.arange(T), 'Cumulative Arrivals': cumulative_arrivals,
                         'Cumulative Departures': cumulative_departures})


def plot_l_vs_lambda_w(presence, arrival_index, visit_index):
    T = presence.shape[1]
    data = []
    for t in range(1, T):
        lam = compute_cumulative_arrival_rate(arrival_index, presence, 0, t)
        L = compute_average_number_in_queue(presence, 0, t)
        W = compute_average_residence_time(visit_index, presence, 0, t)
        data.append({'window_end': t, 'lambda': lam, 'W': W, 'L': L, 'lambda*W': lam * W})
    df = pd.DataFrame(data)
    plt.figure(figsize=(8, 6))
    plt.plot(df['L'], df['lambda*W'], 'o', label='Observed (L vs λW)')
    plt.plot([df['L'].min(), df['L'].max()], [df['L'].min(), df['L'].max()], 'r--', label='x = y')
    plt.xlabel('Average Number in Queue (L)')
    plt.ylabel('Cumulative Arrival Rate × Average Residence Time (λ × W)')
    plt.title('L vs λW over intervals [0, t)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return df


def plot_limit_curves(presence, arrival_index, visit_index):
    T = presence.shape[1]
    data = []
    for t in range(1, T):
        lam = compute_cumulative_arrival_rate(arrival_index, presence, 0, t)
        L = compute_average_number_in_queue(presence, 0, t)
        W = compute_average_residence_time(visit_index, presence, 0, t)
        data.append({'window_end': t, 'lambda': lam, 'W': W, 'L': L})
    df = pd.DataFrame(data)
    limits = estimate_limits(df)
    plt.figure(figsize=(10, 7))
    plt.plot(df['window_end'], df['L'], label='Average Number in Queue (L)')
    plt.plot(df['window_end'], df['lambda'], label='Cumulative Arrival Rate (λ)')
    plt.plot(df['window_end'], df['W'], label='Average Residence Time (W)')
    plt.axhline(limits['lambda_limit'], color='orange', linestyle=':', label='λ limit')
    plt.axhline(limits['W_limit'], color='green', linestyle=':', label='W limit')
    plt.axhline(limits['L_limit'], color='blue', linestyle=':', label='L limit')
    plt.xlabel('Window End Time (Window Size = t - 0)')
    plt.ylabel('Metric Value')
    plt.title('Convergence of L, λ, and W over Increasing Window Sizes')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return df


def compute_lambda_L_W_phase_trajectory(presence, arrival_index, visit_index, window_size=20):
    T = presence.shape[1]
    phase_points = []
    for t in range(1, T):
        metrics = compute_operator_flow_metrics(presence, arrival_index, visit_index, 0, t)
        phase_points.append((metrics['lambda'], metrics['L'], metrics['W']))
    return phase_points


def plot_phase_trajectory(presence, arrival_index, visit_index, T, window_size=20, cmap='plasma'):
    trajectory = compute_lambda_L_W_phase_trajectory(presence, arrival_index, visit_index, window_size)
    avg_W = compute_average_residence_time(visit_index, presence, t0=0, t1=T)
    lambdas, Ls, Ws = zip(*trajectory)
    lambda_vals = np.linspace(min(lambdas), max(lambdas), 200)
    L_ideal = lambda_vals * avg_W
    points = np.array([lambdas, Ls]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(min(Ws), max(Ws))
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(np.array(Ws[:-1]))
    lc.set_linewidth(2)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.add_collection(lc)
    ax.plot(lambda_vals, L_ideal, 'r--', label=f"Little's Law (W̄ = {avg_W:.2f})")
    ax.autoscale()
    ax.set_xlabel('λ (Arrival Rate)')
    ax.set_ylabel('L (Average Number in System)')
    ax.set_title('λ vs L Phase Space Trajectory (Colored by W)')
    ax.legend()
    plt.colorbar(lc, ax=ax, label='W (Residence Time)')
    plt.grid(True)
    plt.show()


def get_entry_exit_times(presence, signal_index, queue_name):
    arrivals = []
    departures = []
    mat = presence[queue_name]
    for i in range(mat.shape[0]):
        times = np.where(mat[i])[0]
        if times.size > 0:
            arrivals.append(times[0])
            departures.append(times[-1] + 1)
    return (arrivals, departures)


def compute_cumulative_arrival_rate(arrival_index, presence, t0, t1):
    """Cumulative arrival rate over [t0, t1): arrivals + number in system at t0, divided by window length."""
    in_system_at_t0 = np.sum(presence[:, t0 - 1]) if t0 > 0 else 0
    arrivals_during_window = np.sum(arrival_index[t0:t1])
    total_signals = in_system_at_t0 + arrivals_during_window
    return total_signals / (t1 - t0) if t1 > t0 else 0.0


def compute_average_residence_time(visit_index, presence, t0, t1):
    """Average time in system for signals present during [t0, t1)."""
    window = presence[:, t0:t1]
    total_time = np.sum(window)
    total_presences = 0
    for row_presences in visit_index:
        total_presences += sum((t0 <= t < t1 for t in row_presences))
    return total_time / total_presences if total_presences > 0 else 0.0


def compute_average_number_in_queue(presence, t0, t1):
    """Average number of signals present during [t0, t1)."""
    window = presence[:, t0:t1]
    count_per_time = np.sum(window, axis=0)
    return np.mean(count_per_time)


def compute_operator_flow_metrics(presence, arrival_index, visit_index, t0, t1):
    return {'lambda': compute_cumulative_arrival_rate(arrival_index, presence, t0, t1),
            'L': compute_average_number_in_queue(presence, t0, t1),
            'W': compute_average_residence_time(visit_index, presence, t0, t1), 'window': (t0, t1)}


def compute_signal_flow_metrics(presence, arrival_index, visit_index, t0, t1):
    active_signals = np.any(presence[:, t0:t1], axis=1)
    signal_rows = presence[active_signals]
    time_presence = np.any(signal_rows, axis=0)
    t_indices = np.where(time_presence)[0]
    if len(t_indices) == 0:
        return {'lambda': 0, 'L': 0, 'W': 0, 'span': (t0, t1)}
    t_prime_0 = t_indices[0]
    t_prime_1 = t_indices[-1] + 1
    return compute_operator_flow_metrics(presence, arrival_index, visit_index, t_prime_0, t_prime_1)


def estimate_limits(df, tail_frac=0.2):
    tail = df.tail(int(len(df) * tail_frac))
    return {'lambda_limit': tail['lambda'].mean(), 'W_limit': tail['W'].mean(), 'L_limit': tail['L'].mean(),
            'L_estimated': tail['lambda'].mean() * tail['W'].mean()}


def detect_stability_by_tail_convergence(df, tail_frac=0.2, epsilon=0.005):
    deltas = []
    window_ends = df['window_end'].values
    for i in range(1, len(df)):
        tail_size = max(1, int(tail_frac * i))
        tail = df.iloc[i - tail_size + 1:i + 1]
        lam_tail = tail['lambda'].mean()
        W_tail = tail['W'].mean()
        L_tail = tail['L'].mean()
        L_estimated = lam_tail * W_tail
        delta = abs(L_tail - L_estimated)
        deltas.append({'window_end': window_ends[i], 'delta': delta, 'L_tail': L_tail, 'L_estimated': L_estimated,
                       'lambda_tail': lam_tail, 'W_tail': W_tail, 'stable': delta < epsilon})
    delta_df = pd.DataFrame(deltas)
    plt.figure(figsize=(10, 6))
    plt.plot(delta_df['window_end'], delta_df['delta'], label='|L - λ×W|')
    plt.axhline(epsilon, color='red', linestyle='--', label=f'ε = {epsilon}')
    plt.xlabel('Window End Time')
    plt.ylabel('Delta: |L - λ×W|')
    plt.title('Convergence of L = λ × W (Tail-Averaged)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return delta_df


def detect_tail_convergence(delta_df, tail_frac=0.2, epsilon=0.05):
    """
    Annotates chart with the first window_end where convergence occurs.
    """
    delta_df = delta_df.copy()
    delta_df['tail_size_days'] = (tail_frac * delta_df['window_end']).astype(int)
    delta_df['converged'] = delta_df['delta'] < epsilon
    tail_size_annotation = int(tail_frac * delta_df['window_end'].max())
    first_converged = delta_df[delta_df['converged']].head(1)
    convergence_point = first_converged['window_end'].values[0] if not first_converged.empty else None
    plt.figure(figsize=(10, 6))
    plt.plot(delta_df['window_end'], delta_df['delta'], label=f'|W_op - W_ent| (tail avg, {tail_size_annotation} days)',
             linewidth=2)
    plt.axhline(epsilon, color='red', linestyle='--', label=f'ε = {epsilon}')
    if convergence_point:
        plt.axvline(convergence_point, color='green', linestyle=':', linewidth=1.5,
                    label=f'Converged at t = {convergence_point}')
        plt.text(convergence_point + 1, epsilon + 0.02, f't = {convergence_point}', color='green', fontsize=10)
    plt.xlabel('Window End Time')
    plt.ylabel('Tail Delta')
    plt.title('Tail Convergence of Residence Time (Entity vs Operator Perspective)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return delta_df[['window_end', 'tail_size_days', 'delta', 'converged']]