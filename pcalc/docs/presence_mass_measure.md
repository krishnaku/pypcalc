
---
title: "From Presences to Measures: Topological Foundations of Presence Mass"
---

# Overview

This document provides an intuitive and formal explanation of how we move from discrete **presences** (interval-based assertions of an entity at a boundary) to a continuous **measure** over time. It explains how slicing, overlap, and accumulation lead to the construction of a **presence mass measure**, and why this requires extending the topology to a **Borel σ-algebra**.

# 1. From Presences to Topology

Each **presence** is a tuple $(e, b, t_0, t_1)$, indicating that element $e$ is present at boundary $b$ over the interval $[t_0, t_1)$.

These intervals form a **basis** for a topology on time:

- Each presence interval $[t_0, t_1)$ is a basic open set.
- The set of all such intervals defines a topology $\mathcal{T}$ on $\mathbb{R}$.
- Finite unions of presence intervals correspond to regions of continuous presence.

This topology provides a combinatorial structure for reasoning about coverage, overlap, and flow.

# 2. From Topology to Content

To quantify presence, we assign a **content value** to any open interval $U$:

$$ 
\mu_0(U) = \sum_{p \in \mathcal{P}} \lambda(p \cap U) 
$$

where:

- $\mathcal{P}$ is the set of (closed) presences,
- $\lambda(\cdot)$ is the **Lebesgue measure** (i.e., length of time),
- $p \cap U$ denotes the intersection of presence $p$ with interval $U$.

This gives a **finitely additive** assignment of duration to regions of time, derived from residence time within the interval.

# 3. Why Content is Not Enough

The function $\mu_0$ is only defined on finite unions of basis elements (open intervals). But in practice, we want to:

- Slice time into arbitrary subintervals,
- Measure the mass in windows that are not aligned with any particular presence,
- Compare or integrate presence across irregular time structures.

This requires assigning values to **more general sets** than just open intervals.

# 4. The Role of the Borel σ-algebra

To support slicing, countable decompositions, and integration, we extend $\mu_0$ to a **Borel measure**:

- The **Borel σ-algebra** $\mathcal{B}(\mathbb{R})$ is the smallest collection of subsets of $\mathbb{R}$ that contains all open intervals and is closed under countable unions, intersections, and complements.
- We define the **outer measure**:

$$ 
\mu^*(A) = \inf \left\{ \sum_{i=1}^\infty \lambda(I_i) \mid A \subseteq igcup I_i 	ext{ with each } I_i 	ext{ open} 
ight\} 
$$

- Then extend $\mu_0$ to $\mu$, a **Borel measure**, using Carathéodory’s extension theorem.

This allows us to compute presence mass for any Borel-measurable subset of time, not just the ones explicitly defined by the original presence basis.

# 5. Presence Mass as a Measure

The resulting **presence measure** $\mu$ is defined as:

$$ 
\mu(U) = \sum_{p \in \mathcal{P}} \lambda(p \cap U) 
$$

for any Borel-measurable time region $U$. This satisfies:

- Non-negativity: $\mu(U) \geq 0$
- Additivity: $\mu(U_1 \cup U_2) = \mu(U_1) + \mu(U_2)$ if $U_1 \cap U_2 = \emptyset$
- Countable additivity over disjoint unions of Borel sets.

# 6. Interpretation

- The measure $\mu$ is **induced** by the topology of presence.
- It corresponds to a **density of presence mass over time**, with the total mass in a window representing the sum of residence times.
- The measure is **continuous** with respect to the underlying time structure but derived from discrete events.

# Summary

You begin with discrete presences that define a topology. By slicing and summing over intervals, you induce a content function. To support arbitrary slicing and integration, this must be extended to a measure over the Borel σ-algebra. The result is a fully defined presence mass measure $\mu$ that makes presence accounting mathematically robust and topologically grounded.
