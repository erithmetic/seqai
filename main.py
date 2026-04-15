import argparse

from mcp.server.fastmcp import FastMCP
from pydantic_ai import Agent
import logfire

from adapter.chroma_db_adapter import ChromaDBAdapter
from adapter.logseq_db_adapter import LogseqDBAdapter
from agents.logseq_agent import LogseqAgent
from service.indexer_service import CHROMADB_PATH, COLLECTION_NAME, IndexerService
from service.query_service import QueryService

class CommandHandler:
    def __init__(self, path):
        self.logseq_db = LogseqDBAdapter.from_journal_path(path)
        self.vector_db = ChromaDBAdapter(COLLECTION_NAME, CHROMADB_PATH)
        self.indexer = IndexerService(self.logseq_db, self.vector_db)

    def configure_otel(self):
        logfire.configure(send_to_logfire=False)  
        logfire.instrument_pydantic_ai()
        logfire.instrument_httpx(capture_all=True)

    def reindex(self):
        self.indexer.vector_db_adapter.destroy()
        self.indexer.index()

    def cli(self):
        self.configure_otel()
        LogseqAgent.load().to_cli_sync()

    def semantic_search(self):
        self.configure_otel()
        query_service = QueryService(self.vector_db)

        while True:
            query = input("Enter your search query (or 'exit' to quit): ")
            if query.lower() == 'exit':
                break
            blocks = query_service.query(query, limit=10)
            print(f"Found {len(blocks)} results:")
            for block in blocks:
                print(f"- {block.content} (URL: {block.url()})")

    def start(self):
        self.configure_otel()

        print("Starting SeqAI Pydantic MCP server...")
        self.vector_db.connect()

        server = FastMCP('Logseq MCP Server')
        server.run()

def main():
    parser = argparse.ArgumentParser(
        prog="seqai",
        description="Make your logseq notes searchable with AI")
    parser.add_argument("-p", "--path", default="/Users/erica/notes", help="Specify the path to your logseq journal directory (e.g., '/Users/erica/notes')")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("cli")
    subparsers.add_parser("server")
    subparsers.add_parser("reindex")
    subparsers.add_parser("semantic-search")
    args = parser.parse_args()

    command_handler = CommandHandler(args.path)

    if args.command == "reindex":
        command_handler.reindex()
    elif args.command == "cli":
        command_handler.cli()
    elif args.command == "server":
        command_handler.start()
    elif args.command == "semantic-search":
        command_handler.semantic_search()

if __name__ == "__main__":
    main()
