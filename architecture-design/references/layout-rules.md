# Layout rules

The goal is a diagram that reads top to bottom and spreads evenly left to right, instead of one long horizontal strip.

## The four layers (top to bottom)

1. **Users and channels:** who starts the flow and where they are
2. **Agent:** the Copilot Studio agent
3. **Approved connectors:** the tools the agent calls
4. **Knowledge and systems:** the content and business systems behind them, plus any human hand-off

## How to keep it uniform

- Put at most 4 nodes in a layer. If there are more, group them (for example "Microsoft 365 apps" instead of three separate boxes) or split the design. Beyond 4 the HTML wraps the layer into rows, and connections to the second row then pass behind the first row, which looks cluttered.
- Prefer edges between neighbouring layers. Route an action through the connectors layer rather than drawing the agent straight to a business system.
- Use `bidirectional: true` for a request and its response. Do not draw return arrows.
- Keep labels short: a verb phrase on edges, "System: action" on connectors.
- Number the steps in the order a person would tell the story: user asks, agent searches, agent acts, hand-off.

## What the two outputs do

- **Mermaid (in the chat):** a top-down flowchart with one box per layer. Mermaid decides node positions itself, so layers may not line up perfectly in every viewer. Show it exactly as the script returns it and do not edit it by hand.
- **Animated HTML (downloadable file):** the script places layers in fixed bands, top to bottom, and spaces the nodes in each band evenly. Press Play to watch a dot travel along each connection in step order. It works offline and has no external links.
