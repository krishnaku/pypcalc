# Auto-generated module

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from .pd_utils import estimate_limits
from .presence_matrix import compute_cumulative_arrival_rate, compute_signal_flow_metrics, compute_operator_flow_metrics, \
    compute_average_residence_time, compute_average_number_in_queue, get_entry_exit_times


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
