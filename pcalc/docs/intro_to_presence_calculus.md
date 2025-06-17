# The Presence Calculus, <br> A Gentle Introduction

**Dr. Krishna Kumar**  
*The Polaris Advisor Program*

<div style="text-align: center; margin:2em">
  <img src="../assets/pcalc/presence_calculus.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 1: A System of Presences
  </div>
</div>

## 1. What is The Presence Calculus?

The Presence Calculus is a quantitative model for reasoning about the  
relationships between signals in a domain over time.

It's purpose is to better support principled modeling and rigorous
decision-making with operational data in business-critical domains. A key
objective was to ensure that the use of data in such decisions rests on a
mathematically precise, logically coherent, and epistemically grounded
foundation.

The presence calculus emerged from a search for better quantitative tools to
reason about operations management in software product development and
engineering, where current approaches to measurement leave much to be desired in
all three aspects.

Minimally, the foundational constructs of the calculus bring mathematical  
precision to widely used—but poorly defined—concepts such as flow, stability,
equilibrium, and coherence in a domain. More importantly, it allows us to relate
them to business-oriented concerns like delay, cost, revenue, and user
experience.

As you’ll see, however, the core concepts behind the calculus are far more
general, with potential applications well beyond the software context it emerged
from.

### The pitch

We introduce the simple but powerful concept of a *presence*.

This lets us reason about time, history and evolution of a set of _signals_ that
measure time-varying properties of a domain using techniques from measure
theory, topology and complex analysis.

Classical statistics and probability theory often struggle here.
*History*—the sequence and structure of changes in the domain over time— is
usually fenced off under assumptions like ergodicity, stationarity, and
independence.

Our thesis is that to move beyond simple descriptive statistics and statistical
or probabilistic inference, and reason effectively about global and long run
behavior of real world systems, we need
analytical techniques that treat time and history as first-class concepts we can
model and calculate with.

The presence calculus is a bridge that lets us combine statistical techniques
with techniques from disciplines such as stochastic process dynamics, queueing
theory, and complex systems science, to reason about the dynamics of such
systems.

We claim that it is a novel, constructive approach to do this from first
principles in a domain - a new, general set of modeling and analytical tools for
working with real world systems including non-linear, stochastic and complex
adaptive systems.

### Learning more about The Presence Calculus

While the calculus was developed with mathematical rigor, an equally important
goal was not to let mathematics get in the way of understanding the simple but
very powerful and general ideas the calculus embodies[^F1].

[^F1]: This document is the first step in that direction. We welcome feedback on
how it can be improved,and the concepts clarified. Please feel free to open a
pull request with thoughts, suggestions or feedback.

In this document, we'll motivate and introduce the key ideas in the calculus
informally, with lots of evocative examples and simplifications to  
illustrate concepts.

In order to maintain rigor, some basic mathematical notation is used in key
sections.
We augment these with examples to build intuition throughout. However, given the
nature of the material we have opted to stay on the side of precision rather
than
dilute the concepts, even in this "gentle" introduction.

If you are inclined to skim over anything with mathematical notation in it,
working through the examples should be sufficient to grasp the key ideas and
claims. However, for those who are comfortable with it, the mathematics should
be easy to understand and verify.

We recommend reading and understanding all the main ideas here before jumping
deeper into the rest of the documentation at this site, which does get a fair
bit more dense and technical.

If that deeper dive is not your cup of tea, we'll continue with ongoing informal
exposition on our
blog [The Polaris Flow Dispatch](https://www.polaris-flow-dispatch.com), where
we will focus mostly on applications of the ideas.

This document can be thought as the middle ground: detailed enough to
understand the concepts and ideas clearly and precisely, but just a starting
point if you want to really dig deeper.

That next level of detail is in the API docs for [The Presence Calculus  
Toolkit](https://py.pcalc.org).

The toolkit is an open source python library that implements all the core
concepts in the presence calculus. It is designed as an analytical middleware
layer suitable for interfacing real world operational systems and complex system
simulation, to the analytical machinery of the presence calculus.

In the API documentation, we go into the
concepts at a level of rigor that you'll need to work with the pcalc API and
apply the concepts. Some mathematical background will be useful here if you want
to apply the concepts and extend beyond the core.

If reading code is more your style than reading mathematical notation, then we
recommend jumping into the code and running the examples (or writing your own)
to understand how things work. If you find bugs, please raise them!

Finally, for those who want to dive deeper into the formal mathematical  
underpinnings of the calculus, we have the theory track, which perhaps goes into
more detail than most people will need to read or understand, but is useful for
the mathematically trained to connect the ideas to their roots in mainstream
mathematics.

Let's jump in...

### What is Presence?

Presence is how reality reveals itself.

We do not perceive the world as disjointed events in time, but rather as an
unfolding—things come into being, endure for a time, and slip away.

Permanence is just a form of lasting presence. What we call *change* is the  
movement of presences in and out of our awareness, often set against that  
permanence.

The sense of something being present—or no longer present—is our most  
immediate way of detecting change. This applies to both the tangible—people,
places, and things—and the intangible—emotions, feelings, and experiences.

Either way, we reason about the world by reasoning about the presences and
absences in our environment over time.

The presence calculus begins here. Before we count, measure, compare, or  
optimize, we observe what *is*.

And what we model is presence.

### An example

Imagine you see a dollar bill on the sidewalk on your way to get coffee.  
Later, on your way back home, you see it again—still lying in the same spot. It
would be reasonable for you to assume that the dollar bill was present there the
whole time.

Of course, that may not be true. Someone might have picked it up in the  
meantime, felt guilty, and quietly returned it. But in the absence of other  
information, your assumption holds: it was there before, and it’s there now, so
it must have been there in between.

This simple act of inference is something we do all the time. We fill in gaps,
assume continuity, and reason about what must have been present based on what we
know from partial glimpses of the world.

The presence calculus gives formal shape to this kind of inference—and shows how
we can build upon it to *reason* about presence and *measure* its  
effects in an environment.

### A software example

Since the ideas here emerged from the software world, let’s begin with a  
mundane, but familiar example: task work in a software team.

By looking closely at how we reason about tasks, we can see how a subtle shift
from an event-centered to a presence-centered perspective changes not just what
we observe, but what we measure, and thus can reason about.

We usually reason about task work using *events* and *snapshots* of the state  
of a process in time. A task “starts” when it enters development, and  
“finishes” when it’s marked complete. We track "cycle time" by measuring the
elapsed time between events, "throughput" by counting finish events, and "
work-in-process" by counting tasks that have started but not yet finished.

When we look at a Kanban board, we see a point-in-time snapshot of where tasks
are at that moment—but not how they got there. And by the time we read a summary
report of how many tasks were finished and how long they took to go
through the process on average, much of the history of the system that produced
those measurements has been lost. That makes it hard to reason about *why*
those measurements are the way they are.

In software development, each task often has a distinct history—different  
from other tasks present at the same time. Losing history makes it hard to  
reason about the interactions between tasks and how they impact the global
behavior of the process.

This problem is not unique to task work. Similar problems exist in almost all
areas of business analysis that rely primarily on event models and descriptive
statistics derived from events as the primary measurement tool for analyzing
system behavior.

We are reduced to trying to make inferences from local descriptive  
statistics —things like cycle times, throughput, and work-in-process levels-
over a rapidly changing process.

We try to reason about a process which is shaped by its history, whose behavior
emerges from non-uniform interactions of individual signals, with measurement
techniques that struggle to represent or reason about that history or the
interactions.

This is difficult to do, and we have no good tools right now that are fit for
this purpose. This is where the presence calculus begins.

The calculus focuses on the time *in between* snapshots of history: when a task
was present, where it was present, for how long, and whether its presence
shifted across people, tools, or systems.

The connective tissue is no longer the task itself, or the process steps it  
followed, or who was working on it, but a continuous, observable *thread of  
presence*—through all of them, moving through time, interacting, crossing
boundaries—a mathematical representation of history.

With the presence calculus, these threads and their interactions across time and
space can now be measured directly, dissected, and analyzed as first-class
constructs—built on a remarkably simple primitive—the presence.

### The heart of the matter

At its core, the calculus exploits the difference between the two independent
statements—“The task started development on Monday” and “The task completed
development on Friday”—and a single, unified assertion: “The task was present in
development from Monday through Friday.”

The latter is called a *presence*, and it is the foundational building block  
of the calculus. At first glance, this might not seem like a meaningful
difference.

But treating the presence as the primary object of reasoning—as a
*first-class* construct—opens up an entirely new space of possibilities.

Specifically, it allows us to apply powerful mathematical tools that exploit the
topology of time and the algebra of time intervals to reason about the
interactions and emergent configurations of presences in a rigorous and
structured, and more importantly, computable way.

## 2. What is a Presence?

Let's start by building intuition for the concept of presence. Consider the
statement: “The task $X$ was in Development from Monday to Friday.”

In the presence calculus, this would be expressed as a statement of the form:
“The element $X$ was in boundary $Y$ from $t_0$ to $t_1$ with mass 1.”

Presences are statements about elements (from some domain) being present in a
boundary (from a defined set of boundaries) over a *continuous* period of time,
measured using some timescale.

So why do we say “with mass 1”?

The presence calculus treats time as a physical dimension, much like space. Just
as matter occupies space, presences occupy time. Just as mass quantifies *how*
matter occupies space, the mass of a presence quantifies *how* a presence
occupies time.

The statement “The task $X$ was in Development from Monday through Friday” is a
**binary presence** with a uniform mass of 1 over the entire duration. The units
of this mass are element-time—in this case, task-days.

Binary presences are sufficient to describe the *fact* of presence or absence  
of things in places in a domain. These presences always have mass 1 in whatever
units we use for elements and time.

### Presence mass

Let's consider a different set of statements:

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

We will describe this using a presence with an arbitrary real valued mass. We
will assume that there is some function, called $\mathsf{load}$ in this case,
that computes this mass.

The presence can then be described as

- $(\mathsf{load}, X, \text{Development}, \text{Monday}, \text{Wednesday}, 2)$
- $(\mathsf{load}, X, \text{Development}, \text{Thursday}, \text{Thursday}, 3)$
- $(\mathsf{load}, X, \text{Development}, \text{Friday}, \text{Friday}, 1)$

Here, $\mathsf{load}(e, b, t)$ is a time-varying function that takes an  
element $e$, a boundary $b$, and a time $t$, and returns a real-valued number  
describing how much presence is concentrated at that point in time.

The *presence mass* of such a presence is the total presence over the  
interval $[t_0, t_1]$, defined as:

$$ \text{mass} = \int_{t_0}^{t_1} \mathsf{load}(e, b, t)\, dt $$

where $\mathsf{load}$ is called a presence density function [^F2].

[^F2]: If integration signs in a "gentle" introduction feels like a
bait-and-switch, rest assured, for the purposes of this document you just need
to
think of them as a way to add up presence masses, in a way that the ideas we use
for binary presences will generalize when we apply them to arbitrary functions.

Binary presences are much easier to understand intuitively, but the real power
of the presence calculus comes from generalizing to *presence density
functions*.

### Domain Signals and Presence Density Functions

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/presence_definition.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 2: Signals, Presence,  and Presence Mass
  </div>
</div>

In our earlier example, we showed a presence that described the *load* placed on
an element at a boundary, and this has a real-valued presence mass. More
generally, we can think of defining a presence over an arbitrary time varying
function with real numbers as values.

In general, such presence density function represent some underlying signal from
the domain that we are interested in measuring. So, in what follows, we will use
the terms signal and presence density functions interchangeably, opting for the
latter only those cases where we want to focus specifically on the fact that
what we are representing about the signal is the "amount" of the signal (its
presence) over time.

As shown in Figure 2, the mass of a presence density function, over any given
time *interval* $[t_0, t1)$ is the integral over the interval, which is also the
area under the signal over that interval[^F3].

[^F3]: The way we've defined signals and mass is directly  
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
examples of presence density functions.

#### "Work" in software

If you've ever written a line of code in your life, you’ve heard the question:  
“When will it be done?” Work in software can be a slippery, fungible concept—  
and the presence calculus offers a useful way to describe it.

We can express the work on a task using a presence density function whose  
value at time $t$ is the *remaining* work on the task at $t$.

This lets us model tasks whose duration is uncertain in general, but whose  
remaining duration can be estimated, subject to revision, at any given time—a
common scenario in software contexts.

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
the impact of binary presences—capturing their downstream or distributed effects
over time, and reasoning about their relationship over a shared timeline.

Another important use case in the same vein is modeling the cost of delay for a
portfolio-level element—and analyzing its cascading impact across the  
portfolio.

These use cases show that it is possible to analyze not just binary presences,  
but entire chains of influence they exert across a timeline—a key prerequisite  
for reasoning about causality.

#### Self-reported developer productivity

Imagine a developer filling out a simple daily check-in:  
"How productive did you feel today?"—scored from 1 to 5, or sketched out as a  
rough curve over the day[^F4].

[^F4]: The use of a rough curve here is an example of how presences can encode  
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

With signals and presences, we now have a framework for describing and measuring
the behavior of time-varying domain signals—each representing how a
specific element behaves within a given boundary.

The key feature of a presence is that it abstracts these behaviors into a
uniform representation—one that we can reason about and compute with.

To summarize, a general presence is defined by:

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

* It might perfectly align with a single support interval (a 'hill' in the
  signal).
* It might span multiple disjoint support intervals, including the "zero"
  regions in between.
* It might capture only a portion of a single support.

All we require is that the interval chosen for the presence calculation
intersects a region of non-zero area from the signal that can be reduced to a
non-zero presence mass.

### Presence Assertions

Thus presence is best thought of as a *sampled measurement* of the underlying
signal, taken by an *observer* over a specific time interval, which yields a
total presence mass for that interval. 

A given observer may not even "see" the full underlying signal—only the *mass*  
of the presence they experience over the interval they observed.

Different observers may observe different intervals of the same signal and
derive different presence values, depending on what part of the function they  
encounter.

This brings us to the concept of *presence assertions*, which formalize the act
of recording a presence based on an observer’s local "view" of the
underlying density function.

A *presence assertion* is simply a presence augmented with metadata:

- *who* the observer was
- and an *assertion timestamp*—the time at which the observation was made.

The assertion time doesn't need to align with the time interval of the presence.
This allows assertions to refer to the past, reflect the present, or even
anticipate the future behavior of a signal.

#### The open world assumption

Time in the presence calculus is explicitly defined to be over <em>extended</em>
reals $\overline{\mathbb{R}}$: the real line $\mathbb{R}$ extended with the
symbols $-\infty$ and $+\infty$.

This is a mathematical representation of an open world assumption, which holds
that the history of a system of presences extends indefinitely into the past and
future.

An observer will typically only see a finite portion of this history and has to
make inferences on the basis of those observations, but in general, we need to
make inferences with partial information about the past and contingent
assumptions about the future.

A presence with $t_0 = -\infty$ represents a presence whose beginning is
unknown, and $t_1 = +\infty$ represents a presence whose end is unknown.

Presences with both start and end unknown are valid constructs and represent
eternal presences.

Many of the most interesting questions in the presence calculus involve
reasoning about the dynamics of a domain under the epistemic uncertainty
introduced by such presences.

#### A note on epistemology 

Presence assertions give us the ability to assign *provenance* to a presence—  
not just *what* we know, but *how* we know it. This is essential in  
representing complex systems where the observer and the act of observation  
are first-class concerns.

Further, since reasoning about time and history is a primary focus of the
calculus, presences with unknown beginnings or endings provide a way to
explicitly model what is known—and unknown—about that history. This will prove
more valuable than it might initially seem.

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

In the next sections, where we introduce this machinery, we will operate under
the assumption that there exists an observable _signal_, and that what is
observed reflects what an observer knows about the domain. We don't presume
anything about the "truth" of the observations, we treat them uniformly as
signals.

One thing we will see is that from the perspective of this machinery, there are
no fundamental differences in behavior between binary signals and arbitrary
signals once they've been reduced to a canonical, presence-mass oriented
representation[^F5].

This greatly increases the scope of the problem domains where the presence
calculus can be applied, and our examples in the previous section only begin to
hint at the possibilities.

This, in the end, is the source of the generality and power of the presence
calculus.

[^F5]: There are several technical conditions that must be satisfied when  
mapping signals to a canonical system of presences in order for this claim to  
hold. To avoid getting bogged down in those details, we’ll simply claim it for  
now. The API docs go into more detail about the mechanics of this canonical  
representation, and what’s needed to ensure a "clean" mapping from a signal to a
system of presences—or more precisely, a system of presence assertions.

#### A note on path dependence

By representing a presence at the granularity of an element in a boundary, we
explicitly recognize the path dependent nature of the domain signals.

In the presence calculus, signals represent some behavior of domain elements in
boundaries. The calculus itself is agnostic to what counts as an "element" or
a "boundary"— this is a domain modeling decision.

Even if they represent the same underlying quantity, we recognize that system
behavior emerges from the interactions between _individual_ signals at the
element-boundary granularity—each potentially with distinct presence density
functions. We are interested in studying _how_ system-level behavior arises from
the _interactions_ between these signals over time.

Modeling boundaries are crucial because, for a given domain element, the
boundary typically determines both which signals are relevant and how we wish to
analyze system behavior using them.

For example, a software feature (an element) may be modeled using one set of
signals during development (one boundary), another during production (a second
boundary), and yet another when customers begin using it (a third boundary).

All three signals are part of the feature’s history. Each feature follows a
unique path through these boundaries, producing its own independent set of
signals with a distinct history and evolution. These signals interact in complex
ways—over time, within boundaries, and with each other. The boundary is what
brings coherence to the analysis—it defines which signals and interactions we
choose to focus on, and why.

In summary, the boundary allows us to bring a coherent set of elements and
related signals together for analysis. That analysis focuses on how these
signals interact in _time_.

Constructing an appropriate set of element-boundary signals is *the* key
modeling decision. But once these are defined, much of the machinery of the
presence calculus can be applied without regard to the semantics of the specific
element-boundaries involved.

Semantics are, of course, crucial in _interpreting_ the inferences one draws  
using the machinery of the calculus.

When we refer to a "system" in the presence calculus we are explicitly defining
it as an _evolving_ set of presence assertions—i.e., the "system"
is what we can assert about a domain using presence assertions at a given time.

In summary, this is what we refer to as a "system of presences" - a time-indexed
collection of presence assertions derived from an underlying set of
path dependent element-boundary signals.

What we choose to model fundamentally shapes the system we are able to reason
about—and the presence calculus provides a powerful foundation for doing so.

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
the observation window[^F6]. This separates the average presence density into
two
interpretable components:

[^F6]: It is equally valid to define $N$ as the number of distinct _presences_
in
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

The key insight here is that the presence invariant establishes a fundamental
relationship between the mass contributions of individual signals and what is
observable about their interactions at a boundary over time—that is, their
presence density. This is precisely the kind of relationship the presence
calculus is designed to capture.

The fact that this invariant holds for any finite observation interval is a
powerful constraint—one we will exploit in reasoning about system behavior with the calculus.


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
conserved across time.

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
also called the _residence time_[^F7] for the task in the observation window.

[^F7]: We note that the residence time represents only the portion of the
duration of the task in some arbitrary observation window. This is a different
quantity from the overall duration of the task from start to finish (or from
signal onset to reset in our terminology). This is the more familiar metric
typically called the cycle time.

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

Now, let's interpret its meaning.

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

which you may recognize as *Little's Law* in its finite-window form.

Thus, the presence invariant serves as a *generalization of Little’s
Law*—extending it to arbitrary systems of presence density functions (signals)
measured over finite observation windows.

It is important to note that we are referring to *Little's Law over a finite
observation window*, rather than the much more familiar, steady-state
equilibrium form of Little's Law.

Unlike the equilibrium form of the law, this version
holds *unconditionally*. The key is that the quantities involved are
*observer-relative*: the time tasks spend *within a finite observation window*,
and the *activation rate* of tasks *over the window*, rather than the
task-relative durations or long-run arrival/departure rates assumed in the
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

All this is the focus of section 6, where we will formally make the connections
between the presence invariant and equilibrium states in systems of presence
with the help of a very general form of Little's Law originally proven by
Stidham.

For now, we will note that for any arbitrary signal, we can always define a
binary presence corresponding to the intervals over which the value of the
density function is non-zero (the support interval). In general then, we can say
the finite window version of Little's Law, with the above definitions, always
applies to _any_ signal under this interpretation.

_In addition,_ the general presence invariant also applies to the full signal.
Yet another version applies in equilibrium states—but all are, in effect,
different manifestations of the same underlying relationship captured in the
presence invariant.

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
a two dimensional manifold[^F8], in a 3 dimensional space.

[^F8]: All solutions to an equation of the form $x=y \times z,$ which is the
form
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
presence matrix for the system in Figure 7[^F9].

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/presence_matrix.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 8: Presence Matrix for a system of presences. 
  </div>
</div>

[^F9]: The alert reader will note the difference between the first two rows in
the matrix. The first signal is represented by a single presence, while the
second is broken up into two disjoint presences. This is entirely an artifact of
the granularity at which the timeline is divided. At a suitably fine sampling
granularity, the first signal could also be represented by two presences. As
discussed in footnote 6 above, this has no real impact on the behavior of the
invariant. In general we will use signals as the unit at which incidence is
measured.

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
  $[i,j]$ in the original presence matrix.


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

### Equilibrium: Convergence and Divergence

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
    Figure 13: Diagonal and top row of the accumulation matrix
  </div>
</div>

Each diagonal entry represents the total presence mass observed across all
signals in a single time interval. Thus, the diagonal traces the discrete-time
evolution of the system's observable activity—one step at a time. We will call
the sequence of values on the diagonal a _sample path_ for the system of
presences.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/diagonal_values.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 14: The values on the diagonal of the accumulation matrix.  
  </div>
</div>


Recall that each entry on the diagonal represents the sum of the presence masses
of the signals active in a time window. This implies that each entry on the top
row is an approximation of an integral[^F10] and equals the _area under the
sample path_ represented by the diagonal.

[^F10]: Specifically, the Riemann sum approximation of the integral $$
A(1, j) = \sum_{k=1}^j A(k,k)
\approx \int_0^j \left( \sum_{(e,b)} P_{(e,b)}(t) \right) dt
$$
where each $P_{(e,b)}(t)$ represents the presence density function of an
underlying element-boundary signal.


<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/top_row_values.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 15: The values on the top row accumulation matrix.  
  </div>
</div>

In other words, the diagonal and top row represent fundamentally different views
of the system: the diagonal captures the *micro-level behavior*—instantaneous  
presence mass across signals in each interval—while the top row encodes the  
*macro-level behavior*—the cumulative effect of those presences over time.  
Both views are compactly encoded in the structure of the  
accumulation matrix.

Figure 16 shows this geometric interpretation of the diagonal and top rows of
the accumulation matrix.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/sample_path_area.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 16: Sample path and the area under it.   
  </div>
</div>

If we divide each of the entries in the accumulation matrix by the length of the
time interval it covers, we get the presence density for each interval. For
the diagonal interval has length 1 (time unit) and for the top row the lengths
range from 1 to $N-1.$

<div style="text-align: center; margin:2em">
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
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 17: Presence density: diagonal and top row.   
  </div>
</div>

So now we have the left-hand side of the presence invariant encoded in matrix  
form for every pair of continuous intervals in the system.

Let's chart the values in both of these rows in the matrix.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/first_row_vs_main_diagonal.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 18: Convergence of long-run average presence density.
  </div>
</div>

We can see that while the values on the sample path are volatile, the values on
the top row converge towards a finite value. We can define this notion of
convergence precisely using the mathematical
concept of a limit. Let:

$$
\Delta = \lim_{T \to \infty} \frac{1}{T} \int_0^T \delta(t) \, dt
$$

Here, $\delta(t)$ is the instantaneous presence density introduced in the
presence invariant.  
The quantity $\Delta$, by contrast, represents the long-run average presence
density —  
the time-averaged total presence across all signals in the system.

In the discrete setting, this corresponds to the limiting value of the top row
of the  
accumulation matrix — a value toward which the green line in Figure 18 appears
to converge:

$$
\Delta = \lim_{j \to \infty} \frac{A(1,j)}{j}
$$

where $A(1,j)$ is the total presence mass accumulated from time 0 through
interval $j$.

Not every system of presences has such a limit. We call a system *convergent*
if  
$\Delta$ exists and is finite, and *divergent* otherwise.

To summarize: in a convergent system, the average presence density over time  
settles toward a finite value. Intuitively, this means that after observing  
enough of the system’s history, additional observation does not significantly  
alter our understanding of its long-term behavior.

Some systems converge rapidly to a single stable limit. Others may not settle  
at all, but instead move among a small number of such limits. These  
represent dominant behavioral modes — quasi-equilibrium states that the system  
can enter and sustain for extended periods. Such behavior is called  
*metastable* or *multi-modal*.

Divergence, by contrast, implies the absence of such limiting behavior. The  
presence density in these systems continues to grow without bound,  
indicating that no stable long-term pattern emerges.

Figure 19 shows examples of each of these behaviors.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/convergence_divergence.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 19: Convergent, Divergent, and Metastable behavior in systems of presences.
  </div>
</div>

If a limit $\Delta$ exists and is sustained over time, it signifies a stable
long-run average presence density for the system. This value represents a
specific pattern of average behavior toward which the system's observable
presence density gravitates over extended periods, regardless of short-term
fluctuations.

This concept aligns with the broader notion of attractors in dynamical systems.
While a system's full, high-dimensional state might exhibit complex dynamics,
the long-run average presence density can itself stabilize around a particular
value or set of values. When the presence density consistently settles around
such a limit, it indicates that the system's observable behavior has entered a
sustainable regime.

This provides a powerful way to characterize the system's overall operational
modes in the long term, even if its micro-level details remain complex and
unpredictable. We will have more to say on this topic shortly.

It is important to emphasize that convergence and divergence are properties  
of the *observed long-run behavior* of a system of presences — not intrinsic  
properties of the underlying system itself.

We cannot infer the system’s nature solely from whether it appears convergent or
divergent at any given time. We can only observe the dynamics of presence  
over time and assess whether they exhibit convergence.

The key difference between convergence and the other two modes is that a  
convergent system can effectively *forget* its history beyond the point of
stabilization.Its future behavior becomes representative of its past, allowing
the system to be characterized by a stable long-run average.

Among other things, the presence calculus equips us with the computational tools
needed to identify convergent, divergent and metastable states of a system of
presences.

#### The Semantics of Convergence

An important point to emphasize is that, depending on how presence density  
is interpreted in a given domain, *any* of the three behavioral modes —  
convergent, divergent, or metastable — may be desirable.  
Convergence is not inherently "good," nor is divergence necessarily "bad."

For example, in repetitive manufacturing or many customer service domains,  
convergence is often desired. In these contexts, presence typically  
represents *demand* on a constrained resource, and keeping that demand  
stable is essential for ensuring consistent service times, throughput,  
and resource utilization. Traditional operations management and queueing theory
therefore seek out — and emphasize — stability and convergence in key  
operational signals.

By contrast, if presence represents a company’s *customer base* or *market  
share*, we *want* the long-run presence density to look like the chart on  
the right: up and to the right — that is, *divergent*.

Metastable modes are common and often highly desirable in software  
development, where teams must shift between modes of operation in  
response to external demands or changing market conditions. Indeed, the  
ability to transition between such modes effectively is often a hallmark of a
high-functioning, adaptive organization — *provided* it is done intentionally
and with awareness.

All too often, however, organizations drift from metastable to chaotic  
behavior, losing the capacity to stabilize in any mode. This often results  
from a lack of visibility into — or the inability to reason about — their  
operational state.

One of the major practical applications of the presence calculus is to  
bring new analytical tools to *observe*, *categorize*, and *steer* the  
behavior of such complex systems — aligning them with the desired modes of  
operation in a given domain, *before* critical tipping points are reached.

### Detecting Convergence

In the last section, we *defined* convergent behavior in terms of the  
existence of the limit $\Delta$, the long-run average presence density  
of the system.

Now we ask: under what observable conditions does such a limit exist?

If we can identify these conditions, we gain levers to begin *steering*  
systems toward desired modes of operation.

It turns out the answer is hiding in plain sight — in the presence  
invariant, which, as we've seen, holds for *any* finite observation  
window. The limit $\Delta$ represents the asymptotic average of $\delta(t)$,  
the left-hand side of the invariant, measured over a sequence of consecutive  
overlapping intervals, each one a prefix of the sample path.

For each such prefix interval $t$ , the _presence invariant_ gives us:

$$
\delta(t) = \iota(t) \times \bar{m}(t)
$$

This tells us that each value of $\delta(t)$ is determined by the  
product of two measurable quantities: $\iota(t)$, the incidence rate,  
and $\bar{m}(t)$, the average mass contribution per signal.

To understand when the long-run average of $\delta(t)$ converges, we can ask  
a simpler question: do the corresponding long-run averages of $\iota(t)$  
and $\bar{m}(t)$ converge? If both do, we should expect that their product —  
and hence $\Delta$ — converges as well,and it does, with some technical
conditions in place[^F11].

[^F11]: While it’s tempting to assume that the limit of a product is simply the
product of the limits, this doesn’t automatically hold here. The long-run
average of presence density, $\Delta$, is defined as a time-based average, while
the average signal mass contribution, $\bar{M}$, is defined over the number of
signals. Since these limits are taken over different denominators, additional
technical conditions are required to ensure that their product equals the limit
of the product.

So, let’s write down precise definitions for the limits of $\iota(t)$ and  
$\bar{m}(t)$ and examine how these limits behave.

#### Convergence of Average Signal Mass Contribution

We will derive the limit for $\bar{m}$. We will denote this by $\bar{M}$.

$$
\bar{M} = \lim_{T \to \infty} \frac{1}{N(0,T)} \sum_{(e,b)} \int_0^T P_{(e,b)}(t) \, dt
$$

This expression means: for each signal $(e,b)$, accumulate its total presence
mass over time, then sum across all signals, and divide by the total number of
signals active during that window. Each integral in the sum is a row sum in the
original presence matrix - the mass contribution of an individual signal over
the interval.

Thus we can also write this as

$$
\bar{M} = \lim_{j \to \infty} \frac{1}{N(1,j)} \sum_{(e,b)} \sum_{k=1}^j P_{(e,b)}(k)
$$

$\bar{M}$ is the limit of average mass contribution per signal over a
sufficiently long observation interval. Here, $P_{(e,b)}(t)$ is the presence
density function for signal $(e,b)$, and $N(0,T)$ is the total number of signals
observed during the interval $[0,T]$.

Let's work this out for our running example and see what it means. We'll
reproduce Figure 9, our starting presence matrix, here for easy reference.

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

The cumulative mass per signal over each interval $[1, j], j \le 10$ is shown
below. Each value in this matrix is the sum of all the values in that row to the
left (inclusive) of the value.

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
      <td>0.3</td><td>2.6</td><td>6.0</td><td>7.1</td><td>10.0</td>
      <td>13.2</td><td>14.3</td><td>14.3</td><td>14.3</td><td>14.3</td>
    </tr>
    <tr>
      <td>e1_b2</td>
      <td>0.3</td><td>2.6</td><td>6.0</td><td>7.1</td><td>7.1</td>
      <td>8.2</td><td>10.4</td><td>12.8</td><td>15.1</td><td>15.9</td>
    </tr>
    <tr>
      <td>e2_b2</td>
      <td>0.0</td><td>0.0</td><td>0.0</td><td>0.0</td><td>0.0</td>
      <td>0.0</td><td>0.9</td><td>2.7</td><td>5.9</td><td>6.8</td>
    </tr>
    <tr>
      <td>e2_b1</td>
      <td>0.8</td><td>2.1</td><td>4.5</td><td>7.3</td><td>10.3</td>
      <td>13.5</td><td>16.9</td><td>19.3</td><td>19.3</td><td>19.3</td>
    </tr>
  </tbody>
</table>
<div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 20: The cumulative mass contribution matrix for the presence matrix.
</div>
</div>

Now lets chart each row of this matrix to see how this cumulative mass grows
over time. Here we are showing each row in the matrix as a line in the chart.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/mass_contribution_per_signal.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 21: Mass contribution per signal
  </div>
</div>

Finally figure 22 shows the cumulative average of the mass contribution. Each
point in this chart represents the cumulative average of the mass contributions
for the window $[1,j]$  which is the sum of the value in column j divided by the
number of non-zero rows in the sub-matrix spanned by the columns in $[1,j]

As we can see, this curve converges to a limit.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/avg_mass_contribution_per_signal.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 22: Average Mass contribution per signal
  </div>
</div>

So lets ask, what would make the average mass contribution _not_ converge to a
finite value?

Figure 21 suggests that the mass contribution of every individual signal is
monotonically non-decreasing and it increases continuously over every non-zero
support interval of the signal and flattens out over every interval where the
underlying signal is zero.

Suppose when measured over a sufficient long interval, each signal remains
bounded, that is every onset is matched with a corresponding reset, then each
individual signal contributes a finite mass to the cumulative average.

Thus, the only way the cumulative average mass can grow without limit is if
_some_ signal grows without limit.

For example, in figure 3 we show some onset-reset patterns for signals and the
last signal in Figure 3, which has an onset but no apparent reset within the
observation window, would grow without limit in Figure 21 if there was no reset.

This gives us the first condition for convergence of $\Delta$ :

<div style="border: 1px solid #ccc; border-radius: 6px; padding: 1em; background-color: #f9f9f9; margin: 2em 0;">
**Boundedness of
Signal Mass**

*In a convergent system of presences, every signal onset is eventually followed
by a corresponding reset, when observed over a sufficiently long time interval.*
</div>

We'll note, once again, that depending upon the semantics of the domain, we may
or may not want to have this condition hold depending upon whether we are
looking to steer the system towards convergence or towards divergence.

For example, if a signal represents a new revenue source, a mass contribution
represents incremental revenues and ideally we want many onsets without matching
resets: every reset corresponds to a lost revenue stream.

If, on the other hand, a signal onset represents a new unfinished task on your
to-do list, then a reset marks its completion — and convergence becomes
desirable, as it indicates tasks are being completed in a timely manner and that
your todo list is not growing without limit.

#### Convergence of Incidence Rate

We now define the long-run incidence rate, denoted $I$, in exact analogy to how
we defined the average mass contribution per signal $\bar{M}$. Recall that
$\iota(t)$ is the incidence rate observed over the interval $[0, t]$, defined as
the number of signals observed in that interval divided by its duration. Then we
define the long-run incidence rate as the following limit:

$$
I = \lim_{T \to \infty} \iota(T) = \lim_{T \to \infty} \frac{N(0, T)}{T}
$$

where $N(0, T)$ is the number of signals observed over the interval $[0, T]$—
that is, the number of distinct element-boundary signals that are active at some
point during the interval. The incidence rate measures how many such signals are
activated, on average, per unit time.

This limit $I$, when it exists, represents the asymptotic rate at which signals
appear in the system. It plays a symmetric role to $\bar{M}$ in the convergence
of the presence density, and its existence is the second key condition we will
examine next.

To better understand the behavior of the incidence rate $\iota(T)$, let’s now
examine the cumulative signal count $N(0,T)$ over the interval $[0,T]$ for
increasing values of $T$. This is directly analogous to how we analyzed the
growth of cumulative mass contributions per signal when analyzing $\bar{M}$.

Recall that for a given observation window $[0,T]$, $N(0,T)$ counts the number
of element-boundary signals that are active at some point within the interval.
We can compute this by scanning across the presence matrix and, for each column
(from $t=1$ to $t=T$), counting how many *new* signals appear—that is, how many
unique element-boundary rows have non-zero values in that column.

The result is a sequence of signal counts, which we can arrange as
a $1 \times T$
row vector:

<div style="text-align: center; margin:2em">
<table>
  <thead>
    <tr>
      <th>Time</th>
      <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th>
      <th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Signal Count</td>
      <td>3</td><td>3</td><td>3</td><td>3</td><td>3</td>
      <td>3</td><td>4</td><td>4</td><td>4</td><td>4</td>
    </tr>
  </tbody>
</table>
<div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 23: Cumulative count of distinct signals observed over the interval $[0, T]$.
</div>
</div>


where $n_j$ is the total number of distinct signals that have appeared at or
before time $j$. Each $n_j$ counts the number of signals with support
intersecting the interval $[0, j]$.

We can chart this row to visualize how the cumulative number of observed signals
grows over time. If $N(0,T)$ grows linearly in $T$, then the incidence rate
$\iota(T) = N(0,T)/T$ should converge to a finite value $I$. On the other hand,
if $N(0,T)$ grows faster than linearly, the incidence rate will diverge—and if
it grows sublinearly, the rate will decay toward zero.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/avg_incidence_rate.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 24: Average signal incidence rate 
  </div>
</div>

Figure 24 shows the incidence rate $\iota(T) = N(0,T)/T$ over time. In this
example, the rate initially decreases and then stabilizes, since the number of
distinct signals $N(0,T)$ stops increasing after a point. In general, the
incidence rate will converge to a finite limit if $N(0,T)$ grows no faster than
linearly with $T$. If $N(0,T)$ grows *faster* than $T$, the ratio $\iota(T)$
will diverge—indicating that signals are being activated at an unbounded rate.
Conversely, if $N(0,T)$ grows *slower* than $T$, the incidence rate will decay
toward zero. Thus, convergence of $\iota(T)$ requires that $N(0,T)$ grows
approximately linearly in $T$.

This kind of divergence typically arises in systems where the *onset rate*— the
rate at which new signals are activated—exceeds the *reset rate*, which closes
those signals. While transient imbalances between onsets and resets are common
during transitions between equilibrium states, divergence only occurs if this
imbalance is sustained indefinitely. In that case, $N(0,T)$ grows without bound
relative to $T$, and the system exhibits an asymptotically increasing incidence
rate. So, divergence of $\iota(T)$ directly reflects a persistent structural
imbalance between signal onsets and resets over time.


<div style="border: 1px solid #ccc; border-radius: 6px; padding: 1em; background-color: #f9f9f9; margin: 2em 0;">
<b>Boundedness of incidence rate</b>

<i>
In a convergent system of presences, the long-run rate of signal onsets does not
exceed the long-run rate of resets, when observed over a sufficiently long time
interval.
</i>
</div>

#### Recap

We began by defining convergence in terms of the existence of a long-run limit
for average presence density.

We then showed how the existence of this global limit depends on the existence
of two other measurable limits: the average incidence rate of signals and their
average mass contribution.

Next, we traced each of these limits back to the local behavior of individual
signals—specifically, the presence or absence of well-behaved signal onsets and
resets.

With this connection in place, we now have a principled way to reason about the
global convergence or divergence of a system by analyzing the patterns of local
signal behavior over time. In the next section, we’ll see how to apply this
principle in practice.

#### Formal Proof of Convergence and Little's Law

In this document, we have presented an accurate—though somewhat simplified—
account of the criteria required to ensure that a system of presences is
convergent. Specifically, based on the definitions above, we assert that for a
given system of presences, if the limits $I$ and $\bar{M}$ exist and are
finite, then the limit $\Delta$ also exists and is finite. Furthermore, we
claim that

$$
\Delta = I \times \bar{M}
$$

Technically, this relationship does not follow automatically from the arguments
we have presented so far. In fact, the statement above is a restatement of a
generalized form of Little’s Law originally proven by Brumelle, and later by
Heyman and Stidham. The full proof—along with the additional technical
conditions required to ensure that the limit of the product equals the product
of the limits—is beyond the scope of this document.

For our purposes, it is safe to state that this relationship, and the
conditions under which it holds, *constitute* the general form of Little’s Law
for a system of presences.

With the exception of certain carefully constructed pathological cases, the
criteria we have outlined—bounded signal mass and balanced onset/reset
rates—will typically suffice to determine whether a system is convergent or
divergent.

#### Convergence, Coherence, and Little's Law

One important point to note is that “Little’s Law” is not a single law, but
rather a family of related laws that apply at different time scales, in
different forms, and with different interpretations. The presence invariant is
the most general version of this law.

In this document, we stated it as a relationship between average presence
density, signal incidence rate, and average mass contribution per signal over
any finite observation window. This relationship holds at all time scales,
_including_ those sufficiently long windows where the limits $\Delta$, $I$, and
$\bar{M}$ exist.

It is natural to ask: what is special, if anything, about those limiting values?

Without going too deeply into technical arguments here, we note that the limits
are indeed special. When a system is observed over a non-convergent interval,
the quantities in the presence invariant are dominated by _partial_ mass
contributions from signals that have not yet completed. Figure 5 shows an
example of this behavior.

The system may _appear_ convergent when the window is long enough for _complete_
signals to dominate the averages. For example, if we extended the window in
Figure 5 to include the full duration of each signal, the
system would appear convergent over that interval.

The important point here is that in such situations, the presence invariant is
not just a relationship about mass _contributions_, but also implicitly a
relationship about the _masses_ of the signals involved. This distinction has
direct operational implications.

For instance, if the signals in Figure 5 represent customer service times, then
over a convergent interval, mass contributions reflect what the customer
actually experiences. But over shorter, non-convergent intervals, those same
contributions primarily reflect what a system operator observes on a day-to-day
basis.

In Figure 5, for example, if we extend the observation window far enough to
include the full duration of all signals shown, the system will appear
convergent over that interval. When we measure presence density, signal masses,
and incidence rates over this longer window, we are implicitly aligning the
customer’s perspective of the system with the operator’s perspective.

In this way, convergence brings these two perspectives—the customer’s and the
operator’s—into alignment. More generally, it aligns time-based averages with
signal-based averages. When these quantities agree, we enter a state of
epistemic coherence: multiple observers, using different vantage points, arrive
at consistent measurements of system behavior.

This alignment occurs only when the system is operating at or near equilibrium.

We will return to this important idea in other posts, particularly in the
context of flow measurement in systems that operate far from equilibrium. But
for now, it is enough to recognize that identifying whether a system is
operating in a convergent or divergent mode is fundamental to making meaningful
decisions when reasoning about a system of presences.

#### A Note on Determinism

A final point we emphasize in this section is that the form of Little’s Law
derived here is entirely deterministic. It does not depend on any probabilistic
or stochastic assumptions about the behavior of the system. In fact, the notion
of a sample path used here originates in a deterministic proof of Little’s Law
by Stidham in 1972. The presence invariant, as we have introduced it, is a
direct analogue of the finite-window constructs used in that proof.

It is important to recognize that Little’s Law is not a statistical artifact. It
is a structural property deeply woven into the behavior of of _any_ system of
presences. Convergence and divergence are deterministic features of how signals
evolve and interact over time—regardless of whether the underlying signals are
random or not.

Even when the signals have randomness, the _observed_ evolution of presence
density is deterministic[^F12] and governed by the law of conservation of
presence mass—that is, the presence invariant. This determinism extends to any
functional quantity that depends on presence density. As we will see, a large
and operationally useful class of system behaviors can be characterized in terms
of the presence density of domain signals. That is why the machinery developed
here is more than just a theoretical curiosity.

[^F12]: It is worth emphasizing the word _observed_ in this statement. Even
though the evolution is deterministic, this does not mean the future behavior of
the system is predictable based on past behavior. That depends entirely on the
nature of the signals involved, which may or may not be predictable. What we can
say is that, given a sufficiently complete history of the system, we can
deterministically reconstruct the current state of presence density from any
starting point. This explanatory power is useful in its own right, as we will
soon see.

This is our main point of departure in the presence calculus: we treat
equilibrium not as a precondition for Little’s Law, but as a special case of a
more general principle. We place the finite version of Little’s Law - in the
general form of the presence invariant at the center of our analysis, because it
continues to hold and yield meaningful insight even when the system is far from
equilibrium—precisely the operating modes traditional queuing theory and other
classical approaches de-emphasize, but where most real-world systems actually
live.

In fact, there is an even more general principle at work. Miyazawa was among the
first to note the existence of a broader class of *rate conservation laws* that
exhibit structural similarities to Little's Law across diverse domains. Sigman
later demonstrated that the generalized form of Little’s Law can be viewed as an
equivalent formulation of such rate conservation principles.

From this perspective, the presence calculus offers constructive tools to
_discover_ and formulate such laws within a domain. The interactions of
element-boundary signals in any system of presences naturally give rise to rate
conservation laws based on the principle of conserved signal mass. Mapping these
laws back to the language of the domain appears to be a fruitful path toward
uncovering the mechanisms by which systems in that domain behave.

## 7. Navigation: defining place and direction

Convergence, as discussed in the last section, is a fundamental concept in the  
presence calculus. We now have the tools to detect convergence or divergence in
the long-run behavior of a system of presences—specifically, the evolution of  
presence density and its underlying drivers: signal mass contributions and  
signal incidence rates.

As noted earlier, _whenever we can model the meaningful behaviors of a system as
interactions between element-boundary signals within a system of presences_,  
this provides a constructive analytical framework for studying system  
dynamics. This framework applies to a wide range of operational problems across
many domains.

We also observed that much of the structure in the presence calculus is  
deterministic. That is, given the observed behavior of a system of presences,  
we can deterministically explain the evolution of presence density in terms of  
its drivers, signal mass and incidence rate—across time and across different
timescales.

In this section, we elaborate on this deterministic structure and introduce  
new tools that help us analyze how local behaviors evolve into global patterns,
and help us understand the dynamics of a system of presence.

First we will develop fundamental tools that help us establish a uniform sense
of place and direction of the system evolution, tha scales from the local to
global timescales. While convergence and divergence establish this for longer
timescales, these concepts are somewhat unwieldy and inapplicable when the
system is operating far from equilibrium, and we need some better tools to
navigate in this complementary region.

We will show how to detect emerging patterns in this evolution that reveal the  
*direction* in which the system is moving—and just as importantly, how to  
detect when that direction is *changing*.

These are essential capabilities for building mechanisms that can steer system
behavior in a desired direction—toward convergence or divergence of presence
density.

### The Presence Accumulation Recurrence

We noted at the end of the last section that the observed evolution of a the
presence density of a system of presences is deterministic. Let's see why this
is the case.

We have reproduced the presence accumulation matrix from Figure 12 below. Recall
from section 5 that given an $MxN$ presence matrix, the accumulation matrix is
an $NxN$ upper triangular matrix where each cell $A[i,j], 1 \le i \lt j \le N$
records the cumulative presence mass in columns $[i,j]$ in the original presence
matrix.

We also noted that the diagonal in the accumulation matrix is a sample path
through the system history and the top row records the cumulative presence mass
over an observation period. It represents the area under the sample path. In
essence, the accumulation matrix is a compact encoding of the evolution of
presence density across timescales.


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

If we look closely at the entries in the matrix though, we will see that there
is much tighter local relationship between the matrix entries. We can, in
general, write the following recurrence describing the entries in the matrix.

We can express this local relationship using the following recurrence:

$$
A[i,j] = A[i,j-1] + A[i+1,j] - A[i+1,j-1]
\quad \text{for } 1 \le i < j \le N
$$

It tells us that the cumulative mass from column $i$ to column $j$ can be  
computed from three nearby entries:

- $A[i,j-1]$: the cumulative mass from $i$ to $j{-}1$
- $A[i+1, j]$: the mass from $i{+}1$ to $j$
- a correction term subtracting the overlap $A[i+1, j-1]$ from $i{+}1$
  to $j{-}1$

This equation reflects the additivity of cumulative presence mass over  
rectangular regions in the presence matrix [^F13].

[^F13]: Recall that we required signals to be measurable. This recurrence  
reflects the finite additivity of measures over overlapping regions. If we  
interpret $A[i,j]$ as the measure of the union of two intervals, then the  
recurrence follows the
identity $$\mu(A \cup B) = \mu(A) + \mu(B) - \mu(A \cap B)$$,  
where $$A = [i, j{-}1] \text{ and } B = [i{+}1, j]$$. The subtraction removes
the overlap $[i{+}1, j{-}1]$, ensuring the correct cumulative mass is assigned
to $[i, j]$.

Thus, the presence accumulation matrix—and by extension, the evolution of  
presence density—is governed by a simple local rule. Given the values on the  
diagonal, the rest of the matrix is fully determined.

The physical interpretation of this is that, given the first $N{-}1$ points  
on the sample path, knowing the $N^{\text{th}}$ point allows us to trace how  
the macro behavior of the system—across every timescale—evolved up to that  
point.

This is the foundation for  
the next tools we will develop: tools for detecting direction and change in  
system behavior based on how these recurrence relationships evolve over time.

### A phase space representation of the presence invariant

So now that we know presence accumulates over timescales according to a  
deterministic rule, let's assemble some machinery that gives us a sense of the  
*direction* in which the system as a whole is moving. For this, it is useful
to  
construct an alternate view of the entries in this matrix using our favorite  
tool: the presence invariant.

We'll start by noting that the presence invariant holds for every entry in the  
accumulation matrix. Therefore, we can write:

$$
\frac{A(i,j)}{T} = \frac{N}{T} \times \frac{A(i,j)}{N} \quad \text{where } T = j - i
$$

Which is just the presence invariant $\delta = \iota \cdot \bar{m}$ written out
for every entry in the matrix A.

Now, let’s revisit the relationship $\delta = \iota \cdot \bar{m}$.  
As noted earlier, this expresses that each entry in the accumulation matrix
can  
be factored into two components: the incidence rate $\iota$ and the average
mass  
$\bar{m}$ per incident signal. There are useful insights to be gained by  
examining this multiplicative structure in log space.

Taking the logarithm of both sides of the presence invariant  
$\delta = \iota \cdot \bar{m}$, we obtain:

$$
\log \delta = \log \iota + \log \bar{m}
$$

This expresses the invariant as an additive relation in log space, which  
provides a natural coordinate system for analyzing system behavior.

Each component now contributes linearly to the overall presence density (in log
space), and changes in incidence rate or average mass can be interpreted as  
vector displacements along orthogonal axes in this space.

This gives us a mapping of the presence invariant in the complex plane.

We now introduce a geometric interpretation of this relation in the complex  
plane. Let’s define a mapping:

$$
z = \log \iota + i \log \bar{m}
$$

Here, the real part of $z$ encodes the logarithm of the incidence rate, and the
imaginary part encodes the logarithm of the average mass.

This mapping allows us to compactly represent the two degrees of freedom in
presence density as a vector in a two-dimensional plane, with the magnitude of
the vector encoding the intensity of the presence: increasing or decreasing, and
the direction of the vector encoding what is driving the increase or decrease:
incidence rate or presence mass.

This vector representation gives us a compact and precise definition of the
magnitude and direction of the _flow_ of presence density in the system at any
point in time. This is what we will use as the  _definition_ of flow in a system
of presences.

Lets formalize these notions.

Following standard techniques in complex analysis, we now introduce two derived
quantities: the norm and the phase angle for the complex number that represents
a presence density of system of presences over a finite interval of time in
log-space.

- The **norm** of $z$ represents the overall intensity of presence
  accumulation  
  in log space:

  $$
  \|z\| = \sqrt{(\log \iota)^2 + (\log \bar{m})^2}
  $$

  This gives a scale-invariant measure of the strength of presence density  
  combining the effects of incidence and mass into a single magnitude.

  - The **phase angle** of $z$ represents the balance between rate and mass  
    contributions:

    $$
    \theta = \arg(z) = \tan^{-1} \left( \frac{\log \bar{m}}{\log \iota} \right)
    $$

    This tells us whether the system’s current trajectory is more rate-dominant
    -ie due to lots of small signals with small mass (small $\theta$) or
    mass-dominant (larger $\theta$) or fewer signals with large mass. $\theta$
    provides a directional sense of what’s driving the observed evolution of
    presence density.

Put together $\|z\|$ and $\theta$ allow us to represent the present density over
any interval in polar co-ordinates in log-space as
$$
z = \|z\| \cdot e^{i.\theta}
$$

Together, $\|z\|$ and $\theta$ allow us to decompose each matrix entry’s
behavior into *how fast* it is growing (norm) and *in what direction* the
contributing factors lie (phase).

Figure 25 shows this mapping of the presence accumulation matrix into polar
co-ordinates in the complex plane.

<div style="text-align: center; margin: 2em">
<table style="border-collapse: collapse; margin: auto; font-family: serif; font-size: 0.95em;">
<thead>
  <tr><th>i\j</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th></tr>
</thead>
<tbody>
    <tr><td><b>1</b></td><td style="background-color: #eef;">1.34 ∠ -0.61</td><td style="background-color: #ddf;">0.98 ∠ 1.14</td><td style="background-color: #eef;">1.70 ∠ 1.57</td><td style="background-color: #ddf;">1.99 ∠ 1.72</td><td style="background-color: #eef;">2.27 ∠ 1.80</td><td style="background-color: #ddf;">2.55 ∠ 1.85</td><td style="background-color: #eef;">2.43 ∠ 1.80</td><td style="background-color: #ddf;">2.60 ∠ 1.84</td><td style="background-color: #eef;">2.74 ∠ 1.87</td><td style="background-color: #ddf;">2.80 ∠ 1.90</td></tr>
<tr><td><b>2</b></td><td></td><td style="background-color: #eef;">1.29 ∠ 0.55</td><td style="background-color: #ddf;">1.67 ∠ 1.32</td><td style="background-color: #eef;">1.90 ∠ 1.57</td><td style="background-color: #ddf;">2.18 ∠ 1.70</td><td style="background-color: #eef;">2.47 ∠ 1.78</td><td style="background-color: #ddf;">2.36 ∠ 1.74</td><td style="background-color: #eef;">2.54 ∠ 1.79</td><td style="background-color: #ddf;">2.68 ∠ 1.83</td><td style="background-color: #eef;">2.74 ∠ 1.87</td></tr>
<tr><td><b>3</b></td><td></td><td></td><td style="background-color: #eef;">1.57 ∠ 0.80</td><td style="background-color: #ddf;">1.61 ∠ 1.32</td><td style="background-color: #eef;">1.90 ∠ 1.57</td><td style="background-color: #ddf;">2.24 ∠ 1.70</td><td style="background-color: #eef;">2.19 ∠ 1.67</td><td style="background-color: #ddf;">2.38 ∠ 1.74</td><td style="background-color: #eef;">2.53 ∠ 1.79</td><td style="background-color: #ddf;">2.60 ∠ 1.84</td></tr>
<tr><td><b>4</b></td><td></td><td></td><td></td><td style="background-color: #eef;">1.21 ∠ 0.44</td><td style="background-color: #ddf;">1.35 ∠ 1.27</td><td style="background-color: #eef;">1.81 ∠ 1.57</td><td style="background-color: #ddf;">1.87 ∠ 1.57</td><td style="background-color: #eef;">2.11 ∠ 1.68</td><td style="background-color: #ddf;">2.29 ∠ 1.75</td><td style="background-color: #eef;">2.36 ∠ 1.81</td></tr>
<tr><td><b>5</b></td><td></td><td></td><td></td><td></td><td style="background-color: #eef;">1.28 ∠ 1.00</td><td style="background-color: #ddf;">1.55 ∠ 1.31</td><td style="background-color: #eef;">1.68 ∠ 1.40</td><td style="background-color: #ddf;">1.93 ∠ 1.57</td><td style="background-color: #eef;">2.12 ∠ 1.68</td><td style="background-color: #ddf;">2.20 ∠ 1.76</td></tr>
<tr><td><b>6</b></td><td></td><td></td><td></td><td></td><td></td><td style="background-color: #eef;">1.43 ∠ 0.70</td><td style="background-color: #ddf;">1.50 ∠ 1.09</td><td style="background-color: #eef;">1.72 ∠ 1.40</td><td style="background-color: #ddf;">1.92 ∠ 1.57</td><td style="background-color: #eef;">1.99 ∠ 1.68</td></tr>
<tr><td><b>7</b></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color: #eef;">1.53 ∠ 0.43</td><td style="background-color: #ddf;">1.44 ∠ 1.07</td><td style="background-color: #eef;">1.62 ∠ 1.39</td><td style="background-color: #ddf;">1.68 ∠ 1.57</td></tr>
<tr><td><b>8</b></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color: #eef;">1.35 ∠ 0.62</td><td style="background-color: #ddf;">1.45 ∠ 1.29</td><td style="background-color: #eef;">1.53 ∠ 1.57</td></tr>
<tr><td><b>9</b></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color: #eef;">1.23 ∠ 0.97</td><td style="background-color: #ddf;">1.28 ∠ 1.57</td></tr>
<tr><td><b>10</b></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="background-color: #eef;">0.71 ∠ -0.23</td></tr>

</tbody>
</table>
<div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 25: Representation of the presence accumulation matrix in polar co-ordinates on the complex plane. 
</div>
</div>

Figure 25 is not particularly insightful, so let's visualize this as a field of
vectors as in Figure 26. We will call this the flow field for the system.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/flow_field.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 26: Figure 25 visualized as a flow field 
  </div>
</div>

Lets dig into how this flow field is constructed and what it means.

Starting with Figure 25, the grid represents rows and columns of the
accumulation matrix.

* Each cell is represented by the log-space vector of the presence density over
  that interval in polar coordinates.
* The length of the vector encodes magnitude $\|z\|$ and the orientation of the
  vector encodes $\theta$ in radians.

Since the matrix in Figure 25 is upper triangular, there is no significant
information encoded in the bottom half of the matrix.

So as a convention, when we visualize it we will drop the bottom half of the
matrix and only show the entries in the upper diagonal.

Now imagine this matrix rotated by 90 degrees so that entries on the diagonal
are on the bottom row, the entries on the next diagonal are laid out above it,
and so on until the we get to the top left entry in the matrix. The result in
the pyramid shape of the flow field diagram in figure 26.

Each vector in the flow field is drawn with a proportional magnitude and theta.

Figure 26 compresses a tremendous amount information about the dynamics of a
system into a very compact representation that is easy to scan and interpret
visually as well as analytically.

In this view, we are not interested in absolute magnitudes or angles for the
most part. Rather we focus on the relative change in magnitude and direction of
these vectors as we sweep left to right in time along a row and from bottom to top in
time scales across the rows. That is, the flow field encodes the _dynamics_ of
the system across time and time scales. 

Lets see how this encoding works. 


<div style="text-align: center; margin:2em">
  <table style="border-collapse: collapse; margin: auto; font-family: sans-serif;">
    <thead>
      <tr>
        <th style="padding: 0.5em 1em;">θ (radians)</th>
        <th style="padding: 0.5em 1em;">Direction</th>
        <th style="padding: 0.5em 1em;">Interpretation</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>π−ϵ</td>
        <td><svg width="24" height="24" viewBox="0 0 24 24" overflow="visible">
          <line x1="20" y1="14" x2="4" y2="10" stroke="black" stroke-width="2"
                marker-end="url(#arrow)"/>
        </svg></td>
        <td>Signal mass dominates completely; incidence rate is negligible</td>
      </tr>
      <tr>
        <td>3π/4</td>
        <td><svg width="24" height="24" viewBox="0 0 24 24" overflow="visible">
          <line x1="20" y1="20" x2="4" y2="4" stroke="black" stroke-width="2"
                marker-end="url(#arrow)"/>
        </svg></td>
        <td>Mass dominates strongly; rate contributes weakly</td>
      </tr>
      <tr>
        <td>π/2</td>
        <td><svg width="24" height="24" viewBox="0 0 24 24" overflow="visible">
          <line x1="12" y1="20" x2="12" y2="4" stroke="black" stroke-width="2"
                marker-end="url(#arrow)"/>
        </svg></td>
        <td>Mass increase only; rate is steady</td>
      </tr>
      <tr>
        <td>π/4</td>
        <td><svg width="24" height="24" viewBox="0 0 24 24" overflow="visible">
          <line x1="4" y1="20" x2="20" y2="4" stroke="black" stroke-width="2"
                marker-end="url(#arrow)"/>
        </svg></td>
        <td>Both mass and rate contribute; mass dominates slightly</td>
      </tr>
      <tr>
        <td>0</td>
        <td><svg width="24" height="24" viewBox="0 0 24 24" overflow="visible">
          <line x1="4" y1="12" x2="20" y2="12" stroke="black" stroke-width="2"
                marker-end="url(#arrow)"/>
        </svg></td>
        <td>Balanced contribution: mass and rate scale proportionally</td>
      </tr>
      <tr>
        <td>−π/4</td>
        <td><svg width="24" height="24" viewBox="0 0 24 24" overflow="visible">
          <line x1="4" y1="4" x2="20" y2="20" stroke="black" stroke-width="2"
                marker-end="url(#arrow)"/>
        </svg></td>
        <td>Both mass and rate contribute; rate dominates slightly</td>
      </tr>
      <tr>
        <td>−π/2</td>
        <td><svg width="24" height="24" viewBox="0 0 24 24" overflow="visible">
          <line x1="12" y1="4" x2="12" y2="20" stroke="black" stroke-width="2"
                marker-end="url(#arrow)"/>
        </svg></td>
        <td>Rate increase only; mass is steady</td>
      </tr>
      <tr>
        <td>−3π/4</td>
        <td><svg width="24" height="24" viewBox="0 0 24 24" overflow="visible">
          <line x1="20" y1="4" x2="4" y2="20" stroke="black" stroke-width="2"
                marker-end="url(#arrow)"/>
        </svg></td>
        <td>Rate dominates strongly; mass contributes weakly or not at all</td>
      </tr>
      <tr>
        <td>−π+ϵ</td>
        <td><svg width="24" height="24" viewBox="0 0 24 24" overflow="visible">
          <line x1="20" y1="10" x2="4" y2="14" stroke="black" stroke-width="2"
                marker-end="url(#arrow)"/>
        </svg></td>
        <td>Incidence rate dominates completely; signal mass is negligible</td>
      </tr>
    </tbody>
  </table>

  <svg height="0" width="0">
    <defs>
      <marker id="arrow" markerWidth="6" markerHeight="6" refX="0" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L6,3 z" fill="#000"/>
      </marker>
    </defs>
  </svg>

  <div style="font-size: 0.9em; color: #555; margin-top: 1em;">
    Table: Interpretation of θ as directional flow in log-space between incidence rate and average mass, with fully rendered vector arrows.
  </div>
</div>






























