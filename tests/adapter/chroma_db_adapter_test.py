from adapter.logseq_semantic_search_adapter import LogseqSemanticSearchAdapter
from model.logseq import Block

SAMPLE_DB_PATH="../sample_logseq_db"

class TestChromaDBAdapter:
    def test_add_params(self):
        adapter = LogseqSemanticSearchAdapter("test_collection", SAMPLE_DB_PATH)
        blocks = [
            Block(uuid="1", content="This is the first block."),
            Block(uuid="2", content="This is the second block."),
            Block(uuid="3", content="This is the third block."),
        ]
        result = adapter.add_params(blocks)

        assert result == {
            "ids": ["1", "2", "3"],
            "documents": [
                "This is the first block.",
                "This is the second block.",
                "This is the third block."
            ],
        }
