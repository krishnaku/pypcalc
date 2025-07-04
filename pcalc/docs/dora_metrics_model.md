---
title: "<strong>Software Delivery Metrics</strong>"
subtitle: "<span style='font-size:1.2em;'>The Presence Calculus way</span>"
author: |
  Dr. Krishna Kumar  
  <em>The Polaris Advisor Program</em>
number-sections: true
figures-numbered: true
link-citations: true
toc-title: "Contents"
toc-depth: 2
figPrefix: "Figure"
---

# Introduction

The Presence Calculus is a quantitative model for reasoning about signal
dynamics in a domain.

Its purpose is to support principled modeling and rigorous decision-making
using operational data in business-critical contexts—ensuring that such
decisions rest on a mathematically precise, logically coherent, and epistemically
grounded foundation.

The Presence Calculus emerged from a search for better tools to reason about
operations management in software product development and engineering—domains
where prevailing approaches to measurement often fall short on all three fronts.

In [*The Presence Calculus: A Gentle Introduction*](./intro_to_presence_calculus.html),
we gave a broad overview of the theory and analytical machinery of the calculus.
That document laid out the conceptual scope of the framework and the types of
tools it brings to the table.

In this note, we dive deep into a concrete application of the Presence Calculus:
measuring and analyzing software delivery systems. This is one of several
application domains we’ll explore—but it’s the one closest to the original
motivations for developing the calculus.

Our goal here is to bridge theory and practice: to connect the core ideas from
the gentle introduction and the formal materials in the
[*Theory Track*](../theory_track.html) to real-world problems in software
delivery.

We aim to illustrate not just the measurement *philosophy* behind the calculus,
but also the detailed design choices and modeling decisions it enables. This is
both a pedagogical document—demonstrating how to apply the calculus—and a
reference for practical implementations in delivery analytics.

## Measuring software delivery

Modern software engineering practices favor frequent delivery of small code
changes to production over infrequent, large releases. The extensive empirical
research conducted by the DevOps Research and Assessment (DORA) program has
identified the capabilities that consistently enable this: trunk-based
development, WIP limits, small batch sizes, continuous integration and testing,
deployment automation, and fast technical and business feedback — among others.

These practices are now widely recognized as *enablers* of improved business
performance, thanks to a decade of DORA’s research. But significant challenges
remain in adopting them at scale across the industry.

As of the 2024 *State of DevOps* report, **60%** of survey respondents still
fall into the *Medium* and *Low* performer categories — reporting that they
deploy less than weekly, and that changes take weeks or months to reach
production.

And this is *despite* the fact that these organizations were engaged enough to
respond to the survey. If we extrapolate to the broader industry — particularly
older, stable enterprises — the true percentage of teams struggling to
modernize is likely even higher. The top tiers are likely overrepresented by
younger, high-growth, or tech-native companies.

Even after a decade of clear evidence about what works, *most* of the industry
has yet to make the shift. The opportunity for improvement remains enormous —
especially in economically critical sectors.

## The AI challenge

AI is only going to make this challenge more pressing — and more visible —
widening the divide between high performers and the rest.

Even in these early stages of AI-augmented development, there’s already evidence
that the core capabilities identified by DORA still apply. Whether code is
written by humans or software agents, it still needs to be integrated, tested,
reviewed, deployed, and supported — with short feedback loops. The structure of
high-performing delivery systems hasn’t fundamentally changed. If anything, AI
accelerates throughput of code delivery — increasing both the demands on
delivery systems and the risks they must absorb.

There’s great optimism that AI can help legacy enterprises catch up. But our
thesis is that AI alone will not enable struggling organizations to leapfrog
into high performance. The companies that failed to adopt modern engineering
practices the first time around won’t suddenly succeed now *unless* they invest
in the same foundational capabilities — now extended to more complex
human–machine systems.

That work still needs to be done — by developers (and agent swarms!), managers,
and leaders — while thoughtfully integrating AI into organizations that have
historically resisted transformation.

## So what?

What does any of this have to do with the *Presence Calculus*?

We believe that while the research into *what* capabilities drive performance
has matured, our methods for *measuring* those capabilities have not.

The Four Key DORA Metrics,

- *Deployment Frequency*,
- *Lead Time for Changes*,
- *Change Fail Percentage*, and
- *Mean Time to Restore*[^cfr-note]

are the gold standard of measurement in software delivery. 

In fact, they are often used as the *definition*
of software delivery performance. But as they stand, they remain poorly
suited to enabling real _operational_ improvement inside actual delivery systems.

[^cfr-note]: MTTR has been replaced in newer editions of the DORA report with
*Failed Deployment Recovery Time*, which is a welcome change. We’re using the
older term here as it may be more familiar to the casual reader.

After six years building tooling to collect and apply these metrics in
real-world improvement programs, I’ve seen several recurring patterns:

- *Ambiguity*: There’s no widely accepted, operational definition of these
  metrics aside from those used in the State of DevOps survey — and those are
  designed to elicit survey responses, not to guide implementation in an operational setting.
- *Fitness for purpose*: The DORA survey measures *perception*. Using these
  metrics to guide improvement in real systems is an entirely different
  challenge.
- *Lack of actionability*: Dashboards may tell you where you are relative to
  benchmarks — but not what to do next.
- *The naive implementation pattern*:
  - Decide to measure DORA metrics to benchmark performance.
  - Skip directly to instrumenting them in your environment.
  - Pick a metric definition (from a vendor or invented ad hoc).
  - Wire up your version control and deployment systems — if possible.
  - Classify your org as Elite, High, Medium, or Low.
  - Track means, medians, percentiles, and trends.
  - Try to move the numbers.
  - Realize the metrics don’t tell you *how* to improve.
  - Try plausible-seeming strategies.
  - Watch dashboards lag, resist, or mislead.
  - Eventually stop using the metrics — except for reporting.

Meanwhile, the actual work — reducing batch size, adopting CI, accelerating
review — either survives _despite_ the lack of good metrics or quietly dies in
the fog induced by chasing the wrong metrics. Even where progress happens, it’s
often ad hoc and unsupported by meaningful feedback. Truly data-driven,
system-wide adoption of DORA *practices* remains rare, because the theory 
and tools to support this properly simply dont exist yet. 

The *Presence Calculus* offers a new foundation: rethinking what we measure and
how we measure it in the real-world delivery environments we actually work in.
So a natural test is to ask: *What do software delivery metrics look like in the
language of the presence calculus?*

This technical note begins to answer that question. We’ll show how presence
calculus gives us a formal language to model and measure delivery systems —
while staying aligned with the original *intent* behind the DORA metrics:
improving delivery capabilities.

For example, *Deployment Frequency* was chosen because it was thought to be a
proxy for batch size[^batch-size-note]. Similarly, *Lead Time for Changes* was
intended to measure delivery latency — the time from commit to deployment. These
metrics are typically reported as independent trends on DORA dashboards - one of
four key factors that characterize high performance delivery. But they’re not
independent. Presence calculus gives us a precise way to express the
relationship between them — and the conditions under which it holds.

[^batch-size-note]: *Accelerate* [@forsgren2018] notes (footnote, p. 16) that
deployment frequency is the reciprocal of batch size. This is not generally true
in software environments. We’ll show exactly when and how this relationship
holds — using the formal machinery of presence calculus.

We’re not proposing *new metrics*. We’re offering a mathematical foundation that
makes existing metrics more meaningful — by placing them in a broader,
structure-aware measurement system, and revealing what actually drives them.

This is what the presence calculus offers:

- Measurement models grounded in observable signals of system behavior.
- Mathematically precise definitions of domains, signals, elements, boundaries,
  and observables.
- A systematic way to uncover *causal* — not just correlative — relationships
  between key variables.
- A foundation for real-time feedback and intervention systems.

And what better place to start applying this machinery than a domain where
better measurement is so clearly needed?

Software delivery metrics may be a *simple* use case for presence calculus — but
they already reveal more actionable structure than most teams have today.

If you're working to improve delivery performance on the ground, this framework
offers a new lens — one that helps you understand what’s happening, and how to
steer it.

And as low-level development increasingly shifts to human–machine systems — with
humans moving further from the keyboard and deeper into domain-driven
engineering — the need for deep visibility and robust measurement of what’s
happening inside the codebase will only grow.

We need to strip software delivery measurement down to its foundations and build
it back up with rigor — to enable tools powerful enough to instrument and steer
the delivery systems that are now emerging.

Our thesis is that the Presence Calculus offers a much stronger foundation for
these next-generation measurement systems — built from first principles and
grounded in a sound, mathematical theory of measurement.

And then, maybe, the dashboards we build on this new foundation will finally be
worth something — not just for reporting, but for actually improving how we
deliver software.

Lets dive and consider our first operational challenge. 

# Operational Challenge: Reducing batch size

---

## References
