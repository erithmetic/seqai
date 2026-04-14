import os

from adapter.chroma_db_adapter import ChromaDBAdapter
from adapter.logseq_db_adapter import LogseqDBAdapter
from service.indexer_service import COLLECTION_NAME, IndexerService

# path to sample logseq transit file located in project root
SAMPLE_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "sample_logseq_db")

def vector_db_adapter_for_sample_db():
    chroma_db_path = os.path.join(os.path.dirname(__file__), "../..", "db/test_chromadb")
    return ChromaDBAdapter(COLLECTION_NAME, chroma_db_path)

def reindex_sample_db():
    logseq_adapter = LogseqDBAdapter(SAMPLE_DB_PATH)
    logseq_adapter.read_all()

    vector_db_adapter = vector_db_adapter_for_sample_db()
    vector_db_adapter.destroy()  # Ensure a clean slate for testing

    indexer = IndexerService(logseq_adapter, vector_db_adapter)
    indexer.index()