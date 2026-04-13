import argparse
import os

from adapter.chroma_db_adapter import ChromaDBAdapter
from adapter.logseq_db_adapter import LogseqDBAdapter
from service.indexer_service import CHROMADB_PATH, COLLECTION_NAME, IndexerService

class CommandHandler:
    def __init__(self, path):
        self.logseq_db = LogseqDBAdapter.from_journal_path(path)
        self.vector_db = ChromaDBAdapter(COLLECTION_NAME, CHROMODB_PATH)
        self.indexer = IndexerService(self.logseq_db, self.vector_db)

    def reindex(self):
        self.indexer.vector_db_adapter.destroy()
        self.indexer.index()

    def start(self):
        self.indexer.index()

def main():
    print("Hello, SeqAI!")

    parser = argparse.ArgumentParser(
        prog="seqai",
        description="Make your logseq notes searchable with AI")
    parser.add_argument("-i", "--index", action="store_true", help="Re-index the search database")
    parser.add_argument("-p", "--path", default="/Users/erica/notes", help="Specify the path to your logseq journal directory (e.g., '/Users/erica/notes')")
    args = parser.parse_args()

    command_handler = CommandHandler(args.path)

    if args.index:
        command_handler.reindex()
    else:
        command_handler.start()

if __name__ == "__main__":
    main()
