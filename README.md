# marionet-agents

An open-source library of focused AI agents that **proves its agents work, on any LLM**, and runs them as **real teams**.

- **Evidence:** every agent ships with test tasks. Agents are `draft` until they pass, then `verified`.
- **Executable teams:** team leads route work, agents hand off through checked documents, and risky actions wait for human approval.
- **Any LLM:** agents name a model tier (`fast`, `standard`, `strong`), not a vendor. You map tiers to Claude, GPT, Gemini or a free local model in `models.yaml`.

## The teams

**51 agents in 11 teams**, with 21 shared skills and 153 eval tasks. Full list with what each agent does: [ROSTER.md](ROSTER.md).

| Team | Lead | Agents |
| --- | --- | --- |
| Leadership | chief-of-staff | 2 |
| Engineering | senior-system-architect | 7 |
| Security | application-security-engineer | 4 |
| Data & ML | lead-data-scientist | 7 |
| AI | senior-ai-engineer | 3 |
| Research | market-research-analyst | 4 |
| Legal | contracts-counsel | 3 |
| Design | senior-ux-designer | 4 |
| Content | content-strategist | 5 |
| Marketing | head-of-growth | 6 |
| Business | product-manager | 6 |

Every request enters through the **chief-of-staff**, which picks one of 10 team leads; each lead picks a specialist. Work moves between agents as documents with required sections (`contracts/`), and actions are tiered:

| Tier | Meaning |
| --- | --- |
| 0 | Read-only |
| 1 | Writes drafts |
| 2 | Changes internal systems (branches, staging) |
| 3 | Waits for human approval (publishing, sending, spending, production) |
| 4 | Human only; the agent prepares, a person acts (payments, signing, legal) |

All agents are currently `draft`. An agent becomes `verified` after it passes 10+ eval tasks; the eval runner (free local models first) is next on the roadmap.

## Layout

```text
agents/<team>/team.yaml            # lead, members, routing
agents/<team>/<agent>/agent.md     # the agent: YAML frontmatter + instructions
agents/<team>/<agent>/evals/       # test tasks and fixtures
skills/<skill>/SKILL.md            # reusable procedures (Agent Skills open standard)
contracts/<name>.yaml              # required sections for handoff documents
capabilities.yaml                  # capability -> each tool's tool names
models.yaml                        # tier -> model per provider
schema/agent.schema.yaml           # allowed frontmatter fields
scripts/lint.py                    # validates everything
scripts/convert.py                 # builds files for each AI tool into dist/
scripts/roster.py                  # regenerates ROSTER.md
```

## Quick start

```bash
pip install -r requirements.txt
python scripts/lint.py          # validate all agents, teams, skills, contracts
python scripts/convert.py       # generate dist/<tool>/ for every target
```

Copy the folder for your tool from `dist/` into your project (for example `dist/claude-code/.claude` into your repo root).

## Targets

| Tool | Output | Status |
| --- | --- | --- |
| Claude Code | `.claude/agents/*.md`, `.claude/skills/` | Format known |
| Cursor | `.cursor/agents/*.md`, `.agents/skills/` | Verify against current Cursor docs |
| Gemini CLI | `.gemini/agents/*.md`, `.agents/skills/` | Verify against current Gemini CLI docs |
| Codex | `.codex/agents/*.toml`, `.agents/skills/` | Field names unconfirmed; verify before release |

All tool-specific knowledge lives in `scripts/convert.py` and `capabilities.yaml`, so a format change is a one-file fix.

## Adding an agent

1. Copy `templates/agent.md` into `agents/<team>/<agent-name>/agent.md`.
2. Fill every section. The `description` must end with a `Not for:` line naming who to hand off to.
3. Add at least 3 tasks to `evals/tasks.yaml` (10+ before it can be `verified`).
4. Add the agent to its `team.yaml`.
5. Run `python scripts/lint.py`, then `python scripts/roster.py`.

## License

MIT
