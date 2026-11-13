# Running the evals

The eval runner gives each agent its test tasks, sends them to an LLM, marks the answers, and writes a report. Everything below is free: one model runs on your own computer, the other uses Google's free Gemini tier.

## How marking works

| Check | Who marks it | Rule |
| --- | --- | --- |
| Required sections, must include, must not include | Code | Must all pass |
| Tests (for coding tasks) | Code runs the tests, including hidden tests the agent never sees | Must pass |
| Checklist items like "refused politely and explained why" | A second LLM (the examiner) | At least 80% of items |

Each task runs 3 times per model. A task **passes** when most runs pass. **Reliable** means it passed every run.

The examiner must be a different model from the one being tested, so we swap them: Gemini marks the local model's answers, and the local model marks Gemini's.

---

## One-time setup (Mac)

### 1. Install Ollama and a free local model

Download Ollama from [ollama.com](https://ollama.com) (or `brew install ollama`) and open it. Then in Terminal:

```bash
ollama pull qwen3:8b      # about 5 GB; fits comfortably in 16 GB of memory
```

### 2. Set up Python for the evals

```bash
cd marionet-agents
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-evals.txt
```

Run `source .venv/bin/activate` again whenever you open a new Terminal window.

### 3. Add your Gemini key (privately)

Create a free key at [Google AI Studio](https://aistudio.google.com/apikey). Then, in Terminal:

```bash
export GEMINI_API_KEY="paste-your-key-here"
```

To keep it for future Terminal windows, add that line to `~/.zshrc`. **Never** put the key in a file inside this repo or paste it in a chat. If it has been shared, delete it in AI Studio and create a new one.

### 4. Find the Gemini model name

```bash
python scripts/eval.py --list-models gemini
```

Pick a **Flash** model from the list (for example `gemini/gemini-2.5-flash`, or whatever newer Flash version appears). Use that exact name in the commands below. Free-tier limits change; check them in AI Studio.

---

## Run the evals

### Start small (about 5 minutes)

One agent, one run per task, to check everything works:

```bash
python scripts/eval.py --agent senior-backend-engineer \
  --model ollama_chat/qwen3:8b --judge gemini/gemini-2.5-flash \
  --runs 1 --allow-commands
```

### The engineering team, local model (roughly 30-60 minutes)

```bash
python scripts/eval.py --team engineering \
  --model ollama_chat/qwen3:8b --judge gemini/gemini-2.5-flash \
  --allow-commands --sleep 2
```

### The engineering team, Gemini (graded by the local model)

```bash
python scripts/eval.py --team engineering \
  --model gemini/gemini-2.5-flash --judge ollama_chat/qwen3:8b \
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

- **Speed:** Qwen3 "thinks" before answering, which makes it slower. The runner removes the thinking from answers before marking.
- **Bigger local model:** `ollama pull qwen3:14b` gives better answers but needs most of 16 GB of memory. Close other apps first.
- **Adding tasks:** every real failure you see while using an agent should become a new task in its `evals/tasks.yaml`. An agent needs 10+ passing tasks to become `verified`.
