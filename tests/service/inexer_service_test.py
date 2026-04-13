import os
import re
from transit.writer import Writer
import pytest

from adapter.chroma_db_adapter import ChromaDBAdapter
from adapter.logseq_db_adapter import LogseqDBAdapter
from service.indexer_service import COLLECTION_NAME, IndexerService

# path to sample logseq transit file located in project root
SAMPLE_DB_PATH = os.path.join(os.path.dirname(__file__), "../..", "sample_logseq_db")

class TestIndexerServiceIndex:
    """
    Feature: Index logseq blocks into ChromaDB
    """

    def test_index_all_blocks(self):
        logseq_adapter = LogseqDBAdapter(SAMPLE_DB_PATH)
        logseq_adapter.read_all()

        chroma_db_path = os.path.join(os.path.dirname(__file__), "../..", "db/test_chromadb")
        vector_db_adapter = ChromaDBAdapter(COLLECTION_NAME, chroma_db_path)
        vector_db_adapter.destroy()  # Ensure a clean slate for testing

        indexer = IndexerService(logseq_adapter, vector_db_adapter)
        indexer.index()

        results = vector_db_adapter.query("vector")
        print("Query results:", results)

        assert str(results['documents'][0][0]).find("vector") > 0


