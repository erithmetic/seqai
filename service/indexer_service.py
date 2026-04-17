import os

from httpx import put
from adapter.logseq_semantic_search_adapter import LogseqSemanticSearchAdapter
from adapter.logseq_db_adapter import LogseqDBAdapter

CHROMADB_PATH = os.path.join(os.path.dirname(__file__), "../..", "db/chromadb")
COLLECTION_NAME = "logseq"

class IndexerService:
    def __init__(self, db_adapter: LogseqDBAdapter, logseq_search_adapter: LogseqSemanticSearchAdapter):
        self.db_adapter = db_adapter
        self.logseq_search_adapter = logseq_search_adapter

    def index(self):
        self.db_adapter.read_all()
        self.logseq_search_adapter.connect()

        blocks = [block for block in self.db_adapter.all_blocks() if block.content != None and len(str(block.content)) > 0]
        self.logseq_search_adapter.upsert(blocks)
