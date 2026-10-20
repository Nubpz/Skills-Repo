---
name: build-guide
description: Use when a Copilot Studio agent design exists, or the person asks how to build it, and they want concrete build steps, a test plan or governance notes. Maps the design to Copilot Studio building blocks and produces a practical build guide. Do not use for gathering requirements or for drawing the architecture.
---

# Build Guide

Turn an agreed design into a step-by-step guide for building the agent in Copilot Studio.

## Steps

1. **Find the design.** Use the confirmed design from this conversation (components, connectors, flow). If there is none, say so and offer to design it first. Do not build a guide from guesses.
2. **Map every component to a building block** using `references/copilot-studio-building-blocks.md`: instructions, knowledge, tools and connectors, topics, triggers, authentication, channels, testing and publishing.
3. **Write the guide** using `assets/build-guide-template.md`. Keep every section, in order, with the same headings.
   - Order the steps as: set up, add knowledge, add tools and connectors, add topics and hand-off, set authentication and channel, test, publish.
   - For every connector, give the approved-by source (the knowledge file that confirmed it), the authentication it needs, and one sentence on what it is used for in this design.
   - Write 5 test messages: three that should work, one that should hand off to a person, and one that the agent should decline.
4. **Fill the governance checklist.** List every connector used with its approved-by source, every connector that was replaced and why, and the items the builder must confirm in the Power Platform admin center before publishing (data policy for the environment, who can use or share the agent, authentication settings).
5. **Stay accurate.** Copilot Studio changes often. Describe where to do things by purpose ("in the agent's tools area") rather than by exact menu names unless you are sure, and close with a note to check the steps against the current Microsoft Learn documentation.

## Rules

- Never add a connector, action or setting that is not in the design or in the approved knowledge.
- Never say a design is approved by governance. Say it uses connectors listed as approved, and that the admin must confirm.
- Keep each step to one or two sentences. The builder should be able to follow the guide while working.
