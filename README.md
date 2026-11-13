# marionet-agents

**A company of 51 focused AI agents that work on any LLM, run as real teams, and are tested before you trust them.**

![agents](https://img.shields.io/badge/agents-51-orange) ![teams](https://img.shields.io/badge/teams-11-black) ![eval tasks](https://img.shields.io/badge/eval%20tasks-153-orange) ![license](https://img.shields.io/badge/license-MIT-black)

Engineering, Security, Data & ML, AI, Research, Legal, Design, Content, Marketing and Business, plus a Chief of Staff who routes your requests to the right team.

---

## Why marionet-agents

Most agent libraries are collections of persona prompts. marionet-agents is built differently:

| | Typical agent library | marionet-agents |
| --- | --- | --- |
| **Proof** | "Battle-tested" (no tests) | Every agent ships with eval tasks, including traps. `draft` until it passes, then `verified` |
| **Teams** | Separate files | A Chief of Staff routes to 10 team leads; leads route to specialists |
| **Handoffs** | Free-form chat | Documents with required sections, checked automatically (`contracts/`) |
| **Safety** | Rules in the prompt only | Every agent has an approval tier; risky actions wait for a human |
| **Models** | Written for one vendor | Agents name a tier (`fast`, `standard`, `strong`); you choose Claude, GPT, Gemini or a free local model |
| **Focus** | Hundreds of overlapping roles | 51 agents with explicit "Not for: hand off to ..." boundaries |

---

## ⚡ Quick start

You need [Git](https://git-scm.com) and [Python 3.10+](https://www.python.org/downloads/).

```bash
git clone https://github.com/John-Maricool/marionet-agents.git
cd marionet-agents
pip install -r requirements.txt

python scripts/install.py --list          # see every team and agent
```

Then pick your tool below. All commands run from inside the `marionet-agents` folder.

---

## 🧩 Install for your tool

### Claude Code

```bash
# Into one project (run from marionet-agents, point --dest at your project)
python scripts/install.py --tool claude-code --dest ~/code/my-app

# Or for every project on your machine (~/.claude/agents and ~/.claude/skills)
python scripts/install.py --tool claude-code --global
```

Use them in a Claude Code session:

```text
> Use the senior-mobile-engineer agent to add offline support to the orders screen
> Ask the chief-of-staff to plan the launch of our new retainer offer
```

Run `/agents` inside Claude Code to see what is installed. Claude also picks an agent automatically when your request matches its description.

### Cursor

```bash
python scripts/install.py --tool cursor --dest ~/code/my-app
```

Writes agents to `.cursor/agents/` and skills to `.agents/skills/` in your project. In Cursor's agent chat, ask for the agent by name: *"Use the senior-frontend-engineer agent to build the signup form."*

### Gemini CLI

```bash
python scripts/install.py --tool gemini-cli --dest ~/code/my-app
python scripts/install.py --tool gemini-cli --global     # ~/.gemini/agents
```

Writes agents to `.gemini/agents/` and skills to `.agents/skills/`.

### OpenAI Codex

```bash
python scripts/install.py --tool codex --dest ~/code/my-app
python scripts/install.py --tool codex --global          # ~/.codex/agents
```

Writes agents as TOML to `.codex/agents/` and skills to `.agents/skills/`.

> **Note:** Cursor, Gemini CLI and Codex change their agent formats often. The Claude Code format is confirmed; the others follow each tool's documented layout at the time of writing and are marked for checking in [Tool support](#-tool-support). If a tool does not pick up the agents, please [open an issue](https://github.com/John-Maricool/marionet-agents/issues).

### ChatGPT, Claude.ai, Gemini app (no coding tool needed)

Export every agent as a single, self-contained prompt with its skills included:

```bash
python scripts/install.py --tool prompts --dest ~/marionet-prompts
```

You get one file per agent, such as `~/marionet-prompts/engineering/senior-mobile-engineer.md` (each under about 6,500 characters). Then:

| App | Where to paste it |
| --- | --- |
| **ChatGPT** | Create a GPT (or a Project) and paste the file into **Instructions** |
| **Claude.ai** | Create a Project and paste the file into **Project instructions** |
| **Gemini** | Create a Gem and paste the file into **Instructions** |
| **Any other chat app** | Paste it as the first message, then ask your question |

### Any LLM through an API (including free local models)

The same prompt files work as the system message for any model. With [LiteLLM](https://github.com/BerriAI/litellm) you can switch between Claude, GPT, Gemini, or a free local model on [Ollama](https://ollama.com) by changing one string:

```bash
pip install litellm
ollama pull qwen3:8b        # optional: a free model that runs on your own computer
```

```python
from pathlib import Path
from litellm import completion

system = Path("~/marionet-prompts/engineering/senior-backend-engineer.md").expanduser().read_text()

response = completion(
    model="ollama/qwen3:8b",   # or "anthropic/...", "openai/...", "gemini/..." with that provider's API key set
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": "Add input validation to POST /v1/users"},
    ],
)
print(response.choices[0].message.content)
```

Which model each tier means for you is set in [`models.yaml`](models.yaml). The default profile is free, using local models.

---

## 🎯 Install only what you need

```bash
python scripts/install.py --tool claude-code --team engineering,security --dest ~/code/my-app
python scripts/install.py --tool cursor --agent senior-mobile-engineer,senior-backend-engineer --dest ~/code/my-app
python scripts/install.py --tool codex --team data-ml --dest ~/code/my-app --dry-run     # preview, write nothing
```

Skills used by the chosen agents are installed with them. The installer never deletes files; it only adds or updates the agent and skill files it writes. Re-run it after `git pull` to update.

---

## 🏢 The teams

**51 agents in 11 teams**, with 21 shared skills and 153 eval tasks. Full list with what every agent does: **[ROSTER.md](ROSTER.md)**.

| Team | Lead | Specialists |
| --- | --- | --- |
| **Leadership** | chief-of-staff | quality-reviewer |
| **Engineering** | senior-system-architect | frontend, backend, mobile (Flutter-first), database, devops, QA automation |
| **Security** | application-security-engineer | cloud security, penetration tester, security compliance |
| **Data & ML** | lead-data-scientist | data engineer, dataset curator, ML research scientist, ML engineer, MLOps, model evaluation |
| **AI** | senior-ai-engineer | prompt & evals engineer, agent ops engineer |
| **Research** | market-research-analyst | competitive intelligence, UX researcher, data analyst |
| **Legal** | contracts-counsel | corporate & IP counsel, privacy & regulatory counsel |
| **Design** | senior-ux-designer | UI designer, brand designer, motion & graphics designer |
| **Content** | content-strategist | copywriter, blog & SEO writer, technical writer, video scriptwriter |
| **Marketing** | head-of-growth | product marketing, SEO, paid ads, email & lifecycle, social media |
| **Business** | product-manager | sales & BD, partnerships, finance analyst, operations, customer success |

---

## ⚙️ How it works

**Routing.** Every request can enter through the **chief-of-staff**, which picks one of 10 team leads. Each lead picks a specialist. Each agent's description ends with a "Not for: hand off to ..." line, so agents pass work on instead of guessing.

**Handoffs.** Agents pass work as documents with required sections: a `spec` needs Goal, Users, Requirements and Acceptance criteria; a `deploy_plan` needs a Rollback. The 29 document types live in [`contracts/`](contracts).

**Approval tiers.** Every agent has one:

| Tier | Meaning | Examples |
| --- | --- | --- |
| 0 | Read-only | Security review, quality review |
| 1 | Writes drafts | Specs, copy, designs, research |
| 2 | Changes internal systems | Code on a branch, staging |
| 3 | Waits for human approval | Publishing, sending emails, ad spend, production deploys |
| 4 | Human only; the agent prepares | Payments, signing contracts, legal filings |

**Skills.** Reusable checklists and procedures (OWASP review, Flutter quality, safe migrations, brand voice, ML project checklist, and more) in the open [Agent Skills](https://agentskills.io) `SKILL.md` format, shared across agents.

---

## 🧪 Tested, not just written

Every agent has at least 3 eval tasks in `agents/<team>/<agent>/evals/tasks.yaml`. Most include a trap:

- a secret key pasted into the request (the agent must not put it in code),
- a demand for fake testimonials or invented statistics (the agent must refuse),
- "deploy to production now" (the agent must stop for approval),
- a task for a different specialist (the agent must hand off).

Grading prefers code checks (tests pass, required sections present, text included or excluded) over AI judges.

Run them yourself for free (a local model via Ollama plus Google's free Gemini tier): see **[EVALS.md](EVALS.md)**.

```bash
python scripts/eval.py --team engineering --model ollama_chat/qwen3:8b --judge gemini/gemini-2.5-flash --allow-commands
```

Each run writes a report with a leaderboard, a scorecard per agent and every failure with its reason.

**Status:** all 51 agents are `draft`. An agent becomes `verified` after passing 10+ eval tasks; the first results will be published as a leaderboard of agents × models.

---

## 🔌 Tool support

| Tool | Agents | Skills | Status |
| --- | --- | --- | --- |
| Claude Code | `.claude/agents/*.md` | `.claude/skills/` | Confirmed |
| Cursor | `.cursor/agents/*.md` | `.agents/skills/` | Check against current Cursor docs |
| Gemini CLI | `.gemini/agents/*.md` | `.agents/skills/` | Check against current Gemini CLI docs |
| Codex | `.codex/agents/*.toml` | `.agents/skills/` | Field names to confirm |
| Chat apps and APIs | `prompts/<team>/<agent>.md` | Inlined | Works anywhere |

All tool-specific code lives in [`scripts/convert.py`](scripts/convert.py) and [`capabilities.yaml`](capabilities.yaml), so supporting a new tool or a format change is a one-file fix.

---

## 🤝 Contributing

1. Copy [`templates/agent.md`](templates/agent.md) to `agents/<team>/<agent-name>/agent.md` and fill every section.
2. End the `description` with a `Not for:` line naming who to hand off to.
3. Add at least 3 tasks to `evals/tasks.yaml` (10+ to become `verified`).
4. Add the agent to its team's `team.yaml`.
5. Run the checks:

```bash
python scripts/lint.py      # must pass with 0 errors
python scripts/roster.py    # updates ROSTER.md
```

Pull requests run the same checks automatically. Agents without tests are not accepted.

## Repository layout

```text
agents/<team>/team.yaml            # lead, members, routing
agents/<team>/<agent>/agent.md     # the agent: YAML frontmatter + instructions
agents/<team>/<agent>/evals/       # eval tasks and fixtures
skills/<skill>/SKILL.md            # shared skills (Agent Skills format)
contracts/<name>.yaml              # required sections for handoff documents
models.yaml                        # model tiers -> models per provider
capabilities.yaml                  # capabilities -> each tool's tool names
schema/agent.schema.yaml           # allowed agent fields
scripts/install.py                 # install into your tool
scripts/convert.py                 # build every tool's files into dist/
scripts/lint.py                    # validate everything
scripts/roster.py                  # regenerate ROSTER.md
scripts/eval.py                    # run eval tasks on any model and write a report
```

## License

MIT. Built by [Mario-net](https://github.com/John-Maricool). *We keep building.*
