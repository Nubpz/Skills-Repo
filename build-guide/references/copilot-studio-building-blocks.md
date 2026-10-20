# Copilot Studio building blocks (general guidance)

This is general guidance. Product names and menus change, so always tell the builder to check the current Microsoft Learn documentation.

| Block | What it is | Use it for | Design question to answer |
|---|---|---|---|
| **Instructions** | Plain-language rules that tell the agent its role, scope, tone and limits | Setting purpose, boundaries and how to use its tools and knowledge | What should it always do, and what should it never do? |
| **Knowledge** | Sources the agent answers from (SharePoint sites and files, uploaded files, websites, business data) | Questions answered from existing content | Which sources, and who owns keeping them current? |
| **Tools and connectors** | Actions the agent can take in other systems through connectors, flows or other tool types | Creating a ticket, sending an email, updating a record, looking up a status | Which system, which action, read or write, which sign-in? |
| **Topics** | Defined conversation paths with trigger phrases, questions and branches | Predictable flows such as collecting details before creating a ticket, and hand-off to a person | Which tasks need a fixed flow instead of free answers? |
| **Triggers** | Events that start the agent without a user message (for example a new item or a new email) | Agents that act on their own | What event, and what should the agent do with it? |
| **Authentication** | How users sign in, and whether the agent acts as the user or as a service identity | Protecting data and applying each person's access | Does everyone sign in? What can each person see? |
| **Channels** | Where users reach the agent (Teams, a website, Microsoft 365 Copilot, others) | Reaching people where they already work | Which channel first? |
| **Testing** | Trying messages in the test experience before publishing | Checking answers, tool calls and hand-offs | Which five messages prove it works? |
| **Publishing and sharing** | Making the agent available to its audience | Release | Who gets access first? |

## Environments and data policy

- Agents are built inside an environment. Data policies (often called DLP policies) in the Power Platform admin center group connectors, for example as business, non-business or blocked, and a blocked connector cannot be used.
- The policy that applies depends on the environment, so the builder must confirm in the admin center that every connector in the design is allowed in the environment where the agent will be built.
- The governance knowledge files are a snapshot. Live policy settings are only visible to admins.

## Common design patterns

- **Answer agent:** knowledge only, no tools. Simplest and lowest risk.
- **Answer and escalate:** knowledge plus a ticket or email tool, and a hand-off topic when the agent cannot answer.
- **Task agent:** topics collect details, then a tool performs the action, with a confirmation step before any write.
- **Autonomous agent:** a trigger starts it, tools do the work, and a person reviews the result before anything irreversible.
