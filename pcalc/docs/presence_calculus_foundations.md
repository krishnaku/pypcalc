---
title: "<strong>Presence</strong>"
subtitle: "<span style='font-size:1.2em;'><em>A measure-theoretic definition</em></span>"
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

**© 2025 Dr. Krishna Kumar, All rights reserved.**

## Measure structure on time

We assume that all reasoning takes place over the real line $\mathbb{R}$
equipped with the Borel $\sigma$-algebra $\mathcal{B}$ and the Lebesgue
measure $\lambda$. This gives us a standard measurable
space $(\mathbb{R}, \mathcal{B}, \lambda)$.

All presence reasoning in the Presence Calculus is grounded in this measurable
structure. When working with unbounded intervals or domains that may extend
to $\pm\infty$, we consider the extended real
line $\overline{\mathbb{R}} = \mathbb{R} \cup \{ -\infty, +\infty \}$.
While $\lambda$ is not defined on all subsets of $\overline{\mathbb{R}}$,
integration on $[a, +\infty)$ or $(-\infty, b]$ is well-defined for functions
that decay appropriately.

## Signals and measurability

Let

$$
F : (e, b, t) \to \mathbb{R}_{\geq 0}
$$

be a function that assigns a non-negative value to each element--boundary--time
triple. This is the general form of a presence density function also called
signal, in the Presence Calculus.

To define a _presence_ over such a function, we require that $F$ induces a
measure over $\mathbb{R}$:
that is, for any fixed pair $(e, b)$, the function $t \mapsto F(e, b, t)$ must
be measurable with respect to the Borel $\sigma$-algebra $\mathcal{B}$, and
Lebesgue integrable over all finite intervals.

This guarantees that for any interval $[t_0, t_1) \subset \mathbb{R}$, the
integral

$$
\mu(e, b, [t_0, t_1)) = \int_{t_0}^{t_1} F(e, b, t)\, dt
$$

is well-defined and finite.

We do not require that $F$ be jointly measurable over $(e, b, t)$, nor that $E$
and $B$ carry their own $\sigma$-algebras. It is sufficient
that $F(e, b, \cdot)$ be measurable for each fixed $(e, b)$.


## Topology of time over observaton intervals

Observation intervals are taken to be half-open intervals of the
form $[t_0, t_1) \subset \mathbb{R}$. The collection of all such intervals forms
a basis:

$$
\mathcal{B}_T = \{ [a, b) \mid a < b \in \mathbb{R} \}
$$

This basis generates a topology $\tau$ on $\mathbb{R}$ via:

$$
\tau = \left\{ \bigcup \mathcal{F} \mid \mathcal{F} \subset \mathcal{B}_T \right\}
$$

This topology is equivalent to the standard topology on $\mathbb{R}$, since open
intervals $(a, b)$ and half-open intervals $[a, b)$ generate the same collection
of open sets under union.

This topological structure supports the finite additivity of presence mass by
ensuring that unions, intersections, and partitions of presence intervals
correspond to open sets in this topology, allowing the induced
measures $\mu_{e,b}$ to be consistently defined across composed regions of time.

## Finite additivity and induced measures

For each fixed $(e, b)$, the function $t \mapsto F(e, b, t)$ induces a measure
on $\mathbb{R}$ via:

$$
\mu_{e,b}(A) = \int_A F(e, b, t)\, dt \quad \text{for all } A \in \mathcal{B}
$$

This measure $\mu_{e,b}$ is finitely additive over measurable sets:
if $A$ and $B$ are disjoint and measurable,

$$
\mu_{e,b}(A \cup B) = \mu_{e,b}(A) + \mu_{e,b}(B)
$$

This follows from standard properties of the Lebesgue integral.

This ensures the presence accumulation recurrence is valid over entries in the
presence accumulation matrix. 