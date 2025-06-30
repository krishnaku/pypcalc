---
title: "<strong>Convergence of systems of presence</strong>"
subtitle: "<span style='font-size:1.2em;'>A consequence of Little's Law</span>"
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

# Introduction

In this technical note, we formalize the relationship between convergence in the
presence calculus and the generalized form of Little’s Law, as originally proven
by Brumelle (1971) and refined through sample path techniques by Heyman and
Stidham (1980). 

This addresses a key gap in our informal exposition: while we
introduced the convergence conditions, and appealed to the general form of
Little's Law for proof, we did not make the connections explicit.

Here, we explicitly bridge that gap by mapping the concepts in the presence
calculus to those in the general form of Little's Law and make clear the
relationships between the two.

In the rest of this document, when we say Little's Law it should be assumed that
we are referring to the general version discussed here.



# Generalized Little’s Law

The generalized form of Little’s Law is concerned with a countable collection of
time-varying functions that represent the activity or occupancy of individual
items in a system over time. Let each item $i$ have an associated function
$f_i(t)$ defined for $t \geq 0$, such that:

$$
\int_0^\infty |f_i(t)| \, dt < \infty
$$

and for some finite $l_i > 0$,

$$
f_i(t) = 0 \quad \text{for} \quad t \notin [t_i, t_i + l_i]
$$

In other words, each $f_i(t)$ is a function of compact support with a finite
integral. These functions describe the temporal footprint or participation
profile of item $i$, capturing its influence on the system while it is "active"—
for example, time spent in a queue, time holding a resource, or time
contributing to some measurable system state.

This formulation originated as a generalization of classical queueing models:
rather than simply recording the arrival and departure times of items, it allows
us to associate an arbitrary time-varying function with each item’s time in the
system. This enables a more flexible description of occupancy-like behavior,
including partial participation, weighted influence, or overlapping resource
use.

It is not hard to see that the notion of *presence* in the presence calculus is
a close generalization of this same idea. The key difference lies in emphasis:
while the classical formulation aims to derive steady-state relationships like
$H = \lambda \cdot G$, the presence calculus takes *presence mass*—the values of
these integrals over finite time windows—as a foundational primitive of the
framework.

From this base, we derive not only long-run behavior but also a rich vocabulary
for describing the dynamics of systems in non-equilibrium states. Convergence is
just one property of interest; divergence and metastability are equally
important in understanding the real-world behavior of complex systems.

Nevertheless, when the system *does* converge, the identity
$\Delta = I \cdot \bar{M}$ stated in our earlier exposition is not an empirical
observation—it is a direct consequence of the generalized Little’s Law presented
here.

To prove this we need to show that our definitions in the presence calculus are
isomorphic to those in this theorem

Lets start with the definitions of the key quantities in Little's Law. 

- $G_i$, the integral of each function:

$$
G_i = \int_0^\infty f_i(t) \, dt, \quad i \geq 1
$$

- $H(t)$, the cumulative instantaneous value of each function:

$$
H(t) = \sum_{i=1}^\infty f_i(t), \quad t \geq 0
$$

From these, define the limiting quantities:

$$
G = \lim_{n \to \infty} \frac{1}{n} \sum_{i=1}^n G_i, \quad H = \lim_{T \to \infty} \frac{1}{T} \int_0^T H(t) \, dt, \quad \lambda = \lim_{n \to \infty} \frac{n}{t_n}
$$

**Theorem:**

If $\lambda$ and $G$ exist and are finite, and if $l_i / t_i \to 0$ as
$i \to \infty$, then $H$ exists and:

$$
H = \lambda \cdot G
$$

This is the general form of Little's Law [@brumelle71], [@heyman80], [@little2011]. Please see Dr. Little's survey article [@little2011]
for an extensive discussion of this law, and its history. 


# Mapping to the Presence Calculus

We now map each element of the theorem above to its counterpart in the presence
calculus.

## Signals and Functions

In the presence calculus, the system is composed of a (possibly infinite) set of
signals indexed by $(e, b)$ — each representing the interaction of an element
$e$ with a boundary $b$. Each such signal is associated with a **presence
function** $P_{(e,b)}(t)$, which records its temporal contribution at time $t$.

This maps directly to the $f_i(t)$ functions in the classical theorem:
each $f_i(t)$ corresponds to a presence function $P_{(e,b)}(t)$.

## Integrability

The condition $\int_0^\infty |f_i(t)| \, dt < \infty$ ensures that each item
contributes a **finite total presence** over its lifespan. In the presence
calculus, we refer to this as *bounded signal mass*. This is a **technical
requirement only for convergence**. The presence calculus allows signals with
unbounded mass in general; we only enforce integrability when analyzing
asymptotic behavior like long-run presence density.

Thus, in the presence calculus:

- Presence functions are always measurable.
- Boundedness of the integral $\int P_{(e,b)}(t) \, dt$ is **only required**
  when we want $\bar{M}$ (mean presence per signal) to exist and be finite.

## Instantaneous Density

The function $H(t)$ in the theorem aggregates the instantaneous contributions of
all $f_i(t)$. In the presence calculus, the analog is:

$$
\delta(t) = \sum_{(e,b)} P_{(e,b)}(t)
$$

We define long-run presence density as:

$$
\Delta = \lim_{T \to \infty} \frac{1}{T} \int_0^T \delta(t) \, dt
$$

So:

$$
\Delta = H
$$

## Average Presence per Signal

Define:

$$
\bar{M} = \lim_{T \to \infty} \frac{1}{N(0,T)} \sum_{(e,b)} \int_0^T P_{(e,b)}(t) \, dt
$$

This matches the limiting average of $G_i$:

$$
G = \lim_{n \to \infty} \frac{1}{n} \sum_{i=1}^n G_i
$$

So:

$$
\bar{M} = G
$$

## Signal Incidence Rate

The classical limit $\lambda = \lim_{n \to \infty} n / t_n$ expresses the
asymptotic rate at which functions $f_i$ arrive in time. In the presence
calculus, the equivalent is:

$$
I = \lim_{T \to \infty} \frac{N(0, T)}{T}
$$

This is the **incidence rate** of signals — the average number of signal onsets
per unit time.

Thus:

$$
I = \lambda
$$



## Unified Statement

Substituting these mappings:

$$
\Delta = I \cdot \bar{M}
$$

This is the **presence calculus** analog of the generalized Little’s Law.

[^F-general-form]: The classical form $H = \lambda \cdot G$
becomes $\Delta = I \cdot \bar{M}$ in the presence calculus. The correspondence
is exact under the mapping $H \mapsto \Delta$, $\lambda \mapsto I$,
and $G \mapsto \bar{M}$.



## Technical Condition: $l_i / t_i \to 0$

The theorem requires that $l_i / t_i \to 0$ as $i \to \infty$. This means that
the duration of each function $f_i$ must become small relative to its arrival
time.

In presence calculus terms, this ensures that **signals do not overlap
indefinitely with later-arriving signals**, which could distort the time-based
averages.

Equivalently, it ensures that:

- The support of $P_{(e,b)}(t)$ becomes **localized** in time.
- Signals arriving later do not have arbitrarily long durations.

**Importance:** This condition is required only to **guarantee** that the
product of limits equals the limit of the product. If one only wants to reason
about the existence of $\Delta$, $I$, or $\bar{M}$ independently, this condition
is not necessary.


# Summary

We restate a general convergence law for systems of presence:

Theorem (Presence Calculus version of Little’s Law):*  
Suppose the following limits exist and are finite:

 - Long-run incidence rate:  
     $$
     I = \lim_{T \to \infty} \frac{N(0,T)}{T}
     $$

- Average presence per signal:  
    $$
    \bar{M} = \lim_{T \to \infty} \frac{1}{N(0,T)} \sum_{(e,b)} \int_0^T P_{(e,b)}(t) \, dt
    $$

 and assume the technical condition that presence durations become vanishingly
 small
 relative to arrival time:

$$
 \text{duration}_{(e,b)} / \text{onset}_{(e,b)} \to 0
 $$

 Then the long-run presence density exists:

$$
\Delta = \lim_{T \to \infty} \frac{1}{T} \int_0^T \delta(t) \, dt
$$

and:

$$
 \Delta = I \cdot \bar{M}
$$

This makes precise the claim used in our introductory material and affirms that
the convergence of long-run presence density is a direct generalization of
Little’s Law. More importantly, it highlights when such a relationship does
*not* hold — namely, when the relevant limits do not exist, or the technical
conditions fail.

While the presence calculus derives much of its analytical machinery from the tools used
to prove Little's Law, it focuses on very complementary applications enabled by 
generalizing some of the underlying proof techniques. 

# References