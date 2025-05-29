---
title: "Foundations of Presence Calculus: Signals, Measures, and Assertions"
author: "Presence Calculus Project"
date: 2025-05-29
---

# Overview

This document provides a formal foundation for the Presence Calculus. It distinguishes between signals and presences, defines presence assertions and measures, and derives the presence invariant from measure-theoretic principles. It also captures the epistemic stance of the framework and the dimensional consistency of its metrics.

---

# 1. Signals and Integrability

A **signal** is a measurable, real-valued function of time defined over element–boundary pairs:

$$
F: (e, b, t) \mapsto \mathbb{R}_{\ge 0}
$$

A signal must be **Lebesgue integrable** over any finite time interval $[t_0, t_1)$. That is:

$$
\int_{t_0}^{t_1} F(e, b, t) \, dt < \infty
$$

This ensures that a signal can induce a **presence measure** over time.

---

# 2. Presence and Mass

Given an integrable signal $F$, we define the **presence mass** over an interval $A \subseteq \mathbb{R}$ as:

$$
\mu_{e,b}(A) = \int_A F(e, b, t) \, dt
$$

This presence measure is **finitely additive** and defined over a topology of time intervals (typically half-open intervals). Presence is the **first-order metric** induced by the signal.

---

# 3. Presence Assertions

A **presence assertion** is an epistemic claim about presence over a bounded interval:

$$
p = (e, b, [t_0, t_1), m)
$$

where $m = \mu_{e,b}([t_0, t_1))$. Assertions are observer-relative and form the basic units of knowledge in the system.

---

# 4. The Presence Invariant

Let $W \subset \mathbb{R}$ be a finite observation window. Define:

- $M(W) = \sum_i \mu_i(W \cap I_i)$ — total presence mass
- $N(W)$ — number of presence assertions active in $W$
- $|W|$ — length of the interval

We derive:

- **Average density**: $H(W) = \frac{M(W)}{|W|}$
- **Average mass per presence**: $G(W) = \frac{M(W)}{N(W)}$
- **Incidence rate**: $\lambda(W) = \frac{N(W)}{|W|}$

Then:

$$
H(W) = \lambda(W) \cdot G(W)
$$

This is the generalized form of Little’s Law in the Presence Calculus.

---

# 5. Epistemic Foundations

A **system** is the evolving set of presence assertions about a domain. Its dynamics are not defined by state transitions, but by changes in the assertion set:

- As assertions are made, revised, or withdrawn, the system evolves.
- Higher-order metrics such as residence time and incidence rate reflect this evolution.
- Presences are **phenomenological**: they represent experienced structure, not just raw data.

---

# 6. Dimensional Analysis

| Quantity          | Formula                           | Units              |
|------------------|------------------------------------|---------------------|
| Signal $f(t)$    | –                                  | dollars             |
| Presence Mass $m$| $\int f(t)\,dt$                    | dollar-seconds      |
| Density $H$      | $M(W)/|W|$                         | dollars             |
| G                | $M(W)/N(W)$                        | dollars             |
| $\lambda$        | $N(W)/|W|$                         | 1/sec (dimensionless) |

---

# 7. Final Remarks

- Only integrable signals induce valid presences.
- Presences are finite samples of signals and provide the substrate for reasoning about flow.
- The invariant $H = \lambda \cdot G$ is a consistency condition that arises from this structure.

This measure-theoretic foundation enables principled modeling of temporal systems where flow, accumulation, and knowledge are central.