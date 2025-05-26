# -*- coding: utf-8 -*-
# Copyright (c) 2025 Krishna Kumar
# SPDX-License-Identifier: MIT

from typing import Generic, Optional, Tuple

import numpy as np


from .presence import Presence
from .presence_matrix import PresenceMatrix, PresenceMap


class PresenceInvariantDiscrete:
    """
    **A finite, scale-invariant, non-equilibrium version of Little's Law.**

    This class computes the components of The Presence Invariant of a presence matrix.

    The Presence Invariant states that for any *finite* interval `[start_time, end_time)` over the timescale `[t0, t1)`
    of a presence matrix, the following invariant condition holds.

    $$
        L = \Lambda \cdot w
    $$
    where

    - **$L$**: the average *presence* per unit time in the interval (see `avg_presence_per_unit_time`).
    - **$\Lambda$**: The *flow rate* - a finite approximation of *presence arrival/departure rate* (see `flow_rate`).
    - **$w$**: The *residence time* - a finite approximation of *presence duration* (see `metamodel.presence.Presence.duration`).

    This invariant extends the classical formulation of Little’s Law, an equilibrium-based identity, by establishing a
    conservation law (of presence) that remains valid across arbitrary timescales, and in non-linear, stochastic processes
    that operate far from equilibrium.

    It holds unconditionally for any presence matrix and finite window, and serves as a foundational
    construct for reasoning about flow in non-linear systems.

    The proof of this invariant is surprisingly simple and elementary.

    **Derivation:**



    Let $A$ be the total presence in the matrix over a finite time window `[start_time, end_time)` of $T$ time units.
    Let $N$ be the number of distinct presences that overlap the window.

    Let $R(p_i)$ be the portion of the duration of $p_i$ that overlaps the window. This is the *residence time* of $p_i$ in the window.

    The following diagram shows these quantities and the derivation.

    ![Presence Invariant](../assets/pcalc/presence_invariant.png)

    Then:

    $$
    A = \sum_{i=1}^{N} R(p_i)
    $$
    represents the sum of the elements in the presence matrix that foll in the time window `[start_time, end_time)`.

    $A = 12$ presence-time-units in our example.

    Average presence per unit time (see `avg_presence_per_unit_time`) is then:

    $$
    L = A/T
    $$

    $L = 3$ presences/time-unit in our example.

    $w = $ Average residence time (see `avg_residence_time`) is then:

    $$
    w = A/N
    $$

    $w=3 time units per presence in our example.

    We will define the flow rate as (see `flow_rate`):

    $$
    \Lambda = N/T
    $$

    $\Lambda = 1$ presence per time unit in our example.

    Combining these:

    $$
    L = A/T = A/N \cdot N/T = N/T \cdot A/N = \Lambda \cdot w
    $$

    So we get

    $$
    L = \Lambda \cdot w
    $$


    This identity—what we call the *Presence Invariant*—is equivalent to a fundamental construct used in
    all proofs of Little’s Law [1], and in particular, to one used by Stidham [2] to give a deterministic
    proof of Little's Law [3] (see `flow_rate`).

    Both the classical and the current presence-based versions are instances of *Rate Conservation Laws*
    (as described by Miyazawa [3]).

    However, the conserved quantities differ <sup>[1](#fn1)</sup>:

    - In classical Little’s Law, $L = \lambda \cdot W$ holds *at equilibrium*, using long run arrival/departure rate $\lambda$ and
    average presence duration $W$.
    - In the Presence Invariant, $L = \Lambda \cdot w$ holds *universally*, where $\Lambda$ and $w$ are finite window
    *approximations* of true arrival/departure rate and  presence duration.

    Stidham [2] proved the relationship between the quantities in the two versions and showed that
    the classical form of Little’s Law emerges as a limiting case of the finite-window identity
    *provided* the system approaches equilibrium as the window grows larger - ie the system is *convergent* in the long run.

    If the system is *divergent* in the long run, at least one of the three quantities grows without limit and
    the conservation law in the classical version does not hold.

    However, the presence invariant continues to hold regardless of whether the system is convergent or divergent.
    More details can be found under `flow_rate` and `avg_residence_time`.

    Since non-linear systems rarely reach or maintain equilibrium, the Presence Invariant provides a more robust
    and widely applicable conservation construct for causal reasoning about flow in such systems.

    <small>
        <a name="fn1"><strong>[1]</strong></a>
        Note that we have lowercase $\lambda$ and uppercase $W$ in the classical law, and uppercase $\Lambda$ and
        lowercase $w$ in the finite-window version, whereas $L$ remains the same in both.

        This reflects the fact that in the Presence Invariant, $\Lambda$ is an overestimate of $\lambda$, and $w$
        is an underestimate of $W$. Both identities refer to the *same* observable construct for $L$.
    </small>

    ## References

    1. **Little’s Law**
       Little, J. D. C. (2011). *Little’s Law as viewed on its 50th anniversary*. MIT.
       [https://people.cs.umass.edu/~emery/classes/cmpsci691st/readings/OS/Littles-Law-50-Years-Later.pdf](https://people.cs.umass.edu/~emery/classes/cmpsci691st/readings/OS/Littles-Law-50-Years-Later.pdf)

    2. **Stidham's Proof of Little's Law**
        Stidham, Shaler. Jr, *A last word on $L = \lambda \cdot W$*.Cornell University. 
        [https://pubsonline.informs.org/doi/epdf/10.1287/opre.22.2.417]

    3. **Miyazawa on Rate Conservation Laws**
       Miyazawa, M. (1994). *Rate conservation laws: a survey*. Science University of Tokyo.
       [https://www.rs.tus.ac.jp/miyazawa/pdf-file/Miya1994-QS-RCL.pdf](https://www.rs.tus.ac.jp/miyazawa/pdf-file/Miya1994-QS-RCL.pdf)


    """
    def __init__(self, matrix: PresenceMatrix):
        self.matrix = matrix
        """"""
        self.presences: list[Presence] = matrix.presences
        """Only presences that overlap the interval [t0, t1) are included in Presence Metrics.
        Note however that this may include presences that started before the interval or ended after the interval."""

        self.presence_map: list[PresenceMap] = matrix.presence_map
        """Only presences that overlap the interval [t0, t1) are included in Presence Metrics.
        Note however that this may include presences that started before the interval or ended after the interval."""

        self.ts = matrix.time_scale
        """The timescale of the presence matrix. This is the default 'window' over which all metrics are computed."""

    def _resolve_range(self, start_time: Optional[float], end_time: Optional[float]) -> tuple[float, float]:
        start = start_time if start_time is not None else self.ts.t0
        end = end_time if end_time is not None else self.ts.t1
        if start_time < self.ts.t0 or end_time > self.ts.t1:
            raise ValueError(
                f"Presence metrics are not defined outside the time scale of the presence matrix."
                f"Time scale = [{self.ts.t0}, {self.ts.t1})."
                f"Provided: [{start_time}, {end_time})"
            )
        return start, end


    def flow_rate(self, start_time: float = None, end_time: float = None) -> float:
        """
        The flow rate Λ is defined as:
            number of active presences in the matrix slice [:start_bin:end_bin] /
            number of time bins in the slice (end_bin - start_bin)

        Conceptually:
            Let N be the number of presences (rows) that are active (non-zero)
            in the matrix between start_time and end_time.

            Let T be the number of discrete time bins (columns) in that interval.

            Then:
                flow_rate = Λ = N / T

        Examples:
            - If 4 presences span a 6-bin window, flow_rate = 4 / 6 = 0.666...
            - If only one open-ended presence remains active over a 4-bin window, flow_rate = 1 / 4 = 0.25

        The flow rate is a finite-window estimate of both long-run arrival rate and departure rate.
        The precise relationship between flow rate, arrival rate, and departure rate is as follows:

            N = number of presences that started *before* start_time (see `starting_presence_count`)
                + number that started *in* the interval [start_time, end_time) (see `arrival_count`)

              — this is also called the cumulative arrivals into the window

            or equivalently:

            N = number of presences that *ended* in [start_time, end_time) (see `departure_count`)
                + number that ended *after* end_time (see `ending_presence_count`)

              — this is the departure contribution from the window

            These two decompositions of N are always equal; they just reflect different
            ways of expressing the same set of active presences.

        Intuitively, over a long enough window, if flow converges, most presences
        will start and end within the window, with fewer presences that partially overlap
        the interval at the beginning and end.

        This makes N an (over) estimate of true arrivals or departures over that interval.

        In other words, if flow through the boundary is asymptotically convergent over [start_time, end_time),
        then:
            flow_rate → arrival_rate → departure_rate

        When flow is fully convergent over the interval, then:
            flow_rate = arrival_rate = departure_rate

        This equality is one of the key conditions for *stable* flow through the boundary.

        On the other hand, if flow is not convergent over the interval, the delta between
        flow rate, arrival rate, and departure rate will be large — either increasing (divergent)
        or decreasing (convergent) over time.
        """
        _, number_of_presences, num_bins = self.get_presence_summary(start_time, end_time)
        return number_of_presences/num_bins if num_bins > 0 else 0.0

    def avg_residence_time(self, start_time: float = None, end_time: float = None) -> float:
        """
            Computes the average residence time over the interval [start_time, end_time).

            Let \$ P \$ be the set of presences that overlap the interval \$[\\text{start\\_time}, \\text{end\\_time})\$.

            The *residence time* \$ R(p) \$ is the time that presence \$ p \\in P \$ is active (overlaps) within that interval.

            Presence is computed using bin-weighted overlap, so contributions may be fractional if presences only
            partially cover a bin.

            The average residence time \$ w \$ is given by:

            \$$
            w = \\frac{\\sum_{p \\in P} R(p)}{|P|}
            \$$

            If no presences are active in the interval, \$ w = 0.0 \$.

            Note:
                There are four possible ways a presence can overlap a window [start, end):

                Ticks:     0   1   2   3   4   5   6   7
                           |---|---|---|---|---|---|---|
                Window:          |-----------|

                Case 1: Fully inside
                                     [=======]

                Case 2: Starts before, ends inside
                              [===========

                Case 3: Starts inside, ends after
                                     ===========]

                Case 4: Fully spans window
                              [====================]

                In all but Case 1, the window clips the presence, so the residence time
                is smaller than the presence duration. In Case 1, residence time equals presence duration.

                Intuitively, over a long enough window, if flow converges, most presences
                will start and end within the window (Case 1), with fewer presences that partially overlap
                the interval at the beginning and end or span the window (Cases 2–4).

                This makes \$ w \$ an (under)estimate of true presence duration.

                In other words, if flow through the boundary is asymptotically convergent over [start_time, end_time),
                then:
                    residence time → presence duration.

                When flow is fully convergent over the interval:
                    residence time = presence duration.

                On the other hand, if flow is not convergent over the interval, the delta between
                residence time and presence duration will be large — either increasing (divergent)
                or decreasing (convergent) over time.
        """
        total_presence_value, number_of_presences, _ = self.get_presence_summary(start_time, end_time)
        return total_presence_value / number_of_presences if number_of_presences > 0 else 0.0

    def avg_presence_per_unit_time(self, start_time: float = None, end_time: float = None) -> float:
        """
        Computes the average presence per time bin over the interval [start_time, end_time).

        Let \$ B \$ be the set of discrete time bins that cover the interval \$[\\text{start\\_time}, \\text{end\\_time})\$,
        and let \$ P(b) \$ denote the total presence across all presences within each bin \$ b \\in B \$.

        The average presence \$ L \$ is given by:

        \$$
        L = \\frac{\\sum_{b \\in B} P(b)}{|B|}
        \$$

        If the interval spans no bins, \$ L = 0.0 \$.

        Note:
            This is equivalent to computing the total presence by summing across rows (i.e., sum of all active presence
            durations we used to compute residence time) divided by the number of bins in the interval.

            Presence is computed using bin-weighted overlap, so contributions may be fractional if presences only
            partially cover a bin.

            Visually, this corresponds to summing presence *vertically* across bins:

            Example: presences over time bins

            Ticks:     0   1   2   3   4
                       |---|---|---|---|
            P1:         [=======]
            P2:             [=======]
            P3:                 [=======]

            Time bin 1:
                          ↑   (bin index 1 = [1, 2))
                          |---|
                      P1:   +
                      P2:   +
                      P3:   -
                    ---------
                    Sum:     2

            So:
                - Bin 1 has total presence = 2
                - If we consider bins 1 to 3 (i.e., [1, 4)), and total presence = 5.5
                - Then \$ L = 5.5 / 3 = 1.833... \$

            Conceptually, \$ L \$ reflects the average "load" or concurrency of presence in the system during the interval.

            This metric is the time-relative (per unit time) complements the element-relative residence time \$ w \$.
        """
        total_presence_value, _, num_bins = self.get_presence_summary(start_time, end_time)
        return total_presence_value / num_bins if num_bins > 0 else 0.0

    def get_presence_summary(self, start_time: float = None, end_time: float = None) -> Tuple[float, float, float]:
        """
            Computes the three core quantities from which all presence-based metrics are derived:

            - Total presence time \$ A \$ over the interval \$[\\text{start\\_time}, \\text{end\\_time})\$
            - Number of active presences \$ N \$ (i.e., rows overlapping the interval)
            - Number of time bins \$ T \$ covering the interval

            These three values form the basis for computing:

            - Average presence per time bin: \$ L = A / T \$
            - Average residence time per presence: \$ w = A / N \$
            - Flow rate: \$ \\Lambda = N / T \$

            This method is the common workhorse that underlies `avg_presence_per_time_bin`,
            `avg_residence_time_per_presence`, and `flow_rate`.

            ... and much of this work lives in `PresenceMap.presence_value_in`
        """
        start, end = self._resolve_range(start_time, end_time)
        start_bin, end_bin = self.ts.bin_slice(start, end)
        total_presence_value = 0
        number_of_presences = 0
        for pm in self.presence_map:
            if pm.is_active(start_bin, end_bin):
                total_presence_value += pm.presence_value_in(start_time, end_time)
                number_of_presences += 1

        return total_presence_value, number_of_presences, end_bin - start_bin

    def get_presence_metrics(self, start_time: float = None, end_time: float = None) -> Tuple[float, float, float]:
        """
        Computes all three components of the *Presence Invariant* for a finite window
        $[ \text{start\_time}, \text{end\_time} )$ within the timescale $[ t_0, t_1 )$
        of the PresenceMatrix.

        The Presence Invariant states that for *any* such interval:

            $$
            L = \Lambda \cdot w
            $$

        This invariant holds unconditionally and forms the foundation for reasoning about flow
        in non-linear systems—systems that often operate far from equilibrium. It generalizes
        the more familiar equilibrium-based Little’s Law by expressing a conservation law
        that applies across all time scales.

        - $L$: the *actual* average presence per unit time in the interval (this is not an approximation)
        - $\Lambda$: the *finite approximation* of presence arrival rate (flow rate)
        - $w$: the *finite approximation* of presence duration (residence time)

        **Derivation:**

        Let $ A $ be the total presence (i.e., the sum of active elements) in the matrix over the window.
        Then:

        $$
        A = \sum_{\text{rows}} \text{row totals} = \sum_{\text{columns}} \text{column totals}
        $$

        Let $ N $ be the number of distinct presences in the window, and $ T $ the window length.

        Then:

        $$
        L = \frac{A}{T} = \frac{A}{N} \cdot \frac{N}{T} = w \cdot \Lambda
        $$

        Hence:

        $$
        L = \Lambda \cdot w
        $$

        This identity—what we call the *Presence Invariant*—is a fundamental lemma used in
        all proofs of Little’s Law [1], and can be seen as its finite-window specialization.

        Both the classical and presence-based versions are instances of *Rate Conservation Laws*
        (as described by Miyazawa [2]). However, the conserved parameters differ:

        - In classical Little’s Law, $L = \lambda \cdot W$ holds *at equilibrium*, using true arrival rate $\lambda$ and average duration $W$.
        - In the Presence Invariant, $L = \Lambda \cdot w$ holds *universally*, where $\Lambda$ and $w$ are finite approximations.

        Since non-linear systems rarely reach or maintain equilibrium, the Presence Invariant provides a more robust
        and widely applicable conservation principle for causal reasoning about flow in such systems.

        ## References

            1. **Little’s Law**
               Little, J. D. C. (2011). *Little’s Law as viewed on its 50th anniversary*. MIT.
               [https://people.cs.umass.edu/~emery/classes/cmpsci691st/readings/OS/Littles-Law-50-Years-Later.pdf](https://people.cs.umass.edu/~emery/classes/cmpsci691st/readings/OS/Littles-Law-50-Years-Later.pdf)

            2. **Miyazawa on Rate Conservation Laws**
               Miyazawa, M. (1994). *Rate conservation laws: a survey*. Science University of Tokyo.
               [https://www.rs.tus.ac.jp/miyazawa/pdf-file/Miya1994-QS-RCL.pdf](https://www.rs.tus.ac.jp/miyazawa/pdf-file/Miya1994-QS-RCL.pdf)

        """
        total_presence_value, number_of_presences, num_bins = self.get_presence_summary(start_time, end_time)

        L = total_presence_value / num_bins if num_bins > 0 else 0.0
        Λ = number_of_presences / num_bins if num_bins > 0 else 0.0
        W = total_presence_value / number_of_presences if number_of_presences > 0 else 0.0

        return L, Λ, W




    def starting_presence_count(self, start_time: float = None, end_time: float = None) -> int:
        start, end = self._resolve_range(start_time, end_time)
        start_bin, end_bin = self.ts.bin_slice(start, end)

        return sum(
            1 for pm in self.presence_map
            if pm.is_active(start_bin, end_bin)
            #Note: here we must explicitly check the un-clipped
            # bin indices, since we are looking for end indices that fall outside the
            # window and even the matrix. So pm.end_bin is not the right test here.
            and self.ts.bin_index(pm.presence.onset_time) < start_bin
        )

    def ending_presence_count(self, start_time: float = None, end_time: float = None) -> int:
        start, end = self._resolve_range(start_time, end_time)
        start_bin, end_bin = self.ts.bin_slice(start, end)

        return sum(
            1 for pm in self.presence_map
            if pm.is_active(start_bin, end_bin)
            and (np.isinf(pm.presence.reset_time) or
                 # Note: here we must explicitly check the un-clipped
                 # bin indices, since we are looking for end indices that fall outside the
                 # window and even the matrix. So pm.end_bin is not the right test here.
                 self.ts.bin_index(pm.presence.reset_time) >= end_bin)
        )

    def arrival_count(self, start_time: float = None, end_time: float = None) -> int:
        """The number of presences that started within the window"""
        start, end = self._resolve_range(start_time, end_time)
        start_bin, end_bin = self.ts.bin_slice(start, end)

        return sum(
            1 for pm in self.presence_map
            if start_bin <= self.ts.bin_index(pm.presence.onset_time) < end_bin
        )

    def departure_count(self, start_time: float = None, end_time: float = None) -> int:
        start, end = self._resolve_range(start_time, end_time)
        start_bin, end_bin = self.ts.bin_slice(start, end)

        return sum(
            1 for pm in self.presence_map
            if np.isfinite(pm.presence.reset_time)
            and pm.is_active(start_bin, end_bin)
            and self.ts.bin_index(pm.presence.reset_time) in range(start_bin, end_bin)
        )


    def foo(self):
        r"""
            The key function of this class is to precisely compute the components of key rate conserved quantities
            tied to Presence under both equilibrium and non-equilibrium conditions.

            The key relationship that matters here is the Presence Invariant, which is rate conservation law
            for a PresenceMatrix under non-equilibrium condition.

            The Presence Invariant states that for *any* finite interval [start_time, end_time) over the timescale [t0, t1)
            of a Presence Matrix:

                    $$
                    L = \Lambda \cdot w
                    $$

                - $L$: the *actual* average presence per unit time in the interval (this is not an approximation)
                - $\Lambda$: a *finite approximation* of presence arrival rate (flow rate)
                - $w$: a *finite approximation* of presence duration (residence time)

                This invariant holds unconditionally and forms the foundation for reasoning about flow
                in non-linear systems—systems that often operate far from equilibrium. It generalizes
                the more familiar Little’s Law that holds under certain equilibrium conditions as a conservation law
                that applies across all time scales and non-equilibrium conditions.

                The proof of this invariant is surprisingly simple and elementary.

                **Derivation:**

                Let $ A $ be the total presence (i.e., the sum of active elements) in the matrix over the window.
                Then:

                $$
                A = \sum_{\text{rows}} \text{row totals} = \sum_{\text{columns}} \text{column totals}
                $$

                Let $ N $ be the number of distinct presences in the window, and $ T $ the window length.

                Then:

                $$

                L = \frac{A}{T} = \frac{A}{N} \cdot \frac{N}{T} = w \cdot \Lambda

                $$

                Hence:

                $$ L = \Lambda \cdot w $$

                The *Presence Invariant*—is a fundamental lemma used in
                all proofs of Little’s Law [1], and can be seen as its finite-window version.

                Both the classical and presence-based versions are instances of *Rate Conservation Laws*
                (as described by Miyazawa [2]). However, the conserved parameters differ:

                - In classical Little’s Law, $L = \lambda \cdot W$ holds *at equilibrium*, using true arrival rate $\lambda$
                and average duration $W$.
                - In the Presence Invariant, $L = \Lambda \cdot w$ holds *universally*, where $\Lambda$ and $w$ are finite
                window approximations.

                Since non-linear systems rarely reach or maintain equilibrium, the Presence Invariant provides a more robust
                and widely applicable conservation principle for causal reasoning about flow in such systems.

                References:

                1. **Little’s Law**
                   Little, J. D. C. (2011). *Little’s Law as viewed on its 50th anniversary*. MIT.
                   [https://people.cs.umass.edu/~emery/classes/cmpsci691st/readings/OS/Littles-Law-50-Years-Later.pdf](https://people.cs.umass.edu/~emery/classes/cmpsci691st/readings/OS/Littles-Law-50-Years-Later.pdf)

                2. **Miyazawa on Rate Conservation Laws**
                   Miyazawa, M. (1994). *Rate conservation laws: a survey*. Science University of Tokyo.
                   [https://www.rs.tus.ac.jp/miyazawa/pdf-file/Miya1994-QS-RCL.pdf](https://www.rs.tus.ac.jp/miyazawa/pdf-file/Miya1994-QS-RCL.pdf)
            """