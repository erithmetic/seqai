from tests.setup import reindex_sample_db, logseq_search_adapter_for_sample_db

from agents.logseq_agent import LogseqAgent, QueryRequest


class TestLogseqAgentQueryLogseq:
    def test_returns_valid_results(self):
        reindex_sample_db()  # Ensure the sample DB is indexed before testing

        agent = LogseqAgent(logseq_search_adapter_for_sample_db())
        response = agent.query_logseq(QueryRequest(query="what is a vector?", limit=5))

        assert response.count > 0, "Expected at least one result from the query"
        assert len(response.blocks) > 0, "Expected at least one block in the results"
        for block in response.blocks:
            assert block.uuid is not None, "Expected block to have a UUID"
            assert block.content is not None, "Expected block to have content"
            assert block.url is not None, "Expected block to have a URL"