from pydantic import BaseModel, Field
from pydantic_ai import Agent

from adapter.chroma_db_adapter import ChromaDBAdapter
from model.logseq import Block
from service.indexer_service import CHROMADB_PATH, COLLECTION_NAME
from service.query_service import QueryService

class QueryRequest(BaseModel):
    """Request model for vector database queries"""
    query: str = Field(..., description="The query string to search for in logseq")
    limit: int = Field(10, description="Maximum number of results to return", ge=1, le=100)

class QueryResultBlock(BaseModel):
    uuid: str = Field(..., description="Unique identifier of the block")
    content: str = Field(..., description="Content of the block")

class QueryResult(BaseModel):
    count: int = Field(..., description="Number of results returned")
    blocks: list[QueryResultBlock] = Field(..., description="Matching blocks")

class Result:
    def __init__(self, count: int, blocks: list[Block]):
        self.count = count
        self.blocks = blocks

class LogseqAgent():
    def __init__(self, vector_db_adapter: ChromaDBAdapter):
        self.query_service = QueryService(vector_db_adapter)

    def query_logseq(self, query: str, limit: int = 10) -> Result:
        blocks = self.query_service.query(query, limit)
            
        return Result(
        count=len(blocks),
        blocks=blocks
    )

def query_logseq(query: str, limit: int = 10) -> Result:
    agent = LogseqAgent(ChromaDBAdapter(COLLECTION_NAME, CHROMADB_PATH))
    return agent.query_logseq(query, limit)

logseq_agent = Agent(  
    'anthropic:claude-sonnet-4-5',
    tools=[query_logseq],
)
