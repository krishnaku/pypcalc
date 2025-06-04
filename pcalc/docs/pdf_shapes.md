## Presences and Presence Density Functions

The relationship between a presence and the underlying presence density function
has a couple of subtle points worth clarifying.

<div style="text-align: center; margin:2em">
  <img src="../assets/pandoc/pdf_examples.png" width="600px" />
  <div style="font-size: 0.9em; color: #555; margin-top: 1em; margin-bottom: 1em;">
    Figure 2: Shapes of presence density functions
  </div>
</div>

This diagram illustrates several shapes of **presence density functions**, or  
PDFs. Each function maps a specific element and boundary to a real value at  
each instant of time.

These functions are defined on a continuous timeline that,  
in principle, spans from $-\infty$ to $+\infty$.

A given PDF is only non-zero over certain intervals. The shape and support of
the function (the interval over which it is non-zero) tell us something about
how presence is distributed over time.

Here are several common shapes classified according to the number of support
intervals and whether the value is constant or variable over those intervals.

#### Single, Variable

**Element 1** shows a single contiguous interval of presence with a  
time-varying intensity. The presence is concentrated in one span of time, but  
the function itself varies continuously—rising, falling, and pulsing in  
strength.

#### Multiple, Variable

**Element 2** illustrates a PDF with multiple disjoint intervals of non-zero  
presence. The density varies across these intervals. This kind of function is  
useful for modeling phenomena that recur or return with different levels of  
intensity—say, repeated user sessions or staggered bursts of engagement.

#### Multiple, Constant

**Element 3** is similar in structure to Element 2, but the density values are  
constant within each interval. This kind of function often arises when
modeling  
repeated activities that impose uniform load or cost while they’re active—for  
instance, scheduled jobs or fixed-length meetings.

#### Multiple, Variable, Open

**Element 4** introduces a qualitatively different case: a PDF that becomes  
non-zero at some point and never returns to zero. These functions do not have  
compact support; they remain “open” over time. In this example, the density  
grows and plateaus, but never falls to zero again.

This kind of function models ongoing, persistent presence—such as the continued
influence of a deployed feature, or the lasting impact of a system change.

When reasoning about presence density functions, these are useful ways to
characterize presence density functions.

- **Constant vs. Variable**: Does the function change over time, or stay flat?
- **Single vs. Disjoint Support**: Is presence concentrated in one interval,
  or  
  spread across many?
- **Closed vs. Open**: Does the function eventually return to zero, or does it  
  continue indefinitely?

These distinctions matter when we define **presences** over these functions,  
especially when we want to measure presence mass, compare intervals, or model  
evolving system behavior.

### Mapping a PDF to presences

Unlike the underlying PDF where the value of the function may drop to zero, a
prescence always has non-zero mass - it represents a portion of the PDF where
the value of the PDF is non-zero at some point over the interval of the
presence.

There are many ways in which a given PDF may be represented as presences, but a
standard approach is to divide up the timeline into disjoint intervals and
report the area of the PDF that intersects each interval as a distinct presence
derived from that PDF.

So for example given the PDF and the partition of the timeline below.

We would represent the PDF as the set of presences. 