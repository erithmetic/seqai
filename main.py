import argparse
import os

from mcp.server.fastmcp import FastMCP
from pydantic_ai import Agent

from adapter.chroma_db_adapter import ChromaDBAdapter
from adapter.logseq_db_adapter import LogseqDBAdapter
from agents.logseq_agent import LogseqAgent
from server import server
from service.configure_otel_service import ConfigureOTELService
from service.indexer_service import CHROMADB_PATH, COLLECTION_NAME, IndexerService
from service.query_service import QueryService

from tests.setup import reindex_sample_db, vector_db_adapter_for_sample_db

SAMPLE_DB_PATH = "db/test_chromadb"

class CommandHandler:
    def __init__(self, path):
        self.logseq_db = LogseqDBAdapter.from_journal_path(path)
        self.vector_db = ChromaDBAdapter(COLLECTION_NAME, CHROMADB_PATH)
        self.indexer = IndexerService(self.logseq_db, self.vector_db)

    def configure_otel(self):
        ConfigureOTELService().run()

    def reindex(self):
        print("Reindexing logseq notes, this may take a while...")
        self.indexer.vector_db_adapter.destroy()
        self.indexer.index()

    def cli(self):
        self.configure_otel()
        LogseqAgent.load(self.vector_db).to_cli_sync()

    def semantic_search(self, test_mode: bool = False):
        self.configure_otel()

        self.vector_db = self.vector_db
        if test_mode:
            reindex_sample_db()
            self.vector_db = vector_db_adapter_for_sample_db()

        query_service = QueryService(self.vector_db)

        while True:
            # exit when user types exit or CTRL-D
            try:
                query = input("Enter your search query (or 'exit' to quit): ")
            except EOFError:
                break
            if query.lower() == 'exit' or query == '':
                break
            blocks = query_service.query(query, limit=10)
            print(f"Found {len(blocks)} results:")
            for block in blocks:
                print(f"- {block.match_value:.2f} {block.content} (URL: {block.url()})")
    
    def start(self):
        print(f"Starting SeqAI Pydantic MCP server...")
        self.configure_otel()
        self.vector_db.connect()
        server.run('streamable-http')


def main():
    parser = argparse.ArgumentParser(
        prog="seqai",
        description="Make your logseq notes searchable with AI")

    home = os.getenv("HOME")
    parser.add_argument("-p", "--path",
                        default=f"{home}/notes",
                        help="Specify the path to your logseq journal directory")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("cli")
    subparsers.add_parser("server")
    subparsers.add_parser("reindex")
    search = subparsers.add_parser("semantic-search")
    search.add_argument("--test", action="store_true", help="Run in test mode with sample data")
    args = parser.parse_args()

    command_handler = CommandHandler(args.path)

    if args.command == "reindex":
        command_handler.reindex()
    elif args.command == "cli":
        command_handler.cli()
    elif args.command == "server":
        command_handler.start()
    elif args.command == "semantic-search":
        command_handler.semantic_search(args.test)

if __name__ == "__main__":
    main()
