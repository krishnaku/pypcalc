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

This, in turn, lets us apply techniques from disclines such as stochastic
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
informally, with lots of highly simplified examples and allusions to  
illustrate concepts.

It is aimed squarely at the non-technical reader. We'll also continue with
ongoing informal exposition on our blog  
[The Polaris Flow Dispatch](https://www.polaris-flow-dispatch.com).

We recommend reading and understanding the ideas here before jumping deeper  
into the rest of the documentation at this site, which does get a fair bit  
more dense.

The next level of detail is in the API docs for the [The Presence Calculus  
Toolkit](https://py.pcalc.org). The toolkit is an open source python library
that is designed to provide efficient implementions for all the core concepts in
the presence calculus. In the API documentation, we go into the concepts at a
level of rigor that you'll need to work with the pcalc API and apply the
concepts. Some mathematical background will be useful here if you want to
develop extensions to the core.

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
interactions and emergent assemblages of presences in a rigorous and structured,
and more importantly, computable way.

## What is a presence?

Let's start by building intuition for this concept we call a *presence*.  
Consider the statement: “The task $X$ was in Development from Monday to  
Friday.”

In the presence calculus, this would be expressed as a presence of the form:  
“The element $X$ was in boundary $Y$ from $t_0$ to $t_1$ with mass 1.”  
Presences are statements about elements (from some domain) being present in a  
boundary (from a defined set of boundaries) over a *continuous* period of
time,  
measured using some time scale.

So why do we say “with mass 1”?

The presence calculus treats time as a physical dimension, much like space.  
Just as matter occupies space, presences occupy time. Just as mass quantifies  
*how* matter occupies space, the mass of a presence quantifies *how* a  
presence occupies time.

The statement “The task $X$ was in Development from Monday through Friday” is  
a **binary presence** with a uniform mass of 1 over the entire duration. The  
units of this mass are element-time—in this case, task-days.

Binary presences are sufficient to describe the *fact* of presence or absence  
of things in places in a domain. These presences always have mass 1 in
whatever  
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

$$ \text{mass} = \int_{t_0}^{t_1} f(e, b, t)\, dt $$

where $f$ is the presence density function [^2].

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
a PDF can be *any* real-valued function over time. The only requirement is  
that you can interpret *presence mass*—defined as the integral of the function  
over a finite interval—as a meaningful *measure* of the effect of presence in  
your domain.

This is where measure theory enters the picture. It’s not essential to  
understand the full technical details, but at its core, measure theory tells  
us which kinds of functions are *measurable*—in other words, which functions  
can support meaningful accumulation, comparison, and composition of values.

Measurability gives us the confidence to do things like compute statistics,  
aggregate over elements or boundaries, and compose presence effects—while  
preserving the semantics of the domain. When a PDF is measurable, we can  
treat its values like any other real number and do math over them, as long as  
we carefully respect the units involved.

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
presence[^3].

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









