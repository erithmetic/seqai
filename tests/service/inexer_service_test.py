import pytest

from service.query_service import QueryService

from tests.setup import reindex_sample_db, logseq_search_adapter_for_sample_db

class TestIndexerServiceIndex:
    """
    Feature: Index logseq blocks into ChromaDB
    """

    def test_index_all_blocks(self):
        reindex_sample_db()

        query_service = QueryService(logseq_search_adapter_for_sample_db())
        results = query_service.query("vector")

        assert len(results) > 0 
        assert len(str(results[0].content)) > 0
