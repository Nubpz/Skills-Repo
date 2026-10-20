---
name: architecture-design
description: Use when requirements for a Copilot Studio agent are known and the person wants the architecture, design, diagram or data flow. Builds a validated design using only approved connectors, shows a Mermaid diagram in the chat and produces a downloadable animated HTML flow. Do not use to gather requirements or to write build steps.
---

# Architecture Design

Turn confirmed requirements into a validated design, a Mermaid diagram for the chat and an animated HTML file.

## Steps

1. **Check you have requirements.** Use the confirmed brief from this conversation. If the requirements are thin, run the requirements-interview skill first.
2. **Choose the components.** Decide the channel, the agent, the knowledge sources, the connectors the agent needs, and any human hand-off.
3. **Check governance for every connector and knowledge source.** Find each one in your knowledge sources before it goes into the design.
   - Listed as approved: use it and record the knowledge file or document that confirms it in `approved_by`.
   - Not listed, blocked or restricted: do not use it. Pick an approved alternative from your knowledge, and add an entry to `replaced` with the reason.
   - Cannot find the governance information at all: leave it out and list it under `assumptions` as "Needs admin check".
4. **Write the design spec** as JSON, following `references/design-spec-format.md` and `references/layout-rules.md`. Use the four layers, at most 4 nodes per layer, edges between neighbouring layers where possible, and numbered steps in the order the story is told.
5. **Run the script.** Save the spec as `design.json` and run:
   `python scripts/build_design.py design.json --out-dir .`
   If you cannot save a file, pass the spec on standard input instead: `python scripts/build_design.py - --out-dir .`
   If the result says `"valid": false`, read the errors, fix the spec and run the script again. Repeat until it passes. Do not show a diagram before the script passes. Never draw the diagram by hand.
6. **Show the Mermaid.** Put the `mermaid` text from the script output in a code block marked as mermaid, exactly as returned, so it renders in the chat.
7. **Hand over the HTML file.** Give the person `architecture-flow.html` as a downloadable file and tell them to open it in a browser and press Play. If you cannot attach files in this session, say so plainly and continue with the Mermaid diagram only. Do not paste the HTML into the chat.
8. **Summarize in a short table:** each component, its type, and for connectors and knowledge the `approved_by` source. Then list what was replaced and why, the assumptions, and any script warnings. Close with one reminder: governance knowledge is a snapshot, so confirm in the Power Platform admin center before building.

## Rules

- Never put a connector or knowledge source in the design unless it is confirmed approved in your knowledge sources.
- Never write an `approved_by` value you did not actually find. If it is not in the knowledge, the connector is not approved.
- Report the script's warnings to the person; do not hide them.
- Keep the design as simple as the requirements allow. A knowledge-only agent needs no connectors.
