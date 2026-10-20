# Build Guide: <agent name>

## 1. Overview
<Two sentences: what the agent does and who it is for.>

## 2. Before you start
- [ ] Access to the Copilot Studio environment where the agent will be built
- [ ] Access to every knowledge source and system listed below
- [ ] Confirmation from your admin that the connectors below are allowed in this environment

## 3. Components to build
| Component | Building block | Details |
|---|---|---|
| | Instructions / Knowledge / Tool / Topic / Trigger / Authentication / Channel | |

## 4. Build steps
1. **Create the agent.** Name, description and the instructions below.
2. **Add knowledge.** <sources>
3. **Add tools and connectors.** <one line per connector with the sign-in it needs>
4. **Add topics and hand-off.** <the flows that need a fixed path>
5. **Set authentication and channel.** <choice and reason>
6. **Test.** Use the test messages in section 6.
7. **Publish and share.** <audience>

## 5. Suggested agent instructions
```
<Draft instructions for the agent, written for the builder to paste, under 2,000 characters.>
```

## 6. Test plan
| # | Message | Expected result |
|---|---|---|
| 1 | | Answers from knowledge |
| 2 | | Answers from knowledge |
| 3 | | Uses a tool |
| 4 | | Hands off to a person |
| 5 | | Declines politely |

## 7. Governance checklist
| Connector | Approved by (knowledge file) | Sign-in used |
|---|---|---|
| | | |

**Replaced during design**
| Requested | Reason | Used instead |
|---|---|---|
| | | |

**Confirm in the Power Platform admin center before publishing**
- [ ] Every connector above is allowed by the data policy of the target environment
- [ ] Who can use and share the agent is set as intended
- [ ] Authentication matches the data sensitivity in the requirements
- [ ] Anything marked "Needs admin check" in the requirements brief is resolved

## 8. Risks and open questions
- <risk or question>

*Check these steps against the current Microsoft Learn documentation for Copilot Studio, because menus and features change.*
