# Presence Invariant and Miyazawa’s Rate Conservation Laws

## Introduction

The generalized presence invariant expresses the conservation of presence mass across time and signal domains, modeled as a product measure space. This framing closely parallels the structure of **Rate Conservation Laws (RCL)** in stochastic processes, particularly as formulated by **Masakiyo Miyazawa**.

This section explores that connection and demonstrates that the presence invariant is a generalization of RCL to arbitrary measurable presence distributions over joint domains.

---

## Miyazawa’s Rate Conservation Law (RCL)

In the context of stationary queueing systems and marked point processes, Miyazawa’s Rate Conservation Law expresses the idea that:

> The **rate at which a measurable event (e.g. arrivals, transitions, completions)** occurs at a boundary is equal to the **rate at which it leaves**, under stationary expectations.

Formally, if \( N(t) \) is a counting process on time, the rate is:
$$
r(t) = \lim_{\delta \downarrow 0} \frac{1}{\delta} \mathbb{E}[N(t + \delta) - N(t)].
$$

In a stable system, this incoming rate is matched by an outgoing rate:
$$
\mathbb{E}[\text{arrivals}] = \mathbb{E}[\text{departures}].
$$

Miyazawa extends this framework using **Palm calculus**, to express invariants such as Little’s Law in the form:
$$
\mathbb{E}[H] = \lambda \cdot \mathbb{E}[G],
$$
where:
- \( H \): number of entities in the system
- \( \lambda \): arrival rate
- \( G \): time spent in the system

---

## Product Measure Framing in Presence Calculus

In Presence Calculus, we consider a measurable function \( f: T \times S \to \mathbb{R}_{\geq 0} \), representing **presence density** over a **product space**:
- \( T \): time domain with measure \( \mu_T \)
- \( S \): signal domain with measure \( \mu_S \)
- Product measure space: \( (T \times S, \mu_T \otimes \mu_S) \)

Total presence mass is:
$$
A = \iint_{T \times S} f(t, s)\, d\mu_T(t)\, d\mu_S(s).
$$

We define:
- Marginal presence density over time: \( D_T(t) = \int_S f(t, s)\, d\mu_S(s) \)
- Marginal presence density over signals: \( D_S(s) = \int_T f(t, s)\, d\mu_T(t) \)

Average densities:
$$
\bar{D}_T = \frac{A}{\mu_T(T)}, \quad \bar{D}_S = \frac{A}{\mu_S(S)}.
$$

The **generalized presence invariant**:
$$
\frac{\bar{D}_S}{\bar{D}_T} = \frac{\mu_T(T)}{\mu_S(S)}.
$$

This structure ensures the consistency of marginal flow across time and signal dimensions — a density-conservation principle.

---

## Interpretation of \( N/T \) and Connection to RCL

Let:
- \( N = \mu_S(S_T) \): measure (or count) of signals co-present in time interval \( T \)
- \( T = \mu_T(T) \): measure of the time interval

Then:
$$
\frac{N}{T} = \text{co-presence rate} = \text{number of active signals per unit time}.
$$

This quantity behaves analogously to a **rate** in Miyazawa’s framework — the expected density of co-occurrence, averaged across one domain.

The presence invariant becomes a statement of **rate consistency**:
$$
\bar{D}_S = \bar{D}_T \cdot \frac{N}{T}.
$$

This mirrors:
$$
\mathbb{E}[H] = \lambda \cdot \mathbb{E}[G],
$$
in that both express mass (or expected count) as the product of:
- A **density** or **rate**, and
- A **measure of extent** (time, presence, or entity domain)

---

## Fubini's Theorem as a Foundation

Fubini’s Theorem ensures that presence mass can be decomposed and integrated in either order:
$$
\iint_{T \times S} f(t, s)\, d\mu_T(t)\, d\mu_S(s)
= \int_T \left( \int_S f(t, s)\, d\mu_S(s) \right) d\mu_T(t)
= \int_S \left( \int_T f(t, s)\, d\mu_T(t) \right) d\mu_S(s).
$$

This symmetry supports the invariant’s structure, just as it supports balance equations and flow conservation in RCL theory.

---

## Summary

- **Miyazawa’s RCL** ensures the conservation of expected flow through state boundaries in stochastic systems.
- **Presence Calculus** models presence mass over a product space \( T \times S \), where marginal densities reflect flow along time or signal dimensions.
- The **generalized presence invariant** ensures consistent density relationships:
  $$
  \frac{\bar{D}_S}{\bar{D}_T} = \frac{\mu_T(T)}{\mu_S(S)},
  $$
  which aligns structurally with the rate–expectation relationships in RCL.

Thus, the presence invariant is a **generalized, measure-theoretic conservation law**, of which Miyazawa’s RCL is a special case under stochastic stationarity.

