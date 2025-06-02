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
so we invite anyone interested in pressure testing the ideas here
further to collaborate on this as an open source project.

While the calculus was developed with mathematical rigor, an equally important  
goal was not to let mathematics get in the way of understanding the simple but
very powerful and general ideas the calculus embodies.

This document is the first step in that direction. We welcome feedback on how it
can be improved,and the concepts clarified. Please feel free to open a pull
request with thoughts, suggestions or feedback.

Dr. Krishna Kumar, The Polaris Advisor Program.

## Learning more about The Presence Calculus

In this document, we'll motivate and introduce the key ideas in the calculus  
informally, with lots of highly simplified examples and allusions to  
illustrate concepts. It is aimed squarely at the non-technical reader.

We recommend reading and understanding the ideas here before jumping deeper  
into the rest of the documentation at this site, which does get a fair bit  
more dense. We'll also continue with ongoing informal exposition on our blog  
[The Polaris Flow Dispatch](https://www.polaris-flow-dispatch.com).

The next level of detail is in the API docs for the [The Presence Calculus  
Toolkit](https://py.pcalc.org). Here we go into the concepts at a level of  
rigor that you'll need to work with the pcalc API and build tools using the  
concepts. Some mathematical background will be useful here if you want to  
work on the core.

Finally, for those who want to dive deeper into the formal mathematical  
underpinnings of the calculus, we have the theory track, which perhaps goes  
into more detail than most people will need to read or understand, but is  
useful for the mathematically trained to connect the ideas to their roots in  
mainstream mathematics.

Let's jump in...

## Why Presence?

Presence is how reality reveals itself. We do not perceive the world  
as disjointed events in time, but rather, as an unfolding—things  
come into being, endure for a time, and slip away.

Permanence is just a form of lasting presence, and what we call  
change is the movement of presences in and out of our awareness, often set  
against this permanence.

The sense of something being present, or no longer present, is our most  
immediate way of detecting change. This applies to both the tangible and the  
intangible.

Either way, we reason about the world around us by reasoning about  
the presences and absences in our environment over time.

The presence calculus begins here. Before counting, measuring, comparing, or  
optimizing, we observe what *is*.

And what we model is presence.

# An example

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

# A software example

Since the ideas here emerged from the  
software world, let’s begin with a familiar example: task work in a software  
team.

By looking closely at how we reason about tasks, we can see how a subtle shift  
to a presence-centered perspective changes not just what we observe, but what  
we measure, and thus can reason about.

We usually reason about task work using *events* and *snapshots* of the state  
of a workflow in time. A task “starts” when it enters development, and  
“finishes” when it’s marked complete. We track "cycle time" by measuring the  
elapsed time between events, "throughput" by counting finish events, and  
"work-in-process" by counting tasks that have started but not yet finished.

When we look at a Kanban board, we see a point-in-time snapshot of where tasks  
are at that moment—but not how they got there. And by the time we read a  
summary report of how many tasks were finished and how long they took on  
average, much of the history of the system that produced those outcomes has  
been lost. That makes it hard to reason about *why* those measurements are the  
way they are.

In complex knowledge work, each task often has a distinct history—different  
from other co-temporaneous tasks. Losing history makes it hard to  
reason about the global behavior of the process.

We are reduced to trying to make inferences from local descriptive statistics of
a rapidly changing system. We try to reason about this system, which is shaped
by its history, without a way to represent or reason about that history. This is
difficult to do, and we have no tools that are fit for this purpose.

This is where the presence calculus begins. While it often starts from the  
same snapshots, the calculus focuses on the time *in between*: when the task  
was present, where it was present, for how long, and whether its presence  
shifted across people, tools, or systems.

The connective tissue is no longer the task itself, or the steps it followed,  
or who was working on it, but a continuous, observable *thread of presence*—  
through all of them, moving through time, crossing boundaries—a mathematical  
representation of history.

With the presence calculus, these threads and their interactions across time  
and space can now be measured, dissected, and analyzed as first-class  
constructs—built on a remarkably simple primitive—the presence.

# The heart of the matter

The calculus, at its core, comes down to the difference between the two  
independent statements—“The task started development on Monday” and “The task  
completed development on Friday”—and a single, unified assertion: “The task  
was present in development from Monday through Friday.”

The latter is called a *presence*, and it is the foundational building block of
the  
calculus.

At first glance, this might not seem like a meaningful difference.

But treating the presence as the primary object of reasoning—as a
*first-class*  
construct—opens up an entirely new space of possibilities, because it allows  
us to apply powerful mathematical tools that exploit the continuity in time  
and the algebra of time intervals to reason about complex assemblages of
presences in a rigorous and structured, and more importantly, computable way.

Let's see how.


