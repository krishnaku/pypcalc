# Computing Flow Metrics from Sample Paths

> **TL;DR** — Model your system as a right-continuous, piecewise-constant stochastic process $N(t)$ driven by point events. Integrate the realized **sample path** exactly between events to obtain cumulative area $A(T)$, time-average WIP $L(T)$, arrival rate $Λ(T)$, and mean time in system $w(T)$. Changing the **sampling schedule** changes only what you report, **not** the underlying path or the exact per-bucket aggregates.

---

## 1. Motivation

Dashboards often estimate flow metrics by averaging spot samples (e.g., “read $N(t)$ every minute and average”). That’s sensitive to sampling rate and phase. If you already have an **event log** (arrivals, departures), you can compute **exact** time integrals for the realized path—no binning, no resampling error—using a single pass.

This post formalizes the processes, defines the **sample path**, shows how it maps to the **Cumulative Flow Diagram (CFD)**, and presents an exact, event-driven algorithm you can implement in a few lines.

---

## 2. The stochastic processes

We consider three processes on time $t \in \mathbb{R}_{\ge 0}$:

- **Arrivals** $A(t)$: cumulative number of processes that have arrived by time $t$.  
  A counting process: nondecreasing, right-continuous, integer-valued, with jumps at arrival times.

- **Departures** $D(t)$: cumulative number that have departed by time $t$.  
  Also a counting process.

- **In-system (WIP)** $N(t)$: number of processes currently present at time $t$.  
  Flow balance (unit-jump case):
  $$
  N(t) \;=\; N(0) \;+\; A(t) \;-\; D(t).
  $$

More generally, view the event stream as a **marked point process** $\{(T_k,\;\Delta N_k,\;a_k)\}$:

- $T_k$ is an event time,  
- $\Delta N_k$ is the “presence mass” jump (e.g., $+1$ on arrival, $-1$ on departure; batch jumps allowed),  
- $a_k \in \{0,1,2,\dots\}$ counts arrivals at that instant (often $0$ or $1$).

**Regularity.** $N(t)$ is càdlàg: right-continuous with left limits, **piecewise constant** between events and jumping only at event times.

---

## 3. Sample paths vs. sampling schedules

- A **sample path** is a single realization $n(t)$ of $N(t)$ determined by the events.  
- Changing the **sampling schedule** (which timestamps you evaluate at) **does not** change the path; it only changes which points on that same path you **report**.

This distinction matters: the method below integrates **between events** exactly. It is *not* the average of discrete spot readings, which would depend on sampling frequency and phase.

---

## 4. Metrics from the sample path (finite-window interpretation)

Fix a reporting start $t_0$ and any $T \ge t_0$. Define:

- **Cumulative area under the path** (process·hours):  
  $$
  A(T) \;=\; \int_{t_0}^{T} N(u)\,du.
  $$

- **Time-average WIP** (processes):  
  $$
  L(T) \;=\; \frac{A(T)}{T - t_0}.
  $$

- **Average arrival rate** (processes/hour):  
  $$
  \Lambda(T) \;=\; \frac{\mathrm{Arrivals}(T)}{T - t_0},
  $$
  where $\mathrm{Arrivals}(T)$ counts arrivals in $(t_0, T]$.

- **Finite-window average residence time (in-window contribution per arrival)** (hours):  
  $$
  w(T) \;=\; \frac{A(T)}{\mathrm{Arrivals}(T)}.
  $$
  This $w(T)$ is **not**, in general, the average of the **full** per-item residence times for arrivals in $(t_0, T]$. It averages **only the portion of residence time accrued *inside* the window** per arriving process. Items already present at $t_0$ contribute to $A(T)$ but are not counted in $\mathrm{Arrivals}(T)$, and items that arrive near $T$ may be censored (not yet departed).

When denominators are defined, these satisfy the finite-interval Little’s Law identity:
$$
w(T) \;=\; \frac{L(T)}{\Lambda(T)}.
$$

**Units.** If time is in hours, then $A$ is process·hours, $L$ is processes, $\Lambda$ is processes/hour, and $w$ is hours.

**Convergence note.** Over long, steady-state windows, boundary effects (censoring and carry-over) diminish and $w(T)$ approaches the true mean per-item residence time.

---

## 5. Relation to the Cumulative Flow Diagram (CFD)

A CFD plots the two cumulative curves $A(t)$ (arrivals) and $D(t)$ (departures).

- **Vertical gap (at time $t$):**  
  $N(t) = A(t) - D(t)$ — the number in system (WIP). This is always well-defined.

- **Horizontal gap (at a fixed cumulative count level):**  
  The time between the instant the $k$-th arrival is recorded on $A(t)$ and the instant the $k$-th departure is recorded on $D(t)$.  
  This reads as a **per-item residence time** only under strong assumptions that let you *pair* arrivals to departures (e.g., FIFO/no overtaking, no splitting/merging/rework, completed items inside the window).  
  Without those assumptions, treating a horizontal distance as an item’s residence time is not generally valid.

- **Finite-window average residence time (what we compute):**  
  We define
  $$
  A(T) = \int_{t_0}^{T} N(u)\,du, \quad
  w(T) = \frac{A(T)}{\mathrm{Arrivals}(T)} = \frac{L(T)}{\Lambda(T)}.
  $$
  Here $w(T)$ is the **average in-window residence contribution per arrival** in $(t_0, T]$.  
  It is **not**, in general, the average of full per-item residence times for arrivals in that window, because:
  (i) items present at $t_0$ contribute to $A(T)$ but are not counted in $\mathrm{Arrivals}(T)$, and  
  (ii) items that arrive near $T$ may not have departed yet (censoring).  
  Over long, steady-state windows these boundary effects diminish and $w(T)$ approaches the true mean residence time.

- **Buckets (day/week/month/…):**  
  For a bucket $(T_{i-1}, T_i]$, use differences:
  $A_i = A(T_i) - A(T_{i-1})$ and $\mathrm{Arrivals}_i = \mathrm{Arrivals}(T_i) - \mathrm{Arrivals}(T_{i-1})$, then
  $$
  L_i = \frac{A_i}{T_i - T_{i-1}}, \qquad
  \Lambda_i = \frac{\mathrm{Arrivals}_i}{T_i - T_{i-1}}, \qquad
  w_i = \frac{A_i}{\mathrm{Arrivals}_i}.
  $$
  This $w_i$ is the **average in-bucket residence contribution per arrival**, not necessarily the average of full per-item residence times for that bucket’s arrivals unless all such items complete within the bucket and valid pairing assumptions hold.

---

## 6. The event-driven algorithm

Given a list of events $(\text{time}, \Delta N, a)$ and any set of **observation times** $T_1,\dots,T_m$, we can compute $N, A, L, Λ, w$ at each $T_j$ in **one pass**.

**Invariant:** Between events, $N(t)$ is constant $\Rightarrow$ the area increment over any interval is a rectangle: $\Delta A = N \cdot \Delta t$. No trapezoids, no approximation.

**Algorithm (sweep):**

1. Sort `events` by time, and `sample_times` ascending. Let $t_0 = \min(\text{sample\_times})$.
2. Initialize: $N \gets 0$, $A \gets 0$, $\text{arrivals} \gets 0$, $\text{prev} \gets t_0$.
3. For each sample time $t$:
   - While there are events with time $\le t$:  
     $A \mathrel{+}= N \cdot (t_\text{ev} - \text{prev})$;  
     $\text{prev} \gets t_\text{ev}$;  
     $N \mathrel{+}= \Delta N$;  
     $\text{arrivals} \mathrel{+}= a$.
   - Tail to the sample point: $A \mathrel{+}= N \cdot (t - \text{prev})$, $\text{prev} \gets t$.
   - Elapsed $Δ = (t - t_0)$. Report:  
     $L = A/Δ$ (if $Δ>0$), $Λ = \text{arrivals}/Δ$ (if $Δ>0$), $w = A/\text{arrivals}$ (if arrivals$>0$), and the current $N$.

**Complexity:** $O(\#\text{events} + \#\text{samples})$ time, $O(1)$ extra state.

**Conventions:**
- Right-continuity: multiple events at the same timestamp are processed with $Δt=0$ between them—only the jump $N \mathrel{+}= \Delta N$ and arrival count update.
- Events before $t_0$: adjust initial state $N$ and arrivals but add no area (integration starts at $t_0$).

---

## 7. Calendar buckets without precision loss

To compute per-bucket metrics (day/week/month/quarter/year), **sample only at bucket boundaries** $T_0 < T_1 < \dots < T_K$ (e.g., midnights, month starts). Because both the area $A(\cdot)$ and cumulative arrivals $\mathrm{Arrivals}(\cdot)$ are **additive**:

- Per-bucket totals are **differences**:
  - $A_i = A(T_i) - A(T_{i-1}) = \int_{T_{i-1}}^{T_i} N(u)\,du$
  - $\mathrm{Arrivals}_i = \mathrm{Arrivals}(T_i) - \mathrm{Arrivals}(T_{i-1})$

- Per-bucket averages are exact:
  - $L_i = A_i / (T_i - T_{i-1})$
  - $Λ_i = \mathrm{Arrivals}_i / (T_i - T_{i-1})$
  - $w_i = A_i / \mathrm{Arrivals}_i = L_i / Λ_i$ (when $\mathrm{Arrivals}_i>0$)

You do **not** need intra-bucket samples. Adding interior points does not change these differences.

**Boundary convention:** Buckets are $(T_{i-1}, T_i]$: events exactly at $T_i$ belong to bucket $i$.

---

## 8. What changes when you change sampling?

- Change the **observation times** $\Rightarrow$ you change *which* $T$ you report $N, A, L, Λ, w$ at.
- You **do not** change the underlying sample path $n(t)$.
- You **do not** change exact per-bucket aggregates if you still difference at the same bucket boundaries.

---

## 9. Reference implementation (sketch)

```python
# events: List[Tuple[pd.Timestamp, int, int]]  # (time, dN, arrivals_mark)
# sample_times: List[pd.Timestamp]             # arbitrary observation times

def compute_sample_path_metrics(events, sample_times):
    if not events:
        return sorted(sample_times), *[np.array([])]*5

    events = sorted(events, key=lambda e: e[0])
    T = sorted(sample_times)
    t0 = T[0]

    N = 0
    A = 0.0
    arrivals = 0
    prev = t0

    out_L, out_Lam, out_w, out_N, out_A = [], [], [], [], []
    i = 0  # event index

    for t in T:
        while i < len(events) and events[i][0] <= t:
            t_ev, dN, a = events[i]
            A += N * ((t_ev - prev).total_seconds() / 3600.0)
            prev = t_ev
            N += dN
            arrivals += a
            i += 1

        A += N * ((t - prev).total_seconds() / 3600.0)
        prev = t

        dt = (t - t0).total_seconds() / 3600.0
        L   = (A / dt) if dt > 0 else np.nan
        Lam = (arrivals / dt) if dt > 0 else np.nan
        w   = (A / arrivals) if arrivals > 0 else np.nan

        out_L.append(L); out_Lam.append(Lam); out_w.append(w)
        out_N.append(N); out_A.append(A)

    return T, np.array(out_L), np.array(out_Lam), np.array(out_w), np.array(out_N), np.array(out_A)
```
For calendar buckets, build boundary times with pd.date_range(..., freq="D"/"W-MON"/"MS"/"QS-..."/"YS-..."), call the function at those boundaries, and difference the cumulative arrays.

## 10. Edge cases & practical tips
- If $T = t_0$, $L$ and $Λ$ are undefined $\Rightarrow$ return NaN.
- If zero arrivals in $(t_0, T]$, $w(T)$ is undefined $\Rightarrow$ return NaN.
- Time zones: perform arithmetic in a consistent TZ (e.g., convert to UTC).
- Batch events: multiple changes at the same timestamp are fine (rectangle area has $Δt=0$).
- Validate inputs: event list sorted, timestamps monotone for sample times, etc.

## 11. Irregular observation schedules (non-uniform sampling)

You do **not** need a regular grid of sampling times. The algorithm accepts **any** set of observation points \(T_1,\dots,T_m\) and produces the exact values of
\(N(T)\), \(A(T)\), \(L(T)\), \(\Lambda(T)\), and \(w(T)\) at those times.

**Why it works**

- The realized sample path \(N(t)\) is **piecewise constant** and changes **only** at event times.
- The area update between any two adjacent times \(\tau_1 < \tau_2\) is exact:
  \[
  A \;\mathrel{+}=\, N \cdot (\tau_2 - \tau_1),
  \]
  regardless of how \(\tau_1,\tau_2\) are spaced. No trapezoids or interpolation are needed.
- Changing the set of observation times only changes **which points you report**; it does **not** change the underlying sample path or the integrals computed between events.

**Practical notes**

- Inputs may be unsorted; we sort both `events` and `sample_times` internally.
- Duplicate observation times are allowed; the second copy will report the same values.
- If an observation time equals the window start \(t_0\), then \(L\) and \(\Lambda\) have a zero elapsed time and are returned as `NaN` by design.
- For **calendar buckets** (day/week/month/quarter/year), you only need the **bucket boundaries**. Adding interior observation points **does not** change per-bucket aggregates because
  \[
  A_{\text{bucket}} = A(T_i) - A(T_{i-1}), \quad
  \mathrm{Arrivals}_{\text{bucket}} = \mathrm{Arrivals}(T_i) - \mathrm{Arrivals}(T_{i-1}).
  \]

**Complexity**

A single pass in \(O(\#\text{events} + \#\text{observations})\) time with \(O(1)\) extra state, independent of whether observations are regular or irregular.

# 12. Takeaways
- Your event log defines the sample path; sampling frequency does not change it.
- Exact integration between events gives unbiased, rate-independent metrics.
- Bucket aggregates are exact via differences at boundaries—no intra-bucket sampling needed.
- This is Little’s Law in practice: $w = L/Λ$, computed from a single pass over your events.