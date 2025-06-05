# The Presence Calculus, <br> A Gentle Introduction

**Dr. Krishna Kumar**  
*The Polaris Advisor Program*

## What is The Presence Calculus?

The Presence Calculus is a new approach for reasoning quantitatively about the  
relationships between things and places in a domain over time.

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

# The pitch

We introduce the simple but powerful concept of a *presence*.

This lets us reason about time, history and evolution using techniques from
measure theory, topology and complex analysis.

Classical statistics and probability theory often struggle here.
*History*—the sequence and structure of changes in the domain over time— is
usually fenced off under assumptions like ergodicity, stationarity, and
independence.

However, probability theory and statistic remain very powerful tools for
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

## Learning more about The Presence Calculus

While the calculus was developed with mathematical rigor, an equally important  
goal was not to let mathematics get in the way of understanding the simple but
very powerful and general ideas the calculus embodies[^1].

[^1]: This document is the first step in that direction. We welcome feedback on
how it can be improved,and the concepts clarified. Please feel free to open a
pull request with thoughts, suggestions or feedback.

In this document, we'll motivate and introduce the key ideas in the calculus  
informally, with lots of highly evocative examples and simplifications to  
illustrate concepts.

It is aimed squarely at the non-technical reader. We'll also continue with
ongoing informal exposition on our blog  
[The Polaris Flow Dispatch](https://www.polaris-flow-dispatch.com).

We recommend reading and understanding the ideas here before jumping deeper  
into the rest of the documentation at this site, which does get a fair bit  
more dense. The next level of detail is in the API docs for
[The Presence Calculus  
Toolkit](https://py.pcalc.org).

The toolkit is an open source python library that is designed to provide
efficient implementations for all the core concepts in the presence calculus. In
the API documentation, we go into the concepts at a level of rigor that you'll
need to work with the pcalc API and apply the concepts. Some mathematical
background will be useful here if you want to develop extend the core.

Finally, for those who want to dive deeper into the formal mathematical  
underpinnings of the calculus, we have the theory track, which perhaps goes  
into more detail than most people will need to read or understand, but is  
useful for the mathematically trained to connect the ideas to their roots in  
mainstream mathematics.

Let's jump in...

## Why Presence?

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

## An example

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

## A software example

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

## The heart of the matter

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

## What is a presence?

Let's start by building intuition for this concept we call a *presence*.  
Consider the statement: “The task $X$ was in Development from Monday to  
Friday.”

In the presence calculus, this would be expressed as a presence of the form:  
“The element $X$ was in boundary $Y$ from $t_0$ to $t_1$ with mass 1.”  
Presences are statements about elements (from some domain) being present in a  
boundary (from a defined set of boundaries) over a *continuous* period of
time,  
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

## What is the mass of a presence?

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
bait-and-switch, rest assured, this is the last time you will need to think of
them in this document - *provided* you accept the statement that anything that
we can do it in presences calculus with binary presences can also be done with
general presence density functions. Besides, we had to say something about why
we call this a
*calculus*, and this is as good a point to do that as any!

## Presence density functions and measure theory

Binary presence functions are much easier to understand intuitively, and we'll  
continue using them in our examples. But the real power of the presence  
calculus comes from generalizing to *presence density functions*.

In our earlier example, we interpreted the presence density function (PDF) as  
expressing the *load* placed on an element at a boundary. But more generally,  
a PDF can be *any* real-valued function over time.

The mass of a presence, over any given time *interval* $[t_0, t1)$ is the
integral above, which is also the area under the presence density function over
that interval[^3].

[^3]: The way we've defined presence density functions and mass is directly  
analogous to how mass is defined for matter occupying space in physics.

    A binary PDF can be thought of as defining a one-dimensional interval over  
    time. For a fixed element and boundary, this gives us an area under the  
    curve in two dimensions: time vs. density.

    If we treat elements and boundaries as additional independent dimensions,  
    then the PDF defines a *volume* in three dimensions, with time as one axis.  

    This interpretation—presence as a physical manifestation of density over  
    time—is a powerful way to reason intuitively and computationally about 
    duration, overlap, and accumulation in time.

    And when we allow multiple PDFs to interact over the same time periods, we  
    begin to model complex, higher-dimensional effects of presence—exactly the  
    kind of generality we’ll need when we move beyond simple binary presences.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/presence_definition.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 2: Presence, Presence Density Function and Presence Mass
  </div>
</div>

The only requirement for a function to be a presence density function is  
that it is *measurable*, and that you can interpret *presence mass*—defined as
the integral of the function over a finite interval—as a meaningful
*measure* of the effect of presence in your domain.

This is where measure theory enters the picture. It’s not essential to  
understand the full technical details, but at its core, measure theory tells  
us which kinds of functions are *measurable*—in other words, which functions  
can support meaningful accumulation, comparison, and composition of values.

Measurability gives us the confidence to do things like compute statistics,  
aggregate over elements or boundaries, and compose presence effects—while  
preserving the semantics of the domain. Informally, when a PDF is measurable, we
can treat its values like any other real number and do math over them, as long
as we carefully respect the units involved.

From our perspective, a presence density function captures a kind of  
measurement that can be *accumulated* across time and across presences. This  
lets us reason mathematically about presences with confidence—and since most  
of this reasoning will be performed by algorithms, we need technical  
constraints that ensure those calculations are both mathematically valid and  
semantically sound.

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

## More examples

Let's firm up our intuition about what presences can describe with a few more  
examples.

### "Work" in software

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

### The effects of interruptions

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

Another important use case in the same vein is modeling the cost of delay for
a  
portfolio-level element—and analyzing its cascading impact across the  
portfolio.

These use cases show that it is possible to analyze not just binary presences,  
but entire chains of influence they exert across a timeline—a key prerequisite  
for reasoning about causality.

### Self-reported developer productivity

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

### Browsing behavior on an e-commerce site

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

### Patient movement in a hospital

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

## Systems of Presences

Let's summarize what we've described so far.

With presence density functions and presences, we now have a general structure  
for describing and measuring the behaviour of an arbitrary time varying
function. The key feature of a presence is that it abstracts these behaviors
into a uniform representation—one that we can reason about and compute with.

### Presence Assertions

In Figure 2, we showed the *onset* and *reset* times of a presence density  
function. The interval between an onset and a reset is called the *support* of  
the PDF. Within this interval, the function is non-zero.

As we see in Figure 3, a given PDF may have *multiple* such disjoint support  
intervals. These represent non-contigous presences of the same element within
the same boundary over time. These may correspond, to episodic behavior in the
underlying domain, for example, user sessions in an e-commerce context, or
rework loops in software development when a task "returns" to development many
times over its lifecycle.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/multiple_support.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 3: A presence as a sample of a PDF over an interval.
  </div>
</div>

A presence may be defined over *any* sub-interval of a PDF, as shown in Figure

3.

There are many possible ways of defining a presence from a PDF, including across
disjoint support intervals. All we require is that the interval in question  
intersects a region of non-zero area that can be reduced to a presence mass.

So, a presence is best thought of as a *sampled measurement* of the underlying  
PDF, taken by an *observer* over two specific points in time and reduced to a  
point-mass measurement over that interval.

A given observer may not even "see" the full underlying PDF—only the *mass*  
of the presence they experience over the interval they observed.

Different observers may observe different intervals of the same PDF and derive  
different presence values, depending on what part of the function they  
encounter.

This brings us to the concept of *presence assertions*, which formalize this  
idea of an observer recording a presence based on their local view of the  
underlying density function.

A *presence assertion* is simply a presence augmented with metadata:

- *who* the observer was
- and an *assertion timestamp*—the time at which the observation was made.

The assertion time doesn't need to align with the time interval of the presence.
This allows assertions to refer to the past, reflect the present, or even
anticipate the future behavior of a PDF.

Presence assertions give us the ability to assign *provenance* to a presence—  
not just *what* we know, but *how* we know it. This is essential in  
representing complex systems where the observer and the act of observation  
are first-class concerns.

We won’t go too deeply into the epistemological aspects of the presence  
calculus here—this remains an active and open area of research. But it’s  
important to acknowledge that this layer exists, and that modeling and  
interpreting the output of the presence calculus requires an explicit treatment
of how observations are made and by whom.

With this caveat in place, once we've represented a problem domain as a  
*system of presences*, much of the machinery of the presence calculus (which  
we'll introduce next) can be applied uniformly.

In particular, there are no fundamental differences in behavior between systems
of binary presences and systems of presences with arbitrary mass—once they've
been reduced to a canonical, presence-oriented representation[^5].

[^5]: There are several technical conditions that must be satisfied when  
mapping PDFs to a canonical system of presences in order for this claim to  
hold. To avoid getting bogged down in those details, we’ll simply claim it for  
now. The API docs go into more detail about the mechanics of this canonical  
representation, and what’s needed to ensure a "clean" mapping from a PDF to a  
system of presences—or more precisely, a system of presence assertions.

## The Presence Invariant

In the last section, we introduced *systems of presences* as collections of
presence assertions defined over a set of presence density functions (PDFs).

Figure 5 illustrates an example of such a system, where we focus on the subset
of presences defined over a *shared observation interval*.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/presence_invariant_continuous.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 5: The Presence Invariant
  </div>
</div>

These presences are called *co-present*—they represent an observer making
simultaneous measurements of presence mass across multiple PDFs over a common
interval of time.

Each presence density function contributes a *presence mass*, defined as the
integral of the density over the observation interval. The sum of these
individual *mass contributions* gives the total presence mass observed across
the system in that interval.

In this section, we introduce a key construct in the presence calculus: the
*presence invariant*. It expresses a general and powerful relationship that
holds for any co-present subset of presences within a finite observation window.

Let

$$ A = M_0 + M_1 + M_3 $$

be the total mass contribution from the PDFs that have non-zero mass over the
interval $[t_0, t_1)$. The length of this interval is $T = t_1 - t_0$.

Since the mass comes from integrating a density function over time, the quantity
$\frac{A}{T}$ represents the *average presence density* over the observation
interval. We can now decompose this as:

$$ \delta = \frac{A}{T} = \frac{A}{N} \times \frac{N}{T} $$

This separates the average presence density into two interpretable components:

- $\bar{m} = \frac{A}{N}$: the *average mass contribution* per active PDF,
- $\iota = \frac{N}{T}$: the *incidence rate*—i.e., the number of active PDFs
  per unit time.

This leads to the *presence invariant*:

$$ \text{Average Presence Density} = \text{Incidence Rate} \times \text{Average
Mass Contribution} $$ or in our notation

$$ \delta = \iota \cdot \bar{m} $$

This identity holds for *any* co-present subset of PDFs over *any* finite time
interval.

While algebraically, this relationship is a tautology, it imposes a powerful
constraint on system behavior—one that is independent of the specific system,
semantics, or timescale.

Indeed, it forms a foundational conservation law of the presence calculus: the
*conservation of mass (contributions)*.

Just as the conservation of energy or mass constrains the evolution of physical
systems—regardless of the specific materials or forces involved—the conservation
of presence mass constrains how observable activity is distributed over time in
a system of presences.

It is independent of the semantics of what is being observed: like energy,
presence mass can shift, accumulate, or redistribute, but it remains balanced
when distributed across presences over a finite interval remains invariant.

Thus, the conservation of mass plays a role in the presence calculus similar to
that of other conservation laws in physics. It constrains the behavior of three
key observable, measurable parameters of any system of presences.

More importantly, exploiting this constraint allows us to study and characterize
the long-run behavior of the system.

This provides a rigorous framework for reasoning about the history of a
path-dependent system of presences—a key prerequisite for analyzing the long-run
evolution of presence systems and understanding emergent patterns in that
evolution.

### The Presence Invariant for Binary Presences

One of the key features of the presence calculus is that it provides very
general mechanisms for computing over functions—but the value of this machinery
is only realized through modeling and reinterpreting its results in the language
of the domain.

At this stage, the presence invariant may still feel rather abstract. Let's make
it more concrete by interpreting this identity in the special case of *binary*
presences.

Recall that a *binary* PDF is a function whose density is either $0$ or $1$.
That is, we are modeling the presence or absence of an underlying signal in the
domain.

In this case, the *mass contribution* of a PDF becomes an element-time duration.
For example, if the PDF represents the time during which a task is present in
development, the mass contribution of that task over an observation interval is
the portion of its duration that intersects the interval. This is also called
the _residence time_ for the task in the observation window.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/presence_invariant_binary.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 6: The Presence Invariant for Binary PDFs
  </div>
</div>

Figure 6 shows possible configurations of binary PDFs intersecting a
finite observation interval.

Suppose the unit of time is days.

The total presence mass accumulation $A$ is $11$ task-days. The number $N$ of
tasks that intersect the observation interval is $4$. The length of the
observation window is $T = 4$ days. It is straightforward to verify that the
presence invariant holds.

Now, let's unpack its meaning.

Since each task contributes $1$ unit of mass for each unit of time it is
present, the average presence density $ \delta = \frac{A}{T}$ represents the
*average number of tasks* present per unit time in the interval—denoted $L$.

Conversely, since each unit of mass corresponds to a unit of time associated
with a task, the average mass per active presence, $\bar{m} = \frac{A}{N}$, is
the average time a task spends in the observation window. This value is
typically called the *residence time* $w$ of a task in the observation window, a
term we will adopt in general for presences.

The incidence rate $\iota = \frac{N}{T}$ may be interpreted as the *activation
rate* of tasks in the interval—a proxy for the rate at which tasks start (onset)
or finish (reset) within the window.

For example, $N$ may be counted as the number of tasks that start inside the
interval, plus the number that started before but are still active. Thus,
$\frac{N}{T}$ approximates a *cumulative onset rate* $\Lambda$.

The presence invariant can now be rewritten as:

$$ L = \Lambda \times w $$

which you may recognize as *Little's Law* applied over a finite observation
window. Thus, the presence invariant serves as a **generalization of Little’s
Law**—extending it to arbitrary systems of presence density functions.

We'll also note that for any arbitrary PDF, we can always define a binary
presence corresponding to the intervals over which the value of the density
function is non-zero (the support interval) and so in general, we can say the
finite window version of Little's Law, with the above definitions, always
applies to _any_ presence density function, _in addition_ to the general
presence invariant, which applies to the full presence density function, not
just its support.

It is important to note that we are referring to *Little's Law over a finite
observation window*, rather than the steady-state equilibrium form of Little's
Law. Just like the presence invariant in the general case, this version of the
law holds *unconditionally*. The key is that the quantities involved are
*observer-relative*: the time tasks spend *within the observation window*, and
the *activation rate* of tasks *over the window*, rather than the task-relative
durations or steady-state arrival/departure rates used in classical queueing
theory.

Indeed, in the general case, the difference between these two forms of the
identity will serve as the basis for how we *define* whether a system of
presences is in equilibrium or not. The idea is that the system of presences is
at equilibrium when observed over sufficiently long observation windows such
that the observer-relative and task-relative values of average presence density,
incidence rate and average presence mass converge.

Since complex systems often operate far from equilibrium—and since the presence
invariant holds *regardless* of equilibrium—the finite-window form becomes far
more valuable for analyzing the long-run behavior of such systems as they *move
into and between* equilibrium states.

We will return to this important topic shortly. But first, let's build a bit
more machinery so that we can work computationally with sets of presences in a
more natural and systematic way.

## The Presence Matrix

In the previous section, we introduced a *system of presences* as a collection
of presence assertions, where each assertion corresponds to the *mass* of an
underlying presence density function over a time interval.

We noted that such presence assertions can be derived in many ways, depending on
how time is partitioned—that is, on the *choice of sampling intervals* used to
evaluate the density functions.

A *presence matrix* captures this structure by sampling a set of presence
density functions over a fixed set of time intervals. Specifically, if we fix a
time granularity—such as hours or days—we can construct a matrix in which:

- *Rows* correspond to individual presence density functions (e.g., for each $(
  e, b)$ pair),
- *Columns* correspond to non-overlapping time intervals _that cover the time
  axis_,
- *Entries* contain the *presence mass*, i.e., the integral of the density
  function over the corresponding interval:

  $$ M_{(e,b),j} = \int_{t_j}^{t_{j+1}} f_{(e,b)}(t) \, dt $$

The resulting matrix provides a discrete, temporally-aligned representation of
this system of presences. Since we are accumulating presence masses over an
interval, the value of presence mass in a matrix entry is always a a real
number.























