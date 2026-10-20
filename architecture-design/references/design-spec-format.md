# Design spec format

The design is a small JSON object. The script `scripts/build_design.py` validates it and generates the Mermaid diagram and the animated HTML from it, so the two always match.

## Fields

| Field | Required | Notes |
|---|---|---|
| `title` | yes | Name of the agent, up to 80 characters |
| `summary` | no | One sentence, up to 200 characters |
| `nodes` | yes | List of nodes (below) |
| `edges` | yes | List of edges (below) |
| `replaced` | no | Connectors the person asked for that were not approved: `requested`, `reason`, `used_instead` |
| `assumptions` | no | List of text items |

## Nodes

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Letters, digits and underscores, starting with a letter. Unique |
| `label` | yes | Up to 60 characters. Say what it is, for example "Planner: create task" |
| `layer` | yes | `users`, `agent`, `connectors` or `data` |
| `type` | yes | `channel`, `agent`, `connector`, `knowledge`, `system` or `human` |
| `approved_by` | for `connector` and `knowledge` | The governance knowledge file or document that confirms it is approved, for example "SharePoint.xlsx" |
| `approval_status` | no | Defaults to `approved`. Any other value is rejected |
| `note` | no | Up to 160 characters, shown as a tooltip in the HTML |

Which type goes in which layer:

| Layer | Types allowed | Typical content |
|---|---|---|
| `users` | `channel`, `human` | Teams, a website, the employee or customer |
| `agent` | `agent` | The Copilot Studio agent (use one node per agent) |
| `connectors` | `connector` | Approved connectors and tools the agent calls |
| `data` | `knowledge`, `system`, `human` | SharePoint knowledge, the business system behind a connector, a hand-off team |

## Edges

| Field | Required | Notes |
|---|---|---|
| `from`, `to` | yes | Node ids |
| `label` | yes | Up to 50 characters, a short verb phrase, for example "Creates follow-up task" |
| `step` | yes | Whole numbers 1 to N, unique, no gaps. This is the order of the animation |
| `bidirectional` | no | `true` for request and response pairs, so no return edge is needed |

## Rules the script enforces

- Every `connector` and `knowledge` node has `approved_by`, and its status is approved.
- Types sit in the right layer; there is at least one `users` node and one `agent` node.
- Every node is connected, and step numbers run 1 to N.

## Warnings (not errors)

- More than 4 nodes in a layer, or more than 12 nodes overall.
- An edge that skips a layer. Knowledge sources attached directly to the agent are the normal exception.

## Example (small)

```json
{
  "title": "HR Policy Assistant",
  "summary": "Answers HR policy questions and hands off to HR when it cannot answer.",
  "nodes": [
    {"id": "emp", "label": "Employee in Microsoft Teams", "layer": "users", "type": "channel"},
    {"id": "agent", "label": "HR Policy Agent", "layer": "agent", "type": "agent"},
    {"id": "mail", "label": "Outlook: send email", "layer": "connectors", "type": "connector", "approved_by": "Outlook.xlsx"},
    {"id": "sp", "label": "SharePoint: HR policies", "layer": "data", "type": "knowledge", "approved_by": "SharePoint.xlsx"},
    {"id": "hr", "label": "HR specialist", "layer": "data", "type": "human"}
  ],
  "edges": [
    {"from": "emp", "to": "agent", "label": "Question and answer", "step": 1, "bidirectional": true},
    {"from": "agent", "to": "sp", "label": "Searches policies", "step": 2, "bidirectional": true},
    {"from": "agent", "to": "mail", "label": "Escalates when unsure", "step": 3},
    {"from": "mail", "to": "hr", "label": "Delivers the question", "step": 4}
  ],
  "replaced": [{"requested": "Gmail", "reason": "Not listed as approved", "used_instead": "Outlook"}],
  "assumptions": ["Employees sign in with their work account"]
}
```
