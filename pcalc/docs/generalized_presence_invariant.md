---
title: "<strong>The Presence Invariant</strong>"
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
---

<div style="text-align: center; font-size: 80%; margin-top: 3em;">
  © 2025 Krishna Kumar. All rights reserved.
</div>

## Setup: Two Orthogonal Measure Spaces

When generalizing from a single presence density function to a system of
presences, it is useful to think of presence as a quantity distributed over a
*product space* formed from two orthogonal domains:

- A **time domain** $T$, with a sigma-algebra $\mathcal{F}_T$ and a
  measure $\mu_T$. This may be the Lebesgue measure $\lambda$, a probability
  measure, or another $\sigma$-finite measure.
- A **signal domain** $S$, with a sigma-algebra $\mathcal{F}_S$ and a
  measure $\mu_S$, typically counting measure or a weighted variant over a
  discrete set.

We define the **product measurable space**:
$$
(T \times S, \mathcal{F}_T \otimes \mathcal{F}_S)
$$
and the **product measure**:
$$
\mu = \mu_T \otimes \mu_S.
$$

Let $f: T \times S \to \mathbb{R}_{\geq 0}$ be a measurable function
representing **presence density** over this joint domain.



## Total Presence Mass

The **total presence mass** accumulated across the full product space is defined
as:
$$
A = \\\iint_{T \times S} f(t, s)\\, d\mu_T(t)\\, d\mu_S(s).
$$

This integral assumes that $f$ is integrable under the product measure $\mu$,
i.e.:
$$
\\\iint |f(t, s)| \\, d\mu_T(t)\\, d\mu_S(s) < \\\infty.
$$

## Marginal Densities

We define marginal densities over each domain:

- **Presence per unit time**:
  $$
  D_T(t) = \\\int_S f(t, s)\\, d\mu_S(s).
  $$

- **Presence per signal**:
  $$
  D_S(s) = \\\int_T f(t, s)\\, d\mu_T(t).
  $$

Intuitively, marginalization distributes total presence mass along the time or
signal dimension by integrating out the other variable.

From a statistical lens, we are accustomed to thinking of these quantities as
averages. Time averages, however, often rely on assumptions like ergodicity or
stationarity of some underlying distribution over which the averages are
computed.

The measure-theoretic definition via marginal densities avoids these assumptions
and provides a structurally invariant description of presence across domains.
Rather than thinking of both quantities as averages, it is more general to treat
them as densities.

**Note:** The averages $\bar{D}_T$ and $\bar{D}_S$ are only well-defined when
$\mu_T(T)$ and $\mu_S(S)$ are finite. This ensures that the total presence mass
can be meaningfully distributed over each domain.

In the common case where the signal domain is finite or countable (e.g., a
discrete set of labeled signals) and the time domain is also quantized
(e.g., measured in ticks or time buckets as in the presence matrix),
$\bar{D}_S$ corresponds to the *average presence per signal*, while $\bar{D}_T$
captures the *average presence per unit time*.

These quantities let us view the system from either a signal-centric or
time-centric perspective, without changing the total mass. In either case, the
mass is obtained by integrating over a presence density function.

## Presence Invariant

Define the average presence densities:
$$
\\\bar{D}_T = \\\frac{A}{\mu_T(T)}, \quad \\\bar{D}_S = \\\frac{A}{\mu_S(S)}.
$$

Then the **generalized presence invariant** becomes:
$$
\\\frac{\\\bar{D}_S}{\\\bar{D}_T} = \\\frac{\mu_T(T)}{\mu_S(S)}.
$$

This expresses that the average presence densities in the time and signal
domains are **proportionally related**, and that the constant of proportionality
is the **ratio of the domain measures**.

## Interpretation of \( N/T \)

In many practical settings, particularly when working with discrete signal
domains, the signal measure $\mu_S$ is a counting measure. In such cases,
if $N = \mu_S(S_T)$ and $T = \mu_T(T)$, then the ratio:
$$
\\\frac{N}{T} = \\\frac{\mu_S(S_T)}{\mu_T(T)}
$$
represents the **ratio of the "sizes" of the sets** over which presence mass is
being distributed. That is:

> **Presence mass exists jointly over time and signal. When we marginalize that
mass, we can average it over the extent of time or the extent of signals. The
ratio \( N/T \) tells us how these marginal densities relate — it quantifies the
structural “rate” or “density of signals per unit time” induced by the
co-presence.**

This view aligns with the intuition of the Radon–Nikodym derivative, where
presence densities reflect the relative rate of one measure with respect to
another across their domain of interaction.

## Fubini's Theorem

If $f: T \times S \to \mathbb{R}$ is integrable over the product
measure $\mu_T \otimes \mu_S$, then:
$$
\\\iint_{T \times S} f(t, s) \\, d\mu_T(t)\\, d\mu_S(s)
= \\\int_T \left( \\\int_S f(t, s) \\, d\mu_S(s) \right) d\mu_T(t)
= \\\int_S \left( \\\int_T f(t, s) \\, d\mu_T(t) \right) d\mu_S(s).
$$

This justifies that presence mass can be **marginalized in either order**, and
confirms the internal consistency of the invariant.

## Summary

- $\mu_T(T)$: the extent of the presence interval in time
- $\mu_S(S)$: the extent of co-present signals or presences
- $A$: the joint mass over time and signal
- $\bar{D}_T$, $\bar{D}_S$: average densities over their respective domains

The invariant tells us:

> **Presence mass is conserved, and marginal densities are scaled by the ratio
of the measures of their support domains.** This allows us to move coherently
> between signal-normalized and time-normalized views of system behavior.
