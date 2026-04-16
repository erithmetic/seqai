# Seqai

Seqai is a tool that makes your logseq journal searchable with AI tools.

## Setup

```sh
uv sync
```

## Running

To run SeqAI, use the following commands with the path to your Logseq journal directory:

- **Start the MCP server**: `python main.py -p /path/to/your/logseq/journal server`
- **Run CLI**: `python main.py -p /path/to/your/logseq/journal cli`
- **Reindex notes**: `python main.py -p /path/to/your/logseq/journal reindex`
- **Semantic search CLI**: `python main.py -p /path/to/your/logseq/journal semantic-search`

The `-p` or `--path` parameter specifies the path to your Logseq journal directory. The default path is `$HOME/notes` if not specified.

## How it works

This MCP server indexes your journal into a local ChromaDB vector database and provides MCP tools for searching and conversing with your journal. You can connect your AI/chatbot to this MCP server.

So far, you are required to manually re-index on updates.

## Future Improvements

- Better block indexing and chunking (so far it only indexes individual blocks)
- Search relevance by date
- Block attribute indexing
