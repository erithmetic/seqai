from adapter.chroma_db_adapter import ChromaDBAdapter
from model.logseq import Block

class QueryService:
    def __init__(self, vector_db_adapter: ChromaDBAdapter):
        self.vector_db_adapter = vector_db_adapter

    def query(self, query: str, limit: int = 10) -> list[Block]:
        self.vector_db_adapter.connect()
        results = self.vector_db_adapter.query(query, limit)
        
        return results