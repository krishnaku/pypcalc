
# Presence Calculus: Topology, Sheaf Semantics, and Matrix Representations

This document presents a mathematically coherent view of the Presence Calculus,
tracing its topological underpinnings and their expression through sheaf theory.
It addresses practical representations such as the presence matrix while ensuring
that all definitions are compatible with formal mathematical constraints.

We begin by defining the topology induced by presence assertions, then describe
how element trajectories arise as connected components. We show how the notion
of an observation window fits within this topological framework and explain the
relationship between presence matrices and the sheaf of presence assertions.




# Presence Assertions

The fundamental object of the Presence Calculus is the **presence assertion**.

A **presence assertion** is a 4-tuple:

$$
p = (e, b, t_0, t_1)
$$

where:
- $e \in E$ is an element (a thing that can be present),
- $b \in B$ is a boundary (a place or context),
- $[t_0, t_1) \subset \mathbb{R}$ is a half-open time interval during which $e$ is asserted to be present in $b$.

### The Space of All Potential Presences

The set of all *possible* presence assertions is the product space:

$$
\mathcal{P}_{\text{all}} = E \times B \times \mathbb{R} \times \mathbb{R}
$$

subject to the constraint that $t_0 < t_1$.

### The Set of Actual Presences

In any given system or model, only a subset of these possible tuples are asserted to hold. This subset is denoted:

$$
\mathcal{P}_{\text{obs}} \subset \mathcal{P}_{\text{all}}
$$

and is treated as given (e.g., from observation, logs, or domain assertions). The Presence Calculus operates entirely on this set of **actual presence assertions**.

### Characteristic Function View (Clarification)

While earlier formulations introduced a function:

$$
P : E \times B \times \mathbb{R} \times \mathbb{R} \to \mathbb{R}
$$

such a function should be interpreted, if used, as the **characteristic function** of the set $\mathcal{P}_{\text{obs}}$:

$$
P(e, b, t_0, t_1) =
\begin{cases}
1 & \text{if } (e, b, t_0, t_1) \in \mathcal{P}_{\text{obs}} \\
0 & \text{otherwise}
\end{cases}
$$

This representation is useful for certain forms of analysis or aggregation, but the presence assertion itself is fundamentally the **tuple** $(e, b, t_0, t_1)$, not the value of a function.

---

## Practical Interpretation

A presence assertion is a primitive fact: "Element $e$ was present in boundary $b$ continuously from time $t_0$ to $t_1$." No assumptions are made about how this assertion was derived—whether from physical sensors, logs, or logical inference. The Presence Calculus treats all such assertions as axiomatic inputs.
We will use the example below to illustrate how we define and construct the topology of presences assertions  over 
a domain. 

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/presence_topology_example.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 1: A set of presence assertions over a domain
  </div>
</div>

---


---


# Presence Topology

Let $D$ be the domain of entities and boundaries, and let presence assertions
be defined over the space $E \times B \times \mathbb{R} \times \mathbb{R}$,
where each presence assertion corresponds to a tuple $(e, b, t_0, t_1)$.

We define a topology $\mathcal{T}$ on this space by specifying a basis of
open sets. Each basis element is defined by a tuple of the form:

$$
U_{e,b,I} = \{ (e', b', t_0', t_1') \mid e' = e, b' = b, [t_0', t_1') \subset I \}
$$

where $e \in E$, $b \in B$, and $I = (a, b) \subset \mathbb{R}$ is an open
interval on the time axis.

The collection of all such $U_{e,b,I}$ for all $e$, $b$, and open intervals
$I$ forms a basis for the presence topology $\mathcal{T}$.

## Intuition

Each basis element isolates a specific element and boundary, and considers
all presence intervals entirely contained within a given time window. This
yields a natural notion of "local neighborhood" around a presence, and allows
us to define continuity, clustering, and flow across the space of presences.

## Use

This topology underpins definitions of co-presence, continuity, and
topological observables such as connected components, accumulation zones,
and persistence regions.


---


# Topological Basis for Presence Assertions

Based on the provided presence diagram, we define the topological basis over
the space $E \times B \times \mathbb{R} \times \mathbb{R}$ using the
Presence Calculus.

## Observed Presence Assertions

Each presence assertion corresponds to a 4-tuple $(e, b, t_0, t_1)$, where:
- $e$ is an entity (element),
- $b$ is a boundary,
- $[t_0, t_1)$ is the half-open time interval of presence.

From the diagram, we identify the following presence assertions:

| Element | Boundary | Interval    |
|---------|----------|-------------|
| e1      | B1       | [1, 6)      |
| e3      | B1       | [3, 10)     |
| e1      | B1       | [11, 13)    |
| e1      | B2       | [1, 6)      |
| e4      | B2       | [3, 10)     |
| e1      | B2       | [11, 13)    |

## Topological Basis Construction

We define a topology $\mathcal{T}$ on the presence space by specifying a
basis of open sets. Each basis element is of the form:

$$
U_{e,b,I} = \{ (e', b', t_0', t_1') \mid e' = e, b' = b, [t_0', t_1') \subset I \}
$$

where $I \subset \mathbb{R}$ is an open interval containing the presence
interval $[t_0, t_1)$.

## Example Basis Elements

- $U_{e1, B1, (0.9,\ 6.1)}$
- $U_{e3, B1, (2.9,\ 10.1)}$
- $U_{e1, B1, (10.9,\ 13.1)}$
- $U_{e1, B2, (0.9,\ 6.1)}$
- $U_{e4, B2, (2.9,\ 10.1)}$
- $U_{e1, B2, (10.9,\ 13.1)}$

Each basis element defines a neighborhood around a specific element in a
specific boundary, over an open interval containing a full presence span.

## Interpretation

These basis elements allow us to reason about local neighborhoods of presence,
enabling analysis of continuity, clustering, transitions, and proximity in
presence space.


---


# Presence Matrix and Sheaf Restriction

In the Presence Calculus, the **presence matrix** is a concrete, computable
representation of presence assertions restricted to an **observation window**.

## Observation Window as an Open Set

An observation window is modeled as:

$$
U = E' \times B' \times [t_0, t_1)
$$

However, this is not open in the base topology $\mathcal{T}$ because:
- $[t_0, t_1)$ is not open in $\mathbb{R}$
- Arbitrary subsets $E' \subseteq E$ and $B' \subseteq B$ are not open unless $E$ and $B$ have the discrete topology

### Resolution

We interpret an observation window as being covered by open sets of the form:

$$
U_{e,b,(t_i - \epsilon, t_i + \epsilon)}
$$

This allows us to treat the presence matrix as a discrete approximation of a restriction of the sheaf to an open cover.

## Presence Matrix Definition

Let $\{t_i\}$ be a discrete time grid in $[t_0, t_1)$.
The matrix:

$$
P_{e,b}(t_i) =
\begin{cases}
1 & \text{if } (e, b, t_i) \text{ lies within a presence assertion} \\
0 & \text{otherwise}
\end{cases}
$$

encodes the observed presence at that time step.

## Summary

The presence matrix represents a **sampled restriction** of the sheaf over an open cover of a bounded domain. It enables computation of metrics like residence time, flow rate, and co-presence.


---


# From Topological Basis to Connected Components and Element Trajectories

## Connecting Presences

Two presence assertions are topologically connected if they:
- Share the same element $e$
- Have overlapping or adjacent time intervals
- Possibly occur in different boundaries

By linking such assertions through overlapping basis elements, we define connected components in the presence topology.

## Example

| Element | Boundary | Interval |
|---------|----------|----------|
| e1      | B1       | [1, 6)   |
| e1      | B1       | [6, 10)  |
| e1      | B2       | [10, 13) |

These form a single connected component for $e1$ across boundaries.

Other elements (e2, e3, e4) have isolated components.

## Element Trajectories

A **maximal connected component** of presence assertions for a given element defines its **trajectory** through time and space.

Trajectories can span multiple boundaries and time intervals and form the structural basis of presence dynamics.


---


# Topological Foundations and Sheaf Semantics of the Presence Calculus

## Observation Windows and Open Sets

Observation windows of the form $E' \times B' \times [t_0, t_1)$ are not open in the base topology. Instead, we use open covers formed from the basis:

$$
\mathcal{U} = \{ U_{e,b,(t_i - \epsilon, t_i + \epsilon)} \}
$$

## From Pre-sheaf to Sheaf

A **pre-sheaf** $\mathcal{P}$ over the space $X = E \times B \times \mathbb{R} \times \mathbb{R}$ is defined as:

- $\mathcal{P}(U)$ = all presence assertions $(e, b, t_0, t_1) \in U$
- Restriction: $\rho^U_V(S) = S \cap V$

### Sheaf Conditions

- **Locality**: If $s_i = s_j$ on overlaps, they represent the same global section
- **Gluing**: Compatible local sections $s_i$ over $U_i$ glue uniquely to a global $s \in \mathcal{P}(U)$


## The Gluing Operator

In the Presence Calculus, the **gluing operator** formalizes the process by which
local presence assertions—defined over overlapping open subsets of presence space—are
combined into a coherent, global trajectory.

This is the constructive content of the sheaf gluing axiom.

### Definition

Let $\mathcal{P}$ be the sheaf of presence assertions over the topological space
$X = E \times B \times \mathbb{R} \times \mathbb{R}$, and let $\{ U_i \}_{i \in I}$
be an open cover of $U \subseteq X$.

Suppose we have a family of local sections $\{ s_i \in \mathcal{P}(U_i) \}$ such that:

$$
\forall i, j \in I: \quad s_i|_{U_i \cap U_j} = s_j|_{U_i \cap U_j}
$$

Then the **gluing operator** is a function:

$$
\text{glue} : \prod_{i \in I} \mathcal{P}(U_i) \to \mathcal{P}(U)
$$

such that:

$$
\text{glue}(\{ s_i \}) = s \quad \text{where } s|_{U_i} = s_i \text{ for all } i
$$

This operator returns the unique global section $s$ whose restriction to each $U_i$
is the given local section $s_i$.

### Interpretation

The glue operator is the formal mechanism that reconstructs a continuous trajectory
from overlapping presence assertions that agree on their overlaps.

In implementation terms, it merges sequences of presence assertions—across time and
boundaries—into a **connected component**, or a **maximal presence trajectory**.


## Presence Matrix as a Sample

The presence matrix samples values from sections over neighborhoods in a grid covering a bounded domain.

It is not a literal sheaf section but a discrete approximation using open set evaluations.
