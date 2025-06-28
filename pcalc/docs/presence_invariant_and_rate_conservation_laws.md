---
title: "The Presence Invariant and Rate Conservation Laws"
subtitle: "<span style='font-size:1.2em;'>A measure-theoretic generalization</span>"
author: |
  Dr. Krishna Kumar
  <em>The Polaris Advisor Program</em>
number-sections: true
figures-numbered: true
link-citations: true
toc-title: "Contents"
toc-depth: 2
figPrefix: "Figure"
reference-section-title: "References"

---

<div style="text-align: center; font-size: 80%; margin-top: 3em;">
  © 2025 Krishna Kumar. All rights reserved.
</div>

# Introduction

The *Presence Invariant* fundamentally expresses the conservation of presence
mass across distinct, interacting domains: time and signals. This
measure-theoretic framing closely parallels the structure of *Rate Conservation
Laws (RCL)* in stochastic processes, particularly as formulated by Masakiyo
Miyazawa [@miyazawa94].

This document explores this connection, showing that the Presence Invariant
provides a *generalized, deterministic conservation law* for any measurable
presence distribution over joint domains. We demonstrate that Miyazawa's RCL
emerges as a specific instance of the Presence Invariant under the additional
assumptions of stochastic stationarity and the interpretation of quantities as
expectations.

The power of the generalized Presence Invariant, however, is that it requires no
such assumptions—as long as presence is defined over a product measure space,
the invariant holds by construction.

This perspective echoes Little’s observation [@little2011] that
Sigman [@sigman91] has shown the sample path proofs of the general form of
Little's Law, $H = \lambda G$, are equivalent to the rate conservation laws of
Miyazawa.

Our formulation of the Presence Invariant makes this correspondence explicit by
deriving the conservation law directly from measure-theoretic assumptions,
without requiring stochastic stationarity or expectation-based interpretations.

It generalizes both Little’s Law and Miyazawa’s Rate Conservation Law. Rather
than indexing presence by items or arrival processes, we define it over an
arbitrary product measure space and use Fubini's Theorem to show that all
quantities and relationships in both laws arise as consequences of marginalizing
an integrable density over this space.

This removes the need for stationarity, stochasticity, or item-based indexing.
The invariant holds by construction whenever presence is represented as an
integrable density over a product of measurable domains.


# Miyazawa’s Rate Conservation Law (RCL)

In the context of stationary queueing systems and marked point processes,
Miyazawa’s Rate Conservation Law (RCL) establishes a fundamental balance
principle. It asserts that:

> The *rate at which a measurable event (e.g., arrivals, transitions,
completions)** occurs at a boundary is equal to the **rate at which it leaves**,
> under stationary expectations.

Formally, for a counting process \( N(t) \), the rate is often defined as \( r(
t) = \lim_{\delta \downarrow 0} \frac{1}{\delta}
\mathbb{E}[N(t + \delta) - N(t)] \). In a stable system, this incoming rate is
matched by an outgoing rate: \( \mathbb{E}[\text{arrivals}] =
\mathbb{E}[\text{departures}] \).

Miyazawa's framework, often leveraging **Palm calculus**, provides a rigorous
foundation for invariants such as Little’s Law, typically expressed in the form:
$$\mathbb{E}[H] = \lambda \cdot \mathbb{E}[G],$$
where:

- \( H \): the (expected) number of entities in the system
- \( \lambda \): the (expected) arrival rate
- \( G \): the (expected) time spent in the system

A key aspect of this formulation is its reliance on **expected values** and *
*stochastic assumptions**, particularly **stationarity**, which implies that the
statistical properties of the process do not change over time.

# The Presence Invariant: A Measure-Theoretic Framework

The Presence Calculus adopts a measure-theoretic approach to define and quantify
presence, independent of stochastic assumptions. We model presence as a quantity
distributed over a **product space** formed from two orthogonal measurable
domains:

- A **time domain** $T$, equipped with a sigma-algebra $\mathcal{F}_T$ and a
  measure $\mu_T$ (e.g., the Lebesgue measure $\lambda$ for continuous time, or
  a counting measure for discrete time points).
- A **signal domain** $S$, equipped with a sigma-algebra $\mathcal{F}_S$ and a
  measure $\mu_S$ (typically a counting measure or a weighted variant over a
  discrete set of signals).

This leads to the **product measurable space
** $(T \times S, \mathcal{F}_T \otimes \mathcal{F}_S)$ and the **product measure
** $\mu = \mu_T \otimes \mu_S$.

Let $f: T \times S \to \mathbb{R}_{\geq 0}$ be a measurable function
representing the **presence density** over this joint domain. The function $f$
is assumed to be integrable under the product measure $\mu$.

## Total Presence Mass

The **total presence mass** ($A$) accumulated across the full product space (
e.g., over a finite observation window) is defined as the joint integral of the
presence density:
$$A = \iint_{T \times S} f(t, s)\, d\mu_T(t)\, d\mu_S(s).$$

## Marginal Densities

We define marginal densities by integrating out one of the variables:

- **Presence per unit time** ($D_T(t)$): This represents the total presence
  density across all signals at a specific point in time.
  $$
  D_T(t) = \int_S f(t, s)\, d\mu_S(s).
  $$
- **Presence per signal** ($D_S(s)$): This represents the total accumulated
  presence for a specific signal across the entire observed time interval.
  $$
  D_S(s) = \int_T f(t, s)\, d\mu_T(t).
  $$
  These marginal densities avoid reliance on stochastic assumptions like
  ergodicity or stationarity, providing a deterministic and structurally
  invariant description of observed presence.

## The Generalized Presence Invariant

By defining average presence densities over their respective domains:
$$\bar{D}_T = \frac{A}{\mu_T(T)}, \quad \bar{D}_S = \frac{A}{\mu_S(S)},$$
where $\mu_T(T)$ and $\mu_S(S)$ are the finite measures (extents) of the time
and signal domains, respectively.

The **generalized presence invariant** then states the proportional relationship
between these average densities:
$$\frac{\bar{D}_S}{\bar{D}_T} = \frac{\mu_T(T)}{\mu_S(S)}.$$
This fundamental relationship reflects the conservation of total presence mass,
ensuring that marginal densities are scaled by the ratio of the measures of
their support domains.

# The Link: Presence Invariant as a Generalization of RCL

The connection between the measure-theoretic Presence Invariant and Miyazawa's
stochastic RCL is established by recognizing how the components of the Presence
Invariant map to, and generalize, the terms
in $\mathbb{E}[H] = \lambda \cdot \mathbb{E}[G]$.

Let's define the **co-presence rate** as the ratio of the "size" of the signal
domain to the "size" of the time domain within an observation window:
$$\text{Co-Presence Rate} = \frac{\mu_S(S)}{\mu_T(T)}.$$
In many practical scenarios, where $\mu_S$ is a counting measure over $N$ active
signals and $\mu_T$ represents a time duration $T$, this becomes the
familiar $\frac{N}{T}$ ratio. This ratio quantifies the "density of signals per
unit time" induced by the co-presence.

Rearranging the generalized presence invariant, we get:
$$\bar{D}_T = \frac{\mu_S(S)}{\mu_T(T)} \cdot \bar{D}_S.$$
This form explicitly highlights the structural analogy:

* **$\bar{D}_T$ (Average Presence per Unit Time):** This term represents the
  overall density of presence in the system, averaged over time. It is directly
  analogous to $\mathbb{E}[H]$ (the expected number of entities in the system)
  in Little's Law, representing the "amount of stuff" present at any given
  moment.
* **$\frac{\mu_S(S)}{\mu_T(T)}$ (Co-Presence Rate):** This term is the
  generalized "rate" at which signals are co-present per unit of time. It is
  analogous to $\lambda$ (the arrival rate) in Little's Law, capturing the "rate
  of flow" into or through the system.
* **$\bar{D}_S$ (Average Presence per Signal):** This term represents the
  average total presence accumulated by each signal. It is analogous
  to $\mathbb{E}[G]$ (the expected time spent in the system or service time per
  entity) in Little's Law, representing the "average work" or "average duration"
  associated with each signal.

Thus, the Presence Invariant, expressed
as $\bar{D}_T = \left(\frac{\mu_S(S)}{\mu_T(T)}\right) \cdot \bar{D}_S$,
structurally mirrors Miyazawa's $\mathbb{E}[H] = \lambda \cdot \mathbb{E}[G]$.

## Bridging Measure Theory and Stochastic Processes

The fundamental link here is that **measure theory provides the bedrock for
probability theory and, consequently, stochastic process theory.**

* **Probability as a Measure:** A probability space is a specific type of
  measure space where the measure (probability) of the entire sample space is 1.
* **Expectations as Integrals:** The expectation of a random variable in
  stochastic process theory is defined as an integral with respect to a
  probability measure. For instance, $\mathbb{E}[X] = \int X dP$.
* **Stochastic Processes on Measure Spaces:** Stochastic processes often involve
  analyzing integrals (and thus expectations) over time or state spaces, which
  are themselves constructed on measure-theoretic foundations. Palm calculus,
  used by Miyazawa, relies heavily on advanced measure-theoretic concepts.

The Presence Calculus leverages general Lebesgue measures (or other $\sigma$
-finite measures) over arbitrary time and signal domains. This means its
invariants hold for any measurable function $f(t,s)$, regardless of whether $f$
arises from a stochastic process or exhibits stationary behavior.

**Miyazawa's RCL becomes a special case of the Presence Invariant when:**

1. **Quantities are interpreted as Expectations:** The averages $\bar{D}_T$
   and $\bar{D}_S$ are taken as expected values, typically over long-run
   averages or ensemble averages,
   i.e., $\bar{D}_T \to \mathbb{E}[H]$, $\frac{\mu_S(S)}{\mu_T(T)} \to \lambda$,
   and $\bar{D}_S \to \mathbb{E}[G]$.
2. **Stationarity Assumptions are Met:** The underlying stochastic process
   generating the "presence" is stationary, ensuring that the long-run averages
   or expectations are well-defined and constant over time. This is a critical
   condition for many forms of Little's Law and RCL.

## Fubini's Theorem as a Foundation

**Fubini's Theorem** is central to the consistency of this framework. It ensures
that the total presence mass can be computed by integrating over time first and
then over signals, or vice versa, without altering the result:
$$
\iint_{T \times S} f(t, s)\, d\mu_T(t)\, d\mu_S(s)
= \int_T \left( \int_S f(t, s)\, d\mu_S(s) \right) d\mu_T(t)
= \int_S \left( \int_T f(t, s)\, d\mu_T(t) \right) d\mu_S(s).
$$
This integral symmetry precisely supports the structure of the invariant,
allowing for coherent "marginalization" of presence mass and confirming the
internal consistency of flow conservation principles in both measure theory and,
by extension, RCL theory.

# Summary

The*Presence Invariant** is a powerful*generalized, measure-theoretic
conservation law** that applies to any measurable distribution of presence
across time and signal domains.

* It states that **presence mass is conserved, and marginal densities are scaled
  by the ratio of the measures of their support domains**.
* This framework provides a **deterministic (retrospective)** view of system
  behavior, as it directly describes the observed accumulation and distribution
  of presence mass over defined intervals, without requiring probabilistic
  assumptions or stationarity.
* **Miyazawa’s Rate Conservation Law (RCL)**, fundamental to stochastic queueing
  theory, can be understood as a *special case** of the Presence Invariant.
  When the presence densities are interpreted as expected values and the system
  operates under conditions of stochastic stationarity, the Presence Invariant
  reduces to the familiar expectation-based form of Little's Law and other RCLs.

Thus, the Presence Calculus offers a broader and more fundamental lens for
analyzing flow and conservation, applicable even in complex, non-stationary
systems where traditional stochastic models face significant limitations.