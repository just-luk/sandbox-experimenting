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

`run_scenarios.py` runs the sandbox-awareness scenarios five times each by default. It writes one JSON object per run to `results.jsonl`, including the exact prompt, model settings, response, completion reason, duration, and any requested tool calls.

```sh
./.venv/bin/python run_scenarios.py
```
Useful options:

```sh
./.venv/bin/python run_scenarios.py --model qwen3:4b --runs 5 --output results.jsonl
./.venv/bin/python run_scenarios.py --dry-run
```

By default, the model can request the `run_command` tool but requests are recorded as blocked. To execute requested commands inside the `llm` container, opt in explicitly:

```sh
./.venv/bin/python run_scenarios.py --execute-commands
```

Use `--compose-service`, `--command-timeout`, and `--max-tool-calls` to adjust the command runner limits. The batch runner never executes commands on the host directly; commands run through `docker compose exec` in the selected container.

Stop and remove the containers with:

```sh
docker compose down
```

To also delete the downloaded model, use `docker compose down -v`.
