# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT
"""
## Introduction

We assume an externally defined domain $D$ with its own structure,
topologies, constraints, and semantics. While these aspects of the domain
influence the kinds of presence assertions that can be expressed over it,
the Presence Calculus itself remains domain-agnostic.

Apart from some weak assumptions about what constitutes a measurable quantity
in the domain, the calculus is solely concerned with
[presence](./presence.html) over $D$, and the constructs and
calculations derived from them.

A [presence](./presence.html) models the concept that “an element was present
continuously in a boundary from time $t_0$ to $t_1$, with a certain measurable value.”

### Elements and Boundaries

It is useful to distinguish Elements ($E$)
and Boundaries ($B$) as subsets of the domain $D$:

- Some entities act as "things" that are present (Elements).
- Others act as "places" or contexts in which presence occurs (Boundaries).

$$
E = \\\\{ e_1, e_2, \dots, e_n \\\\} \subset D
$$

$$
B = \\\\{ b_1, b_2, \dots, b_m \\\\} \subset D
$$

There are no constraints on what an element or boundary can be. These roles
are application-defined, context-dependent, and scoped to a particular set of
presence assertions under analysis.

The same domain entity may be an element in one presence
assertion and a boundary in another.


#### Examples

- In traffic network, the locations and
road segments of the road network might be natural boundaries and vehicles might be elements.

- In a business value network, the participants in the network would be natural boundaries and value exchanges
between the participants would be natural elements.

- In a customer relationship management context, the boundaries might be customer segments and elements might be customers
or prospects.

- In a process management context, the boundaries might be process states and the elements might be processing items.

- In an organizational design context, the organization units might be the boundaries and the elements might be job functions.

- In a software development context, a boundary might be code branch and an element might be a code change.

Please note that these are illustrative examples there may be other choices that can be made even in these same domains.

### Observers

In addition to elements and boundaries, we have a set of observers from the domain, who *assert* presences.
$$
O = \\\\{ o_1, o_2, \dots, o_n \\\\} \subset D
$$
Again there are no constraints on what an observer is other than that it is an entity in the domain.
it could be something that also appears as either an entity or a boundary in the same presence assertion
(reflexive assertions). It could also be a distinguished subset of entities in the domain.


In general, you are free to model elements, boundaries and observers as you wish, provided that
there are meaningful domain semantics you can assign to a statement
like "An observer $o$ asserted at time $t_2$ that an element $e$
was present in a boundary $b$ from time $t_0$ to $t_1$."

Elements, Boundaries and Observers are simply placeholders for entity roles in a presence assertion.

Indeed, the utility of the calculus only extends as far as one can
make inferences using the machinery of the calculus that have useful semantics when mapped back into the
domain $D$.

Therefore, modeling choices are critical.

## Entity Module

The connection between the domain and the calculus is established via the
`EntityProtocol`, which declares the minimal contract a domain entity in
$D$ must satisfy in order to participate in presence assertions over $D$ as an
element or a boundary.

The remaining classes in the module are various utility classes that are provided
to simplify integrating a domain model to the presence calculus.

"""
from __future__ import annotations

import uuid
from typing import Protocol, runtime_checkable, Dict, Any, Optional


@runtime_checkable
class EntityProtocol(Protocol):
    """
    The interface contract for a domain entity to participate in a presence assertion.

    Each entity requires only a unique identifier, a user-facing name.

    Optional metadata may be provided and exposes specific attributes of the domain
    entities that are relevant when interpreting or manipulating the results
    of an analysis using the machinery of the calculus.

    See `Entity` for an example of a concrete implementation.
    """
    __init__ = None  # type: ignore

    @property
    def id(self) -> str:
        """
        A stable, unique identifier for the entity.
        Used for indexing and identity.
        Defaults to a uuid.uuid4().
        """
        ...

    @property
    def name(self) -> str:
        """
        A user facing name for the entity, defaults to the id if None.
        """
        ...

    @name.setter
    def name(self, name: str) -> None:
        """Setter for name"""
        ...

    @property
    def metadata(self) -> Dict[str, Any]:
        """
        Optional extensible key-value metadata.
        """
        ...


class EntityMixin:
    """A mixin class that can be used to inject common shared behavior
    of objects satisfying the EntityProtocol  into existing domain entities.
    """

    def summary(self: EntityProtocol) -> str:
        """
        Return a human-readable summary based on id and metadata.
        """
        meta = getattr(self, "metadata", {})
        if not meta:
            return f"Element[{self.id}] name = {self.name} (no metadata)"
        formatted = ", ".join(f"{k}={v!r}" for k, v in meta.items())
        return f"Element[{self.id}] name = {self.name} {{{formatted}}}"


class EntityView(EntityMixin):
    """
    A view class that allows domain objects to behave like entities

    ```python
    class Customer:
        def __init__(self, id, name, segment):
            self._id = id
            self._name = name
            self._segment = segment

        @property
        def id(self):
            return self._id

        @property
        def name(self):
            return self._name

        @property
        def metadata(self):
            return {"segment": self._segment}
    ```

    You can wrap it with `EntityView` to use it with presence-related infrastructure:

    ```python
    customer = Customer("cust-001", "Alice Chen", "Enterprise")
    entity = EntityView(customer)

    print(entity.id)        # cust-001
    print(entity.name)      # Alice Chen
    print(entity.metadata)  # {'segment': 'Enterprise'}
    print(entity.summary()) # Element[cust-001] name = Alice Chen {segment='Enterprise'}
    ```
    """

    __slots__ = ("_id", "_name", "_metadata")

    def __init__(self, base: EntityProtocol):
        self._base = base

    @property
    def id(self) -> str:
        return self._base.id

    @property
    def name(self) -> Optional[str]:
        return self._base.name

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._base.metadata


class Entity(EntityMixin, EntityProtocol):
    """A default implementation of fully functional entity.

    ```python
    elements = [
        Entity(id="cust-001", name="Alice Chen", metadata={"type": "customer"}),
        Entity(id="cust-002", name="Bob Gupta", metadata={"type": "customer"}),
        Entity(id="pros-003", name="Dana Rivera", metadata={"type": "prospect"}),
    ]
    boundaries = [
        Entity(id="seg-enterprise", name="Enterprise Segment", metadata={"region": "NA"}),
        Entity(id="seg-smb", name="SMB Segment", metadata={"region": "EMEA"}),
        Entity(id="seg-dormant", name="Flight Risk", metadata={"status": "inactive", "last login": "2024-06-01"}),
        Entity(id="seg-prospect", name="Active Prospects", metadata={"status": "demo given"})
    ]

    for e in elements:
        print(f"Element: {e.summary()}")

    for b in boundaries:
        print(f"Boundary: {b.summary()}")
    ```
    """
    __slots__ = ("_id", "_name", "_metadata")

    # noinspection PyProtocol
    def __init__(self, id: Optional[str] = None, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        self._id: str = id or str(uuid.uuid4())
        self._name: str = name or self.id
        self._metadata: Dict[str, Any] = metadata or {}

    @property
    def id(self) -> str:
        return self._id

    # noinspection PyProtocol
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata

    def __str__(self) -> str:
        return self.summary()
