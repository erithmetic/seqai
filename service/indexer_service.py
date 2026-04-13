import os
from adapter.chroma_db_adapter import ChromaDBAdapter
from adapter.logseq_db_adapter import LogseqDBAdapter

CHROMADB_PATH = os.path.join(os.path.dirname(__file__), "../..", "db/chromadb")
COLLECTION_NAME = "logseq"

class IndexerService:
    def __init__(self, db_adapter: LogseqDBAdapter, vector_db_adapter: ChromaDBAdapter):
        self.db_adapter = db_adapter
        self.vector_db_adapter = vector_db_adapter

    def index(self):
        self.db_adapter.read_all()
        self.vector_db_adapter.connect()

        for _, block in self.db_adapter.db.items():
            self.vector_db_adapter.upsert(block)
