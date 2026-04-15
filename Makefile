.PHONY: cli server evals test install-dev search

cli:
	uv run --env-file .env python main.py cli

server:
	uv run --env-file .env python main.py server

evals:
	uv run --env-file .env python evals/logseq_agent_evals.py

reindex:
	uv run --env-file .env python main.py reindex

search:
	uv run --env-file .env python main.py semantic-search

test:
	uv run pytest --tb=long
	
install-dev:
	uv sync --all-extras
