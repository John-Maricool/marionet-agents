# AGENTS.md

Always-on context for any AI tool working in this repo.

## What this repo is

A library of agent definitions. The source of truth is `agents/`, `skills/`, `contracts/`, `models.yaml` and `capabilities.yaml`. Everything in `dist/` is generated; never edit it by hand.

## Rules

- Run `python scripts/lint.py` after any change to agents, teams, skills or contracts.
- Never add a frontmatter field that is not in `schema/agent.schema.yaml`.
- Name tools by capability (`read_files`, `web_search`), never by one tool's command name.
- Name models by tier (`fast`, `standard`, `strong`), never by vendor model name.
- Every agent description ends with `Not for: ... (hand off to <agent>)`.
- An agent may only be marked `verified` after it passes its evals.
