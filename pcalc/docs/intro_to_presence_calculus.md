# The Presence Calculus, <br> A Gentle Introduction

**Dr. Krishna Kumar**  
*The Polaris Advisor Program*

## 1. What is The Presence Calculus?

The Presence Calculus is a new approach for reasoning quantitatively about the  
relationships between signals in a domain over time.

The primary goal is to support rigorous modeling and principled  
decision-making with operational data in complex, business-critical domains.

A key objective was ensuring that the use of data in such decisions rests on a  
mathematically precise, logically coherent, and epistemically grounded  
foundation.

The presence calculus emerged from a search for better quantitative tools to  
reason about software product development and engineering, where current  
approaches leave much to be desired in all three aspects.

Minimally, the foundational constructs of the calculus bring mathematical  
precision to widely used—but poorly defined—concepts such as flow, stability,  
equilibrium, and coherence in a domain. More importantly, it allows us to  
relate them to business-oriented concerns like delay, cost, revenue, and  
user experience.

As you’ll see, however, the ideas behind the calculus are far more general,  
with potential applications well beyond the software product development  
context it emerged from.


<div style="text-align: center; margin:2em">
  <img src="../assets/pcalc/presence_calculus.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 1: Key constructs—presences, element trajectories, presence matrix,  
    and basis topology
  </div>
</div>

### The pitch

We introduce the simple but powerful concept of a *presence*.

This lets us reason about time, history and evolution using techniques from
measure theory, topology and complex analysis.

Classical statistics and probability theory often struggle here.
*History*—the sequence and structure of changes in the domain over time— is
usually fenced off under assumptions like ergodicity, stationarity, and
independence.

However, probability theory and statistics remain very powerful tools for
describing local behavior, identifying patterns and correlations in this
behavior, and modeling uncertainty—all crucial aspects of meaningful analysis of
complex systems.

Our thesis is that to move beyond simple descriptive statistics, statistical
inference and probabilistic models, and start reasoning about global and long
run behavior of complex systems, we need models that treat time and history as
first-class concepts we can reason and compute with.

This, in turn, lets us apply techniques from disciplines such as stochastic
process dynamics, queueing theory, and complex systems science, to reason
holistically about global, long run behavior of complex systems.

We claim the presence calculus is a novel, constructive approach to do this - a
new and powerful reasoning tool for anyone working with complex systems.

But this is a bold claim, and it deserves further scrutiny and validation, and
so we invite anyone interested in doing so to collaborate with us on this open
source project.

### Learning more about The Presence Calculus

While the calculus was developed with mathematical rigor, an equally important  
goal was not to let mathematics get in the way of understanding the simple but
very powerful and general ideas the calculus embodies[^1].

[^1]: This document is the first step in that direction. We welcome feedback on
how it can be improved,and the concepts clarified. Please feel free to open a
pull request with thoughts, suggestions or feedback.

In this document, we'll motivate and introduce the key ideas in the calculus  
informally, with lots of highly evocative examples and simplifications to  
illustrate concepts.

While it is aimed squarely at the non-technical reader, in order to understand
the ideas, some basic mathematical notation is used in key sections. We do
augment these with examples to build intuition throughout.

We recommend reading and understanding all the main ideas here before jumping
deeper into the rest of the documentation at this site, which does get a fair bit more dense.

If that deeper dive is  not your cup of tea, we'll continue with ongoing informal exposition on our blog [The Polaris Flow Dispatch](https://www.polaris-flow-dispatch.com), where we will focus mostly on applications of the ideas. 

So this document can be thought as the middle ground: detailed enough to
understand the concepts and ideas clearly and precisely, but just a starting
point if you want to really dig deeper.

The next level of detail is in the API docs for [The Presence Calculus  
Toolkit](https://py.pcalc.org).

The toolkit is an open source python library that implements all the core
concepts in the presence calculus. In the API documentation, we go into the
concepts at a level of rigor that you'll need to work with the pcalc API and
apply the concepts. Some mathematical background will be useful here if you want
to apply the concepts and extend beyond the core.

The toolkit is reference implementation of the presence calculus. It is designed
as an analytical middleware layer suitable for interfacing real world
operational systems and complex system simulation, to the analytical machinery
of the presence calculus.

Finally, for those who want to dive deeper into the formal mathematical  
underpinnings of the calculus, we have the theory track, which perhaps goes  
into more detail than most people will need to read or understand, but is  
useful for the mathematically trained to connect the ideas to their roots in  
mainstream mathematics.

Let's jump in...

### Why Presence?

Presence is how reality reveals itself.

We do not perceive the world as disjointed events in time, but rather as an
unfolding—things come into being, endure for a time, and slip away.

Permanence is just a form of lasting presence. What we call *change* is the  
movement of presences in and out of our awareness, often set against that  
permanence.

The sense of something being present—or no longer present—is our most  
immediate way of detecting change.

This applies to both the tangible—people, places, and things—and the  
intangible—emotions, feelings, and experiences.

Either way, we reason about the world by reasoning about the presences and  
absences in our environment over time.

The presence calculus begins here. Before we count, measure, compare, or  
optimize, we observe what *is*.

And what we model is presence.

### An example

Imagine you see a dollar bill on the sidewalk on your way to get coffee.  
Later, on your way back home, you see it again—still lying in the same spot.  
It would be reasonable for you to assume that the dollar bill was present  
there the whole time.

Of course, that may not be true. Someone might have picked it up in the  
meantime, felt guilty, and quietly returned it. But in the absence of other  
information, your assumption holds: it was there before, and it’s there now,  
so it must have been there in between.

This simple act of inference is something we do all the time. We fill in gaps,  
assume continuity, and reason about what must have been present based on what  
we know from partial glimpses of the world.

The presence calculus gives formal shape to this kind of inference—and shows  
how we can build upon it to *reason* about presence and *measure* its  
effects in an environment.

### A software example

Since the ideas here emerged from the software world, let’s begin with a  
mundane, but familiar example: task work in a software team.

By looking closely at how we reason about tasks, we can see how a subtle shift  
to a presence-centered perspective changes not just what we observe, but what  
we measure, and thus can reason about.

We usually reason about task work using *events* and *snapshots* of the state  
of a process in time. A task “starts” when it enters development, and  
“finishes” when it’s marked complete. We track "cycle time" by measuring the  
elapsed time between events, "throughput" by counting finish events, and  
"work-in-process" by counting tasks that have started but not yet finished.

When we look at a Kanban board, we see a point-in-time snapshot of where tasks  
are at that moment—but not how they got there. And by the time we read a  
summary report of how many tasks were finished and how long they took to go
through the process on average, much of the history of the system that produced
those measurements has been lost. That makes it hard to reason about *why*
those measurements are the way they are.

In complex knowledge work, each task often has a distinct history—different  
from other tasks present at the same time. Losing history makes it hard to  
reason about their interactions and how they impact the global behavior of the  
process.

This problem is not unique to task work. Similar problems exist in almost all
areas of business analysis that rely primarily on descriptive statistics as the
primary measurement tool for system behavior.

We are reduced to trying to make inferences from local descriptive  
statistics —things like cycle times, throughput, and work-in-process levels-
over a rapidly changing process.

We try to reason about a process which is shaped by its history, with
measurement techniques that struggle to represent or reason about that history.
This is difficult to do, and we have no good tools right now that are fit for  
this purpose.

This is where the presence calculus begins.

While it often starts from the same snapshots, the calculus focuses on the  
time *in between*: when the task was present, where it was present, for how  
long, and whether its presence shifted across people, tools, or systems.

The connective tissue is no longer the task itself, or the process steps it  
followed, or who was working on it, but a continuous, observable *thread of  
presence*—through all of them, moving through time, interacting, crossing
boundaries—a mathematical representation of history.

With the presence calculus, these threads and their interactions across time  
and space can now be measured, dissected, and analyzed as first-class  
constructs—built on a remarkably simple primitive—the presence.

### The heart of the matter

At its core, the calculus exploits the difference between the two independent  
statements—“The task started development on Monday” and “The task completed  
development on Friday”—and a single, unified assertion: “The task was present  
in development from Monday through Friday.”

The latter is called a *presence*, and it is the foundational building block  
of the calculus.

At first glance, this might not seem like a meaningful difference.

But treating the presence as the primary object of reasoning—as a
*first-class* construct—opens up an entirely new space of possibilities.

Specifically, it allows us to apply powerful mathematical tools that exploit the
continuity of time and the algebra of time intervals to reason about the
interactions and emergent configurations of presences in a rigorous and
structured, and more importantly, computable way.

## 2. What is a Presence?

Let's start by building intuition for the concept of presence.  
Consider the statement: “The task $X$ was in Development from Monday to  
Friday.”

In the presence calculus, this would be expressed as a presence of the form:  
“The element $X$ was in boundary $Y$ from $t_0$ to $t_1$ with mass 1.”  
Presences are statements about elements (from some domain) being present in a  
boundary (from a defined set of boundaries) over a *continuous* period of time,
measured using some timescale.

So why do we say “with mass 1”?

The presence calculus treats time as a physical dimension, much like space.  
Just as matter occupies space, presences occupy time. Just as mass quantifies  
*how* matter occupies space, the mass of a presence quantifies *how* a  
presence occupies time.

The statement “The task $X$ was in Development from Monday through Friday” is  
a **binary presence** with a uniform mass of 1 over the entire duration. The  
units of this mass are element-time—in this case, task-days.

Binary presences are sufficient to describe the *fact* of presence or absence  
of things in places in a domain. These presences always have mass 1 in whatever
units we use for elements and time.

### Presence mass

Let's consider a more detailed set of statements:

> “Task $X$ had 2 developers working on it from Monday to Wednesday,  
> 3 developers on Thursday, and 1 developer on Friday.”

These are no longer about just presence, but about the *effects* of presence.  
They describe the **load** that task $X$ placed on the Development boundary  
over time.

The units of this presence are developer-days - potentially in a completely
different space from the task, but grounded over the same time interval as the
task.

Here we are saying: "the task being in this boundary over this time period, had
this effect."

We will describe such presences using a *presence density function,*
called $\mathsf{load}$ in this case:

- $(\mathsf{load}, X, \text{Development}, \text{Monday}, \text{Wednesday}, 2)$
- $(\mathsf{load}, X, \text{Development}, \text{Thursday}, \text{Thursday}, 3)$
- $(\mathsf{load}, X, \text{Development}, \text{Friday}, \text{Friday}, 1)$

Here, $\mathsf{load}(e, b, t)$ is a time-varying function that takes an  
element $e$, a boundary $b$, and a time $t$, and returns a real-valued number  
describing how much presence is concentrated at that point in time.

The *presence mass* of such a presence is the total presence over the  
interval $[t_0, t_1]$, defined as:

$$ \text{mass} = \int_{t_0}^{t_1} \mathsf{load}(e, b, t)\, dt $$

where $\mathsf{load}$ is the presence density function [^2].

[^2]: If integration signs in a "gentle" introduction feels like a
bait-and-switch, rest assured, for the puposes of this document you just need to
think of them as a way to add up presence masses, in a way that the ideas we use
for binary presences will generalize when we apply them to arbitrary functions.

### Domain Signals and Presence Density Functions

Binary presences are much easier to understand intuitively, but the real power
of the presence calculus comes from generalizing to *presence density
functions*.

In our earlier example, we showed a presence that described the *load* placed on
an element at a boundary, and this has a real-valued presence mass. More
generally, we can think of defining a presence over an arbitrary time varying
function with real numbers as values.

Such functions are called _presence density functions_. In general, these
presence density function represent some underlying signal from the domain that
we are interested in measuring. So, in what follows, we will use the terms
signal and presence density functions interchangeably in what follows, opting
for the latter only those cases where we want to focus specifically on the fact
that what we are representing about the signal is the "amount" of the signal (
its presence) over time.

As shown in Figure 2, the mass of a presence density function, over any given
time *interval* $[t_0, t1)$ is the integral over the interval, which is also the
area under the signal over that interval[^3].

[^3]: The way we've defined signals and mass is directly  
analogous to how mass is defined for matter occupying space in physics.

    A binary signal can be thought of as defining a one-dimensional interval over  
    time. For a fixed element and boundary, this gives us an area under the  
    curve in two dimensions: time vs. density.

    If we treat elements and boundaries as additional independent dimensions,  
    then the signal defines a *volume* in three dimensions, with time as one axis.  

    This interpretation—presence as a physical manifestation of density over  
    time—is a powerful way to reason intuitively and computationally about 
    duration, overlap, and accumulation in time.

    And when we allow multiple signals to interact over the same time periods, we  
    begin to model complex, higher-dimensional effects of presence—exactly the  
    kind of generality we’ll need when we move beyond simple binary presences.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/presence_definition.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 2: Signals, Presence,  and Presence Mass
  </div>
</div>

The only requirement for a function to be a presence density function (signal)
is that it is *measurable*, and that you can interpret *presence mass*—defined
as the integral of the function over a finite interval—as a meaningful
*measure* of the effect of presence in your domain.

This is where measure theory enters the picture. It’s not essential to
understand the full technical details, but at its core, measure theory tells us
which kinds of functions are measurable—in other words, which functions can
support meaningful accumulation, comparison, and composition of values via
integration.

When a presence density functions (signal) is measurable,it gives us the
confidence to do things like compute statistics, aggregate over elements or
boundaries, and compose presence effects—while preserving the semantics of the
domain.

Informally, when a presence density function is a measurable we can treat its
values like any other real number and do math over them, as long as we carefully
respect the units involved.

From our perspective, a presence density function is a domain signal whose value
that can be *accumulated* across time and across presences.

This lets us reason mathematically about presences with confidence—and since
most of this reasoning will be performed by algorithms, we need technical  
constraints that ensure those calculations are both mathematically valid and  
semantically sound.

### More examples

Let's firm up our intuition about what presences can describe with a few more  
examples.

#### "Work" in software

If you've ever written a line of code in your life, you’ve heard the question:  
“When will it be done?” Work in software can be a slippery, fungible concept—  
and the presence calculus offers a useful way to describe it.

We can express the work on a task using a presence density function whose  
value at time $t$ is the *remaining* work on the task at that moment.

This lets us model tasks whose duration is uncertain in general, but whose  
remaining duration can be described at any given time—a common scenario in  
software contexts.

A series of presences, where the (non-zero) mass of each presence corresponds  
to the total remaining work over its interval (interpreting the integral as a  
sum), gives us a way to represent *work as presence*.

Such presences can represent estimates, forecasts, or confidence-weighted  
projections—and as we'll see shortly, they can be reasoned about and computed  
with just like any other kind of presence.

#### The effects of interruptions

Another useful example from the software world illustrates a different  
application of a presence. Let’s assume the boundary in this case is a  
developer, the element is an interruption (defined appropriately in the  
domain), and the presence density function captures the *context switching  
cost*—measured in lost time—associated with that interruption.

The key insight here is that the *effects* of the presence extend beyond the  
interval of the interruption itself. This is a classic case of a delayed or  
*decaying effect*—a pattern that appears frequently in real-world systems.

The presence density function can be modeled in different ways:

- As a constant cost: for example, each interruption causes a fixed  
  15-minute recovery period, regardless of its duration.
- As a decaying function: the cost is highest at the moment of interruption  
  and gradually decreases to zero over a defined recovery window (e.g.  
  15 minutes), representing a return to full focus.

This approach gives us a precise way to model and reason about the  
*aftereffects* of events—effects that outlast the events themselves and  
accumulate in subtle but measurable ways over longer timeframes.

In this case, we measured an effect that decayed from a peak, but a similar  
approach can be taken, for example, with a presence density function that  
grows from zero and plateaus over the duration of the presence—such as the net  
increase in revenue due to a released feature.

Used this way, presence density functions give us a powerful tool for modeling  
the impact of binary presences—capturing their downstream or distributed  
effects over time, and reasoning about their relationship over a shared  
timeline.

Another important use case in the same vein is modeling the cost of delay for a
portfolio-level element—and analyzing its cascading impact across the  
portfolio.

These use cases show that it is possible to analyze not just binary presences,  
but entire chains of influence they exert across a timeline—a key prerequisite  
for reasoning about causality.

#### Self-reported developer productivity

Imagine a developer filling out a simple daily check-in:  
"How productive did you feel today?"—scored from 1 to 5, or sketched out as a  
rough curve over the day[^4].

[^4]: The use of a rough curve here is an example of how presences can encode  
continuous inputs more effectively than discrete techniques, thanks to their  
explicit model of time. Forcing a developer to rank their productivity on a  
Likert scale often loses valuable nuance—whereas a fine-grained presence  
captures temporal variation with ease, making it available for downstream  
analysis.

Over a week, this forms a presence density function—not of the developer in a  
place, but of their *sense* of productivity over time.

These types of presences, representing perceptions, are powerful—helping  
teams track experience, spot early signs of burnout, or correlate perceived  
flow with meetings, environment changes, build failures, or interruptions.

Now, let's look at some examples outside software development.

#### Browsing behavior on an e-commerce site

Imagine a shopper visiting an online store. They spend 90 seconds browsing  
kitchen gadgets, then linger for five full minutes comparing high-end  
headphones, before briefly glancing at a discounted blender.

Each of these interactions can be modeled as a presence: the shopper's  
(element) attention occupying different parts of the site (boundaries) over  
time. The varying durations reflect interest, and the shifting presence
reveals  
patterns of engagement.

By analyzing these presences—where and for how long attention dwells—we can  
begin to understand preferences, intent, and even the likelihood of conversion  
(modeled as a different presence density function).

#### Patient movement in a hospital

Consider a patient navigating a hospital stay. They spend the morning in  
radiology, move to a recovery ward for several hours, then are briefly  
transferred to the ICU overnight.

Each location records a presence—when and where the patient was, and for how  
long. These presences can reveal bottlenecks, resource utilization, and  
potential risks.

Over time, analyzing patient presences helps surface patterns in care  
delivery, delays in treatment, and opportunities for improving patient flow.

These are examples of classic operations management problems expressed in the  
language of the presence calculus. The calculus is well-suited to modeling  
scenarios like these as a base case.

## 3. Systems of Presences

Let's summarize what we've described so far.

With signals and presences, we now have the framework for describing and
measuring the behavior of time-varying domain signals, each representing how a
specific element behaves within a given boundary.

The key feature of a presence is that it abstracts these behaviors into a
uniform representation—one that we can reason about and compute with.

To summarize:

A general presence is defined by:

- a density function $f(e, b, t)$,
- an element $e$,
- a boundary $b$,
- and a time interval $[t_0, t_1]$.

Its **mass** is the integral of $f$ over the interval:

$$ \text{mass}(e, b, [t_0, t_1]) = \int_{t_0}^{t_1} f(e, b, t)\, dt $$

This mass captures both *that* the element was present, and *how* it was  
present—uniformly, variably, or intermittently—over the time interval of the
presence.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/pdf_examples.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 3: Signals and Presences
  </div>
</div>

### Presence as a sample of a signal

A domain signal, in general, describes the continuous behavior of an element
within a boundary over time. This continuous signal may have one or more
disjoint periods where its value is non-zero. These non-zero periods are called
the _support_ of the signal.

As we see in Figure 4, a single signal (for a given element and boundary) might
have multiple support intervals. These may correspond to episodic behavior in
the underlying domain, for example, user sessions in an e-commerce context, or
rework loops in software development when a task "returns" to development many
times over its lifecycle.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/multiple_support.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 4: A presence mass as a sample of a signal over an interval.
  </div>
</div>

A *presence* (the 5-tuple $p = (e, b, t_0, t_1, m)$ that we work with in the
calculus) is generated by taking an *observation* of this underlying signal over
a specific time interval $[t_0, t_1)$, and computing its mass. This interval can
be chosen in many ways:

* It might perfectly align with a single period of activity (a 'hill' in the
  signal).
* It might span multiple disjoint periods of activity, including the "zero"
  times in between.
* It might capture only a portion of a period of activity.

All we require is that the interval chosen for the presence calculation
intersects a region of non-zero area from the signal that can be reduced to a
presence mass.

Thus presence is best thought of as a *sampled measurement* of the underlying
signal, taken by an *observer* over a specific time interval, which yields a
total presence mass for that interval. This means that a single presence
assertion can aggregate the mass from multiple disjoint periods of activity of a
signal, depending on how the observer defines their measurement interval.

A given observer may not even "see" the full underlying signal—only the *mass*  
of the presence they experience over the interval they observed.

Different observers may observe different intervals of the same signal and
derive different presence values, depending on what part of the function they  
encounter.

This brings us to the concept of *presence assertions*, which formalize this  
idea of an observer recording a presence based on their local view of the  
underlying density function.

### Presence Assertions

A *presence assertion* is simply a presence augmented with metadata:

- *who* the observer was
- and an *assertion timestamp*—the time at which the observation was made.

The assertion time doesn't need to align with the time interval of the presence.
This allows assertions to refer to the past, reflect the present, or even
anticipate the future behavior of a signal.

Presence assertions give us the ability to assign *provenance* to a presence—  
not just *what* we know, but *how* we know it. This is essential in  
representing complex systems where the observer and the act of observation  
are first-class concerns.

We won’t go too deeply into the epistemological aspects of the presence  
calculus in this document—this remains an active and open area of research and
development and complements much of what we discuss here.

But it’s important to acknowledge that this layer exists, that modeling and
interpreting the output of the presence calculus requires an explicit treatment
of how observations are made and by whom, and the fact that this has a huge
impact on the validity of the inferences one makes using the machinery of the
calculus.

With this caveat in place, once we've represented a problem domain as a  
*system of presences*, much of the machinery of the presence calculus (which  
we'll introduce next) can be applied uniformly.

For the next couple of sections, where we will introduce this machinery, we will
operate under the assumption that there is a _signal_ that can be observed and
what we observe about the signal reflects what an observer knows about the
domain. We don't presume anything about the "truth" of the observations, we
treat them uniformly as signals.

One thing we will see is that from the perspective of this machinery, there are
no fundamental differences in behavior between binary signals and arbitrary
signals once they've been reduced to a canonical, presence-mass oriented
representation[^5].

This greatly increases the scope of the problem domains where this machinery can
be applied, and our examples in the previous section began to hint at the
possibilities.

This, in the end, is the source of the generality and power of the presence
calculus.

[^5]: There are several technical conditions that must be satisfied when  
mapping signals to a canonical system of presences in order for this claim to  
hold. To avoid getting bogged down in those details, we’ll simply claim it for  
now. The API docs go into more detail about the mechanics of this canonical  
representation, and what’s needed to ensure a "clean" mapping from a signal to a
system of presences—or more precisely, a system of presence assertions.

#### A note on path dependence

By representing a presence at the granularity of a element in a boundary, we
explicitly recognize the path dependent nature of the domain signals. Even if
they represent the same underlying quantity we recognize that the behavior of
the system emerges from individual signals at the element-boundary granularity
and that we are interested in studying _how_ the system level behavior emerges
from the interactions between these signals.

To summarize, this is what we refer to as a "system of presences" - a time
indexed collection of presence assertions derived from a an underlying set of
path dependent element-boundary signals.

## 4. Co-Presence and The Presence Invariant

In the last section, we introduced systems of presences as collections of
presence assertions, which are derived from observable signals.

Figure 5 illustrates an example of such a system, where we focus on the subset
of presences defined over a *shared observation interval*.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/presence_invariant_continuous.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 5: The Presence Invariant
  </div>
</div>

These presences are called *co-present*—they represent an observer making
simultaneous measurements of presence mass across multiple signals over a common
interval of time.

Co-presence is a necessary (but not sufficient) condition for interaction
between one or more signals. This section introduces a key construct: the
presence invariant. It expresses a general and powerful relationship that holds
for any co-present subset of presences within a finite observation window, and
it is a fundamental relationship that governs how the masses of co-present
signals interact.

Let's establish this relationship.

Given, any finite observation interval, we've already shown that each presence
density function has a *presence mass*, defined as the integral of the density
over the observation interval.

These can be thought of as mass _contributions_ from those presences to that
interval. The sum of these individual mass contributions
gives the total presence mass observed across the system in that interval.

In our example from Figure 5,

$$ A = M_0 + M_1 + M_3 $$

is the total mass contribution from the signals that have non-zero mass over the
interval $[t_0, t_1)$. The length of this interval is $T = t_1 - t_0$.

Since the mass comes from integrating a density function over time, the quantity
$\delta = \frac{A}{T}$ represents the *average presence density* over the
observation interval $T$.

We can now decompose this as:

$$ \delta = \frac{A}{T} = \frac{A}{N} \times \frac{N}{T} $$

Here $N$ is the number of *active signals*: distinct signals with a presence in
the observation window[^6]. This separates the average presence density into two
interpretable components:

[^6]: It is equally valid to define $N$ as the number of distinct _presences_ in
the observation window. For example for the signal $P2$ in Figure 5, this
corresponds to asking if $N=5$ (if we count the disjoint presences individually)
or $N=3$ (if we count the signals). These give different values for $\bar{m}$
and $\iota$ but their product _still equals_ $\delta$, as long as a single
consistent definition of N is used. This is ultimately a modeling decision that
depends on what you are trying to measure. By default we will assume that $N$ is
measured at the signal granularity.

- $\bar{m} = \frac{A}{N}$: the *average mass contribution* per active signal,
- $\iota = \frac{N}{T}$: the signal *incidence rate*—i.e., the number of active
  signals
  per unit time.

This leads to the *presence invariant*:

$$ \text{Average Presence Density} = \text{Signal Incidence Rate} \times \text{Average Mass Contribution per Signal} $$
or in our notation

$$ \delta = \iota \cdot \bar{m} $$

This identity holds for *any* co-present subset of signals over *any* finite
time interval.

### An example

To build intuition for these abstract terms, let's look at a practical example.

For example, suppose our signals represent revenues from customer purchase over
some time period. If we look at a system of presences, across an interval of
time, say a week, the total presence mass $A$ represents the total revenues
across all customers who contributed to that revenue. $T$ is the time period
measured in some unit of time (say days) and $N$ is the number of paying
customers in that period.

The average presence density is the daily revenue rate, the signal mass
contribution for each signal is revenue for each customer, the average signal
mass contribution is the average revenue per customer for that week, and the
incidence rate represents the average daily rate of active customers over the
week.

So the presence invariant is stating that the revenue rate for the week is the
product of the average revenue per customer and the average number of active
customers over the week.

### Why it matters

While algebraically, the presence invariant is a tautology, it imposes a
powerful constraint on system behavior—one that is independent of the specific
system, semantics, or timescale. Think of it as the generalization of our
intuitive revenue example to any arbitrary system of presences.

Indeed, it forms a foundational conservation law of the presence calculus: the
*conservation of mass (contribution)*.

Just as the conservation of energy or mass constrains the evolution of physical
systems—regardless of the specific materials or forces involved—the conservation
of presence mass constrains how observable activity is distributed over time in
a system of presences. This conservation law applies to how presence mass is
conserved across time. While independent of the semantics of what is being
observed, like energy, presence mass can shift, accumulate, or redistribute, but
its total balance across presences within a finite time interval remains
invariant

While independent of the semantics of what is being observed, like energy,
presence mass can shift, accumulate, or redistribute, but its total balance
across presences within a finite time interval remains invariant.

Thus, the conservation of mass plays a role in the presence calculus similar to
that of other conservation laws in physics: it constrains the behavior of three
key observable, measurable parameters of any system of presences.

It is important to note that this makes the "averages" in the presence invariant
much more than descriptive statistics. While they may be interpreted as such,
these are not simply measures of centrality on a set of observed presences, but
quantities with a concrete physical interpretation, expressed via the invariant,
that directly govern how a system of presences behaves in time.

Exploiting this constraint allows us to study and characterize the long-run
behavior of a system.

### Binary Presences and Little's Law

At this stage, the presence invariant may still feel a bit abstract. Let's make
it more concrete by interpreting this identity in the special case of *binary*
presences.

Recall that a *binary* signal is a function whose density is either $0$ or $1$.
That is, we are modeling the presence or absence of an underlying signal in the
domain.

In this case, the *mass contribution* of a signal becomes an _element-time
duration_. For example, if the signal represents the time during which a task is
present in development, the mass contribution of that task over an observation
interval is the portion of its duration that intersects the interval. This is
also called the _residence time_[^7] for the task in the observation window.

[^7]: We note that the residence time represents only the portion of the duration of the task in some arbitrary observation window. This is a different quantity from the overall duration of the task from start to finish (or from signal onset to reset in our terminology). This is the more familiar metric typically called the cycle time. 

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/presence_invariant_binary.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 6: The Presence Invariant for binary signals
  </div>
</div>

Figure 6 shows possible configurations of binary signals intersecting a finite
observation interval. Suppose the unit of time is days.

The total presence mass accumulation $A$ is $11$ task-days. The number $N$ of
tasks that intersect the observation interval is $4$. The length of the
observation window is $T = 4$ days. It is straightforward to verify that the
presence invariant holds.

Now, let's unpack its meaning.

Since each task contributes $1$ unit of mass for each unit of time it is
present, the average presence density $\delta=\frac{A}{T}$ represents the
*average number of tasks* present per unit time in the interval—denoted $L$.

Conversely, since each unit of mass corresponds to a unit of time associated
with a task, the average mass per active signal, $\bar{m} = \frac{A}{N}$, is
the average time a task spends in the observation window. This value is
typically called the *residence time* $w$ of a task in the observation window.

The incidence rate $\iota = \frac{N}{T}$ may be interpreted as the *activation
rate* of tasks in the interval—a proxy for the rate at which tasks start (onset)
or finish (reset) within the window.

For example, $N$ may be counted as the number of tasks that start inside the
interval, plus the number that started before but are still active. Thus,
$\frac{N}{T}$ is a *cumulative onset rate* $\Lambda$.

The presence invariant can now be rewritten as:

$$ L = \Lambda \times w $$

which you may recognize as *Little's Law* applied over a finite observation
window. Thus, the presence invariant serves as a *generalization of Little’s
Law*—extending it to arbitrary systems of presence density functions (signals)
measured over finite observation windows.

It is important to note that we are referring to *Little's Law over a finite
observation window*, rather than the much more familiar, steady-state
equilibrium form of Little's Law.

Unlike the equilibrium form of the law, this version
holds *unconditionally*. The key is that the quantities involved are
*observer-relative*: the time tasks spend *within a finite observation window*,
and the *activation rate* of tasks *over the window*, rather than the
task-relative durations or steady-state arrival/departure rates used in the
equilibrium form.

Indeed, the difference between these two forms of the
identity will serve as the basis for how we *define* whether a system of
presences is in equilibrium or not. The idea is that the system of presences is
at equilibrium when observed over sufficiently long observation windows such
that the observer-relative and task-relative values of average presence density,
incidence rate and average presence mass converge.

Since complex systems often operate far from equilibrium—and since the presence
invariant holds *regardless* of equilibrium—the finite-window form becomes far
more valuable for analyzing the long-run behavior of such systems as they *move
into and between* equilibrium states.

We'll also note that for any arbitrary signal, we can always define a binary
presence corresponding to the intervals over which the value of the density
function is non-zero (the support interval). In general then, we can say the
finite window version of Little's Law, with the above definitions, always
applies to _any_ signal under this interpretation. _In addition,_ the general
presence invariant also applies to the full signal.

We will return to this important topic shortly. But first, let's understand the
implications of the presence invariant.

### Causal Reasoning

The presence invariant gave us an important constraint that applies to the
behavior of three key parameters of a system of presences when measured over any
finite time interval: the average presence density, the signa incidence rate,
and the average mass contribution per signal.

This means that if we observe the behavior of a system of presences over a
continuous sequence of non-overlapping time intervals, the presence invariant
holds in _each_ such interval, and given the value of any two of the parameters,
the third is completely determined.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/system_presences_discrete.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 7: Sampling a system of presence across uniform intervals. 
  </div>
</div>

The requirement that presence mass is conserved across each interval means that
there are only two degrees of freedom between three variables.

Furthermore, within the structure of this identity, presence density is the
resultant variable, while the incidence rate and signal mass contribution act as
its fundamental, independent variables.

Thus, the invariant explicitly states that any change in presence density is an
_outcome_ that is necessarily accounted for by a change in incidence rate or
signal mass contribution.

This means that if you observe a shift in presence density, you know it must
originate from changes in either how frequently signals appear (incidence rate)
or how much 'mass' each signal contributes on average (average mass
contribution), or both.

Since the invariant holds across *any* finite interval, this also implies that
if we study how these parameters change in concert as we move _across_ time
intervals, we will get unique insights into how a _particular_ system of
presences evolves over time.

This is a powerful tool in causal reasoning: being able to analyze _why_ a
system of presences behaves the way it does. Specifically, it provides a
powerful framework for structural causal attribution when analyzing the changes
in behavior of a system or presences.

Specifically, if we think of these three parameters of a system as defining the
unique co-ordinates of the state of the system over a small finite interval, we
can "trace" the movement of the system by following these co-ordinates. But
since there are only two degrees of freedom these coordinates will always lie on
a two dimensional manifold[^8], in a 3 dimensional space.

[^8]: All solutions to an equation of the form $x=y \times z,$ which is the form
of the presence invariant, lie on a 2D surface, called a manifold in 3
dimensions: think of the manifold a rubber sheet suspended in a 3 dimensional
space. All the values of $x, y, \text{ and } z$  that satisfy this equation will
lie on the surface of this rubber sheet. This is a powerful geometric constraint
that we can exploit to reason about the possible behavior of a system of
presences over time.

If fact, remarkably, the state of _every_ possible system of presences, no matter
how general, always has a trajectory in time that lies on this *same* manifold.
This is a powerful constraint and insight that we can use to study the behavior
of a system of presences over time.

We will now introduce a tool called the presence matrix that makes it easier to
visualize and manage the computations involved in doing so.

## 5. The Presence Matrix

A *presence matrix* records the presence mass distribution obtained by sampling
a set of presence density functions over a fixed set of time intervals.
Specifically, if we fix a time granularity—such as hours, days or weeks—we can
construct a matrix in which:

- *Rows* correspond to individual signals (e.g., for each $(
  e, b)$ pair),
- *Columns* correspond to non-overlapping time intervals at that fixed time
  granularity _that cover the time axis_,
- *Entries* contain the *presence mass*, i.e., the integral of the density
  function over the corresponding interval:

  $$ M_{(e,b),j} = \int_{t_j}^{t_{j+1}} f_{(e,b)}(t) \, dt $$

The resulting matrix provides a discrete, temporally-aligned representation of
this system of presences.

Since we are accumulating presence masses over an interval, the value of
presence mass in a matrix entry is always a a real number. Figure 8 shows the
presence matrix for the system in Figure 7[^9].

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/presence_matrix.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 8: Presence Matrix for a system of presences. 
  </div>
</div>

[^9]: The alert reader will note the difference between the first two rows in
the matrix. The first signal is represented by a single presence, while the
second is broken up into two disjoint presences. This is entirely an artifact of
the granularity at which the timeline is divided. At a suitably fine sampling
granularity, the first signal could also be represented by two presences. As
discussed earlier, this has no real impact on the behavior of the invariant. In
general we will use signals as the unit at which incidence is measured.

The presence matrix encodes some deep structural properties of a system of
presences. Many of key concepts we want to highlight are easier to define and
understand in terms of this representation.

The Presence Calculus Toolkit documentation has more details on the mechanics of
its construction and the computations it enables. For now, these details are not
critical, and we will focus on the insights it surfaces.

### The presence invariant and the presence matrix.

Let's revisit Figure 3, reproduced below, which introduced the idea of thinking
of presence mass as a sample of an underlying signal.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/multiple_support.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 3: A presence as a sample of a signal over an interval.
  </div>
</div>

When we observe a system of presences across a finite observation window, as we
do in deriving the presence invariant, we are looking at presence mass across
a "vertical" slice of time across all signals.

<div style="text-align: center; margin:2em">
<table>
  <thead>
    <tr>
      <th>E\B</th>
      <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
      <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>e1_b1</td>
      <td style="background-color: #c6f6c6">0.3</td>
      <td style="background-color: #c6f6c6">2.3</td>
      <td style="background-color: #c6f6c6">3.4</td>
      <td style="background-color: #c6f6c6">1.1</td>
      <td style="background-color: #c6f6c6">2.9</td>
      <td style="background-color: #c6f6c6">3.2</td>
      <td style="background-color: #c6f6c6">1.1</td>
      <td>0.0</td><td>0.0</td><td>0.0</td>
    </tr>
    <tr>
      <td>e1_b2</td>
      <td style="background-color: #c6f6c6">0.3</td>
      <td style="background-color: #c6f6c6">2.3</td>
      <td style="background-color: #c6f6c6">3.4</td>
      <td style="background-color: #c6f6c6">1.1</td>
      <td>0.0</td>
      <td style="background-color: #c6f6c6">1.1</td>
      <td style="background-color: #c6f6c6">2.2</td>
      <td style="background-color: #c6f6c6">2.4</td>
      <td style="background-color: #c6f6c6">2.3</td>
      <td style="background-color: #c6f6c6">0.8</td>
    </tr>
    <tr>
      <td>e2_b2</td>
      <td>0.0</td><td>0.0</td><td>0.0</td><td>0.0</td><td>0.0</td>
      <td>0.0</td>
      <td style="background-color: #c6f6c6">0.9</td>
      <td style="background-color: #c6f6c6">1.8</td>
      <td style="background-color: #c6f6c6">3.2</td>
      <td style="background-color: #c6f6c6">0.9</td>
    </tr>
    <tr>
      <td>e2_b1</td>
      <td style="background-color: #c6f6c6">0.8</td>
      <td style="background-color: #c6f6c6">1.3</td>
      <td style="background-color: #c6f6c6">2.4</td>
      <td style="background-color: #c6f6c6">2.8</td>
      <td style="background-color: #c6f6c6">3.0</td>
      <td style="background-color: #c6f6c6">3.2</td>
      <td style="background-color: #c6f6c6">3.4</td>
      <td style="background-color: #c6f6c6">2.4</td>
      <td>0.0</td><td>0.0</td>
    </tr>
  </tbody>
</table>
<div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 9: The presence matrix from Figure 8, reproduced
  </div>
</div>

The presence matrix, shown in figure 9, makes this notion explict - assuming
some fixed granularity of observation window, a vertical slice in time
corresponds to a column in the presence matrix.

Looking at the sums of the presence masses along the rows of the matrix gives us
the mass contributions per signal (or presence) and the row sums give us
cumulative presence mass per signal across all presences.

Given a sequence of columns of the presence matrix, the signal incidences are
simply the number of rows that have non-zero values those rows. It's
straightforward now to interpret the presence invariant in terms of the presence
matrix.

Further, you can see that we can construct a presence matrix from any subset of
the rows of another presence matrix, and it would still be a presence matrix,
for which the presence invariant applies. What is more, the presence invariant
applies for any _consecutive_ sequence of columns of the presence matrix.

Thus the presence invariant encodes very strong _local_ constraints in how
presence mass distributes in time across signals, and we can use these to derive
meaningful constraints on the global accumulation of presence mass across a
system of presences.

### The Presence Accumulation Matrix

To visualize and reason about both the micro and macro behaviors of a system of
presences in a natural way, we will need the help of a data structure called the
Presence Accumulation matrix. It compresses a lot of information about the
interaction between local and global behavior of a system of presences across
time scales and relies heavily on the fact that the presence invariant is
scale-independent.

We'll continue with the presence matrix of Figure 9, to illustrate how it is
constructed. 

Recall that the columns of the presence matrix represent time intervals at the finest level of granularity at which an underlying system of signals and presences is sampled. If we have an $MxN$ of $M$ signal sampled at $N$ consecutive intervals, the value in the presence matrix at row $i$ and column $j$ represents the sampled presence mass of signal $i$ at time interval $j$. 

Consider the matrix $A$ that we accumulates presences masses across consecutive time intervals of various length between 1 and $N$. This is a square matrix of size $NxN$ and is constructed as follows. For our example, this is a 10x10 matrix. 

The diagonal of the matrix contains the accumulated presence mass across each interval of length 1. This corresponds to the sum of each column of the presence matrix. 

<div style="text-align: center; margin:2em">
  <table>
  <thead>
    <tr>
      <th>i\\j</th>
      <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
      <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td style="background-color:#e6ffe6">1.4</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td>2</td><td></td><td style="background-color:#e6ffe6">5.9</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td>3</td><td></td><td></td><td style="background-color:#e6ffe6">9.2</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td>4</td><td></td><td></td><td></td><td style="background-color:#e6ffe6">5.0</td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td>5</td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">5.9</td><td></td><td></td><td></td><td></td></tr>
    <tr><td>6</td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">7.5</td><td></td><td></td><td></td></tr>
    <tr><td>7</td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">7.6</td><td></td><td></td></tr>
    <tr><td>8</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">6.6</td><td></td></tr>
    <tr><td>9</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">5.5</td></tr>
    <tr><td>10</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">1.7</td></tr>
  </tbody>
</table>
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 10: Cumulative presence mass along intervals of length 1. 
  </div>
</div>

The next diagonal row contains the cumulative presence mass for intervals of length 2 - ie $A(1,2)$ contains the sum of all entries in columns 1 and 2. $A(2,3)$ contains the sum of all entries column 2 and 3 and so on.. 

<div style="text-align: center; margin:2em">
  <table>
  <thead>
    <tr>
      <th>i\\j</th>
      <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
      <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td style="background-color:#e6ffe6">1.4</td>
      <td style="background-color:#e6f0ff">7.3</td>
      <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
    </tr>
    <tr>
      <td>2</td>
      <td></td>
      <td style="background-color:#e6ffe6">5.9</td>
      <td style="background-color:#e6f0ff">15.1</td>
      <td></td><td></td><td></td><td></td><td></td><td></td>
    </tr>
    <tr>
      <td>3</td>
      <td></td><td></td>
      <td style="background-color:#e6ffe6">9.2</td>
      <td style="background-color:#e6f0ff">14.2</td>
      <td></td><td></td><td></td><td></td><td></td>
    </tr>
    <tr>
      <td>4</td>
      <td></td><td></td><td></td>
      <td style="background-color:#e6ffe6">5.0</td>
      <td style="background-color:#e6f0ff">10.9</td>
      <td></td><td></td><td></td><td></td>
    </tr>
    <tr>
      <td>5</td>
      <td></td><td></td><td></td><td></td>
      <td style="background-color:#e6ffe6">5.9</td>
      <td style="background-color:#e6f0ff">13.4</td>
      <td></td><td></td><td></td>
    </tr>
    <tr>
      <td>6</td>
      <td></td><td></td><td></td><td></td><td></td>
      <td style="background-color:#e6ffe6">7.5</td>
      <td style="background-color:#e6f0ff">15.1</td>
      <td></td><td></td>
    </tr>
    <tr>
      <td>7</td>
      <td></td><td></td><td></td><td></td><td></td><td></td>
      <td style="background-color:#e6ffe6">7.6</td>
      <td style="background-color:#e6f0ff">14.2</td>
      <td></td>
    </tr>
    <tr>
      <td>8</td>
      <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
      <td style="background-color:#e6ffe6">6.6</td>
      <td style="background-color:#e6f0ff">12.1</td>
    </tr>
    <tr>
      <td>9</td>
      <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
      <td style="background-color:#e6ffe6">5.5</td>
      <td style="background-color:#e6f0ff">7.2</td>
    </tr>
    <tr>
      <td>10</td>
      <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
      <td style="background-color:#e6ffe6">1.7</td>
    </tr>
  </tbody>
</table>
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 11: Cumulative presence mass along intervals of length 2. 
  </div>
</div>
We can continue filling the matrix out in diagonal order this way until we get the presence accumulation matrix shown below. 
<div style="text-align: center; margin:2em">
  <table>
  <thead>
    <tr>
      <th>i\\j</th>
      <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
      <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
    </tr>
  </thead>
  <tbody>
    <!-- Row 1 -->
    <tr>
      <td>1</td>
      <td style="background-color:#e6ffe6">1.4</td>
      <td style="background-color:#e6f0ff">7.3</td>
      <td style="background-color:#e6ffe6">16.5</td>
      <td style="background-color:#e6f0ff">21.5</td>
      <td style="background-color:#e6ffe6">27.4</td>
      <td style="background-color:#e6f0ff">34.9</td>
      <td style="background-color:#e6ffe6">42.5</td>
      <td style="background-color:#e6f0ff">49.1</td>
      <td style="background-color:#e6ffe6">54.6</td>
      <td style="background-color:#e6f0ff">56.3</td>
    </tr>
    <!-- Row 2 -->
    <tr>
      <td>2</td>
      <td></td>
      <td style="background-color:#e6ffe6">5.9</td>
      <td style="background-color:#e6f0ff">15.1</td>
      <td style="background-color:#e6ffe6">20.1</td>
      <td style="background-color:#e6f0ff">26.0</td>
      <td style="background-color:#e6ffe6">33.5</td>
      <td style="background-color:#e6f0ff">41.1</td>
      <td style="background-color:#e6ffe6">47.7</td>
      <td style="background-color:#e6f0ff">53.2</td>
      <td style="background-color:#e6ffe6">54.9</td>
    </tr>
    <!-- Row 3 -->
    <tr>
      <td>3</td>
      <td></td><td></td>
      <td style="background-color:#e6ffe6">9.2</td>
      <td style="background-color:#e6f0ff">14.2</td>
      <td style="background-color:#e6ffe6">20.1</td>
      <td style="background-color:#e6f0ff">27.6</td>
      <td style="background-color:#e6ffe6">35.2</td>
      <td style="background-color:#e6f0ff">41.8</td>
      <td style="background-color:#e6ffe6">47.3</td>
      <td style="background-color:#e6f0ff">49.0</td>
    </tr>
    <!-- Row 4 -->
    <tr>
      <td>4</td>
      <td></td><td></td><td></td>
      <td style="background-color:#e6ffe6">5.0</td>
      <td style="background-color:#e6f0ff">10.9</td>
      <td style="background-color:#e6ffe6">18.4</td>
      <td style="background-color:#e6f0ff">26.0</td>
      <td style="background-color:#e6ffe6">32.6</td>
      <td style="background-color:#e6f0ff">38.1</td>
      <td style="background-color:#e6ffe6">39.8</td>
    </tr>
    <!-- Row 5 -->
    <tr>
      <td>5</td>
      <td></td><td></td><td></td><td></td>
      <td style="background-color:#e6ffe6">5.9</td>
      <td style="background-color:#e6f0ff">13.4</td>
      <td style="background-color:#e6ffe6">21.0</td>
      <td style="background-color:#e6f0ff">27.6</td>
      <td style="background-color:#e6ffe6">33.1</td>
      <td style="background-color:#e6f0ff">34.8</td>
    </tr>
    <!-- Row 6 -->
    <tr>
      <td>6</td>
      <td></td><td></td><td></td><td></td><td></td>
      <td style="background-color:#e6ffe6">7.5</td>
      <td style="background-color:#e6f0ff">15.1</td>
      <td style="background-color:#e6ffe6">21.7</td>
      <td style="background-color:#e6f0ff">27.2</td>
      <td style="background-color:#e6ffe6">28.9</td>
    </tr>
    <!-- Row 7 -->
    <tr>
      <td>7</td>
      <td></td><td></td><td></td><td></td><td></td><td></td>
      <td style="background-color:#e6ffe6">7.6</td>
      <td style="background-color:#e6f0ff">14.2</td>
      <td style="background-color:#e6ffe6">19.7</td>
      <td style="background-color:#e6f0ff">21.4</td>
    </tr>
    <!-- Row 8 -->
    <tr>
      <td>8</td>
      <td></td><td></td><td></td><td></td><td></td><td></td><td></td>
      <td style="background-color:#e6ffe6">6.6</td>
      <td style="background-color:#e6f0ff">12.1</td>
      <td style="background-color:#e6ffe6">13.8</td>
    </tr>
    <!-- Row 9 -->
    <tr>
      <td>9</td>
      <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
      <td style="background-color:#e6ffe6">5.5</td>
      <td style="background-color:#e6f0ff">7.2</td>
    </tr>
    <!-- Row 10 -->
    <tr>
      <td>10</td>
      <td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>
      <td style="background-color:#e6ffe6">1.7</td>
    </tr>
  </tbody>
</table>
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 12: Final presence accumulation matrix for the presence matrix of Figure 9. 
  </div>
</div>

 We can see that in practice, this matrix compresses a large amount of information in a very compact form. For example if the columns represent weekly samples of signals a 52x52 matrix allows us to analyze a whole years worth of presence accumulation across every time-scale ranging from a single week to a whole year in one compact structure. We'll shortly see why this is useful. 

First lets define the general structure of the presence accumulation matrix.

Let $P \in \mathbb{R}^{M \times N}$ be the presence matrix of $M$ signals 
sampled at $N$ consecutive time intervals. The **Presence Accumulation Matrix** 
$A \in \mathbb{R}^{N \times N}$ is defined by:

$$
A(i, j) = \sum_{k=1}^{M} \sum_{\ell=i}^{j} P(k, \ell)
\quad \text{for all } 1 \leq i \leq j \leq N
$$

That is, $A(i,j)$ gives the total presence mass of all signals across the 
interval $[i,j]$.

### Properties

- $A$ is upper triangular: $A(i,j)$ is defined only when $i \leq j$.
- The diagonal entries $A(i,i)$ equal the column sums of $P$.
- Each entry $A(i,j)$ reflects the cumulative presence mass over the interval 
  $[i,j]$.


As we will see below, this matrix compactly encodes multi-scale information about system behavior 
and supports the analysis of both micro and macro scale behavior of a system of presences. 

## 6. Applying the Presence Calculus

The presence calculus might seem like a highly abstract, theoretical framework,
but much of its utility emerges when we *interpret* its concepts in a specific,
applied context.

Concepts such as presence mass, incidence rates, and density are not unlike
abstract physical notions like force, mass, and acceleration. In principle,
these are measurable quantities that nature constrains to behave in prescribed
ways at a micro scale.

Once we understand the rules governing their micro-scale behavior, we gain tools
to systematically measure, reason about, and explain a vast range of observable
macro-scale phenomena. Much of physics is built on this principle.

In a similar vein, the presence calculus—and especially the *presence invariant*
—provides a foundational law that governs the local, time-based behavior of any
system composed of time-varying signals and the presences they induce.

Once we recognize that such a governing constraint exists, the presence calculus
equips us with tools to describe, interpret, explain, and, in certain cases,  
make verifiable predictions about the macro-scale behavior of these systems.

Newtonian mechanics, for example, allows us to describe and predict the motion
of physical systems with remarkable precision—such as planetary orbits or the
paths of falling objects. Yet even within this well-established framework,
certain limits remain: the general three-body problem has no closed-form
solution, and systems like the double pendulum exhibit chaotic behavior that
defies long-term prediction.

Still, we can represent the behavior and evolutions of such systems as
deterministic trajectories through a parameter space, uncovering structure even
where precise global behavior remain unpredictable. In much the same way, the
presence calculus does not seek to forecast the exact evolution of complex
systems. Instead, by explicitly modeling signal histories and representing
element trajectories over time, it equips us with powerful descriptive and
explanatory tools.

In this way, structural constraints and local invariants help us interpret
locally observed dynamics and connect it to system behavior at the macro scale.

Let's see how.

### Sample Paths and Convergence

Consider the highlighted portions of the accumulation matrix $A$ in figure 13.
<div style="text-align: center; margin:2em">
  <table>
  <thead>
    <tr>
      <th>i\\j</th>
      <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
      <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td style="background-color:#e6ffe6">1.4</td>
      <td style="background-color:#ffffcc">7.3</td>
      <td style="background-color:#ffffcc">16.5</td>
      <td style="background-color:#ffffcc">21.5</td>
      <td style="background-color:#ffffcc">27.4</td>
      <td style="background-color:#ffffcc">34.9</td>
      <td style="background-color:#ffffcc">42.5</td>
      <td style="background-color:#ffffcc">49.1</td>
      <td style="background-color:#ffffcc">54.6</td>
      <td style="background-color:#ffffcc">56.3</td>
    </tr>
    <tr><td>2</td><td></td><td style="background-color:#e6ffe6">5.9</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td>3</td><td></td><td></td><td style="background-color:#e6ffe6">9.2</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td>4</td><td></td><td></td><td></td><td style="background-color:#e6ffe6">5.0</td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td>5</td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">5.9</td><td></td><td></td><td></td><td></td></tr>
    <tr><td>6</td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">7.5</td><td></td><td></td><td></td></tr>
    <tr><td>7</td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">7.6</td><td></td><td></td></tr>
    <tr><td>8</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">6.6</td><td></td></tr>
    <tr><td>9</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">5.5</td></tr>
    <tr><td>10</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">1.7</td></tr>
  </tbody>
</table>
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 13: Sample paths, micro and macro scale accumulation. 
  </div>
</div>

The diagonal represents a sequence of measurements of independent intervals at
the finest measurement granularity. The top row represents the other extreme, a
series of measurements along a single long interval, each of which contains the
presences in all the previous intervals. The top row in the matrix represents
the presence history over all the intervals - the cumulative presences for
intervale $[0,j) \text{for} 1 \le j \lt N.$

We can divide each of the entries in the accumulation matrix with the length of
the time interval it covers to get the presence density for each interval. For
the diagonal interval has length 1 (time unit) and for the top row the lengths
range from 1 to $N-1.$

<div style="width: 100%; display: flex; justify-content: center; margin-top: 1em; margin-bottom: 1em;">
<table style="border-collapse: collapse;">
  <thead>
    <tr>
      <th>i\\j</th>
      <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
      <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td style="background-color:#e6ffe6">1.4</td>
      <td style="background-color:#ffffcc">3.6</td>
      <td style="background-color:#ffffcc">5.5</td>
      <td style="background-color:#ffffcc">5.4</td>
      <td style="background-color:#ffffcc">5.5</td>
      <td style="background-color:#ffffcc">5.8</td>
      <td style="background-color:#ffffcc">6.1</td>
      <td style="background-color:#ffffcc">6.1</td>
      <td style="background-color:#ffffcc">6.1</td>
      <td style="background-color:#ffffcc">5.6</td>
    </tr>
    <tr><td>2</td><td></td><td style="background-color:#e6ffe6">5.9</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td>3</td><td></td><td></td><td style="background-color:#e6ffe6">9.2</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td>4</td><td></td><td></td><td></td><td style="background-color:#e6ffe6">5.0</td><td></td><td></td><td></td><td></td><td></td></tr>
    <tr><td>5</td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">5.9</td><td></td><td></td><td></td><td></td></tr>
    <tr><td>6</td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">7.5</td><td></td><td></td><td></td></tr>
    <tr><td>7</td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">7.6</td><td></td><td></td></tr>
    <tr><td>8</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">6.6</td><td></td></tr>
    <tr><td>9</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">5.5</td></tr>
    <tr><td>10</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color:#e6ffe6">1.7</td></tr>
  </tbody>
</table>
</div>

So now we have the left hand side of the presence invariant encoded matrix form
for every pair of continuous intervals in the system.

We refer to the diagonal of the accumulation matrix as a *sample path* through
the presence history of the system. It records the presence mass observed at
each time interval independently, forming a discrete, time-indexed sequence.
This captures the micro-scale behavior of the system of presences.

The top row of the matrix represents the cumulative presence mass across each
prefix of that path — that is, the total presence observed from the beginning of
the observation period up to each point along the path. It reflects the long-run
trend in average presence density and captures the macro-scale behavior of the
system.

Let's chart the values in both of these rows in the matrix.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/first_row_vs_main_diagonal.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 9: Convergence of long run average presence density.
  </div>
</div>

We note that while the values measured along a sample path can be volatile, the
long-run averages along that path stabilize and converge to a finite
value.

We call a system of presences *convergent* if there exists a sufficiently long
sample path along which this stabilization occurs. Otherwise, we say the system
is *divergent*.

In a convergent system, the average presence density over time settles toward a
finite value. Intuitively, this means that after observing enough of the
system's history, additional observation does not significantly alter our
understanding of its long-term behavior.

Some systems converge rapidly to a single stable limit. Others may not settle on
one fixed point, but instead move between a small number of such limits. These
represent dominant behavioral modes—equilibrium states that the system can enter
and sustain for extended periods.

Divergent systems, by contrast, exhibit no such limiting behavior. The presence
density in these systems continues to grow without bound, indicating that no
stable long-term pattern emerges.

It is important to emphasize that convergence and divergence are properties of
the observed *behavior* of a system of presences, not of the underlying system
itself. We cannot infer the nature of the underlying system solely from whether
it appears convergent or divergent. We can only observe the presence dynamics
over time and assess whether they exhibit convergence.



<table style="border-collapse: collapse; margin: auto;">
  <thead>
    <tr>
      <th>i\\j</th>
      <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
      <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>2</td><td></td><td>3</td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>3</td><td></td><td></td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>4</td><td></td><td></td><td></td><td>2</td><td>2</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>5</td><td></td><td></td><td></td><td></td><td>2</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>6</td><td></td><td></td><td></td><td></td><td></td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>7</td><td></td><td></td><td></td><td></td><td></td><td></td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>8</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>3</td><td>4</td><td>4</td></tr>
    <tr><td>9</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2</td><td>3</td></tr>
    <tr><td>10</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2</td></tr>
  </tbody>
</table><table style="border-collapse: collapse; margin: auto;">
  <thead>
    <tr>
      <th>i\\j</th>
      <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
      <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>2</td><td></td><td>3</td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>3</td><td></td><td></td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>4</td><td></td><td></td><td></td><td>2</td><td>2</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>5</td><td></td><td></td><td></td><td></td><td>2</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>6</td><td></td><td></td><td></td><td></td><td></td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>7</td><td></td><td></td><td></td><td></td><td></td><td></td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>8</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>3</td><td>4</td><td>4</td></tr>
    <tr><td>9</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2</td><td>3</td></tr>
    <tr><td>10</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2</td></tr>
  </tbody>
</table><table style="border-collapse: collapse; margin: auto;">
  <thead>
    <tr>
      <th>i\\j</th>
      <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
      <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>2</td><td></td><td>3</td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>3</td><td></td><td></td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>4</td><td></td><td></td><td></td><td>2</td><td>2</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>5</td><td></td><td></td><td></td><td></td><td>2</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>6</td><td></td><td></td><td></td><td></td><td></td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>7</td><td></td><td></td><td></td><td></td><td></td><td></td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>8</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>3</td><td>4</td><td>4</td></tr>
    <tr><td>9</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2</td><td>3</td></tr>
    <tr><td>10</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2</td></tr>
  </tbody>
</table><table style="border-collapse: collapse; margin: auto;">
  <thead>
    <tr>
      <th>i\\j</th>
      <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
      <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>2</td><td></td><td>3</td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>3</td><td></td><td></td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>4</td><td></td><td></td><td></td><td>2</td><td>2</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>5</td><td></td><td></td><td></td><td></td><td>2</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>6</td><td></td><td></td><td></td><td></td><td></td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>7</td><td></td><td></td><td></td><td></td><td></td><td></td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>8</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>3</td><td>4</td><td>4</td></tr>
    <tr><td>9</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2</td><td>3</td></tr>
    <tr><td>10</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2</td></tr>
  </tbody>
</table><table style="border-collapse: collapse; margin: auto;">
  <thead>
    <tr>
      <th>i\\j</th>
      <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
      <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>2</td><td></td><td>3</td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>3</td><td></td><td></td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>4</td><td></td><td></td><td></td><td>2</td><td>2</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>5</td><td></td><td></td><td></td><td></td><td>2</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>6</td><td></td><td></td><td></td><td></td><td></td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>7</td><td></td><td></td><td></td><td></td><td></td><td></td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>8</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>3</td><td>4</td><td>4</td></tr>
    <tr><td>9</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2</td><td>3</td></tr>
    <tr><td>10</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2</td></tr>
  </tbody>
</table><table style="border-collapse: collapse; margin: auto;">
  <thead>
    <tr>
      <th>i\\j</th>
      <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
      <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>2</td><td></td><td>3</td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>3</td><td></td><td></td><td>3</td><td>3</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>4</td><td></td><td></td><td></td><td>2</td><td>2</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>5</td><td></td><td></td><td></td><td></td><td>2</td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>6</td><td></td><td></td><td></td><td></td><td></td><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>7</td><td></td><td></td><td></td><td></td><td></td><td></td><td>4</td><td>4</td><td>4</td><td>4</td></tr>
    <tr><td>8</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>3</td><td>4</td><td>4</td></tr>
    <tr><td>9</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2</td><td>3</td></tr>
    <tr><td>10</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2</td></tr>
  </tbody>
</table>



<table style="border-collapse: collapse; margin: auto;">
  <thead>
    <tr>
      <th>i\\j</th>
      <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
      <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>0.13 ∠ -0.29</td><td>0.68 ∠ -0.3</td><td>0.9 ∠ -0.29</td><td>1.08 ∠ -0.31</td><td>1.15 ∠ -0.33</td><td>1.2 ∠ -0.38</td><td>1.22 ∠ -0.43</td><td>1.24 ∠ -0.47</td><td>1.26 ∠ -0.51</td><td>1.26 ∠ -0.55</td></tr>
    <tr><td>2</td><td></td><td>0.86 ∠ -0.29</td><td>1.02 ∠ -0.29</td><td>1.17 ∠ -0.31</td><td>1.26 ∠ -0.34</td><td>1.29 ∠ -0.39</td><td>1.31 ∠ -0.44</td><td>1.32 ∠ -0.48</td><td>1.34 ∠ -0.52</td><td>1.34 ∠ -0.56</td></tr>
    <tr><td>3</td><td></td><td></td><td>0.71 ∠ -0.23</td><td>0.94 ∠ -0.26</td><td>1.14 ∠ -0.3</td><td>1.2 ∠ -0.35</td><td>1.26 ∠ -0.41</td><td>1.31 ∠ -0.46</td><td>1.34 ∠ -0.5</td><td>1.36 ∠ -0.54</td></tr>
    <tr><td>4</td><td></td><td></td><td></td><td>0.06 ∠ 0.0</td><td>0.42 ∠ 0.19</td><td>0.61 ∠ 0.18</td><td>0.8 ∠ 0.16</td><td>0.91 ∠ 0.14</td><td>0.97 ∠ 0.13</td><td>1.01 ∠ 0.12</td></tr>
    <tr><td>5</td><td></td><td></td><td></td><td></td><td>0.1 ∠ 0.0</td><td>0.46 ∠ 0.21</td><td>0.69 ∠ 0.2</td><td>0.83 ∠ 0.18</td><td>0.91 ∠ 0.17</td><td>0.97 ∠ 0.16</td></tr>
    <tr><td>6</td><td></td><td></td><td></td><td></td><td></td><td>0.19 ∠ 0.0</td><td>0.56 ∠ 0.23</td><td>0.75 ∠ 0.22</td><td>0.88 ∠ 0.21</td><td>0.97 ∠ 0.2</td></tr>
    <tr><td>7</td><td></td><td></td><td></td><td></td><td></td><td></td><td>0.15 ∠ 0.0</td><td>0.51 ∠ 0.24</td><td>0.73 ∠ 0.23</td><td>0.89 ∠ 0.22</td></tr>
    <tr><td>8</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0.06 ∠ 0.0</td><td>0.43 ∠ 0.23</td><td>0.67 ∠ 0.22</td></tr>
    <tr><td>9</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0.08 ∠ 0.0</td><td>0.44 ∠ 0.25</td></tr>
    <tr><td>10</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0.0 ∠ 0.0</td></tr>
  </tbody>
</table>


























