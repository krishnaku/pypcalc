### Flow Models and Flow Dashboards

What you measure, and how you measure it, matter.

In our last post, *The Many Faces of Little's Law*, we revisited the mathematics
behind Little's Law. We showed that—contrary to popular belief—it’s not a
manufacturing artifact, but a multi-faceted mathematical result that is foundational for 
measuring the flow of work and economic value in software development and
engineering.

This post looks at one such application: defining "flow metrics" for software
development work.

The industry-standard definition of flow metrics—Throughput, WIP, Cycle Time, and Work Item 
Age—originated in the Kanban community, later adapted into the Flow Framework 
and SAFe with slightly different terminology. These are the basis for most 
commercial flow dashboards used in product and engineering operations today. 
Their theoretical lineage traces back to the throughput formula from 
manufacturing.

As we showed in our previous post, this formula applies cleanly only under 
strong assumptions that hold in repetitive manufacturing by default—but not in 
software. And it breaks down in software not because of the nature of software, 
but because of *what* is measured and *how* the measurements are taken.

In this post, we look at what we should be measuring instead, how to measure it 
correctly, and why it matters. But first, let’s see why a different approach is 
necessary and what benefits it brings.

We'll start with an analogy

## Weather Models and Weather Reports

Consider the relationship between a weather report and a weather model. A 
weather report summarizes observed conditions—temperature, precipitation, 
wind—at specific points in place and time. But it’s anchored in measurements 
shaped by physical laws: pressure, humidity, and motion all tie back to 
Newton’s laws and thermodynamics.

A weather model embeds these same laws directly, simulating the dynamics of the 
atmosphere. This physics-based foundation not only governs how we interpret 
point measurements, it allows reasoning about higher-level constructs like cold 
fronts, pressure ridges, and storm systems. Weather reports tell us *what* is 
happening now; weather models reveal *why* it is happening and how it may 
evolve. Even forecasts in a weather report are grounded in the model.

Current flow dashboards are closer to weather reports without weather models.
And they have a critical weakness: the quantities being measured are largely
unmoored from the underlying physics of flow in the domain. The popular
frameworks derive metrics from the throughput formula, gesturing vaguely toward
Little’s Law as justification for why *these* metrics matter.

But the measurements themselves are disconnected from the conservation 
relationships we presented in our last post, which govern how the law actually 
works. Without that grounding, flow metrics are just point-in-time statistics. 
They describe recent activity but don’t reliably explain why changes occur, 
constrain how the system will respond, or simulate how it might evolve. Most 
commercial dashboards simply report these as independent statistics over 
point-in-time data samples.

Just as weather reports without a model can’t track fronts or anticipate 
storms, flow dashboards without a model can’t reason about capacity 
constraints, demand surges, seasonal patterns, or regime shifts.

Yes, many dashboards now include “forecasts,” but without a model these are not 
forecasts in the rigorous sense. We’ll need more foundations in place to 
explain why.


## The Proposal

Since Little’s Law in its various forms is a more general model for the physics 
of flow, we propose defining and measuring flow metrics using the parameters of 
the law rather than the throughput formula. The throughput formula represents 
the physics of flow only in certain special cases—it’s not fit for purpose 
beyond them.

This path gives us the tools to build physics-based models for the flow of work 
and model its economic impacts using a common set of principles. 

Doing this correctly means going deeper into the foundations of Little’s Law 
and deriving what we measure from first principles for the software domain—rather than 
lifting quantities from the throughput formula and reporting them as flow 
metrics.

We outlined the high-level theory in our earlier post. Now we’ll dig into the 
details of how to measure and report physics-based flow metrics correctly for 
software.

These details may seem technical, but they matter—if we want flow metrics that 
reflect the physics of work and support rigorous reasoning about economic value 
in software development.




