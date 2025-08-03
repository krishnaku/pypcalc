### Flow Models and Flow Dashboards

What you measure, and how you measure it, matter.

In our last post, *The Many Faces of Little's Law*, we revisited the mathematics
behind Little's Law. We showed that—contrary to popular belief—it’s not a
manufacturing artifact, but a foundational law that applies directly to
measuring the flow of work and economic value in software development and
engineering.

This post looks at one such application: defining "flow metrics" for software
development work.

The familiar set of flow metrics—Throughput, WIP, Cycle Time, and Work Item
Age—originated in the Kanban community, later adapted into the Flow Framework
and SAFe with slightly different terminology and definitions. These are the
basis for all the commercial flow metrics dashboards in use in product and
engineering operations today. Their theoretical lineage traces back to the
throughput formula from manufacturing.

As we showed in our previous post, this formula applies cleanly only under
strong assumptions that hold in repetitive manufacturing by default—but not in
software. We also explained *why* it breaks down in software: not because of the
nature of software itself, but because of how the measurements are taken.

In this post, we go deeper into what we should be measuring instead, how to make
those measurements correctly, and why it matters. But first, lets see why a
different approach is necessary and what benefits it brings relative to the
status quo.

We'll start with an analogy

## Weather Models and Weather Reports

Consider the relationship between a weather report and a weather model. A
weather report summarizes observed conditions — temperature, precipitation,
wind — at specific points in place and time, but it’s anchored in measurements
shaped by physical laws. What gets measured, and how, comes from the physics:
pressure, humidity, and motion all tie back to Newton’s laws and thermodynamics.

A weather model embeds these same laws directly, simulating the dynamics of the
atmosphere. This physics-based foundation not only governs how we interpret
point measurements, it allows reasoning about higher-level constructs like cold
fronts, pressure ridges, and storm systems. Weather reports tell us what is
happening now; weather models, grounded in the physics, reveal why it is
happening and how it may evolve. A weather report may also include a forecast,
but that forecast is also grounded in the weather model.

Current flow metrics dashboards are closer to weather reports without underlying
weather models. And they have an important weakness: the quantities being
measured are largely unmoored from the underlying physics of flow. Most popular
frameworks derive metrics from the throughput formula, hand-waving vaguely
toward Little’s Law as the justification for why
*these* particular metrics are important to measure.

But the measurements themselves are disconnected from the conservation
relationships we presented in our last post, and that govern how the law
actually works. Without that grounding, flow metrics are just point-in-time
statistics. They describe metrics of recent activity, but don’t reliably explain
why changes occur, constrain how the system will respond, or help simulate how
they might evolve. Indeed most commercial flow metrics tools simply report these
metrics as independent statistical measures over point in time samples of data.

Just as weather reports without a model can’t meaningfully track fronts or
anticipate storms, flow metrics without a model can’t reason about higher-level
constructs like capacity constraints, demand surges, seasonal patterns or
regime-shifts.

Yes, flow metrics dashboards often come with “forecasts” these days, but without
a model, they are not reliable forecasts in a rigorous sense. We’ll need more
foundations in place to explain why this is the case.


## The Proposal 

Since we know that Little's Law in its various forms is a more general model for
the physics of flow, we propose that flow metrics should be defined and measured using the parameters
of law in its various forms rather than the throughput formula. The latter represents the physics
of flow in certain special cases and is not fit for purpose  beyond those special cases. 
Taking this path gives us the tools to build physics based models for the flow of work and also model its
economic impacts under a common measurement system. 

Implementing this correctly requires going deeper into the foundations of Little’s Law
and deriving the things we want to measure from first principles for software
rather than simply measuring quantities in the throughput formula and reporting
them as flow metrics.

We outlined the high-level theory for doing this in our earlier post. Now we’ll
dig into the details and see how to apply it to measuring and reporting physics
based flow metrics correctly in software.

These details may seem highly technical, but they matter if we want flow metrics
that truly reflect the physics of work and help us reason rigorously about economic value
in software development.




