# The presence calculus, <br> A Gentle Introduction

**Dr. Krishna Kumar**  
*The Polaris Advisor Program*

## What is The Presence Calculus?

The Presence Calculus is a new approach for reasoning about the relationship  
between things, places, and time — through the lens of measurable  
*presence*.

The primary goal is to support rigorous modeling and principled  
decision-making with data in complex, real-world domains, while ensuring  
that the use of data in such decisions rests on a mathematically  
precise, logically coherent, and epistemically grounded foundation.

The presence calculus emerged from a search for better quantitative tools to  
reason about complex systems in software development, where current  
approaches to measurement are deficient in all of these aspects.

But as you’ll see, these ideas are far more general, with applications well  
beyond software.

<div style="text-align: center; margin:2em">
  <img src="../assets/pcalc/presence_calculus.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 1: Key constructs—presences, element trajectories, presence matrix,  
    and basis topology
  </div>
</div>

Formally, the presence calculus builds on mathematical concepts from measure  
theory, topology, and complex analysis, and connects it to stochastic  
process dynamics, queueing theory, and complex systems science.

The foundational constructs of the calculus allow us to define derived  
notions such as flow, stability, equilibrium, and coherence in complex  
systems precisely, and to relate them to practically useful measures like  
delay, cost, revenue, and user experience.

In this document, we'll motivate our ideas using simplified real-world  
decision problems.

While the calculus was developed with mathematical rigor, an  
equally important goal was not to let mathematics get in the way of  
understanding the rather simple but very powerful and general ideas  
embodied by the calculus.

Our goal is to make this framework accessible enough to build powerful  
applications on top of it — not just for us, but as a new reasoning tool for  
anyone working with complex systems. 

## Learning more about The Presence Calculus

In this document, we'll motivate and introduce the key ideas in the calculus  
informally, with lots of simplified examples to illustrate concepts. It is  
aimed squarely at the non-technical reader. We recommend reading and  
understanding the ideas here before jumping deeper into rest of the  
documentation at this site.

The next level of detail is in The API docs for the [The Presence Calculus  
Toolkit](https://py.pcalc.org). Here we go into the concepts at a level of  
rigor that you'll need to work with the pcalc API and build tools using the  
concepts. Some mathematical background will be useful here if you want to  
work on the core. 

Finally for those who want to see the underlying mathematical underpinnings of  
the calculus, we have the theory track which perhaps goes into more detail  
than most people will likely need to read or understand, but is useful for the  
mathematically trained to connect the ideas in pcalc to its roots in  
mainstream mathematics. 

Lets  jump in... 

## Why Presence? 

Presence is how reality discloses itself to us. We do not perceive the world  
as a collection of disjointed events, but as a continual unfolding—things  
coming into being, enduring for a time, and slipping away.

What we call permanence is just a form of lasting presence, and what we call  
change is the movement of presences in and out of awareness, often set  
against this permanence.

The sense of something being present, or no longer present, is our most  
immediate way of detecting change. This applies to the tangible and the  
ephemeral—either way, we reason about the world around us by reasoning about  
the presences and absences in our environment over time.

The presence calculus begins here. Before we count, measure, compare, or  
optimize, we observe. And what we observe, first and always, is presence.

# An example 

Imagine you see a dollar bill on the sidewalk on your way to get coffee. Later,  
on your way back home, you see it again—still lying in the same spot. It would  
be reasonable for you to assume that the dollar bill was present there the  
whole time.

Of course, that may not be true. Someone might have picked it up in the  
meantime, felt guilty, and quietly returned it. But in the absence of other  
information, your assumption holds: it was there before, and it’s there now,  
so it must have been there in between.

This simple act of inference is something we do all the time. We fill in gaps,  
assume continuity, and reason about what must have been present based on  
partial glimpses of the world.

The presence calculus gives formal shape to this kind of inference—and shows  
how we can build upon it to *reason* about presence and *measure* its  
effects in an environment.
  
# A software example

Since this work grew out of studying common operations management problems in 
the software world, let’s begin with a familiar example: task work in a software team. 
By looking closely at how we reason about tasks, we can see how a subtle shift to a  
presence-centered perspective changes not just what we observe, but what we  
can *reason* about—and what we can measure.

In software workflows, we often reason about work using *events* and  
*snapshots* of the state of a system in time. A task “starts” when it enters  
development, and “finishes” when it’s marked complete. We track "cycle time"  
by measuring the elapsed time between events, "throughput" by counting finish  
events, and "work-in-process" by counting tasks that have started but not yet  
finished.

When we look at a Kanban board, we see a point-in-time snapshot of where tasks  
are at that moment—but not how they got there. When we read a summary report  
of how many tasks were finished and how long they took on average, much of the  
history of the system that produced those outcomes has been lost. That makes  
it hard to reason causally about *why* those measurements are the way they  
are.

And because, in complex knowledge work, each task often has a distinct  
history—different from other co-temporaneous tasks—losing this information  
makes it hard to reason about the system purely from snapshots. We are reduced  
to making inferences about a system shaped by its history, without a way to  
represent or reason about that history.

This is where we begin. While the presence calculus often starts from  
the same snapshots, it focuses on the time *in between*: when the task was  
present, where it was present, for how long, and whether its presence shifted  
across people, tools, or systems.

The connective tissue is no longer the task itself, or the steps it followed,  
or who was working on it, but a continuous, observable *thread of presence*—  
moving through time, crossing boundaries.

With the presence calculus, these threads and their interactions across time  
and space can now be measured, dissected, and analyzed as first-class  
mathematical constructs—built on a remarkably simple primitive - the presence.

The presence calculus, at its core, comes down to the difference between the  
two independent statements—“The task started development on Monday” and “The  
task completed development on Friday”—and a single, unified assertion: “The  
task was present in development from Monday through Friday.” 

The latter is the *presence*, and it is the foundational building block  
of the calculus.

At first glance, this might not seem like a meaningful difference.

But treating the presence as the primary object of reasoning—as a *first-class*  
construct—opens up an entirely new space of possibilities, because it allows  
us to apply powerful mathematical tools that exploit the continuity in time  
and the algebra of time intervals to reason about *sets* of presences in a  
rigorous and structured, and more importantly, computable way.
