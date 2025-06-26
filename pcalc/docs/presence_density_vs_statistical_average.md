% Presence Density vs Statistical Average
% A Summary of Key Cases and Counterexamples
% June 26, 2025

# Introduction

In presence calculus, we use _presence density_ as the most fundamental unit of measurement of signals. 
In statistics we are usually working with sampled values of the underlying quantities. The sampling process
usually abstracts away the time that elapses between the samples and focuses on the frequency of the values themselves. 

So we have

- **Presence density**: a time-based measure of how much of a signal (or set of signals) is present at each moment, integrated over a time interval.
- **Statistical average**: a value-based measure that treats each observation as a sample and computes their unweighted average.

This document explores when these two notions are equal, when they diverge, and why.

# Case 1: Binary Presence — Uniform Duration

## Setup

Let \( N \) binary presence signals \( p_i(t) \in \{0, 1\} \) be defined over a total interval \( [0, T] \). Each signal is either present or absent at each time.

## Key Identity

We define:

- Presence density:
  $$
  \rho(t) = \frac{1}{N} \sum_{i=1}^N p_i(t)
  $$

- Time-averaged presence density:
  $$
  \bar{\rho} = \frac{1}{T} \int_0^T \rho(t)\,dt
  $$

- Per-signal average duration:
  $$
  \bar{d} = \frac{1}{N} \sum_{i=1}^N \frac{1}{T} \int_0^T p_i(t)\,dt
  $$

Since the integral and summation commute:
$$
\bar{\rho} = \bar{d}
$$

✅ In this case, **presence density average equals the statistical average** of the durations.

# Case 2: Binary Presence — Unequal Duration

If presence durations differ (some signals are present longer), the identity still holds because the time integral distributes linearly.

✅ As long as presence is binary, **equilibrium is defined by the match between presence density and statistical average**.

# Case 3: General Presence Functions

Let presence functions \( p_i(t) \in [0,1] \) vary over time. Presence mass is:

$$
m_i = \int_0^T p_i(t)\,dt
$$

- Time-averaged presence density:
  $$
  \bar{\rho} = \frac{1}{T} \int_0^T \left( \frac{1}{N} \sum_{i=1}^N p_i(t) \right) dt = \frac{1}{N} \sum_{i=1}^N \frac{m_i}{T}
  $$

- Statistical average of **durations**:
  $$
  \bar{d} = \frac{1}{N} \sum_{i=1}^N \text{duration}_i
  $$

❌ These two are **not equal** unless each presence function is binary and flat. Presence **mass ≠ duration** in the general case.

# Case 4: Piecewise Constant Signal (Zero-Order Hold)

Let a scalar time-varying signal be sampled at equal intervals:

- Samples: \( x_0, x_1, \dots, x_{T-1} \)
- Each value held over \([t, t+1)\)
- Presence density is constant on each interval:
  $$
  \bar{x}_{\text{presence}} = \frac{1}{T} \sum_{t=0}^{T-1} x_t
  $$
- Statistical average:
  $$
  \bar{x}_{\text{stat}} = \frac{1}{T} \sum_{t=0}^{T-1} x_t
  $$

✅ These are **equal** under uniform sampling with zero-order hold.

# Case 5: Linearly Interpolated Signal

Let samples be interpolated linearly:

- Between \( x_i \) and \( x_{i+1} \), define:
  $$
  f(t) = x_i + \frac{x_{i+1} - x_i}{\Delta t}(t - t_i)
  $$

- Presence average:
  $$
  \bar{f}_{\text{presence}} = \frac{1}{T} \sum_{i=0}^{N-1} \int_{t_i}^{t_{i+1}} f(t) dt = \frac{1}{T} \sum_{i=0}^{N-1} \frac{\Delta t}{2}(x_i + x_{i+1})
  $$

- Statistical average:
  $$
  \bar{f}_{\text{stat}} = \frac{1}{N} \sum_{i=0}^{N-1} x_i
  $$

❌ These values **differ** unless all sample values are equal or the slope between each pair is zero.

## Example:

```text
x = [1, 3, 2]
T = 2
```

- Presence average:

  $$
  \frac{1}{2} \left( \frac{1 + 3}{2} + \frac{3 + 2}{2} \right) = 2.25
  $$

- Statistical average:

  $$
  \frac{1 + 3 + 2}{3} = 2.0
  $$

# Summary Table

| Case                          | Presence Avg = Stat Avg? | Why?                                       |
|-------------------------------|---------------------------|--------------------------------------------|
| Binary, equal duration        | ✅                         | Equal weighting                            |
| Binary, unequal duration      | ✅                         | Integral distributes uniformly              |
| General-valued presence       | ❌                         | Mass ≠ duration                            |
| Zero-order hold (constant)    | ✅                         | Duration uniform, values held constant     |
| Linear interpolation          | ❌                         | Slopes shift presence density vs samples   |


# Presence Density and Statistical Average in the Presence Matrix

Once a signal is sampled into a presence matrix, each entry represents the accumulated presence mass over a window of fixed duration (typically unit-length). This structure allows us to compute average behavior over time directly from the matrix.

## Equivalence of Presence Density and Statistical Average (at matrix resolution)

Let the signal be sampled into \( T \) contiguous windows, producing values \( x_0, x_1, \dots, x_{T-1} \), where each \( x_i \) represents the average or total mass in window \([i, i+1)\).

We define:

- Presence density at matrix scale:
  $$
  \bar{\rho}_{\text{matrix}} = \frac{1}{T} \sum_{i=0}^{T-1} x_i
  $$

- Statistical average of the samples:
  $$
  \bar{x}_{\text{stat}} = \frac{1}{T} \sum_{i=0}^{T-1} x_i
  $$

These are clearly equal:

$$
\bar{\rho}_{\text{matrix}} = \bar{x}_{\text{stat}}
$$

This equivalence holds because both are computed from the same set of values — the average (or total mass) per window — and each window contributes equally.

> **At the resolution of the presence matrix, the long-run presence density is equal to the statistical average over sampled values.**

## But This Is Only True Modulo the Sampling Unit

This equality is relative to the **granularity of the presence matrix**. If you sample a signal daily and compute the average presence density across 10 days, it will equal the average of the 10 samples — but only at **daily resolution**.

If each "day" in your data consists of 24 hours of high-frequency variation, and the signal is not constant within those days, the **true average presence density at hourly resolution** will generally differ from the coarser daily average.

In short:

> **Presence density is resolution-dependent.**  
> Equating it with statistical averages assumes uniformity within windows — a condition rarely met in dynamic systems.

## Loss of Information in the Sampling Process

When we lift a signal into a presence matrix, we retain only aggregate behavior per window (e.g., total presence mass or average value). This process is **lossy**:

- It discards fine-grained variation within each window.
- It cannot recover timing of internal events or transitions.
- Different signals can yield the same presence matrix if their intra-window integrals are identical.

Thus, the presence matrix is a **scale-specific approximation** of the original signal. It provides tractable and meaningful summaries of flow behavior, but at the cost of resolution.

> **Presence matrices preserve mass and average, not microstructure.**

Understanding this tradeoff is essential when interpreting long-run averages or comparing systems at different timescales. Reasoning from the matrix must always be contextualized by the sampling unit used to construct it.

# Convergence in the Presence Matrix: Statistical vs Analytical

When we define convergence or divergence using the presence matrix, we are fundamentally working in a **discrete statistical setting**, not a continuous analytical one.

## Presence Matrix-Based Convergence

Let \( x_0, x_1, \dots, x_{T-1} \) be the presence masses (or densities) recorded over uniform intervals of duration \( \Delta t \).  
We define the **long-run average presence density** as:

$$
\bar{\rho}_T = \frac{1}{T} \sum_{t=0}^{T-1} x_t
$$

As \( T \to \infty \), we may observe:

- **Convergence**: if \( \bar{\rho}_T \to L \) for some stable value \( L \)
- **Divergence**: if \( \bar{\rho}_T \to \infty \), oscillates without limit, or does not settle

This is a form of **empirical convergence** — a running average over discretely sampled windows.

## Not a Continuous Limit

This form of convergence:

- **Does not reflect** pointwise convergence of a continuous function
- **Does not imply** that the underlying signal \( f(t) \) converges in any analytical sense
- **Does not see** what happens inside each window

Unless the sampling is dense enough and the signal is well-behaved (e.g., bounded variation), the presence matrix only provides a **coarse-grained convergence** profile.

## Interpretation

In this context:

> Convergence in the presence matrix means that presence behavior is **statistically stable** at a particular resolution.

It is analogous to convergence of sample means in statistics — **not** to limits of functions in analysis.

## Consequence

Reasoning about convergence or divergence from a presence matrix is meaningful for:

- Understanding long-run average behavior
- Detecting equilibrium at a sampling scale
- Diagnosing instability or accumulation over time

…but it must always be interpreted **in the context of the sampling resolution** and **not mistaken for fine-grained analytical limits**.


## Finite Additivity of Presence Matrix Values

A key feature of the presence matrix is that its entries are not arbitrary values — they are **measures** computed over time intervals.  
Each value represents the **presence mass** accumulated during a fixed-duration window:

$$
A(i, i+1) = \int_i^{i+1} f(t)\,dt
$$

These values are additive over disjoint, contiguous intervals:

$$
A(i, j) + A(j, k) = A(i, k)
$$

This property holds because integration defines a **finitely additive set function** over measurable intervals.

### Why This Matters

Finite additivity allows us to:

- Aggregate presence over time without ambiguity
- Define long-run averages in terms of accumulated mass
- Construct coherent accumulation matrices and invariants
- Ensure that total mass is preserved under interval composition

### Not True for Point Samples

If we instead had pointwise samples \( f(i) \), we would not be able to assert:

$$
f(i) + f(i+1) = \int_i^{i+2} f(t)\,dt
$$

unless the function \( f \) is known to be constant. Point values have no duration, and so **do not support additive composition across intervals** without additional modeling assumptions (e.g., constant interpolation).

# Why Presence Mass Is Fundamental: Invariants, Balance, and Sample Paths

One of the deepest motivations for building presence calculus on **presence mass** rather than point samples is that it allows us to state and prove invariant properties that rely on **flow, accumulation, and conservation over time**.

## The Role of Presence Mass in the Invariant

The **presence invariant** compares how much each signal contributes across locations or queues. It requires:

- That we can compute **mass contributions** per interval
- That we can compare mass totals across partitions
- That we can reason about **balance** over time and space

None of this is possible with raw point samples. Pointwise values have no duration and no composability. Without mass, there is no flow — and without flow, there can be no conservation law.

> Presence calculus is fundamentally built on the assumption that **signals have mass over time**.

## Analogy: Sample Paths vs Ergodicity

This distinction echoes a foundational divide in queueing theory:

- **Stidham’s sample path proof** of Little’s Law works because it uses cumulative **flow paths** over time — essentially integrating over real arrival and departure histories.
- **Little’s original probabilistic proof** relies on **ergodic assumptions** — that time averages and ensemble averages converge — without necessarily invoking flow structure directly.

In presence calculus:

- **Sample-path-style reasoning** becomes possible because we treat presence as a measure.
- If we used only point samples, we would be limited to **frequency-based reasoning**, requiring stronger probabilistic assumptions and losing the ability to assert flow-based invariants.

## Summary

> The presence invariant — and presence calculus as a whole — is only meaningful because presence is defined as an **accumulated, finitely additive measure** over time.  
> This gives us access to the machinery of flow, balance, and convergence, and explains why the invariant cannot even be stated in a purely sample-based framework.

This is not just a technical preference — it’s the reason presence calculus offers a richer and more composable foundation for reasoning about flow systems than purely sample-based models.



### Summary

> Presence matrix values are meaningful because they are **measures**, not samples.  
> This enables a calculus of flow that preserves total mass and supports rigorous interval-based reasoning — something that is not possible with raw pointwise observations alone.

# Conclusion

Presence density and statistical averages coincide **only in special cases**.  
In general, presence encodes **time-weighted structure**, while statistical averages encode **frequency-weighted samples**.

Understanding their divergence is key to interpreting flow systems, especially in intermittent, chaotic, or temporally skewed domains.
