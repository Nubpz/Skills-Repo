---
name: requirements-interview
description: Use when a person wants to design, plan or build a new Copilot Studio agent, or describes an agent idea, and the requirements are not fully known yet. Runs a short structured interview and produces a confirmed requirements brief. Do not use for questions about an existing agent or general Copilot Studio how-to questions.
---

# Requirements Interview

Gather what is needed to design a Copilot Studio agent, then write it up as a brief the person can confirm. Do not design the architecture in this step.

## Steps

1. **Restate the idea** in one sentence so the person can correct you straight away.
2. **Interview in rounds.** Ask at most 3 questions per round, taken from `references/question-bank.md` in the order listed there. Skip anything the person has already told you. Offer short multiple-choice options where the question bank gives them, so answering is quick. Plan for 3 rounds at most.
3. **Check governance as systems come up.** When the person names a system or tool (for example a ticketing tool, a mailbox, a CRM), look it up in your knowledge sources straight away. Tell them in one line whether it is listed as approved, and if it is not, offer an approved alternative. Do this during the interview, not after, so they do not describe a design that cannot be built.
4. **Do not stall.** If the person says "just design it" or stops answering, continue with sensible assumptions. Mark every assumption in the brief as "ASSUMED".
5. **Write the brief** using `assets/requirements-brief-template.md`. Keep every section, in order. Write "Not specified" for anything unknown instead of leaving it blank.
6. **Ask the person to confirm or correct the brief** before any design work starts. End with one clear question, for example "Is this right, or should I change anything before I design it?"

## Rules

- One short question at a time is fine; never send a long questionnaire.
- Use the person's own words for the goal and for the user groups.
- Never invent a system, a limit or a policy. If governance information cannot be found in knowledge, say so and mark it "Needs admin check".
- Keep the whole interview friendly and brief. Most people building a first agent do not know every answer, and that is fine.
