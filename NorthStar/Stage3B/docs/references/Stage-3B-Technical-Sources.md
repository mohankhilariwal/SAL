# Stage 3B Technical Sources

**Verification date:** 2026-07-31

The architecture is vendor-neutral. The vendor documents below are comparative implementation references, not NorthStar's source of authority.

1. Yao et al., **ReAct: Synergizing Reasoning and Acting in Language Models**, arXiv:2210.03629, submitted 2022-10-06. https://arxiv.org/abs/2210.03629
   - Primary research source for interleaving observations/actions and task-oriented reasoning.
   - NorthStar adopts the observation-action concept, but does not store or require private chain-of-thought.
2. OpenAI, **Agents SDK — Running agents / Runner reference**, accessed 2026-07-31. https://openai.github.io/openai-agents-python/running_agents/ and https://openai.github.io/openai-agents-python/ref/run/
   - Vendor-specific example of final-output termination, tool-call iteration and a `max_turns` guard.
3. Microsoft, **AutoGen — Termination conditions**, accessed 2026-07-31. https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/termination.html
   - Vendor-specific examples of message-count, token, timeout and handoff termination conditions.
4. LangChain, **LangGraph overview and Graph API**, accessed 2026-07-31. https://docs.langchain.com/oss/python/langgraph/overview and https://docs.langchain.com/oss/python/langgraph/use-graph-api
   - Evidence that graphs are a later option for explicit state, branches and loops; NorthStar deliberately defers graph execution in S03B.
5. NIST, **Strengthening AI Agent Hijacking Evaluations**, accessed 2026-07-31. https://www.nist.gov/publications/strengthening-ai-agent-hijacking-evaluations
   - Security-evaluation motivation for testing whether untrusted content can redirect tool-connected agents.
6. OpenAI, **Agents SDK RunState reference**, accessed 2026-07-31. https://openai.github.io/openai-agents-python/ref/run_state/
   - Vendor-specific durable pause/resume model; cited as a later-stage comparison, not an implemented S03B capability.

## Source-quality notes

- Established practice in this stage: explicit state, strict tool contracts, deterministic authorization, bounded iteration and independent completion checks.
- Emerging/vendor-specific practice: exact agent SDK abstractions and framework termination APIs.
- Experimental or deferred: unrestricted self-reflection, search trees, durable graph migration and autonomous recovery.
