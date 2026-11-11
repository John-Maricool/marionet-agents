---
name: llm-evals
description: How to build and run evaluations for prompts, LLM features and agents — test sets, graders, AI judges, repeated runs, and free-first model choice. Use when measuring AI quality or deciding if an agent is verified.
---

# LLM and agent evals

## Test sets
- 20-50 tasks to start; grow from real usage and every failure.
- Include easy, typical, hard and adversarial cases (tricks, missing info, prompt injection).
- Keep a held-back set that is never used for tuning.

## Graders (prefer the top)
1. **Code checks:** tests pass, required sections present, text contains or omits something, JSON valid.
2. **Rubric with an AI judge:** specific yes/no criteria; the judge must be a different model from the one tested.
3. **Human review:** spot-check about 10% of judged results to confirm the judge agrees.

Grade the outcome, not the exact steps taken.

## Runs
- Run each task 3 times; report pass rate and consistency.
- Record model, prompt or agent version, cost, tokens and time.
- Change one thing at a time.

## Free-first
- Local open-weight models via Ollama for most runs.
- Free API tiers for comparison; check their current limits.
- Paid models only with budget approval.

## In this library
- Tasks live in `agents/<team>/<agent>/evals/tasks.yaml`.
- Grader types: `contract`, `rubric`, `command`, `contains`, `not_contains`.
- An agent is `verified` with 10+ tasks passing at its `pass_mark`.
