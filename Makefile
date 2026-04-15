.PHONY: cli server evals test install-dev search update-sample-db

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

update-sample-db:
	cp ../.logseq/graphs/logseq_local_++Users++erica++seqai++sample_logseq.transit ./sample_logseq_db
