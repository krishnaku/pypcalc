---
title: "<strong>Measuring flow with sample paths</strong>"
subtitle: "<span style='font-size:1.2em;'>A deterministic approach</span>"
author: |
  Dr. Krishna Kumar  
  <a href="https://exathink.com"><em>The Polaris Advisor Program</em></a>
number-sections: true
figures-numbered: true
link-citations: true
toc-title: "Contents"
toc-depth: 2
figPrefix: "Figure"

---

## What is the "system"?

We tend to think of queueing systems in terms of things moving through space ---
queues form and drain as "items" in some process move from stage to stage. And
thus the mental picture we draw of the "system" is a sequence of things moving
from point A to B, periodically waiting in queues. Assembly lines, service
processes Kanban boards, etc. fit this model well, and so Little's Law is deeply
associated with the flow of things called items from some source to a
destination.

But we have been also emphasizing in this series that sample path analysis is a deterministic
approach that does not require queueing models or probability distributions. So
what kind of "systems" does it analyze? 

In Stidham's original proof of Little's Law [@stidham72] he used the term "
input-output" system which is technically correct in that it describes the kind
of "black box" analysis that we are going to find Little's Law very useful for.

But we need to be more precise. Sample path proofs show that Little's Law is a
theorem not about things moving through space, but about events — and their
effects — that overlap in time.

The core mathematical object that models this is called a *deterministic point
process*, and this is nothing more than a sequence of *timestamps* (think: an
event log) representing events of some sort that we are observing [^-deterministic]. 
We may attach some attributes called *marks* to each event, and
the resulting object is called a *marked point process* [^-mpp].

![A marked point process](../../assets/pandoc/mpp.png){#fig:mpp}

[^-deterministic]: Despite its name, this does not imply that the underlying processes 
    that generate these events are deterministic. This is a bit confusing, but it is an artifact of the history
    of this work. The point processes in question were generally considered to be single realizations
    of stochastic processes. So the word deterministic here means that the observations are deterministic, as are the
    techniques used to analyze the processes. But this also means that the techniques apply equally well to 
    deterministic and stochastic processes. 

[^-mpp]: 
    Formally, a **point process** is an ordered sequence of timestamps

    $$
    \{t_i : i \in \mathbb{N}\}, \quad 0 \leq t_1 < t_2 < t_3 < \dots
    $$

    Each $t_i$ is the occurrence time of the $i$-th event.
    
    In a marked point process, events have attributes in addition to their
    timestamps. These attributes are called *marks*.

    - Let $\mathcal{M}$ be a mark space (e.g., service times, item sizes,
      priorities).
    - Each event is represented as a pair $(t_i, m_i)$ where $t_i$ is the time
      of the event and $m_i \in \mathcal{M}$ is its mark.

    Thus, a **marked point process** is the sequence
    
    $$
    \{(t_i, m_i) : i \in \mathbb{N}\}, \quad 0 \leq t_1 < t_2 < \dots
    $$

In simple terms, a marked point process, shown in [@fig:mpp],  is a *timestamped log* of events, where
each log entry carries additional metadata - the marks.

- The timestamps capture **when** events happen.
- The marks let us attach metadata to the event: ID, class, duration, workload, cost,
   etc.

From this, we can construct _sample paths_ of derived quantities like presence,
workloads, and from these measure $L$, $\Lambda$, and $W$. These derived
quantities are called *processes* in the technical literature, and sample paths
are always defined in terms of these derived processes [^-domain-definition]. 

[^-domain-definition]: In El-Taha and Stidham [@eltaha1999] the domain of sample path analysis is defined as "
processes with embedded point processes". This simply says that there is an
underlying event log and we are analyzing the time-varying behavior of certain
kinds of functions we extract from this log.

The key point is that the domain of sample path analysis should be very familiar
to anyone working with operational data: these are simply *event logs* from
processes we observe. In today's data-rich operational environments, they are
everywhere. Thus our starting point has shifted: instead of the abstract world
of queueing systems and probability distributions, we begin with the *real-world
logs of operational processes*.

This framing has also moved the domain purely to one of _observed_
behavior of processes, without any need to consider the internal structure of
the systems that generate that behavior. This clean separation between
*structure* and *behavior*, enabled by sample path analysis, will be crucial
when analyzing traces from complex systems where presupposing a structure
is often misleading or even impossible.

The final thing to note is that Little's Law and its generalizations are simply
*one kind of result* we can obtain from sample path analysis. Once we understand
the core ideas in sample path analysis as applied to Little's Law, this sets the
stage for a general approach to analyzing marked point processes that yields many more
useful results. These are all discussed in much greater detail in El-Taha and Stidham
(*Sample-Path Analysis of Queueing Systems*, 1999) [@eltaha1999].

In this series, we will use Little's Law as our focusing use case, but the same
sample-path concepts apply much more broadly, giving us a general method for
reasoning about a broad class of operational data.

## Processes and Sample Paths

In stochastic process theory, a process is defined as a collection of random
variables: time-varying values drawn from some probability distribution, or
outcomes from a system with random behavior. In that setting, a sample path is a
single realization of a process. In our case, since we are focusing on a single
sample path, we do not care whether the process is stochastic or deterministic.
In practice, we can think of a process as a time-varying function applied to an
event log in order to extract a sample path for analysis.

Let us consider some core examples to help solidify this intuition. The
simplest, and in many ways the most important, process we can define over a
point process is the **counting process**. It is defined as

$$
N(t) = \#\{\, i : t_i \leq t \,\}, \quad t \geq 0
$$

Put simply, $N(t)$ gives the total number of events observed up to time $t$. As
shown in [@fig:counting-sample-path], each realization of $N(t)$, obtained by
applying this function to an event log, is a **sample path**: a non-decreasing,
integer-valued, right-continuous function of time.

![A sample path for the counting process $N(t)$](../../assets/pandoc/counting_process_sample_path.png){#fig:counting-sample-path}

As a very straightforward instance of applying sample path analysis, El-Taha and
Stidham [@eltaha1999] show the well-known result that the long-run arrival rate
of items to a queue is equal to the reciprocal of the long-run average
interarrival time, provided both limits exist. 

This is one of the simplest possible relationships between a long-run time
average (the arrival rate) and a sample average (the mean interarrival time). In
many ways, the proof of this claim provides the template for proving similar
relationships, such as Little's Law, so it can be instructive to understand it.

But our focus here is not on the proofs themselves, so we will not dwell on this
aspect further, and will jump straight to defining the kind of marked point
processes to which we can apply Little's Law [^-info-model].

[^-info-model]: Note that we have shifted focus from asking "what kind of system does Little's Law
apply to" toward asking "what kind of marks must a point process expose so that the quantities
in Little's Law are measurable."






## References