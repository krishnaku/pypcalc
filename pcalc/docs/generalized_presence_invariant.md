# Generalized Presence Invariant via Product Measure Spaces

## Setup: Two Orthogonal Measure Spaces

Let us define presence as a quantity distributed over a **product space** formed from two orthogonal domains:

- A **time domain** $T$, with a sigma-algebra $\mathcal{F}_T$ and a measure $\mu_T$. This may be the Lebesgue measure $\lambda$, a probability measure, or another $\sigma$-finite measure.
- A **signal domain** $S$, with a sigma-algebra $\mathcal{F}_S$ and a measure $\mu_S$, typically counting measure or a weighted variant over a discrete set.

We define the **product measurable space**:
$$
(T \times S, \mathcal{F}_T \otimes \mathcal{F}_S)
$$
and the **product measure**:
$$
\mu = \mu_T \otimes \mu_S.
$$

Let $f: T \times S \to \mathbb{R}_{\geq 0}$ be a measurable function representing **presence density** over this joint domain.

---

## Total Presence Mass

The **total presence mass** accumulated across the full product space is defined as:
$$
A = \\\iint_{T \times S} f(t, s)\\, d\mu_T(t)\\, d\mu_S(s).
$$

This integral assumes that $f$ is integrable under the product measure $\mu$, i.e.:
$$
\\\iint |f(t, s)| \\, d\mu_T(t)\\, d\mu_S(s) < \\\infty.
$$

---

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

---

## Presence Invariant

Define the average presence densities:
$$
\\\bar{D}_T = \\\frac{A}{\mu_T(T)}, \quad \\\bar{D}_S = \\\frac{A}{\mu_S(S)}.
$$

Then the **generalized presence invariant** becomes:
$$
\\\frac{\\\bar{D}_S}{\\\bar{D}_T} = \\\frac{\mu_T(T)}{\mu_S(S)}.
$$

This expresses that the average presence densities in the time and signal domains are **proportionally related**, and that the constant of proportionality is the **ratio of the domain measures**.

---

## Interpretation of \( N/T \)

In many practical settings, particularly when working with discrete signal domains, the signal measure $\mu_S$ is a counting measure. In such cases, if $N = \mu_S(S_T)$ and $T = \mu_T(T)$, then the ratio:
$$
\\\frac{N}{T} = \\\frac{\mu_S(S_T)}{\mu_T(T)}
$$
represents the **ratio of the "sizes" of the sets** over which presence mass is being distributed. That is:

> **Presence mass exists jointly over time and signal. When we marginalize that mass, we can average it over the extent of time or the extent of signals. The ratio \( N/T \) tells us how these marginal densities relate — it quantifies the structural “rate” or “density of signals per unit time” induced by the co-presence.**

This view aligns with the intuition of the Radon–Nikodym derivative, where presence densities reflect the relative rate of one measure with respect to another across their domain of interaction.

---

## Fubini's Theorem (Context)

If $f: T \times S \to \mathbb{R}$ is integrable over the product measure $\mu_T \otimes \mu_S$, then:
$$
\\\iint_{T \times S} f(t, s) \\, d\mu_T(t)\\, d\mu_S(s)
= \\\int_T \left( \\\int_S f(t, s) \\, d\mu_S(s) \right) d\mu_T(t)
= \\\int_S \left( \\\int_T f(t, s) \\, d\mu_T(t) \right) d\mu_S(s).
$$

This justifies that presence mass can be **marginalized in either order**, and confirms the internal consistency of the invariant.

---

## Summary

- $\mu_T(T)$: the extent of the presence interval in time  
- $\mu_S(S)$: the extent of co-present signals or presences  
- $A$: the joint mass over time and signal  
- $\bar{D}_T$, $\bar{D}_S$: average densities over their respective domains

The invariant tells us:

> **Presence mass is conserved, and marginal densities are scaled by the ratio of the measures of their support domains.** This allows us to move coherently between signal-normalized and time-normalized views of system behavior.
