---
title: "Toward a General Theory of Presence: A Unified Analytic Framework for Flow, Time, and Structure"
author: "The Presence Calculus Project"
date: "2025"
---

# Introduction

The **Presence Calculus** is a measure-theoretic framework for modeling the accumulation, distribution, and transformation of "presence"—a generalization of flow—in systems that evolve across time and structure. It emerges as a unifying abstraction over deterministic, stochastic, and discrete flow systems, and subsumes a range of classical results in operations research, queueing theory, and stochastic process theory.

This document lays out the **conceptual and mathematical roadmap** for the Presence Calculus, with emphasis on its connections to:

- Little’s Law and its deterministic generalizations
- Miyazawa’s Rate Conservation Laws (RCL)
- Palm calculus in stochastic models
- Product measure spaces and Fubini's theorem
- Scale-invariant density conservation over co-presence domains

We argue that the Presence Calculus both **generalizes** and **reinterprets** these historical structures under a single, unified analytic lens.

---

# 1. Lineage of the Theory

## 1.1 From Little's Law to Deterministic Sample Paths

Little’s Law ($L = \lambda W$) began as a probabilistic identity relating queue length, arrival rate, and waiting time. In a landmark contribution, **Stidham (1974)** recast this law as a deterministic relationship over **time averages** along **sample paths**, eliminating the need for stationarity or ergodicity.

This shift made the law applicable to real-time systems and simulations, and served as the conceptual bridge from stochastic to **pathwise** reasoning.

## 1.2 Brumelle's Generalization

**Brumelle** extended this deterministic view to **arbitrary measurable functions** attached to arrivals and departures, laying the groundwork for generalized conservation laws over flow-related attributes (e.g. service time, workload, cost). This formulation anticipated the idea that *mass can be arbitrary*—a critical insight that the Presence Calculus formalizes precisely.

## 1.3 Miyazawa and Rate Conservation

**Miyazawa** introduced a more general class of **Rate Conservation Laws (RCL)**, particularly for queueing networks and marked point processes. His use of **Palm calculus** allowed for transitioning between time-based and entity-based expectations—what we now recognize as **orthogonal marginalizations** of flow.

Despite its power, Miyazawa’s formulation remained rooted in **stationary stochastic systems**, limiting its applicability to non-steady-state or deterministic domains.

---

# 2. Presence as a Product Measure Theory

## 2.1 Two Orthogonal Domains

Presence Calculus introduces the notion that **presence mass lives in a product space**:
- **Time domain** $T$, with measure $\mu_T$ (e.g. Lebesgue, counting, or probability)
- **Signal domain** $S$, with measure $\mu_S$ (e.g. entity count, probability mass, weighting)

A presence is a measurable function:
$$
f : T \times S \to \mathbb{R}_{\geq 0}
$$
with total presence mass:
$$
A = \\\iint_{T \times S} f(t, s)\\, d\mu_T(t)\\, d\mu_S(s)
$$

## 2.2 Marginalization and Co-Presence

This formulation naturally supports marginal views:

- Presence per unit time: $D_T(t) = \int_S f(t, s)\, d\mu_S(s)$
- Presence per signal/entity: $D_S(s) = \int_T f(t, s)\, d\mu_T(t)$

These marginals are structurally constrained by **Fubini’s Theorem**, which ensures:
$$
A = \\\int_T D_T(t)\\, d\mu_T(t) = \\\int_S D_S(s)\\, d\mu_S(s)
$$

This **density symmetry** is the heart of the presence invariant.

## 2.3 The Invariant

We define average densities:
$$
\\\bar{D}_T = \frac{A}{\mu_T(T)}, \quad \\\bar{D}_S = \frac{A}{\mu_S(S)}
$$

The **generalized presence invariant** asserts:
$$
\\\frac{\\\bar{D}_S}{\\\bar{D}_T} = \\\frac{\mu_T(T)}{\mu_S(S)}
$$

That is: **presence densities are proportionally related** by the **ratio of the measures** over which presence is distributed. This echoes Miyazawa’s RCL, but in a **fully measure-theoretic and domain-neutral form**.

---

# 3. Stochastic Specialization and Palm Duality

## 3.1 Probability Measures as a Special Case

By replacing $\mu_T$ or $\mu_S$ with **probability measures**, the entire presence machinery specializes to classical stochastic systems. This includes:

- Random arrival processes
- Marked point processes
- Empirical distribution modeling

Here, presence mass becomes **expected presence**, and the invariant becomes an **expectation identity**.

## 3.2 Palm Calculus as Marginal Reweighting

Palm calculus defines conditional expectations over events like arrivals. In the presence calculus, this conditioning arises **naturally** through marginal densities over product spaces.

Thus, **Palm probability is subsumed** by the presence framework—it becomes a special case of marginalizing a joint measure over co-presence.

---

# 4. Generalization and Novel Contributions

## 4.1 Beyond Steady State

Unlike classical queueing theory, the presence invariant holds over **arbitrary time intervals**, not just in steady state. This enables:

- Transient analysis
- Adaptive systems
- Flow behavior across dynamically shifting domains

This opens up modeling of systems where flow is **not ergodic**, **not Markovian**, and **not stationary**.

## 4.2 Multiple Invariants

Presence calculus supports **multiple invariants** based on:

- Different marginal projections
- Alternative measures (e.g., weighted roles, forecasted signals)
- Normalizations over cardinality, duration, or probability mass

Each invariant expresses a **conservation law** grounded in the geometry and measure structure of presence.

---

# 5. Summary and Roadmap

The Presence Calculus:

- Generalizes Little's Law and RCL into a measure-theoretic structure over \( T \times S \)
- Replaces stochastic assumptions with product measure formalism
- Unifies deterministic, probabilistic, and discrete systems under one analytic framework
- Captures both **steady** and **non-steady** behavior
- Makes Fubini—not Palm—a foundational tool
- Supports compositional, scalable reasoning in complex domains

This marks a shift from classical queueing theory to a **unified flow framework** capable of supporting modern systems modeling, simulation analysis, and intelligent flow control.

---

# Appendix: Glossary

| Term             | Meaning |
|------------------|---------|
| Presence Mass    | Integral of presence density over time × signal |
| Co-presence      | Simultaneous nonzero presence over time and signal |
| Product Measure  | Joint measure over $T \times S$ |
| Presence Invariant | Conservation law: $A = D_T \cdot \mu_T = D_S \cdot \mu_S$ |
| Fubini’s Theorem | Guarantees interchangeability of marginal integrations |
| Palm Calculus    | Conditional expectations over events (subsumed by marginal densities) |

