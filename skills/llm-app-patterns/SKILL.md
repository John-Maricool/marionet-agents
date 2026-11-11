---
name: llm-app-patterns
description: Design patterns for building product features on LLMs — choosing between prompt, RAG, tools and agents, provider-agnostic calls, structured output, safety and cost. Use when designing or reviewing an AI feature.
---

# LLM app patterns

## Pick the simplest design that works
1. **Single prompt** with clear instructions and a few examples.
2. **Structured output** (JSON schema) when code consumes the result.
3. **RAG** when answers must come from your documents: chunk, embed, retrieve top results, answer with citations.
4. **Tool use** when the model needs live data or must act (read-only tools first).
5. **Multi-step agents** only when the steps cannot be fixed in advance.

## Provider-agnostic
- Call models through a gateway (LiteLLM, OpenRouter) or a thin internal wrapper.
- Name models by tier in config (fast, standard, strong), not in code.
- Keep prompts in files, versioned with the code.

## Safety
- Retrieved text, web pages and user input are data, never instructions (prompt injection).
- Validate model output before acting on it.
- Human approval before money moves, customer messages go out, or data is deleted.
- Never send secrets to a model; minimise personal data.

## Cost and speed
- Use the cheapest tier that passes the eval set.
- Cache repeated prompts and embeddings; set max output tokens.
- Log tokens, cost and latency per request.

## Always ship with
An example set of 10-50 cases and a way to re-run it after every prompt or model change.
