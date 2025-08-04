### The Physics of Flow in Software Development
What you measure, and how you measure it, matter.

In our last post, *The Many Faces of Little's Law*, we revisited the mathematics
behind Little's Law. We showed that—contrary to popular belief—it’s not a
manufacturing artifact, but a multi-faceted mathematical result that is foundational for 
measuring the flow of work and economic value in software development and
engineering.

This post looks at one such application: defining "flow metrics" for software
development work.

The industry-standard definition of flow metrics—Throughput, WIP, Cycle Time, and Work Item 
Age—originated as offshoots of the Lean Software development movement. Originally these metrics
were used by Agile teams adopting the Kanban method. In recent years they have been adopted 
at the Enterprise level in the Flow Framework and SAFe with slightly different terminology. These are the basis for most 
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

## A Brief History of Flow Metrics in Software Development

The discussion of flow metrics in software traces back to **Mary and Tom
Poppendieck**, who translated *Lean manufacturing principles* into the software
domain.

They mapped the seven Lean principles — eliminate waste, amplify learning,
decide as late as possible, deliver as fast as possible, empower the team, build
integrity in, optimize the whole — to software, creating a bridge between
manufacturing’s operational discipline and software’s dynamic nature. They also
showed how queueing theory could optimize flow of work, with metrics like Lead
Time, Cycle Time, Throughput, and WIP as measures of delivery. Little’s Law was
cited as the theoretical basis, with the caveat that it assumes stable systems —
which they noted is rarely true in software delivery.

Their work remains the foundation for much of Lean software development. These
principles are still powerful guides for building efficient and effective
delivery systems.

**David J. Anderson** built on this foundation, combining Lean thinking and
service delivery ideas into the **Kanban Method** (2007). His contribution was
practical: a lightweight, evolutionary change method for managing knowledge
work. Kanban operationalized Lean for software through visualizing work,
limiting WIP, managing flow, making policies explicit, and improving
collaboratively. Alongside these practices came a core set of *service delivery
metrics*: **Lead Time, Cycle Time, Throughput, WIP, and Aging WIP** — with more
precise operational definitions.

**Dan Vacanti** refined the measurement side, emphasizing lightweight
instrumentation and operational tooling grounded in flow principles and Little’s
Law. He popularized cycle time scatterplots, cumulative flow diagrams, and aging
WIP charts to help teams reason about risk, forecast more realistically, and
improve predictability. These ideas have been expanded through the **Pro Kanban
** community and widely adopted via the Actionable Agile family of tools.

**DORA (DevOps Research and Assessment)**, emerging around the same time,
developed DevOps practices rooted in **Lean principles** — small batch sizes,
rapid feedback, and continuous delivery. However, while the *practices* were
Lean‑inspired, DORA’s four key metrics — Deployment Frequency, Lead Time for
Changes, Change Failure Rate, and Mean Time to Restore — were designed as
*outcome indicators for DevOps capabilities*. DORA metrics benchmark *
*capability maturity** across organizations, but they are not operational flow
metrics like Kanban’s service delivery measures.

**Mik Kersten** added to the conversation in 2019 with the **Flow Framework**,
focusing on aligning software delivery with *business value* at scale. His
framework introduced **Flow Velocity, Flow Time, Flow Load, and Flow Efficiency
**. The first three map roughly to Throughput, Cycle Time, and WIP; the last is
similar to a queueing efficiency metric at the portfolio level. These metrics
are aimed at exposing flow principles to C‑suite decision‑makers and connecting
portfolio‑level delivery metrics to value outcomes. While inspired by Lean,
these metrics target portfolio‑level reporting rather than team‑level delivery
management, and have become popular in the **Value Stream Management**
community.

Despite their shared Lean heritage, these approaches operate in **siloed
communities** — Kanban, Pro Kanban, DORA, and Value Stream Management each have
distinct philosophies on metrics, which on the surface appear quite different.

The unifying thread is **Little’s Law**, which underlies all of them (yes, even
DORA). Every one of these problem domains can be modeled as an input‑output
system where Little's Law applies. Ironically, most of these metric systems
don’t satisfy the law in practice, due to both what they measure and how the
measurements are taken.

But Little’s Law governs the dynamics of all these processes regardless.
Understanding why — and where gaps arise when applying it to software delivery —
opens new insights and capabilities. These measurement systems are pragmatic
adaptations of Lean ideas, and many concepts map to software “close enough” to
be useful for situational awareness and as loose guides for decision making.

Thus, as we’ve noted before, current flow metrics in software are more like
*weather reports* than *weather models*. Connecting them explicitly to the
underlying physics of flow reveals the real gaps — and how to close them. This
enables us to build modeling and measurement systems with provable guarantees
that support higher‑quality operational decision making.

That is our primary goal.















