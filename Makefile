.PHONY: cli server evals test install-dev

cli:
	uv run --env-file .env python main.py cli

server:
	uv run --env-file .env python main.py server

evals:
	uv run --env-file .env python evals/logseq_agent_evals.py

test:
	uv run pytest --tb=long
	
install-dev:
	uv sync --all-extras
