# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT
import os
from typing import List, Optional, Tuple, Sequence

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from spath.filter import FilterResult
from spath.metrics import FlowMetricsResult, compute_dynamic_empirical_series, compute_tracking_errors, \
    compute_coherence_score, compute_end_effect_series, compute_total_active_age_series

def _add_caption(fig: Figure, text: str) -> None:
    """Add a caption below the x-axis."""
    fig.subplots_adjust(bottom=0.28)
    fig.text(
        0.5,
        0.005,
        text,
        ha="center",
        va="bottom",
        fontsize=9,
    )


def _format_date_axis(ax: Axes, unit: str = "timestamp") -> None:
    """Format the x-axis for dates if possible."""
    ax.set_xlabel(f"Date ({unit})")
    try:
        ax.figure.autofmt_xdate()
    except Exception:
        pass


def _format_axis(ax: Axes, title: str, unit: str, ylabel: str) -> None:
    """Set axis labels, title, and legend with date formatting."""
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.legend()
    _format_date_axis(ax, unit=unit)


def _format_fig(caption: Optional[str], fig: Figure) -> None:
    """Finalize figure with optional caption and layout adjustment."""
    fig.tight_layout()
    if caption:
        _add_caption(fig, caption)


def _format_and_save(
    fig: Figure,
    ax: Axes,
    title: str,
    ylabel: str,
    unit: str,
    caption: Optional[str],
    out_path: str,
) -> None:
    """Format the axis, add optional caption, save the figure, and close it."""
    _format_axis(ax, title, unit, ylabel)
    _format_fig(caption, fig)
    fig.savefig(out_path)
    plt.close(fig)


# ── Common plotting engines (de-duplicated) ───────────────────────────────────


def _init_fig_ax(figsize: Tuple[float, float] = (10.0, 3.4)) -> Tuple[Figure, Axes]:
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax


def _plot_series(
    ax: Axes,
    times: Sequence[pd.Timestamp],
    values: Sequence[float],
    label: str,
    style: str = "line",
    where: str = "post",
) -> None:
    if style == "step":
        ax.step(times, values, where=where, label=label)
    else:
        ax.plot(times, values, label=label)


def draw_series_chart(
    times: Sequence[pd.Timestamp],
    values: Sequence[float],
    title: str,
    ylabel: str,
    out_path: str,
    unit: str = "timestamp",
    caption: Optional[str] = None,
    style: str = "line",
    figsize: Tuple[float, float] = (10.0, 3.4),
) -> None:
    fig, ax = _init_fig_ax(figsize=figsize)
    _plot_series(ax, times, values, label=ylabel, style=style)
    _format_and_save(fig, ax, title, ylabel, unit, caption, out_path)


def draw_line_chart(
    times: List[pd.Timestamp],
    values: np.ndarray,
    title: str,
    ylabel: str,
    out_path: str,
    unit: str = "timestamp",
    caption: Optional[str] = None,
) -> None:
    draw_series_chart(
        times, values, title, ylabel, out_path, unit=unit, caption=caption, style="line"
    )


def draw_step_chart(
    times: List[pd.Timestamp],
    values: np.ndarray,
    title: str,
    ylabel: str,
    out_path: str,
    unit: str = "timestamp",
    caption: Optional[str] = None,
) -> None:
    draw_series_chart(
        times, values, title, ylabel, out_path, unit=unit, caption=caption, style="step"
    )


def draw_lambda_chart(
    times: List[pd.Timestamp],
    values: np.ndarray,
    title: str,
    ylabel: str,
    out_path: str,
    lambda_pctl_upper: Optional[float] = None,
    lambda_pctl_lower: Optional[float] = None,
    lambda_warmup_hours: Optional[float] = None,
    unit: str = "timestamp",
    caption: Optional[str] = None,
) -> None:
    """Line chart with optional percentile-based y-limits and warmup exclusion."""
    fig, ax = _init_fig_ax(figsize=(10.0, 3.6))
    ax.plot(times, values, label=ylabel)

    # Inline percentile clipping
    vals = np.asarray(values, dtype=float)
    if vals.size > 0:
        mask = np.isfinite(vals)
        if lambda_warmup_hours and times:
            t0 = times[0]
            ages_hr = np.array([(t - t0).total_seconds() / 3600.0 for t in times])
            mask &= ages_hr >= float(lambda_warmup_hours)
        data = vals[mask]
        if data.size > 0 and np.isfinite(data).any():
            top = (
                np.nanpercentile(data, lambda_pctl_upper)
                if lambda_pctl_upper is not None
                else np.nanmax(data)
            )
            bottom = (
                np.nanpercentile(data, lambda_pctl_lower)
                if lambda_pctl_lower is not None
                else 0.0
            )
            if np.isfinite(top) and np.isfinite(bottom) and top > bottom:
                ax.set_ylim(float(bottom), float(top))

    _format_and_save(fig, ax, title, ylabel, unit, caption, out_path)


# ── Higher-level plotting functions (unchanged except captions fixed) ─────────


def plot_core_flow_metrics(
    df: pd.DataFrame,
    args,
    filter_result: Optional[FilterResult],
    metrics: FlowMetricsResult,
    out_dir: str,
) -> List[str]:
    out_dir = ensure_output_dir(out_dir)
    filter_label = filter_result.label if filter_result else ""
    note = f"Filters: {filter_label}"

    path_N = os.path.join(out_dir, "timestamp_N.png")
    draw_step_chart(
        metrics.times, metrics.N, "N(t) — Active elements", "N(t)", path_N, caption=note
    )

    path_L = os.path.join(out_dir, "timestamp_L.png")
    draw_line_chart(
        metrics.times,
        metrics.L,
        "L(T) — Time-average N(t)",
        "L(T)",
        path_L,
        caption=note,
    )

    path_Lam = os.path.join(out_dir, "timestamp_Lambda.png")
    draw_lambda_chart(
        metrics.times,
        metrics.Lambda,
        "Λ(T) — Cumulative arrival rate",
        "Λ(T) [1/hr]",
        path_Lam,
        lambda_pctl_upper=args.lambda_pctl,
        lambda_pctl_lower=args.lambda_lower_pctl,
        lambda_warmup_hours=args.lambda_warmup,
        caption=note,
    )

    path_w = os.path.join(out_dir, "timestamp_w.png")
    draw_line_chart(
        metrics.times,
        metrics.w,
        "w(T) — Average residence time",
        "w(T) [hrs]",
        path_w,
        caption=note,
    )

    path_LLw = os.path.join(out_dir, "timestamp_LLw.png")
    draw_L_vs_Lambda_w(
        metrics.times,
        metrics.L,
        metrics.Lambda,
        metrics.w,
        title="L(T) vs Λ(T).w(T)",
        out_path=path_LLw,
        caption=note
    )

    path_little_law = os.path.join(out_dir, "timestamp_little_law.png")
    draw_L_vs_lambdaW(df, metrics.times, metrics.L, "Little's Law Empirical Convergence", out_path=path_little_law,
                      caption=note)
    return [path_N, path_L, path_Lam, path_w, path_LLw, path_little_law]



def draw_line_chart_with_scatter(times: List[pd.Timestamp],
                                 values: np.ndarray,
                                 title: str,
                                 ylabel: str,
                                 out_path: str,
                                 scatter_times: List[pd.Timestamp],
                                 scatter_values: np.ndarray,
                                 line_label: str = 'average residence time',
                                 scatter_label: str = "element sojourn time",
                                 unit: str = "timestamp",
                                 caption: Optional[str] = None
                                 ) -> None:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(times, values, label=line_label)
    if scatter_times is not None and scatter_values is not None and len(scatter_times) > 0:
        ax.scatter(scatter_times, scatter_values, s=16, alpha=0.6, marker='o', label=scatter_label)

    _format_and_save(fig, ax, title, ylabel, unit, caption, out_path)



def draw_L_vs_Lambda_w(
    times: List[pd.Timestamp],          # kept for symmetry with other draw_* funcs (not used here)
    L_vals: np.ndarray,
    Lambda_vals: np.ndarray,
    w_vals: np.ndarray,
    title: str,
    out_path: str,
    caption: Optional[str] = None,
) -> None:
    """
    Scatter plot of L(T) vs Λ(T)·w(T) with x=y reference line.
    All valid (finite) points should lie on the x=y line per the finite version of Little's Law
    This chart is a visual consistency check for the calculations.
    """
    # Prepare data and drop non-finite points
    x = np.asarray(L_vals, dtype=float)
    y = np.asarray(Lambda_vals, dtype=float) * np.asarray(w_vals, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]

    # Build figure (square so the x=y line is at 45°)
    fig: Figure
    ax: Axes
    fig, ax = plt.subplots(figsize=(6.0, 6.0))

    # Scatter with slightly larger markers to reveal clusters
    ax.scatter(x, y, s=18, alpha=0.7)

    # Reference x=y line across the data range with small padding
    if x.size and y.size:
        mn = float(np.nanmin([x.min(), y.min()]))
        mx = float(np.nanmax([x.max(), y.max()]))
        pad = 0.03 * (mx - mn if mx > mn else 1.0)
        lo, hi = mn - pad, mx + pad
        ax.plot([lo, hi], [lo, hi], linestyle="--")  # reference line
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)

    # Make axes comparable visually
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linewidth=0.5, alpha=0.4)

    # Labels and title
    ax.set_xlabel("L(T)")
    ax.set_ylabel("Λ(T)·w(T)")
    ax.set_title(title)

    # Layout + optional caption (bottom)
    if caption:
        _add_caption(fig, caption)  # uses the helper you already have
    fig.tight_layout(rect=(0.05, 0, 1, 1))
    fig.savefig(out_path)
    plt.close(fig)

def draw_L_vs_lambdaW(
    df: pd.DataFrame,
    times: List[pd.Timestamp],
    L_vals: np.ndarray,
    title: str,
    out_path: str,
    caption: Optional[str] = None,
) -> None:
    """
    Scatter plot of L(T) vs λ*(T)·W*(T) with an x=y reference line.
    Uses empirical λ*(T) and W*(T) from compute_dynamic_empirical_series.
    Layout tweaks:
      • square figure + equal aspect (true 45° reference)
      • left margin so y-label isn't cut
      • caption added after tight_layout, with extra bottom space
    """
    # Empirical series
    W_star, lam_star = compute_dynamic_empirical_series(df, times)

    # x = L(T), y = λ*(T)·W*(T)
    x = np.asarray(L_vals, dtype=float)
    y = np.asarray(lam_star, dtype=float) * np.asarray(W_star, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]

    fig, ax = plt.subplots(figsize=(6.0, 6.0))

    # Slightly larger markers + alpha to show clustering
    ax.scatter(x, y, s=18, alpha=0.7)

    # x = y reference line with small padding
    if x.size and y.size:
        mn = float(np.nanmin([x.min(), y.min()]))
        mx = float(np.nanmax([x.max(), y.max()]))
        pad = 0.03 * (mx - mn if mx > mn else 1.0)
        lo, hi = mn - pad, mx + pad
        ax.plot([lo, hi], [lo, hi], linestyle="--", color="gray")
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)

    # Make axes visually comparable
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linewidth=0.5, alpha=0.4)

    # Labels and title
    ax.set_xlabel("L(T)")
    ax.set_ylabel("λ*(T)·W*(T)")
    ax.set_title(title)

    # Layout:
    # 1) Tight layout with a bit of extra LEFT margin so the y-label isn't clipped
    if caption:
        _add_caption(fig, caption)  # uses the helper you already have
    fig.tight_layout(rect=(0.05, 0, 1, 1))

    fig.savefig(out_path)
    plt.close(fig)


def draw_convergence_panel(times: List[pd.Timestamp],
                           w_vals: np.ndarray,
                           lam_vals: np.ndarray,
                           W_emp: float,
                           lam_emp: float,
                           title: str,
                           out_path: str,
                           lambda_pctl_upper: Optional[float] = None,
                           lambda_pctl_lower: Optional[float] = None,
                           lambda_warmup_hours: Optional[float] = None
                           ) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(12, 6.5), sharex=True)

    axes[0].plot(times, w_vals, label='w(T) [hrs]')
    if np.isfinite(W_emp):
        axes[0].axhline(W_emp, linestyle='--', label=f'W* ≈ {W_emp:.2f} h')
    axes[0].set_title('w(T) vs W*  — residence time convergence')
    axes[0].set_ylabel('hours')
    axes[0].legend()

    axes[1].plot(times, lam_vals, label='Λ(T) [1/hr]')
    if np.isfinite(lam_emp):
        axes[1].axhline(lam_emp, linestyle='--', label=f'λ* ≈ {lam_emp:.4f} 1/hr')
    axes[1].set_title('Λ(T) vs λ*  — arrival rate convergence')
    axes[1].set_ylabel('1/hr')
    axes[1].set_xlabel('Date')
    axes[1].legend()

    _clip_axis_to_percentile(axes[1], times, lam_vals,
                             upper_p=lambda_pctl_upper,
                             lower_p=lambda_pctl_lower,
                             warmup_hours=lambda_warmup_hours)

    for ax in axes:
        _format_date_axis(ax)

    fig.suptitle(title)
    plt.tight_layout(rect=(0, 0, 1, 0.96))

    fig.savefig(out_path)
    plt.close(fig)


def draw_dynamic_convergence_panel(times: List[pd.Timestamp],
                                   w_vals: np.ndarray,
                                   lam_vals: np.ndarray,
                                   W_star: np.ndarray,
                                   lam_star: np.ndarray,
                                   title: str,
                                   out_path: str,
                                   lambda_pctl_upper: Optional[float] = None,
                                   lambda_pctl_lower: Optional[float] = None,
                                   lambda_warmup_hours: Optional[float] = None,
                                   caption: Optional[str] = None
                                   ) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(12, 6.5), sharex=True)

    axes[0].plot(times, w_vals, label='w(T) [hrs]')
    axes[0].plot(times, W_star, linestyle='--', label='W*(t) [hrs] (completed ≤ t)')
    axes[0].set_title('w(T) vs W*(t)')
    axes[0].set_ylabel('hours')
    axes[0].legend()

    axes[1].plot(times, lam_vals, label='Λ(T) [1/hr]')
    axes[1].plot(times, lam_star, linestyle='--', label='λ*(t) [1/hr] (arrivals ≤ t)')
    axes[1].set_title('Λ(T) vs λ*(t)  — arrival rate')
    axes[1].set_ylabel('1/hr')
    axes[1].set_xlabel('Date')
    axes[1].legend()

    _clip_axis_to_percentile(axes[1], times, lam_vals,
                             upper_p=lambda_pctl_upper,
                             lower_p=lambda_pctl_lower,
                             warmup_hours=lambda_warmup_hours)

    for ax in axes:
        _format_date_axis(ax)

    fig.suptitle(title)
    if caption:
        _add_caption(fig, caption)  # uses the helper you already have
    fig.tight_layout(rect=(0.05, 0, 1, 1))

    fig.savefig(out_path)
    plt.close(fig)


def draw_dynamic_convergence_panel_with_errors(times: List[pd.Timestamp],
                                               w_vals: np.ndarray,
                                               lam_vals: np.ndarray,
                                               W_star: np.ndarray,
                                               lam_star: np.ndarray,
                                               eW: np.ndarray,
                                               eLam: np.ndarray,
                                               epsilon: Optional[float],
                                               title: str,
                                               out_path: str,
                                               lambda_pctl_upper: Optional[float] = None,
                                               lambda_pctl_lower: Optional[float] = None,
                                               lambda_warmup_hours: Optional[float] = None
                                               ) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(12, 9.2), sharex=True)

    axes[0].plot(times, w_vals, label='w(T) [hrs]')
    axes[0].plot(times, W_star, linestyle='--', label='W*(t) [hrs] (completed ≤ t)')
    axes[0].set_title('w(T) vs W*(t) — dynamic')
    axes[0].set_ylabel('hours')
    axes[0].legend()

    axes[1].plot(times, lam_vals, label='Λ(T) [1/hr]')
    axes[1].plot(times, lam_star, linestyle='--', label='λ*(t) [1/hr] (arrivals ≤ t)')
    axes[1].set_title('Λ(T) vs λ*(t) — dynamic')
    axes[1].set_ylabel('1/hr')
    axes[1].legend()
    _clip_axis_to_percentile(axes[1], times, lam_vals,
                             upper_p=lambda_pctl_upper,
                             lower_p=lambda_pctl_lower,
                             warmup_hours=lambda_warmup_hours)

    axes[2].plot(times, eW, label='rel. error e_W')
    axes[2].plot(times, eLam, label='rel. error e_λ')
    if epsilon is not None:
        axes[2].axhline(epsilon, linestyle='--', label=f'ε = {epsilon:g}')
    axes[2].set_title('Relative tracking errors')
    axes[2].set_ylabel('relative error')
    axes[2].set_xlabel('Date')
    axes[2].legend()

    err = np.concatenate([eW[np.isfinite(eW)], eLam[np.isfinite(eLam)]])
    if err.size > 0:
        ub = float(np.nanpercentile(err, 99.5))
        axes[2].set_ylim(0.0, max(ub, (epsilon if epsilon is not None else 0.0) * 1.5 + 1e-6))

    for ax in axes:
        _format_date_axis(ax)

    fig.suptitle(title)
    plt.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out_path)
    plt.close(fig)


def draw_dynamic_convergence_panel_with_errors_and_endeffects(times: List[pd.Timestamp],
                                                              w_vals: np.ndarray,
                                                              lam_vals: np.ndarray,
                                                              W_star: np.ndarray,
                                                              lam_star: np.ndarray,
                                                              eW: np.ndarray,
                                                              eLam: np.ndarray,
                                                              rA: np.ndarray,
                                                              rB: np.ndarray,
                                                              rho: np.ndarray,
                                                              epsilon: Optional[float],
                                                              title: str,
                                                              out_path: str,
                                                              lambda_pctl_upper: Optional[float] = None,
                                                              lambda_pctl_lower: Optional[float] = None,
                                                              lambda_warmup_hours: Optional[float] = None
                                                              ) -> None:
    """Four-row dynamic convergence view with end-effect metrics."""
    fig, axes = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

    axes[0].plot(times, w_vals, label='w(T) [hrs]')
    axes[0].plot(times, W_star, linestyle='--', label='W*(t) [hrs] (completed ≤ t)')
    axes[0].set_title('w(T) vs W*(t) — dynamic')
    axes[0].set_ylabel('hours')
    axes[0].legend()

    axes[1].plot(times, lam_vals, label='Λ(T) [1/hr]')
    axes[1].plot(times, lam_star, linestyle='--', label='λ*(t) [1/hr] (arrivals ≤ t)')
    axes[1].set_title('Λ(T) vs λ*(t) — dynamic')
    axes[1].set_ylabel('1/hr')
    axes[1].legend()
    _clip_axis_to_percentile(axes[1], times, lam_vals,
                             upper_p=lambda_pctl_upper,
                             lower_p=lambda_pctl_lower,
                             warmup_hours=lambda_warmup_hours)

    axes[2].plot(times, eW, label='rel. error e_W')
    axes[2].plot(times, eLam, label='rel. error e_λ')
    if epsilon is not None:
        axes[2].axhline(epsilon, linestyle='--', label=f'ε = {epsilon:g}')
    axes[2].set_title('Relative tracking errors')
    axes[2].set_ylabel('relative error')
    axes[2].legend()

    err = np.concatenate([eW[np.isfinite(eW)], eLam[np.isfinite(eLam)]])
    if err.size > 0:
        ub = float(np.nanpercentile(err, 99.5))
        axes[2].set_ylim(0.0, max(ub, (epsilon if epsilon is not None else 0.0) * 1.5 + 1e-6))

    axes[3].plot(times, rA, label='r_A(T) = E/A', alpha=0.9)
    axes[3].plot(times, rB, label='r_B(T) = B/starts', alpha=0.9)
    axes[3].set_title('End-effects: mass share and boundary share')
    axes[3].set_ylabel('share [0–1]')
    axes[3].set_ylim(0.0, 1.0)
    ax2 = axes[3].twinx()
    ax2.plot(times, rho, linestyle='--', label='ρ(T)=T/W*(t)', alpha=0.7)
    ax2.set_ylabel('ρ (window / duration)')
    lines1, labels1 = axes[3].get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    axes[3].legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    for ax in axes:
        _format_date_axis(ax)

    fig.suptitle(title)
    plt.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out_path)
    plt.close(fig)


def _clip_axis_to_percentile(ax: plt.Axes,
                             times: List[pd.Timestamp],
                             values: np.ndarray,
                             upper_p: Optional[float] = None,
                             lower_p: Optional[float] = None,
                             warmup_hours: float = 0.0) -> None:
    if upper_p is None and lower_p is None:
        return
    vals = np.asarray(values, dtype=float)
    if vals.size == 0:
        return
    mask = np.isfinite(vals)
    if warmup_hours and times:
        t0 = times[0]
        ages_hr = np.array([(t - t0).total_seconds() / 3600.0 for t in times])
        mask &= (ages_hr >= float(warmup_hours))
    data = vals[mask]
    if data.size == 0 or not np.isfinite(data).any():
        return
    top = np.nanpercentile(data, upper_p) if upper_p is not None else np.nanmax(data)
    bottom = np.nanpercentile(data, lower_p) if lower_p is not None else 0.0
    if not np.isfinite(top) or not np.isfinite(bottom) or top <= bottom:
        return
    ax.set_ylim(float(bottom), float(top))






def plot_sojourn_time_scatter(args, df, filter_result, metrics,out_dir) -> List[str]:
    t_scatter_times: List[pd.Timestamp] = []
    t_scatter_vals = np.array([])
    written = []
    if args.incomplete:
        if len(metrics.times) > 0:
            t_scatter_times = df["start_ts"].tolist()
            t_scatter_vals = df["duration_hr"].to_numpy()

    else:
        df_c = df[df["end_ts"].notna()].copy()
        if not df_c.empty:
            t_scatter_times = df_c["end_ts"].tolist()
            t_scatter_vals = df_c["duration_hr"].to_numpy()

    if len(t_scatter_times) > 0:
        ts_w_scatter = os.path.join(out_dir, "timestamp_w_with_scatter.png")
        label = "age" if args.incomplete else "sojourn time"
        draw_line_chart_with_scatter(metrics.times, metrics.w,
                                     f"Element {label} vs Average residence time",
                                     f"Time [hrs]", ts_w_scatter, t_scatter_times, t_scatter_vals, scatter_label=f"element {label}",
                                      caption=f"{filter_result.label}")

        written += [ts_w_scatter]

    return written


def draw_four_panel_column(times: List[pd.Timestamp],
                           N_vals: np.ndarray,
                           L_vals: np.ndarray,
                           Lam_vals: np.ndarray,
                           w_vals: np.ndarray,
                           title: str,
                           out_path: str,
                           lambda_pctl_upper: Optional[float] = None,
                           lambda_pctl_lower: Optional[float] = None,
                           lambda_warmup_hours: Optional[float] = None,
                           caption:Optional[str] = None
                           ) -> None:
    fig, axes = plt.subplots(4, 1, figsize=(12, 11), sharex=True)

    axes[0].step(times, N_vals, where='post', label='N(t)')
    axes[0].set_title('N(t) — active elements')
    axes[0].set_ylabel('N(t)')
    axes[0].legend()

    axes[1].plot(times, L_vals, label='L(T)')
    axes[1].set_title('L(T) — time-average of N(t)')
    axes[1].set_ylabel('L(T)')
    axes[1].legend()

    axes[2].plot(times, Lam_vals, label='Λ(T) [1/hr]')
    axes[2].set_title('Λ(T) — cumulative arrival rate')
    axes[2].set_ylabel('Λ(T) [1/hr]')
    axes[2].legend()
    _clip_axis_to_percentile(axes[2], times, Lam_vals,
                             upper_p=lambda_pctl_upper,
                             lower_p=lambda_pctl_lower,
                             warmup_hours=lambda_warmup_hours)

    axes[3].plot(times, w_vals, label='w(T) [hrs]')
    axes[3].set_title('w(T) — average residence time')
    axes[3].set_ylabel('w(T) [hrs]')
    axes[3].set_xlabel('Date')
    axes[3].legend()

    for ax in axes:
        _format_date_axis(ax)

    plt.tight_layout(rect=(0, 0, 1, 0.90))
    fig.suptitle(title, fontsize=14, y=0.97)  # larger main title
    if caption:
        fig.text(0.5, 0.945, caption,  # small gray subtitle just below title
                 ha="center", va="top")




    fig.savefig(out_path)
    plt.close(fig)


def draw_five_panel_column(times: List[pd.Timestamp],
                           N_vals: np.ndarray,
                           L_vals: np.ndarray,
                           Lam_vals: np.ndarray,
                           w_vals: np.ndarray,
                           A_vals: np.ndarray,
                           title: str,
                           out_path: str,
                           scatter_times: Optional[List[pd.Timestamp]] = None,
                           scatter_values: Optional[np.ndarray] = None,
                           scatter_label: str = "Item time in system",
                           lambda_pctl_upper: Optional[float] = None,
                           lambda_pctl_lower: Optional[float] = None,
                           lambda_warmup_hours: Optional[float] = None
                           ) -> None:
    fig, axes = plt.subplots(5, 1, figsize=(12, 14), sharex=True)

    axes[0].step(times, N_vals, where='post', label='N(t)')
    axes[0].set_title('N(t) — active elements')
    axes[0].set_ylabel('N(t)')
    axes[0].legend()

    axes[1].plot(times, L_vals, label='L(T)')
    axes[1].set_title('L(T) — time-average of N(t)')
    axes[1].set_ylabel('L(T)')
    axes[1].legend()

    axes[2].plot(times, Lam_vals, label='Λ(T) [1/hr]')
    axes[2].set_title('Λ(T) — cumulative arrival rate')
    axes[2].set_ylabel('Λ(T) [1/hr]')
    axes[2].legend()
    _clip_axis_to_percentile(axes[2], times, Lam_vals,
                             upper_p=lambda_pctl_upper,
                             lower_p=lambda_pctl_lower,
                             warmup_hours=lambda_warmup_hours)

    axes[3].plot(times, w_vals, label='w(T) [hrs]')
    if scatter_times is not None and scatter_values is not None and len(scatter_times) > 0:
        axes[3].scatter(scatter_times, scatter_values, s=16, alpha=0.6, marker='o', label=scatter_label)
    axes[3].set_title('w(T) — average residence time')
    axes[3].set_ylabel('w(T) [hrs]')
    axes[3].legend()

    axes[4].plot(times, A_vals, label='A(T) [hrs·items]')
    axes[4].set_title('A(T) — cumulative area ∫N(t)dt')
    axes[4].set_ylabel('A(T) [hrs·items]')
    axes[4].set_xlabel('Date')
    axes[4].legend()

    for ax in axes:
        _format_date_axis(ax)

    fig.suptitle(title)
    plt.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(out_path)
    plt.close(fig)


def draw_five_panel_column_with_scatter(times: List[pd.Timestamp],
                                        N_vals: np.ndarray,
                                        L_vals: np.ndarray,
                                        Lam_vals: np.ndarray,
                                        w_vals: np.ndarray,
                                        title: str,
                                        out_path: str,
                                        scatter_times: Optional[List[pd.Timestamp]] = None,
                                        scatter_values: Optional[np.ndarray] = None,
                                        scatter_label: str = "Item time in system",
                                        lambda_pctl_upper: Optional[float] = None,
                                        lambda_pctl_lower: Optional[float] = None,
                                        lambda_warmup_hours: Optional[float] = None
                                        ) -> None:
    fig, axes = plt.subplots(5, 1, figsize=(12, 14), sharex=True)

    axes[0].step(times, N_vals, where='post', label='N(t)')
    axes[0].set_title('N(t) — active elements')
    axes[0].set_ylabel('N(t)')
    axes[0].legend()

    axes[1].plot(times, L_vals, label='L(T)')
    axes[1].set_title('L(T) — time-average of N(t)')
    axes[1].set_ylabel('L(T)')
    axes[1].legend()

    axes[2].plot(times, Lam_vals, label='Λ(T) [1/hr]')
    axes[2].set_title('Λ(T) — cumulative arrival rate')
    axes[2].set_ylabel('Λ(T) [1/hr]')
    axes[2].legend()
    _clip_axis_to_percentile(axes[2], times, Lam_vals,
                             upper_p=lambda_pctl_upper,
                             lower_p=lambda_pctl_lower,
                             warmup_hours=lambda_warmup_hours)

    axes[3].plot(times, w_vals, label='w(T) [hrs]')
    axes[3].set_title('w(T) — average residence time (plain, own scale)')
    axes[3].set_ylabel('w(T) [hrs]')
    axes[3].legend()

    axes[4].plot(times, w_vals, label='w(T) [hrs]')
    if scatter_times is not None and scatter_values is not None and len(scatter_values) > 0:
        axes[4].scatter(scatter_times, scatter_values, s=16, alpha=0.6, marker='o', label=scatter_label)
    axes[4].set_title('w(T) — with per-item durations (scatter, combined scale)')
    axes[4].set_ylabel('w(T) [hrs]')
    axes[4].set_xlabel('Date')
    axes[4].legend()

    try:
        w_min = np.nanmin(w_vals); w_max = np.nanmax(w_vals)
        if np.isfinite(w_min) and np.isfinite(w_max):
            pad = 0.05 * max(w_max - w_min, 1.0)
            axes[3].set_ylim(w_min - pad, w_max + pad)
        if scatter_values is not None and len(scatter_values) > 0:
            s_min = np.nanmin(scatter_values); s_max = np.nanmax(scatter_values)
            cmin = np.nanmin([w_min, s_min]); cmax = np.nanmax([w_max, s_max])
        else:
            cmin, cmax = w_min, w_max
        if np.isfinite(cmin) and np.isfinite(cmax):
            pad2 = 0.05 * max(cmax - cmin, 1.0)
            axes[4].set_ylim(cmin - pad2, cmax + pad2)
    except Exception:
        pass

    for ax in axes:
        _format_date_axis(ax)

    fig.suptitle(title)
    plt.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(out_path)
    plt.close(fig)


def ensure_output_dir(csv_path: str) -> str:
    base = os.path.basename(csv_path)
    stem = os.path.splitext(base)[0]
    out_dir = os.path.join("charts", stem)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def plot_coherence_charts(df, args, filter_result, metrics, out_dir):
    # Empirical targets & dynamic baselines
    horizon_days = args.horizon_days
    epsilon = args.epsilon
    lambda_pctl_upper = args.lambda_pctl
    lambda_pctl_lower = args.lambda_lower_pctl
    lambda_warmup_hours = args.lambda_warmup
    mode_label = filter_result.label

    written: List[str] = []

    if len(metrics.times) > 0:
        W_star_ts, lam_star_ts = compute_dynamic_empirical_series(df, metrics.times)
    else:
        W_star_ts = lam_star_ts = np.array([])
    # Relative errors & coherence
    eW_ts, eLam_ts, elapsed_ts = compute_tracking_errors(metrics.times, metrics.w, metrics.Lambda, W_star_ts,
                                                         lam_star_ts)
    coh_summary_lines: List[str] = []
    if epsilon is not None and horizon_days is not None:
        h_hrs = float(horizon_days) * 24.0
        sc_ts, ok_ts, tot_ts = compute_coherence_score(eW_ts, eLam_ts, elapsed_ts, float(epsilon), h_hrs)
        coh_summary_lines.append(
            f"Coherence (timestamp): eps={epsilon:g}, H={horizon_days:g}d -> {ok_ts}/{tot_ts} ({(sc_ts * 100 if sc_ts == sc_ts else 0):.1f}%)")
    # Convergence diagnostics (timestamp)
    if len(metrics.times) > 0:
        ts_conv_dyn = os.path.join(out_dir, 'timestamp_convergence_dynamic.png')
        draw_dynamic_convergence_panel(metrics.times, metrics.w, metrics.Lambda, W_star_ts, lam_star_ts,
                                       f"Little's Law Empirical Convergence", ts_conv_dyn,
                                       lambda_pctl_upper=lambda_pctl_upper, lambda_pctl_lower=lambda_pctl_lower,
                                       lambda_warmup_hours=lambda_warmup_hours,
                                       caption=filter_result.display)
        written.append(ts_conv_dyn)

        ts_conv_dyn3 = os.path.join(out_dir, 'timestamp_convergence_dynamic_errors.png')
        draw_dynamic_convergence_panel_with_errors(metrics.times, metrics.w, metrics.Lambda, W_star_ts, lam_star_ts,
                                                   eW_ts, eLam_ts, epsilon,
                                                   f'Dynamic convergence + errors (timestamp, {mode_label})',
                                                   ts_conv_dyn3, lambda_pctl_upper=lambda_pctl_upper,
                                                   lambda_pctl_lower=lambda_pctl_lower,
                                                   lambda_warmup_hours=lambda_warmup_hours)
        written.append(ts_conv_dyn3)
    # --- End-effect diagnostics ---
    rA_ts, rB_ts, rho_ts = compute_end_effect_series(df, metrics.times, metrics.A, W_star_ts) if len(
        metrics.times) > 0 else (np.array([]), np.array([]), np.array([]))
    if len(metrics.times) > 0:
        ts_conv_dyn4 = os.path.join(out_dir, 'timestamp_convergence_dynamic_errors_endeffects.png')
        draw_dynamic_convergence_panel_with_errors_and_endeffects(
            metrics.times, metrics.w, metrics.Lambda, W_star_ts, lam_star_ts, eW_ts, eLam_ts,
            rA_ts, rB_ts, rho_ts, epsilon,
            f'Dynamic convergence + errors + end-effects (timestamp, {mode_label})', ts_conv_dyn4,
            lambda_pctl_upper=lambda_pctl_upper, lambda_pctl_lower=lambda_pctl_lower,
            lambda_warmup_hours=lambda_warmup_hours)
        written.append(ts_conv_dyn4)

        # Write coherence summary (and print)
        if coh_summary_lines:
            txt_path = os.path.join(out_dir, "coherence_summary.txt")
            with open(txt_path, "w") as f:
                for line in coh_summary_lines:
                    f.write(line + "\n")
            print("\n".join(coh_summary_lines))
            written.append(txt_path)

    return written


def plot_core_metrics_stack(args, filter_result, metrics, out_dir):
    four_col_stack = os.path.join(out_dir, 'timestamp_stack.png')
    draw_four_panel_column(metrics.times, metrics.N, metrics.L, metrics.Lambda, metrics.w,
                           f'Sample Path Flow Metrics', four_col_stack, args.lambda_pctl,
                           args.lambda_lower_pctl, args.lambda_warmup, caption=f"{filter_result.display}")
    return [four_col_stack]


def plot_five_column_stacks(df, args, filter_result, metrics, out_dir):
    t_scatter_times = df["start_ts"].tolist()
    t_scatter_vals = df["duration_hr"].to_numpy()
    written = []
    if args.with_A:
        col_ts5 = os.path.join(out_dir, 'timestamp_stack_with_A.png')
        draw_five_panel_column(metrics.times, metrics.N, metrics.Lambda, metrics.Lambda, metrics.w, metrics.A,
                               f'Finite-window metrics incl. A(T) (timestamp, {filter_result.label})', col_ts5,
                               scatter_times=t_scatter_times, scatter_values=t_scatter_vals,
                               lambda_pctl_upper=args.lambda_pctl, lambda_pctl_lower=args.lambda_lower_pctl,
                               lambda_warmup_hours=args.lambda_warmup)
        written.append(col_ts5)

    elif args.scatter:
        col_ts5s = os.path.join(out_dir, 'timestamp_stack_with_scatter.png')
        draw_five_panel_column_with_scatter(metrics.times, metrics.N, metrics.L, metrics.Lambda, metrics.w,
                                            f'Finite-window metrics with w(T) plain + w(T)+scatter (timestamp, {filter_result.label})',
                                            col_ts5s,
                                            scatter_times=t_scatter_times, scatter_values=t_scatter_vals,
                                            lambda_pctl_upper=args.lambda_pctl,
                                            lambda_pctl_lower=args.lambda_lower_pctl,
                                            lambda_warmup_hours=args.lambda_warmup)
        written.append(col_ts5s)

    return written

def plot_rate_stability_charts(
    df: pd.DataFrame,
    args,                 # kept for signature consistency
    filter_result,        # may provide .title_prefix and .display
    metrics,              # FlowMetricsResult with .times, .N, .t0, .w
    out_dir: str,
) -> List[str]:
    """
    Produce:
      - timestamp_rate_stability_n.png          (N(T)/T)
      - timestamp_rate_stability_r.png          (R(T)/T)
      - timestamp_rate_stability_stack.png      (4-row stack: N/T, R/T, λ*(T), W-coherence)

    The stacked figure has suptitle "Equilibrium and Coherence" and a caption with the filter display.
    """
    written: List[str] = []

    # Observation grid
    times = [pd.Timestamp(t) for t in metrics.times]
    if not times:
        return written

    # Elapsed hours since t0
    t0 = metrics.t0 if hasattr(metrics, "t0") and pd.notna(metrics.t0) else times[0]
    elapsed_h = np.array([(t - t0).total_seconds() / 3600.0 for t in times], dtype=float)
    denom = np.where(elapsed_h > 0.0, elapsed_h, np.nan)

    # Core rate series
    N_raw = np.asarray(metrics.N, dtype=float)
    R_raw = compute_total_active_age_series(df, times)  # hours

    with np.errstate(divide="ignore", invalid="ignore"):
        N_over_T = N_raw / denom
        R_over_T = R_raw / denom

    # Dynamic empirical series (for λ* and W*)
    W_star_ts, lam_star_ts = compute_dynamic_empirical_series(df, times)
    w_ts = np.asarray(metrics.w, dtype=float)

    # Optional display bits
    title_prefix = getattr(filter_result, "title_prefix", None)
    caption_text = getattr(filter_result, "display", None)

    # --------------------- Chart 1: N(T)/T ---------------------
    out_path_N = os.path.join(out_dir, "timestamp_rate_stability_n.png")
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.plot(times, N_over_T, label="N(T)/T", linewidth=1.9, zorder=3)
    ax.axhline(0.0, linewidth=0.8, alpha=0.6, zorder=1)
    ax.axhline(1.0, linewidth=1.0, alpha=0.35, linestyle=":", zorder=1)  # reference guide

    _format_date_axis(ax)
    ax.set_xlabel("time")
    ax.set_ylabel("rate")
    ax.set_title(f"{title_prefix}: N(T)/T" if title_prefix else "N(T)/T")
    ax.legend(loc="best")

    finite_vals_N = N_over_T[np.isfinite(N_over_T)]
    if finite_vals_N.size:
        top = float(np.nanpercentile(finite_vals_N, 99.5))
        bot = float(np.nanmin(finite_vals_N))
        ax.set_ylim(bottom=min(0.0, bot * 1.05), top=top * 1.05)

    fig.tight_layout()
    fig.savefig(out_path_N, dpi=200)
    plt.close(fig)
    written.append(out_path_N)

    # --------------------- Chart 2: R(T)/T ---------------------
    out_path_R = os.path.join(out_dir, "timestamp_rate_stability_r.png")
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.plot(times, R_over_T, label="R(T)/T", linewidth=1.9, zorder=3)
    ax.axhline(0.0, linewidth=0.8, alpha=0.6, zorder=1)
    ax.axhline(1.0, linewidth=1.0, alpha=0.35, linestyle=":", zorder=1)  # reference guide

    _format_date_axis(ax)
    ax.set_xlabel("time")
    ax.set_ylabel("rate")
    ax.set_title(f"{title_prefix}: R(T)/T" if title_prefix else "R(T)/T")
    ax.legend(loc="best")

    finite_vals_R = R_over_T[np.isfinite(R_over_T)]
    if finite_vals_R.size:
        top = float(np.nanpercentile(finite_vals_R, 99.5))
        bot = float(np.nanmin(finite_vals_R))
        ax.set_ylim(bottom=min(0.0, bot * 1.05), top=top * 1.05)

    fig.tight_layout()
    fig.savefig(out_path_R, dpi=200)
    plt.close(fig)
    written.append(out_path_R)

    # --------------------- 4-row stack: Equilibrium and Coherence --------------
    out_path_stack = os.path.join(out_dir, "timestamp_rate_stability_stack.png")
    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(12, 13.5), sharex=True)

    # Panel 1: N(T)/T
    axN = axes[0]
    axN.plot(times, N_over_T, label="N(T)/T", linewidth=1.9, zorder=3)
    axN.axhline(0.0, linewidth=0.8, alpha=0.6, zorder=1)
    axN.axhline(1.0, linewidth=1.0, alpha=0.35, linestyle=":", zorder=1)
    _format_date_axis(axN)
    axN.set_ylabel("rate")
    axN.set_title("N(T)/T")
    axN.legend(loc="best")
    if finite_vals_N.size:
        topN = float(np.nanpercentile(finite_vals_N, 99.5))
        botN = float(np.nanmin(finite_vals_N))
        axN.set_ylim(bottom=min(0.0, botN * 1.05), top=topN * 1.05)

    # Panel 2: R(T)/T
    axR = axes[1]
    axR.plot(times, R_over_T, label="R(T)/T", linewidth=1.9, zorder=3)
    axR.axhline(0.0, linewidth=0.8, alpha=0.6, zorder=1)
    axR.axhline(1.0, linewidth=1.0, alpha=0.35, linestyle=":", zorder=1)
    _format_date_axis(axR)
    axR.set_ylabel("rate")
    axR.set_title("R(T)/T")
    axR.legend(loc="best")
    if finite_vals_R.size:
        topR = float(np.nanpercentile(finite_vals_R, 99.5))
        botR = float(np.nanmin(finite_vals_R))
        axR.set_ylim(bottom=min(0.0, botR * 1.05), top=topR * 1.05)

    # Panel 3: λ*(T)
    axLam = axes[2]
    axLam.plot(times, lam_star_ts, label="λ*(T) [1/hr]", linewidth=1.9, zorder=3)
    axLam.axhline(0.0, linewidth=0.8, alpha=0.6, zorder=1)
    _format_date_axis(axLam)
    axLam.set_ylabel("[1/hr]")
    axLam.set_title("λ*(T) — running arrival rate")
    axLam.legend(loc="best")
    # Clip like other charts
    try:
        _clip_axis_to_percentile(
            axLam, times, lam_star_ts,
            upper_p=getattr(args, "lambda_pctl", None),
            lower_p=getattr(args, "lambda_lower_pctl", None),
            warmup_hours=float(getattr(args, "lambda_warmup", 0.0) or 0.0),
        )
    except Exception:
        pass

    # Panel 4: W-coherence overlay
    axW = axes[3]
    axW.plot(times, w_ts,        label="w(T) [hrs] (finite-window)", linewidth=1.9, zorder=3)
    axW.plot(times, W_star_ts,   label="W*(T) [hrs] (completed mean)", linewidth=1.9, linestyle="--", zorder=3)
    axW.axhline(0.0, linewidth=0.8, alpha=0.6, zorder=1)
    _format_date_axis(axW)
    axW.set_xlabel("time")
    axW.set_ylabel("hours")
    axW.set_title("w(T) vs W*(T) — coherence")
    axW.legend(loc="best")

    # Subtitle + caption
    fig.suptitle("Equilibrium and Coherence", fontsize=14, y=0.98)
    try:
        if caption_text:
            _add_caption(fig, caption_text)
    except Exception:
        pass

    fig.tight_layout(rect=(0, 0.06, 1, 0.96))
    fig.savefig(out_path_stack, dpi=200)
    plt.close(fig)
    written.append(out_path_stack)

    return written