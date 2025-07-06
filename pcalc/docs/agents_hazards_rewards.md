## Agents, Hazards, and Rewards: Where the Presence Calculus Meets the Rest of the World

The Presence Calculus is built around the idea that *presence* — what is
observed, asserted, or known to hold within a system — is the right primitive
for modeling many real-world decision environments. In particular, it offers a
way to describe systems where multiple agents interact in the presence of both
*hazards* and *rewards*, and where human agency plays a central role in
interpreting and steering the system.

That framing isn’t unique — versions of it have appeared in economics,
artificial intelligence, and systems science for decades. But what’s often
missing from those approaches is a *first-class treatment of the signal dynamics
that agents observe and act on* — how they perceive signals as they unfold over
time, how they interpret those signals, and how they reason with them under
partial observability and bounded agency.

### Multi-Agent Reinforcement Learning (MARL)

In AI, the field of *multi-agent reinforcement learning* studies systems where
agents learn policies through interaction with each other and their
environment [@zhang2021]. Rewards and penalties are often externally
defined, and agents aim to optimize expected return over time. Many MARL
frameworks assume a shared world model and focus on convergence to optimal
policies or equilibria across agents.

Where Presence Calculus aligns with MARL is in recognizing that *reward and
hazard signals interact*, and that different agents may see the same system
very differently.

The way we would position the Presence Calculus in this context is as follows:

- Each agent observes a shared world model through a system of presence signals
  that represent hazards and rewards. Some of these signals may be globally
  observable or shared across agents, while others may be private or locally
  scoped.

- The objective for each agent is to interpret these presence signals —
  particularly by learning the *convergence limits* of hazard and reward signals
  in order to make effective decisions. These decisions may serve cooperative or
  competitive goals, depending on the broader system context.

The Presence Calculus provides the mathematical and structural tools to reason
about the accumulation, dissipation, and interaction of presence over time.

Rather than assuming a fixed reward function or global equilibrium, it allows
each agent to operate with partial observability, bounded knowledge, and
context-sensitive strategies grounded in measurable presence dynamics.

### Game Theory and Mechanism Design

In economics, *game theory* provides a well-developed framework for modeling
strategic interactions between agents [@fudenberg1991game]. Hazards are often
modeled as losses or risks to utility, and rewards as payoffs. The goal is often
to find equilibrium solutions or optimal mechanisms for aligning incentives.

Presence Calculus departs from this tradition by not assuming that global
equilibria are meaningful or even reachable. Instead, it assumes agents operate
under *partial knowledge*, with access to *signal systems* that help them steer
rather than solve. 

### Active Inference and Free Energy

In neuroscience and theoretical AI, the *free energy principle*
[@friston2010free] models agents as systems that minimize surprise (or "free
energy") by balancing exploration and exploitation. The framework integrates
perception, action, and prediction under a unified probabilistic model.

Presence Calculus shares this sense of *epistemic pragmatism* — that agents act
to reduce uncertainty and manage risk — but frames it in terms of *presence
assertions* of hazard signals rather than probability distributions. It
emphasizes the role of *temporal structure and boundary conditions* in how
signals are interpreted and acted on.

### What Presence Calculus Contributes

Presence Calculus contributes several key ideas that are underdeveloped in most
of these fields:

1. *Presence as a First-Class Epistemic Primitive*  
   Presence isn’t just state, observation, or belief — it’s a measurable
   assertion that can persist, overlap, and interact. This enables a new class
   of metrics and invariants for reasoning about flow, delay, and convergence.

2. *Rate Conservation Laws as Invariants*  
   Every system of presence signals carries with it a local and global rate
   conservation law that constrains how the system accumulates presence — hazards
   or rewards — over time. Ultimately, the evolution of the system of systems is
   governed indirectly by these constraints. Recognizing that such constraints
   exist in every system of presence signals, and are governed by variants of
   Little's Law, is a key insight that drives the utility of the calculus.
   Providing a formal way to systematically identify these local constraints is
   a contribution of the calculus.

3. *System-of-Systems Framing*  
   Each signal system (hazard, reward, status, etc.) has internal structure, but
   their interactions are emergent. This allows modeling *contingent
   interactions across layered systems*, with no assumption of global
   solvability.

4. *Human-in-the-Loop Steering*  
   Rather than aiming for optimization or equilibrium, Presence Calculus is
   oriented around *interpreting signals and steering behavior*. It treats the
   system as navigable, not solvable — a key distinction in messy real-world
   environments.

### Conclusion

While the basic ingredients — agents, signals, rewards, and risks — have been
studied for decades, the *Presence Calculus* adds new analytical tools to the
mix: a language for interpreting, modeling, and measuring the internal dynamics
of non-equilibrium system behavior from an agents perspective. It offers an
alternate substrate for integrating existing approaches and for reasoning
pragmatically about systems of interaction.

---

### References

```bibtex

