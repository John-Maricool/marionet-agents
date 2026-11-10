---
name: agent-name
description: >-
  What this agent does and when to use it, in one or two sentences.
  Not for: X (hand off to other-agent), Y (hand off to another-agent).
team: team-folder-name
role: member
version: 0.1.0
status: draft
model: standard
capabilities: [read_files]
skills: []
inputs: []
outputs: []
handoffs: []
approval_tier: 1
---

# Role

One paragraph: what this agent owns and the standard it works to. No backstory.

# Scope

In scope:
- ...

Not in scope (hand off):
- ... -> other-agent

# Inputs

What the agent needs before it starts, and what to do if it is missing.

# Workflow

1. ...
2. ...
3. Check the output against the task goal and the output contract before finishing.

# Output format

The exact document(s) produced, with required sections. Match the contract in `contracts/`.

# Done when

- ...

# Escalate when

- The input is missing or contradictory.
- The same step has failed twice.
- The action is at or above approval tier 3.

# Guardrails

- ...

# Examples

Short input -> output example, or a pointer to a fixture in evals/fixtures/.
