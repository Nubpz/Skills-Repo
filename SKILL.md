---
name: architecture-diagram-detailed
description: Create complex, detailed, accurate architecture diagrams for agents and solutions built on Microsoft 365 Copilot - users, channels, the agent, skills, knowledge sources, synced and federated Copilot connectors, identity, security controls and external systems. Use this skill whenever the user asks for an architecture diagram, solution design, data flow, component view, sequence or runtime view, trust boundary view, "how does this agent connect to X", or wants an existing diagram improved, extended or redrawn, even if they never say the word "architecture".
---

# Detailed architecture diagram

Your job is to turn what the user describes, plus what the agent's knowledge sources say, into a small set of precise Mermaid diagrams with a flow table, assumptions and gaps. A reviewer (architect, security, admin) should be able to read the result and trust it, so accuracy matters more than looking impressive. Every box and arrow must come from the user, from the approved connector guide, or from a clearly labelled assumption.

## Principles (and why)

- **Do not invent components.** An invented box looks like a real design decision and gets built. If a fact is missing, ask or list it under Assumptions.
- **Use only approved connectors.** The approved connector guide in your knowledge sources is the source of truth. If the user names something not in it, draw it with the "risk" style, label it "not approved" and mention it in Gaps.
- **Several clear diagrams beat one crowded one.** Readers should grasp any single diagram in under a minute, so split rather than shrink text.
- **Show movement and trust, not only boxes.** The questions people actually ask are: where does the data live, who signs in, and where are permissions enforced.
- **Say what you do not know.** Never present a guess as a fact, and never claim the diagram was rendered or validated; you can only say it follows the syntax rules.
- **Keep names stable** across all diagrams in one answer and across revisions, so people can compare versions.

## 1. Intake

Take facts from the user's message and the knowledge sources first. Then ask only for what is missing, in one message, at most four short questions. If the user wants a result now, proceed and record each guess under Assumptions.

- Purpose of the agent or solution, in one sentence.
- Users: which groups, and which surface (Copilot chat, Teams, Outlook, other).
- Knowledge: SharePoint or OneDrive locations, Teams or Outlook content, public sites, Copilot connectors (synced or federated), and any scoping such as project, space, repository or folder.
- Actions: read only, or also create, update, delete; in which systems.
- Identity and access: who signs in to what, service accounts, rollout audience.
- Security and compliance: sensitivity labels, DLP, audit, approvals.

## 2. Choose the diagram set

| Request | Produce |
| --- | --- |
| Quick or simple | View A |
| Normal | Views A and B |
| "Complex", "detailed", "full", "for architects or security review" | Views A, B, C and D |

- **View A, system context:** actors and main components, max 12 boxes, no internals.
- **View B, solution detail:** the agent, skills, knowledge sources and connectors with every data path, sign-in and permission check, max 18 boxes. If more are needed, split by area (knowledge, actions) and say how the diagrams connect.
- **View C, runtime sequence:** one sequence diagram of a typical question from prompt to answer, including one failure or fallback path.
- **View D, trust and data view:** trust boundaries, where data is stored versus passed through, how each source is authenticated, where permissions are enforced, what is logged.

## 3. Facts about Microsoft 365 Copilot components

Use these when drawing. Do not add detail beyond them unless the user supplies it.

- **Declarative agent (Agent Builder):** has instructions (8,000 character limit), knowledge sources, optional skills (up to 8, loaded only when a task needs them) and optional Copilot connectors. It runs inside Microsoft 365 Copilot with the signed-in user's access.
- **Skills:** a package with an instructions file plus optional resources and scripts. Scripts run in a sandbox with no network, so never draw an arrow from a skill script to an outside system.
- **Native Microsoft 365 knowledge:** SharePoint, OneDrive, Teams, Outlook, reached through Microsoft Graph with the user's existing permissions and sensitivity labels.
- **Synced connector:** an admin deploys it; a scheduled crawl copies items from the external system into the tenant's Microsoft Graph index with an access control list per item. Copilot searches the index. Data is as fresh as the last crawl. Users do not sign in to the source.
- **Federated connector:** uses Model Context Protocol (MCP) to fetch from the source at question time. Nothing is indexed or stored in Microsoft 365. Each user signs in with their own account. Write tools, where offered, need user approval.
- **Self-serve synced connector (preview):** each user connects their own account and only that user's content is indexed.
- **Actions:** Agent Builder does not author actions that call external services. Draw an action path only if the user says one exists, and name the mechanism they give.
- **Identity and governance:** Microsoft Entra ID signs users in; the Microsoft 365 admin center controls connector deployment, user access and staged rollout; Microsoft Purview provides audit, sensitivity labels and DLP.

## 4. Notation

Use these shapes and classes consistently.

| Kind | Mermaid shape | Class |
| --- | --- | --- |
| Person or group | `id(["Label"])` | person |
| Copilot surface | `id["Label"]` | surface |
| Agent | `id[["Label"]]` | agent |
| Skill | `id[/"Label"/]` | skill |
| Native knowledge | `id[("Label")]` | native |
| Synced connector | `id{{"Label<br/>synced"}}` | synced |
| Federated connector | `id{{"Label<br/>federated, MCP"}}` | federated |
| Graph index | `id[("Microsoft Graph index")]` | index |
| External system | `id["Label"]` | external |
| Control (Entra, Purview, admin center) | `id>"Label"]` | control |
| Not approved or unknown | `id["Label<br/>not approved"]` | risk |

Lines: solid arrow is a request or data already stored in the tenant; dashed arrow is a live call at question time or a scheduled crawl; thick arrow `==>` is the main user journey (use for one path only); dotted link `-.-` is a control applying to something.

Paste these definitions at the end of every flowchart, keeping only the classes used:

```
classDef person fill:#EEF2FF,stroke:#4F46E5,color:#1E1B4B
classDef surface fill:#F3F4F6,stroke:#4B5563,color:#111827
classDef agent fill:#ECFDF5,stroke:#059669,color:#064E3B
classDef skill fill:#F0FDFA,stroke:#0D9488,color:#134E4A
classDef native fill:#FFFBEB,stroke:#D97706,color:#78350F
classDef synced fill:#FDF2F8,stroke:#DB2777,color:#831843
classDef federated fill:#FDF2F8,stroke:#DB2777,color:#831843,stroke-dasharray:5 3
classDef index fill:#FEF3C7,stroke:#B45309,color:#78350F
classDef external fill:#F3F4F6,stroke:#4B5563,color:#111827
classDef control fill:#EFF6FF,stroke:#2563EB,color:#1E3A8A
classDef risk fill:#FEF2F2,stroke:#DC2626,color:#7F1D1D,stroke-dasharray:5 3
```

Apply with `class id1,id2 agent`.

## 5. Layout

1. `flowchart LR`, flowing Users, then Microsoft 365 and Copilot, then knowledge and connectors, then external systems. Governance and identity go in their own subgraph, declared last.
2. Draw the Microsoft 365 tenant as an outer subgraph containing Copilot, the Graph index and the connectors. External systems sit outside it. The arrow that crosses the tenant boundary is the one to label with the sign-in method.
3. Arrows run from caller to answerer, so external systems end up on the far right.
4. Number the main-flow arrows (`1.`, `2.`, ...) to match the flow table.
5. Declare the main user journey first so it lays out first. Every box needs at least one arrow.

Arrow labels follow `step. verb + data`, with the access method on a second line via `<br/>` when it matters. Good: `5. fetches live tickets<br/>user signs in`. Bad: `connects`, `uses`, `data`.

## 6. Security overlay for Views B and D

State for each source: how it is authenticated (user sign-in, admin service account, or Graph with the signed-in user); where permissions are enforced (the source system, or the access list stored with each indexed item); where data lives (tenant index, source only, or already in Microsoft 365); who can see the connector (tenant ceiling, staged rollout group, content visibility); and that Copilot interactions are audited in Purview.

Check these known gaps every time and list the ones that apply: a synced connector set to visible to everyone can overshare; incremental crawls may not pick up permission changes until a full crawl; sensitivity labels on external data may not be recognised; text written by outsiders in tickets or wikis can carry hidden instructions to the agent.

## 7. Mermaid safety rules

These exist because one syntax slip makes the whole diagram fail to render.

- IDs: one word, letters, digits, underscores, starting with a letter. Never `end`, `graph`, `subgraph`, `class`, `style`, `click` or `default`.
- Double-quote every label. Inside labels avoid double quotes, parentheses, square or curly brackets, the pipe character, and angle brackets other than `<br/>`.
- Put spaces around arrows. Every `subgraph` has an ID, a quoted title and its own `end`.
- Never draw an arrow to a subgraph when you mean a box inside it.
- classDef and class lines go after all nodes and arrows.
- Sequence diagrams: no colons inside message text, close every `alt`, `opt` and `loop` with `end`.
- Over about 45 arrow lines, split the diagram.

## 8. Output template

Return in this order:

1. **Title and summary:** one-line title, then two or three sentences on what the solution does and which views follow.
2. **Views** requested, each in its own `mermaid` code block with a one-sentence caption above.
3. **Flow table** of the main journey: Step, From, To, Data, Authentication, Permission check, Stored or live.
4. **Legend:** shapes, line styles, colors used.
5. **Assumptions:** one line each.
6. **Gaps and risks:** anything missing, not approved or worth review, with the reason.
7. **Open questions:** at most four, ranked by how much the answer would change the diagram.
8. **Self-check:** one line per item in section 10, marked pass or fix (fix it before answering).

If the Mermaid does not display in the user's interface, offer the same content as an indented text outline plus the flow table.

## 9. Revising an existing diagram

When the user supplies a diagram or asks for changes, keep every existing node ID and name, change only what was asked, add a **Changes** list (added, removed, renamed, re-routed), and re-run the self-check. Redraw from scratch only if asked.

## 10. Self-check before answering

1. Every box came from the user, the connector guide or a listed assumption.
2. No connector outside the approved guide, unless drawn as not approved.
3. Box counts within limits for each view.
4. Every arrow has a label with a verb and data.
5. Every connector is marked synced or federated.
6. Sign-in is shown for every arrow that leaves the tenant.
7. External systems are outside the tenant boundary.
8. No skill script has an arrow to an outside system.
9. Syntax follows section 7 and every subgraph is closed.
10. Names match across views and the flow table.
11. No credentials, keys or tokens appear anywhere.

## 11. Example (View A and View C)

```mermaid
flowchart LR
  subgraph USERS["Users"]
    emp(["Employees"])
  end
  subgraph TENANT["Microsoft 365 tenant"]
    subgraph COP["Microsoft 365 Copilot"]
      chat["Copilot chat"]
      ag[["Onboarding agent"]]
      sk1[/"Architecture skill"/]
    end
    subgraph DATA["Knowledge and connectors"]
      sp[("SharePoint policies")]
      idx[("Microsoft Graph index")]
      cw{{"Confluence<br/>synced"}}
      tk{{"Ticket source<br/>federated, MCP"}}
    end
  end
  subgraph OUT["Outside the tenant"]
    conf["Confluence spaces"]
    tsys["Ticket system"]
  end
  subgraph GOV["Governance and identity"]
    entra>"Microsoft Entra ID"]
    pur>"Microsoft Purview audit"]
  end
  emp ==>|"1. asks question"| chat
  chat ==>|"2. passes prompt"| ag
  ag -->|"3. loads skill when needed"| sk1
  ag -->|"4. reads files<br/>trimmed to user access"| sp
  ag -->|"5. searches indexed pages<br/>trimmed to user access"| idx
  cw -->|"stores items with ACLs"| idx
  cw -.->|"crawls on schedule<br/>admin service account"| conf
  ag -.->|"6. calls connector live"| tk
  tk -.->|"fetches tickets<br/>user signs in"| tsys
  emp -.- entra
  chat -.- pur
  classDef person fill:#EEF2FF,stroke:#4F46E5,color:#1E1B4B
  classDef surface fill:#F3F4F6,stroke:#4B5563,color:#111827
  classDef agent fill:#ECFDF5,stroke:#059669,color:#064E3B
  classDef skill fill:#F0FDFA,stroke:#0D9488,color:#134E4A
  classDef native fill:#FFFBEB,stroke:#D97706,color:#78350F
  classDef synced fill:#FDF2F8,stroke:#DB2777,color:#831843
  classDef federated fill:#FDF2F8,stroke:#DB2777,color:#831843,stroke-dasharray:5 3
  classDef index fill:#FEF3C7,stroke:#B45309,color:#78350F
  classDef external fill:#F3F4F6,stroke:#4B5563,color:#111827
  classDef control fill:#EFF6FF,stroke:#2563EB,color:#1E3A8A
  class emp person
  class chat surface
  class ag agent
  class sk1 skill
  class sp native
  class cw synced
  class tk federated
  class idx index
  class conf,tsys external
  class entra,pur control
```

```mermaid
sequenceDiagram
  autonumber
  actor U as Employee
  participant C as Copilot chat
  participant A as Onboarding agent
  participant G as Microsoft Graph index
  participant T as Ticket source MCP
  U->>C: Asks how to get a laptop
  C->>A: Passes prompt with user identity
  A->>G: Searches indexed pages
  G-->>A: Returns items the user may see
  alt User has connected the ticket source
    A->>T: Fetches open requests as the user
    T-->>A: Returns live status
  else Not connected
    A-->>C: Says live status needs a sign in
  end
  A-->>C: Cited answer
  C-->>U: Shows answer with citations
```

| Step | From | To | Data | Authentication | Permission check | Stored or live |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Employees | Copilot chat | Prompt | Microsoft Entra ID | Signed-in user | Live |
| 4 | Agent | SharePoint | Policy files | User identity | Existing file permissions | Stored in Microsoft 365 |
| 5 | Agent | Graph index | Indexed pages | User identity | ACL on each item | Stored in tenant index |
| 6 | Agent | Ticket source | Open requests | User signs in to source | Source system | Live, not stored |
