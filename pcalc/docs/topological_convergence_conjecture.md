# Conjectures on Sheaf Convergence in the Presence Calculus

This document introduces conjectures regarding the convergence behavior of presence assertions modeled as sheaves over topological domains. The conjectures aim to provide a topologically grounded understanding of when flow systems stabilize and how unbounded or incomplete presences affect this behavior.

## Background

In the Presence Calculus, a **presence assertion** is a tuple:

$$
p = (e, b, t_0, t_1)
$$

where:

- $e$ is an element,  
- $b$ is a boundary,  
- $t_0$ is the onset time,  
- $t_1$ is the reset time.

These presences are modeled as sections over open sets in a topological space $E \\\times B \\\times \\\mathbb{R}$. The goal is to understand how such systems behave as the observation window expands over time.

We define $\\\mathcal{T}_T$ as the topology on $E \\\times B \\\times [T_0, T_1)$, and $\\\mathcal{S}_T$ as the sheaf of presence sections over this topology.

## Epistemically Incomplete Presences

To handle presences with unknown start or end times, we introduce special values:

- $t_0 = \\\bot$ (unknown or infinite past)  
- $t_1 = \\\top$ (unknown or infinite future)

These encode epistemically incomplete assertions and are critical when discussing convergence and divergence.

Such assertions:

- Contribute partially to residence and incidence metrics.
- May intersect all future windows ($t_1 = \\\top$), thereby affecting convergence.
- Are treated as presences with **non-compact support**.

## Conjecture 1: Boundedness is Necessary for Convergence

A presence sheaf $\\\mathcal{S}_T$ is **divergent** if it contains any assertion with $t_1 = \\\top$.

**Conjecture:** Boundedness of all presence assertions is a **necessary** condition for convergence:

$$
\\\forall p \\\in \\\bigcup_T \\\mathcal{P}_T,\quad t_1 < \\\infty
$$

This ensures that all presences fully resolve within finite observation windows.

## Conjecture 2: Stabilization is Sufficient for Convergence

Let $\\\operatorname{res}_{T+\\\delta,T}$ be the restriction map:

$$
\\\operatorname{res}_{T+\\\delta,T}: \\\mathcal{S}_{T+\\\delta} \\\to \\\mathcal{S}_T
$$

**Conjecture:** If there exists $T^*$ such that for all $T > T^*$, these maps are isomorphisms, then the sheaf has **converged**:

- No new global sections appear.
- Existing global sections stabilize.

## Conjecture 3: Local Finiteness Required for Metric Convergence

Let $U \\\subseteq E \\\times B \\\times \\\mathbb{R}$ be any bounded open set.

**Conjecture:** The sheaf $\\\mathcal{S}_T$ supports meaningful metric convergence (e.g., residence time, incidence rate) only if:

$$
\\\forall U,\quad \\\text{the number of presence assertions intersecting } U \\\text{ is finite}
$$

This implies that the sheaf is **locally of finite type**.

## Summary

We propose that convergence of presence sheaves requires:

1. **Boundedness** — no presence persists indefinitely.  
2. **Stabilization** — restriction maps stabilize global sections.  
3. **Local Finiteness** — only finitely many presences intersect any bounded region.

These conditions together characterize when a flow system modeled in the Presence Calculus can be said to converge topologically. Each is individually testable and contributes to a coherent foundation for reasoning about dynamic systems and evolving domains.

> These are currently proposed as **conjectures** pending formal proof.
