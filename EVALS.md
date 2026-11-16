# Running the evals

The eval runner gives each agent its test tasks, sends them to an LLM, marks the answers, and writes a report. Everything below is free: one model runs on your own computer, the other uses Google's free Gemini tier.

## How marking works

| Check | Who marks it | Rule |
| --- | --- | --- |
| Required sections, must include, must not include | Code | Must all pass |
| Tests (for coding tasks) | Code runs the tests, including hidden tests the agent never sees | Must pass |
| Checklist items like "refused politely and explained why" | A second LLM (the examiner) | At least 80% of items |

Each task runs 3 times per model. A task **passes** when most runs pass. **Reliable** means it passed every run.

The examiner must be a different model family from the one being tested (models mark their own answers too kindly).

**Recommended free setup:** Qwen3 (by Alibaba) answers, Gemma 3 (by Google) marks, both running on your Mac with no limits. Gemini's free tier is useful for spot-checks, but its daily quota runs out after a couple of dozen marks.

---

## One-time setup (Mac)

### 1. Install Ollama and a free local model

Download Ollama from [ollama.com](https://ollama.com) (or `brew install ollama`) and open it. Then in Terminal:

```bash
ollama pull qwen3:8b      # the model being tested, about 5 GB
ollama pull gemma3:12b    # the examiner, about 8 GB (use gemma3:4b if memory is tight)
```

### 2. Set up Python for the evals

```bash
cd marionet-agents
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-evals.txt
```

Run `source .venv/bin/activate` again whenever you open a new Terminal window.

### 3. Optional: add a Gemini key (privately)

Create a free key at [Google AI Studio](https://aistudio.google.com/apikey). Then, in Terminal:

```bash
export GEMINI_API_KEY="paste-your-key-here"
```

To keep it for future Terminal windows, add that line to `~/.zshrc`. **Never** put the key in a file inside this repo or paste it in a chat. If it has been shared, delete it in AI Studio and create a new one.

### 4. Optional: find the Gemini model name

```bash
python scripts/eval.py --list-models gemini
```

Pick a **Flash** model from the list (at the time of writing, `gemini/gemini-3.8-flash`). Use that exact name in the commands below. Google retires old models: if a run says a model is "no longer available", run this command again and use the newer Flash name it shows. Free-tier limits change; check them in AI Studio.

---

## Run the evals (recommended: answer first, mark second)

Running both local models at the same time makes them swap in and out of memory. It is faster to collect all the answers first, then mark them in one go.

**Step 1: collect answers** (no examiner; code checks still run). Takes 1-3 hours for the engineering team:

```bash
caffeinate -i python scripts/eval.py --team engineering \
  --model ollama_chat/qwen3:8b --allow-commands --no-think
```

**Step 2: mark them** with the local examiner (use the folder name printed at the end of step 1):

```bash
python scripts/eval.py --regrade results/2026-11-16_0113 \
  --judge ollama_chat/gemma3:12b --allow-commands
```

This writes a new folder ending in `_regraded_HHMM` with the full report.

### Re-marking (`--regrade`)

`--regrade` marks saved answers again without asking the model to answer again. Use it when:

- the examiner ran out of quota or failed (the report says **"⚠️ only X/Y runs graded"**),
- you want a second opinion from another examiner,
- a test was fixed, and you want old answers marked with the corrected test.

It does **not** pick up changes to an agent's instructions; for that, collect new answers.

## Other ways to run

### Start small (about 5 minutes)

One agent, one run per task, to check everything works:

```bash
python scripts/eval.py --agent senior-backend-engineer \
  --model ollama_chat/qwen3:8b --judge gemini/gemini-3.8-flash \
  --runs 1 --allow-commands
```

### The engineering team, local model (roughly 30-60 minutes)

```bash
python scripts/eval.py --team engineering \
  --model ollama_chat/qwen3:8b --judge gemini/gemini-3.8-flash \
  --allow-commands --sleep 2
```

### The engineering team, Gemini (graded by the local model)

```bash
python scripts/eval.py --team engineering \
  --model gemini/gemini-3.8-flash --judge ollama_chat/qwen3:8b \
  --allow-commands --sleep 5
```

`--sleep` adds a pause between calls so you stay inside free-tier rate limits. If you see rate-limit errors, raise it.

### Useful options

| Option | What it does |
| --- | --- |
| `--team engineering,security` | Test whole teams |
| `--agent senior-mobile-engineer` | Test one or more agents |
| `--task token-storage` | Test one task only |
| `--runs 1` | One run per task (faster, less reliable) |
| `--allow-commands` | Run the coding tasks' tests. It runs `pytest` on files the model wrote, inside a temporary folder. Use it only with this repo's tasks |
| `--model A --model B` | Test several models in one go (they share the same examiner) |
| `--regrade results/<folder>` | Mark saved answers again (no new answers) |
| `--no-think` | Tells Qwen3 to skip its long thinking phase. Much faster; answers may be a little weaker |

---

## Reading the results

Each run creates `results/<date-time>/` with:

| File | What it is |
| --- | --- |
| `report.md` | The report: leaderboard, a scorecard per agent, and every failure with the reason |
| `summary.json` | The same numbers for the leaderboard page |
| `raw.jsonl` | Every answer in full, for digging into failures |

The **Failures** section matters most. Each failure says which check failed and why, which tells you exactly what to fix in the agent.

`results/` is not committed to Git. Copy a report into an issue or pull request when you want to share it.

## Tips

- **Speed:** Qwen3 "thinks" before answering, which can take several minutes per answer on a laptop. Add `--no-think` to skip it. The runner removes any thinking from answers before marking.
- **Long runs:** the full engineering team with 3 runs can take 1-3 hours on a laptop. Put `caffeinate -i` in front of the command (for example `caffeinate -i python scripts/eval.py ...`) so your Mac does not sleep, and keep it plugged in.
- **One run is not enough:** small models can pass a task once and fail it the next time. Judge an agent on 3 runs.
- **Updating:** after `git pull`, run `pip install -r requirements-evals.txt` again in case new packages were added.
- **"Grading problems" in the report:** the examiner failed (for example a missing package or a rate limit). Those runs are not counted against the agent; fix the problem and re-run.
- **Bigger local model:** `ollama pull qwen3:14b` gives better answers but needs most of 16 GB of memory. Close other apps first.
- **Adding tasks:** every real failure you see while using an agent should become a new task in its `evals/tasks.yaml`. An agent needs 10+ passing tasks to become `verified`.
