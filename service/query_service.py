from adapter.logseq_semantic_search_adapter import LogseqSemanticSearchAdapter
from model.logseq import Block

class QueryService:
    def __init__(self, logseq_search_adapter: LogseqSemanticSearchAdapter):
        self.logseq_search_adapter = logseq_search_adapter

    def query(self, query: str, limit: int = 10) -> list[Block]:
        self.logseq_search_adapter.connect()
        results = self.logseq_search_adapter.query(query, limit)
        
        return results