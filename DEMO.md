# Skills demo: Copilot Studio Agent Architect (Agent Builder)

One agent, one set of instructions, three skills added one at a time. Run the same test message at every step and compare.

## Files
- `instructions.md`: paste into the agent's Instructions field (about 2,400 characters, limit 8,000). Never change it between steps.
- `skill-packages/requirements-interview.zip`, `architecture-design.zip`, `build-guide.zip`: upload the complete .zip in Configure > Skills > Add.
- `sample/hr-policy-agent.spec.json`: an example design spec, to see what the skill produces.
- `sample/example-output-architecture-flow.html`: an example of the downloadable animated file. Open it in a browser.

## Agent setup
1. New agent in Agent Builder. Name: Copilot Studio Agent Architect.
2. Paste `instructions.md` as the instructions.
3. Knowledge: add your governance Excel files as a **SharePoint** knowledge source (not as uploaded files). Microsoft lists skills combined with embedded (uploaded) files as unsupported in the preview.
4. Turn off web search so the agent stays grounded in your governance knowledge.

## Test messages (use the same at every step)
1. "I want an agent that answers HR policy questions from SharePoint for employees in Teams. If it can't answer, it should email HR and create a follow-up task."
2. A governance trap: "Also use Gmail to send the email." (Swap in any connector that is not on your approved list.)

## The ladder

| Step | Skill added | What the audience should notice |
|---|---|---|
| 0 | none | Some questions, a basic Mermaid diagram (likely a long left-to-right strip), connectors with sources, generic build steps |
| 1 | requirements-interview | Questions come a few at a time, governance is checked while asking, and it ends with a confirmed requirements brief before any design |
| 2 | architecture-design | The Gmail request is replaced with an approved alternative and the reason is shown. Every connector has an "approved by" source. Top-to-bottom layered Mermaid. A downloadable animated HTML file. The script rejects a design with no approval source |
| 3 | build-guide | Concrete build steps, 5 test messages, and a governance checklist to confirm in the admin center |

Talk track for step 2: the script, not the model, decides whether a design is valid. Ask the agent to "add a connector that isn't approved" and show it refuse.

## What I tested here, and what I could not
Tested in my workspace:
- The design script: it accepts the sample spec, and rejects specs with a missing approval source, a blocked connector, gaps in step numbers, an unconnected node, or a connector in the wrong layer.
- The Mermaid output parses with the Mermaid library (syntax only).
- The HTML opens in headless Chromium with no JavaScript errors. The dot travels along each connection, the steps play in order, and Play, Next step and Reset work.

**Not tested: inside Agent Builder itself.** Check these before presenting:
1. The agent can save `design.json` and run the script in the skill sandbox (the script uses only the Python standard library).
2. The agent can hand back `architecture-flow.html` as a downloadable file. If not, the skill falls back to the Mermaid diagram only.
3. How the Mermaid layout looks in your chat. Mermaid places nodes itself, so it may not line up as tidily as the HTML.
4. Skills together with a SharePoint knowledge source (only embedded files are documented as unsupported).
5. The skill descriptions fire on your test messages. If one does not load, tell me and I will tune its description.

## Limits to mention
8 skills per agent, 50 MB per package, 350 files, SKILL.md under 20,000 characters, scripts run in a sandbox with no network and no package installs. All three packages are far under these limits.

## Keeping it current
The governance files stay your source of truth in SharePoint, so updating them updates the agent. The `capabilities` reference in the build-guide skill is general guidance; refresh it when Copilot Studio changes.
