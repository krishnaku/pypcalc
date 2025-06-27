% Statistics and Time % Some connections % Dr. Krishna Kumar % June 26, 2025

In software development and many other operational contexts, we often have to
reason about the time it takes for processes to run, tasks to complete, things
to be delivered etc. Further these "things" we are reasoning about are not
uniform the same "kind" of thing - say fixing a bug, or delivering a change
requested by a user, make take vastly different amounts of time ranging from a
few minutes to few months. In other words, value and time taken to do something
are not always correlated.

So lets consider a setup where we have a some operational process that we are
trying to measure and and that the durations and ___timescales_ of these
processes can vary widely. Some things take days, some things take minutes, etc.

The point with this setup is that these durations are irreducible. Maybe all of
them produce the similar customer impacts, for example. Any time you are dealing
with a process that involves something that you cant influence directly - say
getting a customer to buy your product, or give you feedback on your new
features, or even just the time it takes you make a code change because of
pre-existing technical debt you face this situation,

These kinds of processes exist all over the place happens nearly every day in
software development but this sort of thing happens in many other operational
areas such as sales, marketing, HR, R&D etc. So lets assume we cant hand-wave
our way out of the situation. Variability is a given.

Now the question is how do we make reliable measurements and reason about these
processes with data. It is actually trickier to do this consistently than one
imagines.

Lets take an example to see why. Say we have a process with highly variable
duration and we want to make a set of measurements to analyze these durations.

A very standard way of doing this would be observe the process for a period of
time, keep track of when a process starts and when it finishes, and every time a
process finished, we store its duration and analyze it with standard tools of
statistics.

But note that in collecting this data time is involved in two ways: there is an
period over which we are collecting the data by observing start and finish
times - the observation window that determines the set we are collecting
statistic over, and then the actual data we are measuring is also a duration
which is measured in units of time. We are sampling the process in time, but in
that window we have a complete set of samples of the all the durations, since we
are tracking all the start and finish times of processes.

Lets start with a simple statistical question we can ask of this data set: "what
is the average duration of a process"? This is straight forward to answer: we
add up all the sample durations and divide it by the number of samples and we
are done. Since our sample set is complete, we know our answer reflects the "
correct" average duration of the processes over the observation window.

Now we ask another question: what is the average number of processes at any
given time over the observation interval? We can also try and answer this by
statistical sampling. Over the same observation window as earlier, periodically
take samples and see how many processes are running, and at the end of the
observation window we divide the observed process counts by the number of
samples we collected and report the result as the average process count over the
interval.

Now, while this is latter number is valid statistical average, this average
feels less "right" than the average duration we computed earlier. For one thing
we only see snapshots of the process in time, and depending upon the granularity
of the sampling process we may miss many data points if they fall in between the
sampling granularity. So this sampling process is a sampling process in time and
also a sampling of time. There is more room for error in this sampling
technique, and we need to take many more samples to ensure that our sample
counts approach the true average process counts.

Since the underlying processes are highly variable, you cant really repeat the
experiment many times and rely on the law of large numbers to get you to the "
right" answer, because in the next observation window the underlying
distribution of values may be very different. So in a sense, you cant measure
both the average duration and the average number of processes _over the same
observation window_ using independent sampling of the same observation window.

This is because we are in a sense sampling over a dimension, time that also
figures as the measure of the sample size we are computing averages over. The "
average" number of processes running per unit of time' is a "time average" and
if we want a consistent set of observations of both average duration and average
number of processes we cannot use an independent statistical sampling technique
for both and expect to arrive at a consistent answer for both values - they are
tightly dependent and have to be sampled _at the same time_ over the same
observation window.

Now of course we went through all this rigmarole only because we are trying to
show that these two quantities cant be sampled indpendentky if you want to
reason about their relationships together as averages.

The solution is derive both average from the same sample data set, and this is
not difficult because we know when each process started and finished, and the
number of processes can change only when a process starts and finished. So the
fix is not hard- we dont sample the number of processes, we _compute_ it from
the sample data we used to compute the average duration.

But this relies on the fact that time is continuous, and that we can assume that
when a processes has started at time t0 and it finishes at time t1, then it is
_present_ in the process over the continuous interval from t0 to t1. So if we
know this, we can implicitly construct a full picture of how many processes were
running in the system at any time by tracking the number of these _presences_ of
processes over the entire observation window.

The result is a curve in 2 dimensions that we can call a _sample path_ for the
process for _that particular_ observation window.

So what is the number of processes running per unit time? We can divide this
curve into rectangular areas and think of each rectangle as a chunk of "process
presence" and divide the area of the rectangle by the length of the time and
_call_ the average nuber of processes running per unit time. Now each rectangle
may be considered as sample and since these rectangles cover the entire area
under the sample path, we can be sure we have a complete sample for processes.
So if we take the total area under the sample path and divide it by the length
of the observation window we now have a consistent pair of measurements for
average duration and average number of processes over that observation window.

When dealing with highly variable, time dependent processes, where the
measurements are properties of time this is the only way we can get a consistent
measurement of both averages.

Now all this is irrelevant if we are not dealing with measurements that are not
time dependent, time varying or neither, but a huge number of economically
important operational measurements are in this category, so we need to take a
more careful approach to measuring these time dependent quantities and reasoning
about them through statistical or other techniques.

Luckily, while time introduces complexities as a dimension - it only runs
forward and you only get one shot to measures something over the periods on
which you need to make decisions etc.. time also has rich topological structure
that enables us to asset properties such as continuity and measurabilty, that
when exploited carefully yield a very rich and general set of techniques to
reason about not just the statistical properties of such signals, but understand
their behavior and evolution over time, even when this behavior is not at all
uniform statistically.

This is what the presence calculus enables.

When reasoning about time and time related measurements you need to treat that
as special cases in standard statistical inference. While specialized
techniques (autocorrelation, trends, seasonality) and models (ARIMA, GARCH,
state-space models, Kalman filters, etc.) have been developed to address the
complexities of time-varying data—often as adaptations or 'extensions' to
frameworks that typically assume uniformity or stationarity—the Presence
Calculus takes a fundamentally different starting point.

Time is special from a statistical perspective, but the presence calculus
accepts the non-uniformity of behavior over time as the default.

It is built from the ground up with the inherent non-uniformity and
path-dependent nature of time-varying data as its default assumption. We assume
you can only measure things in time once, and we still need to make consistent
decisions based on those measurements.

From this premise, it constructs a general set of computational and reasoning
tools specifically designed to manage and analyze such dynamics naturally,
rather than treating them as exceptions requiring special considerations.

Further, the statistical measures we compute here are standard statistical
measures in every sense of the word. The key difference is a highly
constrained "sampling process" for non-uniform processes that allows us to
safely use standard statistical techniques on the resulting sample spaces.

Thus this is a fundamentally different approach to treating time and statistics.

Statistics is mostly about uncovering the "commonality" across a set of time
based samples of a system - whereas PC is mostly focused on measuring the
dynamics - how those samples change over time.

The two paradigms are complementary and can support and inform each other when
used with this understanding in mind. 









