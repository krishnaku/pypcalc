---
title: "<strong>Little's Law</strong>"
subtitle: "<span style='font-size:1.2em;'>A History</span>"
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

## Little's Law

Little’s Law began its life in the mundane world of operations management—as an
empirical regularity observed in retail stores, call centers, and other service
operations. It's a commonplace observation that stores get more crowded when
more customers come in and stay longer.

This leads to a mathematical relationship capturing this
phenomenon, one that was also observed empirically.

$$L = λW$$

where λ is the rate at which customers arrive, W is the average time a customer
spends in the store, and L is the average number of customers in the store.

> In a general setting, we imagine _items_ arriving and departing from a system,
> as observed over some time window, expressed in some unit of time (hours,
> days,
> etc).
>
> - λ is called the _arrival rate_ — the number of items arriving per unit time,
> - W is called the _average time in system_ — the average number of time units
> for which an item is present in the system,
> - L is called the _average number in the system_ — the average number of items
> present in the system per unit of time.

![A queuing system](../assets/pandoc/queueing_system.png){#fig:queueing-system}

[^-queueing-notes]: The "system" in this case includes both the arrival and
    service processes. Little’s Law applies to items that have arrived for service
    but have not yet completed it. In queueing theory, it is common to distinguish
    between items that are *in service* and those *waiting for service*. By
    convention, Little’s Law includes both groups in the definition of "in the
    system." 

    The quantities $L$ and $W$ therefore represent the average number of
    items in the system and the average time per item across the _union_ of these two
    sets. In the diagram, we show the arrival and service processes separately to
    reflect standard queueing theory notation and to emphasize that these are the
    processes for which Little’s Law assumes conditions like stationarity and
    ergodicity.

[@fig:queueing-system] shows a canonical queueing system [^-queueing-notes]. We
can see that Little's Law relates three distinct _kinds_ of averages:

- _L_ is a _time average_ — the number of items present in the system per unit
  of time,
- _W_ is an _item average_ — the average number of time units an item
  accumulates while present in the system,
- λ is a rate — a number of items per unit of time.

Notably, the denominator in the first average is a continuous quantity (time),
while the denominator in the second average is a discrete quantity (items), and
the third quantity is a rate relating the denominators of the other two
quantities. 

The law expresses the intuition that _the total time accumulated in a system_ by a
set of discrete [^-discreteness] items over a time window, when averaged _per item_, is
proportional to the average _number_ of _items_ present in the system over the
window. The constant of proportionality is the _rate_ at which items enter (or
leave) the system over the window.

[^-discreteness]: As we will see later, even discreteness of items is not
essential for the law to hold in the most general setting. The law has
generalizations to continuous input-output systems [@eltaha1999]. However, we will keep this
discrete item framing for now as this is the most familiar variant for Little's Law and makes 
many key ideas simpler to explain. 

The law was widely assumed to be true in operational settings and used without
proof because it was intuitive, could be empirically confirmed, and its symmetry
was appealing.

As we will see, the law is anything but obvious to prove mathematically in a
general setting. Answering this question rigorously has led to some deep results
that have proven very valuable in solving economically critical problems in a
variety of domains.

Much of the technical complexity in proving Little’s
Law arises from the challenge of relating a time average—measured over a
continuous interval—to a sample average over discrete items. These fundamentally
different types of averages are not directly comparable and require some
carefully constructed mathematical machinery to reconcile.

Examining the journey of its proofs and the generalizations they uncover,
reveals a foundational collection of physical and economic laws
governing the conservation of time-value in input-output systems.

Our goal in this post is to demystify the technicalities and argue that much of
this law's power remains untapped. We contend that, especially in software
product development and engineering, a deeper understanding of these concepts is
essential to transforming operations management from a collection of anecdotes
and informal practices into a mathematically grounded science.

### Proofs and generalizations of Little's Law

Dr. John C. Little [@little1961] gave the first mathematical proof in 1961 using
techniques from queueing theory and probabilistic analysis. His proof involved
assumptions including steady state conditions and stationary probability distributions, 
that were largely true in the operational settings under which the
law was being applied, and thus the equation—and the assumptions under which Dr.
Little proved it—became known as Little's Law

It found applications in manufacturing, computer systems performance analysis,
service operations management, and countless other operational settings. It is
considered a foundational law akin to Newton’s law _F = m·a_ in these domains
[@hopp2000] [^-throughput-form].

[^-throughput-form]: The operating conditions under which Little's Law is
    typically applied in manufacturing settings are considerably stricter and lead
    to the throughput-centered form described in [@hopp2000]:
    $$
    \text{Throughput} = \frac{\text{WIP}}{\text{Cycle Time}}.
    $$

    This version of Little's Law holds only under more stringent assumptions, but
    these are often realistic in repetitive manufacturing environments, making it
    reasonable to treat this form as the default:
    
    - Items have uniform cycle times.
    - The arrival rate is below the maximum capacity of the service process.
    - The system is observed in steady state—startup and shutdown transients are
    excluded.
    
    Under these assumptions, the steady-state throughput equals the arrival rate,
    and this version becomes a simple rearrangement of the standard form of Little's
    Law.
    
    However, while this throughput form is often taken as the default in Lean
    software development [@vacanti2015], the original assumptions rarely hold in
    most software delivery contexts. Therefore, we will focus primarily on the arrival-rate version of Little's Law
    in this post. The throughput form remains valid under steady-state conditions,
    but the definition of "steady state" in a software context is far more nuanced
    and requires careful qualification.

Since Dr. Little's original proof, the result has been significantly generalized
by researchers [@stidham72], [@brumelle71], [@heyman80], [@sigman91],
[@miyazawa94], [@eltaha1999].

> It is now known to be a purely _deterministic_ result
> independent of queueing and probability theory, and applicable to both
> stochastic and deterministic processes.

These later generalizations make Little’s Law—and the techniques used to prove
its general forms—very relevant to the analysis of non-linear systems far
removed from the original application areas that Dr. Little’s formulation
targeted. In particular, it is highly relevant to the analysis of complex
adaptive systems such as those commonly encountered in software product
development and engineering.

However, due to the strong association of the original formulation with
assumptions about stochastic processes—and the extensive applications in
repetitive manufacturing and service contexts—it is often assumed that Little’s
Law is not applicable outside these domains.  It is not uncommon to hear
the opinion that, because software product development is knowledge work,
Little’s Law has nothing useful to say about the kind of highly variable,
non-uniform processes common in software development.

It doesn’t help that most applications of Little’s Law in software development
explicitly rely on the formulation imported from Lean manufacturing, focusing on
_making_ variable work more uniform and predictable. Even in these
applications, the law often fails to hold when measured empirically in
operational settings mostly because of _how_ it has been applied. So it has
remained more of a theoretical curiosity in software - pointing to a desired
ideal state, rather than something consistently observable and applicable to 
real-world development processes. 

So the belief that “Little’s Law does not apply in software” is not entirely
unfounded—but nevertheless, it is demonstrably false. For those familiar with
Little’s Law only through its association with Lean manufacturing concepts and
its applications in software, or from cursory readings on sources like
Wikipedia, or even standard queueing theory texts, this post offers an
introduction to the state-of-the-art understanding of the law as it stands
today.

Applying Little’s Law correctly in more general settings requires understanding
the techniques used to prove its broader forms. These techniques not only
justify its wider applicability, but also show how to apply it usefully
in domains like software product development and engineering.

In this post, we introduce the history of the law and the proof techniques that
led to its increasingly general formulations. Understanding _why_ the law
generalizes is key to understanding _how_ to apply it in more general settings.
Little’s Law remains a highly intuitive result, remarkably general in its
applicability, yet subtle and often misunderstood and misapplied outside its original context.

### The significance of Little's Law

Before we jump into the details, it’s worth pausing to understand why this law
even matters.

Empirical observations often surface correlations—observed associations where
two quantities move in concert. Such correlations are frequently a starting
point for causal reasoning, prompting us to search for underlying mechanisms
that might explain the apparent linkage.

But even though Little's Law arose from empirical observations, it
establishes something much stronger than a correlation. The law expresses a
strict equation between three observable quantities, even though the quantities
involved may appear to be statistical measures on the surface.

An equation is a constraint, and a much stronger foundation for causal reasoning than
a correlation. When we observe change, the space of plausible explanations 
narrows dramatically. For example, if the average number of customers in
a system increases, there are only three possibilities: the arrival rate
increased, the average time each item spent in the system increased, or both
did. No other explanation is consistent with equality. Any other explanation must show
how it affects one or both of those variables.

In every generalization of Little's Law we will examine, there is a provable,
tightly constrained causal relationship between the same key averages. What
changes with each generalizations are the conditions under which they apply -
they relax various restrictions and make the law applicable in different
contexts, and yield different interpretations of what the averages _represent_
in that context.

Knowing the conditions under which an equation like Little’s Law holds gives us
an exceptionally robust framework for causal reasoning about _observable_ system
behavior. It doesn't tell us what will happen in the future, but it _constrains_
what can happen: regardless of how the system evolves, these three quantities
must remain bound by their relationship.

Few such relationships exist outside domains governed by strict conservation
laws, and in a deep sense, the proofs of Little's Law give us a template for
*discovering* such conservation laws in a new domain. Little’s Law is thus a
rare find—an intuitive, rigorously provable mathematical relationship among key
system properties that applies across linear, non-linear, stochastic,
deterministic, complex, and even some chaotic systems under some very weak
assumptions.

In their majestic textbook [@hopp2000], Hopp & Spearman liken Little’s Law to
_F = m·a_
for factory physics—a foundational constraint that helped move manufacturing
from art toward science. We take the view that, with the generalizations
developed since its early use in those domains, Little’s Law deserves this
status on a much grander scale.

In software product development and engineering, it has the same potential to serve
as one of the foundational laws of operations—helping move the field from a
collection of intuitive practices and empirical
conjectures [^-empirical-research] to a physical and economic science, grounded
in provable theory, data, constraints, and measurement.

[^-empirical-research]: This is not to say that intuition and empiricism don't
have a vital role to play in science—they are the foundation. However, the arc
of mature natural sciences is to build analytical and mathematical rigor atop
this foundation, producing testable, generalizable, and rigorous theories. In
software operations management, this arc is nascent at best. The concepts in
this post represent one necessary step toward a more principled and scientific
status quo.

Doing so requires us to go beyond the interpretations of Little’s Law found in
Lean manufacturing and embrace a more general framing—one that reflects the
nature of complex systems and the dynamics of knowledge work.

Let's now examine the evolution of this law through its various generalizations.

## 1961: Dr. Little proves the law

Dr. John Little, at the MIT Sloan School, gave the first mathematical
proof [@little1961] of this empirical relationship in 1961. His proof method
was based on the dominant paradigm for analyzing such problems at the time: queueing
theory, developed decades earlier to model congestion in telephone exchanges.

Queueing theory is built on a foundation of probabilistic models of arrival and
service processes that describe how items enter, wait in, and depart from the
system. Most theoretical results depend on specific assumptions about how these
stochastic processes behave. These assumptions not only model randomness, but
also make it possible to prove results that apply across broad classes of
queueing systems.

The precise result he proved was the following:

> In a queuing process, let λ be the long-run average arrival rate (i.e., the
> limit of the number of arrivals per unit time), L be the time-average number
> of items in the system, and W be the average time an item spends in the
> system. It is shown that, if the three means are finite, and the associated
> stochastic processes are strictly stationary, and if the arrival process is
> metrically transitive with nonzero mean, then L = λW.



### The assumptions in Dr. Little's proof

In Little’s original proof, several assumptions play a central role:

- The long-run averages L, W, and λ exist and are finite.
- The arrival and service processes, as well as the number in the system, are
  strictly stationary—meaning their joint distributions are invariant under
  time shift.
- The arrival process is metrically transitive (i.e., ergodic), which ensures
  that over the long run, expected values converge to long run time averages and that the
  its statistical profile is representative of the observed system behavior over time. 

These assumptions allowed Little to define L, W, and λ as *expected values*
with respect to a stationary stochastic process and to prove that the equality
L = λW holds under the additional condition that these expectations exist and
are finite.

### Why it is remarkable

What made his result so remarkable was how broadly it applied. Specifically, he
showed that it held regardless of the shapes of the probability distributions.
That was an unexpectedly general result for queueing theory, where many results
depend on strong assumptions about inter-arrival or service time distributions.

In fact, his proof showed that many internal details of the system—such as
queue discipline, scheduling order, or service time variability—do not affect
the validity of the relationship. Little’s Law, it turns out, is not a result
about the mechanisms of queuing per se, but about the aggregate behavior of
arrival and departure processes over time. No matter what these processes look
like internally, the relationship among their averages is constrained by the
equation. 

So it points to the fact that there is something deeper at play here than
randomness. Understanding his proof strategy sheds light on where the line lies. 

Little’s Law is fundamentally a statement about _time averages_—quantities that
can be directly observed in real-world systems over time. Dr. Little, however,
used probabilistic techniques to prove a relationship between the *expected
values* of random variables. Unlike time averages, expected values, also called
_ensemble averages_ are computed across the entire probability distribution of a
process and are defined independently of how the system evolves over time.

Given his probabilistic framing, Little’s proof started by establishing
the equality as a relationship between ensemble averages. To apply this result
to time-averages, he needed to assume that the ensemble averages and the time
averages of the corresponding processes converge to the same value. This
convergence is guaranteed when the underlying stochastic processes are strictly
stationary and ergodic—hence the need for those assumptions in Little’s original
proof.

But this doesn’t mean that stationarity and ergodicity are _required_ for the law
itself to hold. It suggests that it is entirely possible to prove Little’s Law
_directly_ for time averages, bypassing probability and queueing theory
altogether. In other words, the conditions that Dr. Little assumed are
sufficient, and an artifact of his proof technique, but not necessary for the
relationship between the quantities in the equation to hold.

 This is precisely what Dr. Shaler Stidham of Cornell showed in 1972, in a paper titled
_“Little’s Law, the last word”_ [@stidham72].

## 1972: Stidham’s Proof

Stidham gave the first purely deterministic proof of Little's Law free from any
probabilistic assumptions. This was important because it showed that, the
conditions under which Little's Law holds could be stated independently of
whether the underlying process was deterministic or stochastic. 

Stidham's framing considers the following input-output system
_observed over a sufficiently long time interval_ $[0, T)$.:

- Customers arrive at time instants $t_n$,  
  $n = 1, 2, \ldots$
- The time in system for the $n$th customer is $W_n$
- The number of customers in the system at time $t$ is $L(t)$ for $t \geq 0$

The theorem can now be stated informally[^-stidham-math] as follows:

> If the time-average arrival rate _over this window_ and the average time  
> each item spends in the system _over this sequence of items_ each _converge_  
> to finite limits—call them λ and W, respectively—then the time-average number  
> of items in the system also converges to a finite limit L, and the  
> relationship L = λW holds.

[^-stidham-math]:  
In [@stidham72], the result is stated formally as follows: 

    Let $N(t)$ be the number of items in the system at time $t$, and  
    $$L = \lim_{T \to \infty} \frac{1}{T} \int_0^T N(t)\,dt$$  
    Let $W_i$ be the time in system for item $i$, and  
    $$W = \lim_{n \to \infty} \frac{1}{n} \sum_{i=1}^n W_i$$  
    Let $Λ(t)$ be the cumulative number of arrivals up to time $t$, and  
    $$λ = \lim_{t \to \infty} \frac{Λ(t)}{t}$$  

    **Theorem**: If $λ$ and $W$ exist and are finite, then $L$ exists and $L = λW$.

### The generalization 

The first thing to note is that this version is framed as a theorem about an
_input-output system_ with observable arrivals and departures - not a __queueing system__ There are no mentions of
arrival and service _processes_ or their probability distributions, and no assumptions
about the stationarity or ergodicity those processes.

What remains are the assumptions about observable arrivals and the same three
averages in the original law, with a requirement that their long-run limits
exist and are finite. This marks a significant generalization beyond Dr.
Little’s original theorem.

> Little's Law has been completely separated from queueing theory and stochastic  
> processes.

Unlike Dr. Little’s result, Stidham’s theorem is proved using _observed long run averages_ :

- The time average of the number of items in the system,  
- The average time in system per item,  
- The arrival rate relating the two.

along a single _sample path_ [^-sample-path]

![Sample path and area under the sample path](../assets/pandoc/stidhams_sample_path_area.png){#fig:sample-path-area}

[@fig:sample-path-area] shows an example of a sample path for an input-output
system, where $N(t)$ is the number of items in the system at time $t$. Over a
window of length $T$, the time average of the number of items in the system is
given by the area under the sample path divided by $T$. 

That is, if $$A(T) = \int_0^T N(t)\,dt $$ is the area under the sample path
and $$ L(T) = \frac{A(T)}{T} $$
is the average number of items in the systems up to time $T$

Then, if the limit $$\lim_{T \to \infty} L(T) = L$$ exists, then
the long run time average of the number of items in the system converges to  $L$.

[^-sample-path]: In classical stochastic process theory, a process can evolve in different ways
    depending on the outcomes of some underlying random variables. For example,
    consider repeatedly tossing a coin: each possible sequence of heads and tails is
    a different sample path of the "coin toss" process. 

    When we observe a particular sequence of tosses over time, we’re observing one such sample path.
    We can think of a deterministic process as one that has exactly one sample path - which is the only one we can possibly observe. 

For stochastic processes this is very useful because Little's Law can now be applied to
analyze non-ergodic and non-stationary stochastic processes [^-stochastic]. And of course, it opened up
the same possibilities for deterministic processes as well.

[^-stochastic]:  
Separating the law from stochastic assumptions only means that it 
    can be combined with the rich theory of stochastic processes in even 
    more general contexts. 

    Stidham’s proof technique, known as sample path analysis, has had wide utility beyond the proof of Little’s Law. In the study of stochastic processes, this approach has allowed researchers to establish general properties of systems without requiring stationarity or ergodicity from the outset. These developments are extensively documented in [@eltaha1999], and their implications extend deeply into real-world operational settings.

The significance of Stidham’s theorem lies its focus on sample path convergence
of the averages. Stidham’s key insight was that, from the perspective of
Little’s Law, it doesn’t matter whether the process being observed is stochastic
or not. A sample path _can simply be the trajectory of a system unfolding in real time_, regardless of
whether that behavior arises from chance, deterministic rules, feedback loops,
or external influences. What matters is whether the long run _averages_ defined
in Little’s Law converge along a sufficiently long sample path.

This redefinition has powerful implications. It shifts the question from "_what
kind of system is this?_" to "_how does this system behave when we observe it
over the long run?_" The most important distinction now becomes whether the
system is _convergent_—whether the required limits exist—or
_divergent_, meaning one or more limits do not exist. 

This distinction applies across the board: linear systems, non-linear systems,
complex adaptive systems, and even chaotic ones can exhibit either convergent or
divergent behavior and can transition from one type of behavior to the other
depending upon their internal state. Sample path analysis and the constraints of
Little's Law allow us to consider the question of convergence or divergence of
an input-output system without having to consider the internal state of the
system.

![Patterns of sample path average behavior](../assets/pandoc/sample_path_patterns.png){#fig:convergent-divergent}

[@fig:convergent-divergent] shows several possible patterns of convergence or divergence 
of long run averages on the sample path of an input-output system, depending on its
history and internal state [^-note-average]. As we see, a system can exhibit a wide variety
of behaviors—even when it is convergent.

[^-note-average]: It is crucial to note that _we are not displaying the sample path here_
but the _cumulative time-average of the sample path_, ie we are showing $L(T) = \frac{1}{T} \int_0^T N(t)\,dt$ not $N(t)$. 

Purely divergent behavior implies unbounded growth in the area under the sample
path, but these four patterns are by no means exhaustive. The goal of sample
path analysis is not to divide systems into rigid categories—linear vs.
nonlinear, simple vs. complex—but to recognize that *any* deterministic or
stochastic system may exhibit *any* of these behaviors under the right conditions. What matters is not
classification, but having the tools to detect and understand mode shifts in
system behavior when they occur.

Little’s Law holds in *any* of the convergent modes. This reframes the key
question: rather than asking *whether* Little’s Law applies to a particular
input-output system (it almost always does), we ask *when* it applies, and
*under what limits*. That is, at a given point in a system’s evolution, do the
limits that define the relevant averages exist?

This becomes a practical matter—often resolved through domain-specific
reasoning, or simply through empirical observation over a sufficiently long
sample path. These approaches are far more tractable and broadly useful in
practice than requiring formal conditions like ergodicity or stationarity, as in
Dr. Little’s original version of the law.

With sample path analysis, Little's Law  becomes a tool for studying the long-run observed
behavior of input-output systems. It allows us to characterize a system not by
its internal structure or stochastic assumptions, but by whether its
macroscopic (and as we will see soon, microscopic) behavior satisfies certain
constraints when observed over time. And importantly, it gives us a concrete
operational definition that lets us  _measure_ and _verify_ this condition from
observed data.

It makes Little’s Law applicable to deterministic or stochastic systems that are
non-stationary, non-ergodic, and potentially highly sensitive to initial
conditions—exactly the kind of behavior we expect to encounter with complex adaptive systems
in domains like software development.

### What we lose

When we 

---

## Post Script 1

It’s worth pausing to explain why the version of Little’s Law commonly used in
software today looks quite different from the one we’ve discussed so far.

Dr. Little’s original proof applied to stationary systems with finite
averages—conditions that most manufacturing processes in steady state
typically satisfy. In practice, this means that under equilibrium, arrival rates
can be assumed equal to departure rates. This allows us to write:

L = X ⋅ W

where X is the departure rate or throughput. Rearranging this and renaming the
terms gives us the familiar form:

Throughput = WIP / Cycle Time

This is the form popularized by Lean, and it’s natural in manufacturing, where
factory managers focus on optimizing WIP and cycle time to meet a fixed
throughput goal derived from stable production orders.

But in software development, this metaphor often fails. Software teams usually
don’t control arrivals. Instead, they’re reactive to demand, making arrival rate
the critical metric. In these environments, the arrival-rate form of Little’s
Law becomes far more relevant.

In our treatment of Little's Law going forward, we’ll mostly abandon the
throughput-centric view from Lean manufacturing. Instead, we’ll adopt the
arrival-rate form and use equilibrium conditions to treat throughput as a
consequence of managing arrivals properly.

As discussed in the next post, this is also critical to build a proper causal
model for flow. As in general queueing systems, understanding flow in software
requires treating arrivals as the cause and throughput as the effect.

---

## Post Script 2

In 2011, Dr. Little published a survey of all the developments related to
Little's Law on its 50th anniversary. Most of this series started from a close
reading of that paper. I highly recommend it if you’re interested in a more
technical, yet accessible, presentation of the material in this post.

## References
