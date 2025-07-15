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

## The Law

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

We can see that this equation relates three distinct _kinds_ of averages:

- _L_ is a _time average_ — the number of items present in the system per unit
  of time,
- _W_ is an _item average_ — the average number of time units an item
  accumulates while present in the system,
- λ is a rate — a number of items per unit of time.

Notably, the denominator in the first average is a continuous quantity (time), the
denominator in the second average is a discrete quantity (items), and the
third quantity is a rate relating the denominators of the other two quantities.

The law was widely assumed to be true in operational settings and used without
proof because it was intuitive, could be empirically confirmed, and its symmetry
was appealing. But no one knew _why_ this relationship between these averages
should hold. As we will see, this is anything but obvious to prove in a general
setting.

### Proofs and generalizations of Little's Law

Dr. John C. Little [@little1961] gave the first mathematical proof in 1961 using
techniques from queueing theory and probabilistic analysis. His proof involved
assumptions including steady state conditions and stationary probability distributions, 
that were largely true in the operational settings under which the
law was being applied, and thus the equation—and the assumptions under which Dr.
Little proved it—became known as Little's Law.

It found applications in manufacturing, computer systems performance analysis,
service operations management, and countless other operational settings. It is
considered a foundational law akin to Newton’s law _F = m·a_ in these domains
[@hopp2000].

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
Law is not applicable to complex adaptive systems. It is not uncommon to hear
the opinion that, because software product development is knowledge work,
Little’s Law has nothing useful to say about the kind of highly variable,
non-uniform processes common in software development.

It doesn’t help that most applications of Little’s Law in software development
explicitly rely on the formulation imported from Lean manufacturing, focusing on
_making_ variable work more uniform so it can "flow". Even in these
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
applicability, yet subtle and often misapplied outside its original context.

This post lays the foundation to change that.

## The significance of Little's Law

Before we jump into the details, it’s worth pausing to understand why this law
even matters.

The world of empirical research is awash in correlations—observed associations
where two quantities move in concert. These correlations are often a starting
point for causal reasoning, prompting us to search for the underlying mechanisms
that might explain the apparent linkage.

But even though Little's Law arose from empirical observations, the law itself
establishes something much stronger than a statistical relationship, even though
the quantities involved may appear to be statistical properties on the surface.
Unlike a correlation, the law expresses a strict equation between three
observable quantities.

When variables are related by an equation, the space of plausible explanations
for change narrows dramatically. For example, if the average number of customers
in a system increases, there are only three possibilities: the arrival rate
increased, the average time each item spent in the system increased, or both
did. No other explanation is consistent with equality. Any other claim must show
how it affects one or both of those variables.

In every generalization of Little's Law we will examine, it shows that under
certain conditions there is a provable, tightly constrained causal relationship
between changes in arrival rate, time in system, and the average number of items
in the system. What changes with each generalizations are the conditions - they
become less and less restrictive, and make the law more general and easier to
apply correctly in more contexts.

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
developed since its early use in those domains, Little’s Law deserves the same
status on a much broader scale.

In software product development and engineering, it has the potential to serve
as one of the foundational laws of operations—helping move the field 
from a collection of intuitive practices unmoored from provable theory to a science grounded
in data, constraint, and measurement.

Doing so requires us to go beyond the interpretations of Little’s Law found in Lean
manufacturing and embrace a more general framing—one that reflects the nature of
complex systems and the dynamics of knowledge work.

Let's now examine the evolution of this law through its various generalizations.

## Version 1: Dr. Little proves the law

In 1961, Dr. John Little, at the MIT Sloan School, gave the first mathematical
proof of this empirical relationship. His proof method used the most widely
accepted framework for analyzing these problems: queueing theory, developed
decades earlier to model congestion in telephone exchanges.

The precise result he proved was the following:

> In a queuing process, let λ be the long-run average arrival rate (i.e., the
> limit of the number of arrivals per unit time), L be the time-average number
> of items in the system, and W be the average time an item spends in the
> system. It is shown that, if the three means are finite, and the associated
> stochastic processes are strictly stationary, and if the arrival process is
> metrically transitive with nonzero mean, then L = λW.

Queueing theory is built on a foundation of probabilistic models of arrival and
service processes that describe how items enter, wait in, and depart from the
system. Most theoretical results depend on specific assumptions about how these
stochastic processes behave. These assumptions not only model randomness, but
also make it possible to prove results that apply across broad classes of
systems.

In Little’s original proof, several assumptions play a central role:

- The long-run averages L, W, and λ exist and are finite.
- The arrival and service processes, as well as the number in the system, are
  strictly stationary—meaning their joint distributions are invariant under
  time shift.
- The arrival process is metrically transitive (i.e., ergodic), which ensures
  that over the long run, time averages converge to expected values and that the
  observed system behavior over time is representative of its statistical
  ensemble.

These assumptions allowed Little to define L, W, and λ as *expected values*
with respect to a stationary stochastic process and to prove that the equality
L = λW holds under the additional condition that these expectations exist and
are finite.

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

Little’s Law is fundamentally a statement about _time averages_—quantities that
can be directly observed in real-world systems over time. Dr. Little, however,
used probabilistic techniques to prove a relationship between the *expected
values* of random variables, known as ensemble averages. Unlike time averages,
ensemble averages are computed across the entire probability distribution of a
process and are defined independently of how the system evolves over time.

Little’s proof established the equality between _expected values_ - i.e.,
ensemble averages. To apply this result to real-world systems, he needed to
assume that the ensemble averages and the time averages of the corresponding
processes converge to the same value. This convergence is guaranteed when the
underlying stochastic processes are strictly stationary and ergodic—hence the need for
those assumptions in Little’s original proof.

But this doesn’t mean that stationarity and ergodicity are required for the law
itself to hold. It suggests that it is entirely possible to prove Little’s Law
_directly_ for time averages, bypassing probability and queueing theory
altogether. In other words, the conditions that Dr. Little assumed are
sufficient, and an artifact of his proof technique, but not necessary for the
relationship between the quantities in the equation to hold.

 This is precisely what Dr. Shaler Stidham of Cornell did in 1972, in a paper titled
_“Little’s Law, the last word.”_

## Stidham’s Proof of Little’s Law

Stidham demonstrated that Little's Law was even more general than previously
believed. His proof was purely deterministic and did not rely on any
probabilistic or queueing theory techniques. It was based on standard techniques
from continuous analysis, using time averages on sample paths for queue length,
calculated over finite intervals. It eliminated the requirements for
stationarity, ergodicity, and related assumptions.

The specific statement he proved was the following:

> Consider a system observed over a sufficiently long interval [0, T).  
> If the time-average arrival rate and the average time each item spends in the  
> system over this window each converge to finite limits—call them λ and W,  
> respectively—then the time-average number of items in the system also  
> converges to a finite limit L, and the relationship L = λW holds.

In contrast to Dr. Little’s original formulation, which relates the expected
values of probability distributions, this version establishes a relationship
between the limits of time averages observed along a sufficiently long sample
path.

This is a significant generalization, but it also needs to be read carefully to
understand precisely what Little’s Law is asserting—and the specific conditions
under which it holds.

Stidham’s proof did not require even queueing theory assumptions like a defined
arrival or departure process. So, technically, he showed that Little's Law is
much more than a result that applies only to queueing systems. He showed that
Little's Law is a remarkably general statement about the population dynamics of
any system where entities arrive at and depart from the system over time.

The only requirements for the law to hold were that the three averages in the
equation were well-defined and converged to a finite limit when measured over
sufficiently long observation windows.

His proof reinforces the idea that Little’s Law applies only to systems in
equilibrium—albeit under much weaker conditions than those in Dr. Little’s
original proof. As we’ll see in the next post in the series, this generalization
of equilibrium conditions is what allows Little’s Law to bridge from stable
manufacturing environments to dynamic, evolving, and complex systems like
software development.

In the next post, we will examine Stidham's specific result more carefully,
using his ideas to show that when measured appropriately, Little's Law can
always be empirically validated in software development. This will refute the
notion that it cannot be applied to software development—but it will do much
more than that.

Stidham’s proof technique for Little's Law, called sample path analysis, is a
powerful method with many more applications, including one that led to a very
general version of Little's Law where W can be replaced with arbitrary functions
subject to weak regularity constraints. This version, known as the Generalized
Little's Law, has important implications for modeling the economics of flow and
will be essential in understanding how to measure the relationship between the
flow of work and the flow of value—something we have been exploring in some
detail in this series.

At this point, Little's Law is considered to be much more than a result in
queueing theory. It has earned something close to the ontological status of a
natural equilibrium law that reveals a fundamental duality between population
size and individual item lifetimes in dynamic systems.

This is a powerful property that can be exploited in many different ways once
you establish it, and this has been the real reason why Little's Law has been so
useful in every domain where it has been successfully applied.

Before we jump into the technical details of how Little's Law can be applied in
software development, our next post asks: what does knowing Little's Law holds
in a domain help us do? Why should we even care whether Little's Law is true or
not, in any given domain context?

This sets up the stakes for the kind of reasoning tools we give up when we
blithely assume that “Little’s Law does not apply to software development.”

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
