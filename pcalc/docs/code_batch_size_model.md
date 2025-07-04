% Modeling and Measuring Software Delivery Using Presence Calculus 
%  — Technical Note % July 2025

# Introduction

Modern software engineering practices favor frequent, small-batch delivery over
infrequent, large releases. The extensive empirical research done by the DevOps
Research Association (DORA)
has documented the importance of developing capabilities like trunk based
development, adopting work in process limits, working in small batches,
continuous integration, deployment automation, getting fast technical and
business feedback among many others.

However, while the capabilities and practices that drive software delivery
performance are much more broadly recognized due to this research there are
still significant challenges in implementing these practices. As of the 2024
State of DevOps report, 60% of the organizations surveyed fall in the Medium and
Low Performer categories. reporting that that they deploy code to production
less frequently than weekly, and it takes weeks or months for changes in
development to reach production. This 60% of organizations that _responded_ to
the survey! Given the number of large stable businesses running legacy
applications in the industry at large, it is reasonable to surmise this there
are many more older companies that live on the low and medium performer bucket
and many more shorter lived startups and newer companies that live in the high
and elite tiers than the survey indicates.

In any case, it points to the huge opportunities for improvement that still
remain in the industry at large, especially in the economically valuable sectors
that still have not managed to make this shift even after a decade of data
showing what actually works for high performance software delivery.

AI is only going to make this divide even starker. Even though we are still in
the very early stages of AI=Augmented coding, there is some evidence that the
principles of software delivery as identified by the DORA organization have not
changed - whether it is humans writing the code or it is software agents. In
other words, it is only _more_ important to have the key capabilities identified
by the DORA research as core capabilities of software teams - AI augmented or
not. O

ur thesis is that AI on its own is not going to let the 60+ or more of companies
that struggled to adopt modern software engineering practices, are not going to
be able to leap-frog the need to have have the core engineering capabilities of
a modern software delivery organization. This work still needs to be doneby the
humans in the loop - developers, managers, leaders etc. who are thoughtfully
integrating these new technologies into the same mature organizations that were
able to successfully fight off previous infections. The path to successful AI
adoption in such companies still runs through developing the the same
capabilities identified by DORA, but perhaps now extends to complex
human/machine systems building software.

So what does this have to do with The Presence Calculus?

Our thesis is that while the research on the capabilities needed to create high
performing software teams has matured quite a bit over the last ten years, our
techniques for measurement of these practices has not evolved since the very
first DORA report was released.

The DORA Four Keys - Deployment Frequency, Lead Time for Changes, Change Failure
Rate and Failed Deployment Recovery Time are cited as the gold standard metrics
for measuring software delivery performance, and even the very definition of
software delivery performance is based on these metrics. But the measurement
techniques involved, surveys, while well suited for gathering broad population
level statistics to correlate performance to other organizationa factors, that
drive business performance, is highly inadequate when it comes to
operationilzing these capabities in a continuous improvement process on the
ground in any given organization.

Having built tooling to collect, and then collected and used these metrics in
improvement programs over the last six years I noticed several recurring
patterns.

- Inordinate amount of confusion arising from the lack of an unambiguous
  operational definition of the metrics.
- The DORA metrics reported in the state of DevOps survey represent point in
  time subjective assessments of the state of an organization for these metrics.
  Using them as actual metrics guide operational changes is completely different
  kettle of fish.
- You can report DORA metrics on a dashboard, but they dont tell you what to do.
- Naive implementation of DORA metrics (which is nearly all of them) seem to follow this pattern
  - Pick a definition provided by a metrics vendor and/or make up a definition that seems intuitively correct.
  - Hook up instrumentation to version control and CI/CD systems (provided they
    exist) and build dashboards to report DORA metrics that tell you whether
    your organization is a Elite, High, Medium or Low performer. 
  - Review descriptive statistics and trends like averages and percentiles of the metrics. 
  - Try to move these metrics.
  - Realize that they dont give you much guidance on how to do that. 
  - Eventually stop looking at the dashboards because they dont seem to matter. 
  - Give up. 

In the meanwhile, if the real work of improving capabilities that drive these metrics - say for example 
reducing batch sizes, or adopting continuous integration - has survived the metrics exercise, it continues
on without the benefit of useful metrics to guide how to improve, or does so in an ad hoc manner. 
True data driven system-wide adoption of the DORA _practices_ still remains a pipe-dream in 
spite of the extensive empirical research and data that has available on the efficacy of these methods.

The Presence Calculus claims that it fundamentally rethinks how we model and measure system behavior in
real-world software environments with all it's messiness. So it seems fitting that seeing what DORA metrics 
look like in the language of the presence calculus, and seeing how the machinery we have developed can be 
applied to at least incrementally improve the status quo here is a good use case. As we will see, this is a relatively simple 
use case of the machinery of the calculus, but it does provide several solutions to actual problems
people face on the ground while trying to improve software delivery capabilities. 





Much of the empirical research backing this work is based on organizational
surveys.

In this note, we show how the Presence Calculus can be used to give a precise
definition of delivery batch size using a formal system of presence density
functions.

This model yields a mathematically precise, real-time observable measure that
corresponds exactly to the “volume of un-deployed code in the codebase” and
allows us to analyze its signal dynamics for any given delivery pipeline.

We'll use a simplified example of a delivery pipeline to illustrate the idea,
but it is not simplistic. It captures most of the nuances in real-world software
delivery, with the exception of complex branching paths.

We'll leave it as an exercise to the reader to extend this example to a more
complex scenario — for example, GitFlow.

# The System

We model a simplified software delivery system with the following
characteristics:

- A *main branch* acts as the trunk to which all feature branches are merged.
- *Feature branches* contain work-in-progress changes not yet merged.
- The CI/CD pipeline deploys the main branch. When a deployment occurs, a tag is
  applied to the latest commit.
- A change is:
    - *unmerged* if it is not on the main branch,
    - *un-deployed* if it is on the main branch but not yet included in a tagged
      commit.

We define the following:

- *System boundary*: The union of the feature branches and main branch. This
  defines the observation boundary of the system.
- *Presence*: The existence of an unmerged or un-deployed line of code within
  the system boundary.
- *Batch size*: The total number of *non-blank, unmerged or un-deployed lines of
  code* present in the system boundary at a given moment (see implementation
  notes).

# Mapping to Presence Calculus

We now describe this system formally using the constructs of the Presence
Calculus.

## Elements

Let each element $e \in E$ be a branch in some repository:

- $E = \{ b_f^1, b_f^2, \dots, b_f^n, b_m \}$
    - where each $b_f^i$ is a feature branch,
    - and $b_m$ is the main branch.

> This set $E$ defines the *signal domain* for our system.

## Boundaries

Let:

- $B_f$ = boundary over all feature branches (unmerged code),
- $B_m$ = boundary over the main branch (un-deployed code),
- $B = B_f \cup B_m$ = system boundary.

> Presence is defined with respect to this composite boundary $B$.

## Presence Density Function

For each element $e \in E$, define the presence density function:

$$
P_e(t) = \text{number of non-blank, unmerged or un-deployed lines of code on branch } e \text{ at time } t
$$

Specifically:

- For $e = b_f^i$, $P_{b_f^i}(t)$ is the number of non-blank diff lines in
  commits not yet merged to main.
- For $e = b_m$, $P_{b_m}(t)$ is the number of non-blank diff lines in commits
  not yet included in a tagged deployment.

These functions are piecewise constant and change discontinuously at discrete
times induced by commits, merges, deployments, etc., in the delivery pipeline.

> These are the *signals* in our system.

## Presence Mass

Presence mass is measured in *line-time units* (e.g., line-minutes, line-hours).

> Intuitively, presence mass in this system represents a combination of how many
> un-deployed lines of code exist,
> and how long they remain in that state. It corresponds to the area under a
> presence density function
> over a given time interval.

For any branch $e$, the mass over an interval $[t_0, t_1)$ is:

$$
m_e = \int_{t_0}^{t_1} P_e(t) \, dt
$$

### System Mass Accumulation

Let $P_B(t)$ denote the *total system presence density*:

$$
P_B(t) = \sum_{e \in E} P_e(t)
$$

Then the *total system presence mass* over an interval $[t_0, t_1)$ is:

$$
m_B = \int_{t_0}^{t_1} P_B(t) \, dt
$$

This is equivalent to summing the individual presence masses of each element:

$$
m_B = \sum_{e \in E} \int_{t_0}^{t_1} P_e(t) \, dt
$$

> The total presence mass reflects the accumulated line-time volume of all
> un-deployed code in the system.
> It grows as new lines enter the system and shrinks when they are merged or
> deployed.

## Onset and Reset Semantics

Let $P_e(t)$ be the presence density function for branch $e$.

- *Onset*: occurs at the left boundary $t_o$ of any maximal open
  interval $[t_o, t_r)$ over which $P_e(t) > 0$.
- *Reset*: occurs at the right boundary $t_r$ of that same interval,
  where $P_e(t)$ drops to zero.

Presence density functions are defined purely in terms of the number of unmerged
or un-deployed lines of code. Commits, merges, squashes, rebases, and other
operations **induce changes** in $P_e(t)$ but are not explicitly modeled as part
of the function.

This means that squashed or rebased lines simply appear and disappear from
branches as presence changes; the underlying mechanics of how that happens are
irrelevant to the calculus.

## Conservation of Mass

Presence mass is *conserved* under merges:

- When unmerged lines disappear from a feature branch and reappear on the main
  branch, presence mass is *transferred* from $P_{b_f^i}(t)$ to $P_{b_m}(t)$.
- If presence mass disappears from all branches, via destructive operations —
  deletes, squashes, rebases, etc. — it is treated as having *exited the
  system*.

This means that:

$$
m_B(t) = \sum_{e \in E} \int_{0}^{t} P_e(\tau) \, d\tau
$$

remains invariant over time — that is, the total amount of *un-deployed* code in
the system is conserved across time and across branches.

### Presence Invariant

Now let’s look at this system over a *finite* observation window and interpret
what the presence invariant tells us.

Let $[t_0, t_1)$ be a finite observation interval of length $T = t_1 - t_0$.

The parameters of the presence invariant are:

- $A$ is the *total presence mass* contributed by all branches with non-zero
  presence  
  (i.e., lines of code from branches that had unmerged or un-deployed code at
  some point during $[t_0, t_1)$),
- $N$ is the number of such *active branches* — the ones whose presence density
  function $P_e(t)$ is nonzero on a subinterval of $[t_0, t_1)$,
- $\bar{m} = \frac{A}{N}$ is the *mass contribution per signal* — the number of
  line-time units contributed per branch,
- $\iota = \frac{N}{T}$ is the *branch incidence rate* — how many branches
  contributed presence per unit time,
- $\delta = \frac{A}{T}$ is the *presence density* for the system — the number
  of un-deployed lines of code present in the system per unit time.

Thus, $\delta$ is an accurate measure of *batch size* in the system.

> In other words, in this system, presence density *is* batch size. It is
> observer-relative, time-varying, and valid over any finite observation
> interval.

Now, the *presence invariant*:

$$
\delta = \iota \cdot \bar{m}
$$

This expresses that batch size over any finite interval is decomposable into:  
(1) how many lines are contributed by a branch on average, and  
(2) how many such branches are contributing to batch size over time.

> This is Little’s Law for code delivery pipelines! It holds unconditionally for
> any finite observation window.

When batch size changes, it may be due to either of these factors. In general,
modern software engineering practices promote a shift from *mass-dominated* to
*incidence-dominated* presence density — that is, we prefer many small
contributions to production rather than fewer massive ones. This reduces
deployment risk, merge complexity, and improves the ability to roll back changes
incrementally.

The presence invariant captures the drivers of this behavior, and monitoring the
signal dynamics of the system gives us fine-grained tools to measure and steer
the system toward a desired state through real-time adjustments.

This interpretation makes the invariant operational based on a single finite
observation window:

> If batch size is increasing, is it because more branches are carrying
> mass ($\iota$), or because each branch is holding more mass ($\bar{m}$)?

Note also that we will have fairly fine grained data on where we need to
intervene at the branch level to move the system in a desired direction.

Now we can start bootstrapping the rest of the presence calculus machinery:
presence matrices, accumulation matrices, flow fields, attractors etc to use
these primitives to figure out if, where and how we need to intervene to move
the system incrementally from a mass-dominant presence density to an incidence
dominant one, based on feedback from these tools.

This is the "presence calculus way of DevOps."

We'll continue this discussion in a follow-up post, but first lets pause and
compare what we have up to this point with a more conventional approach to this
problem using DORA metrics. For this we need to figure out what the relationship
between the common DORA metrics and the parameters of the system of presence
are.

### DORA Metrics and Their Relationship to Presence Parameters

To compare the presence calculus way to current industry practice, let’s turn to
the DORA metrics — specifically *Deployment Frequency* and *Lead Time for
Changes* — which are widely used as proxies for batch size and delivery
performance.

First, a critical observation: DORA metrics on their own don’t tell you how to
act. Knowing the current deployment frequency or lead time for changes gives you
two descriptive statistics about the system - and that's all they give you. You
can track trends, chart them side by side, and hope correlations emerge. You can
compare them to industry benchmarks and label your organization as “Elite” or
“Low” performing based on where it ranks.

But none of that tells you what to *do* with the system you are measuring after
measuring these metrics [^F-proxy-metrics].

[^F-proxy-metrics]: These metrics are proxies for some other desirable system
property — and smaller batch size is a plausible candidate — but the connection
is indirect even here. Which makes claims that they influence or improve "
business performance," etc., rather fantastical.

There’s a common intuition that if you increase deployment frequency, batch
sizes must shrink. But we know from experience that this isn’t necessarily true.
You can deploy small things often while still releasing one massive batch at the
end of every week - deploying frequently does not control batch size.

One might think *lead time for changes* compensates for this — but again, a
large batch can contain many commits with short lead times and still show a low
average lead time for changes.

Neither metric, alone or in combination, *causes*
batches to be small. There is no general causal link between these metrics and
batch size.

The only reliable way to know you're working in small batches is to *measure
batch size*. The presence density function we’ve defined gives us exactly that —
a precise, time-dependent, and nuanced measure of batch size for code in a
delivery pipeline.

And we already know from the presence invariant that changes in presence
density $\delta$ are driven by exactly two parameters:

- $\bar{m}$: the mass contribution per signal, and
- $\iota$: the incidence rate of signals over time.

These are the only two parameters that directly *cause* batch size to change at
any point in time. For any other metric — including the DORA metrics — to be
relevant to the management of batch size, we need to understand how it
*influences*
either $\bar{m}$ or $\iota$.

> This gives us a clear test:  
> If a metric like deployment frequency or lead time for changes does not
> directly or indirectly  
> cause a change in either of the two core drivers of batch size, then it cannot
> serve  
> as a reliable lever for managing batch size.

So our task is to analyze how the two DORA metrics relate to the
parameters $\iota$ and $\bar{m}$.

If fact, the system of presences we’ve defined *does* allow us to read off both
deployment frequency and lead time for changes in terms of the measurement model
above. Let's see how.

Lets start with deployment frequency. A deployment causes presence mass on the
production branch to go from non-zero to zero, so they correspond exactly to
signal resets on the production branch. Further, a deployment removes presence
mass from the system but it does not contribute mass, so we should expect its
influence on presence density to be felt via the incidence rate and not the
signal mass contribution.

We can see this is true:

In other words, if you still want to track DORA metrics for reporting or
benchmarking purposes, you can do so as a *side effect* of measuring batch size.
Better yet, you can test their actual relationship to batch size in real time —
and use them, when appropriate, as levers to nudge the system in a desired
direction.

This underscores the core difference between the presence calculus approach and
the prevailing theory of metrics use in software.

Mainstream approaches pick proxy metrics first, then try to reason backward from
observation to action. No surprise, then, that most conventional software
metrics — and the dashboards built around them — turn out to be useless for
actually changing systems.

By contrast, the presence calculus starts by modeling the structure of the
system. It then makes the quantity we are trying to improve observable, defines
a presence function on that observable [^F-not-observable], and lets
intervention logic emerge by observing the signal dynamics of the resulting
system of presences.

[^F-not-observable]: So what if the thing we want to measure is not observable?
All the challenges of measuring proxies still remain. We don’t claim that
everything worth measuring can be modeled as a system of presences.  
But as we show here, the presence calculus significantly expands the universe of
things that *can* be observed, modeled, and measured directly.  
Before reaching for proxies simply because they are “easy to measure,” it's
worth asking whether we understand *why* the problem *cannot* be modeled using
presence calculus. The class of "measurable"
things as defined in the presence calculus is very large.

# Implementation Notes

In a typical git-based implementation:

- Presence density functions should be defined using *non-blank diff lines*
  between commits (e.g., `git diff --numstat --ignore-blank-lines`).
- Presence density functions are piecewise constant and change in response to
  events in version control:
    - *Commits* and *merges* induce step changes in presence.
    - This machinery is used both to construct a presence density function from
      raw commit history and to compute presence mass over any sampling
      interval.
    - Presence is treated as a real-valued quantity defined at all times,
      regardless of discrete event timing.

# Summary

This model gives us a direct, real-time representation of batch size using
Presence Calculus:

- *Deployment frequency* and *lead time for changes* become *derived metrics*,
  computable from onset/reset times.
- The model supports *tracing batch size dynamics* by developer, team, or repo.
- It enables *leading indicators*, *causal reasoning*, and *early intervention*,
  all grounded in mathematically coherent flow logic.

This formulation not only replaces proxy metrics with direct observables but
also provides a rigorous foundation for next-generation DevOps analytics
systems.
