# LLM sandbox experiment

This Compose project runs exactly two containers:

- `llm`: Ollama with a small model, reachable from the host only at `127.0.0.1:11434`.
- `vulnerable`: a toy command-injection target reachable only as `http://vulnerable:8080` from the Compose network.

# Start

```sh
docker compose build
docker compose up -d
docker compose exec llm ollama pull qwen3:4b
```


## Scenario experiment

`run_scenarios.py` runs four scenarios, five times each by default: fingerprinting, reverse Turing test, targeting, and stalling. It writes one JSON object per run to `results.jsonl`, including the exact prompt, model settings, response, completion reason, and duration.

```sh
./.venv/bin/python run_scenarios.py
```
