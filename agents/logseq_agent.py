from pydantic import BaseModel, Field
from pydantic_ai import Agent

from adapter.chroma_db_adapter import ChromaDBAdapter
from model.logseq import Block
from service.indexer_service import CHROMADB_PATH, COLLECTION_NAME

logseq_agent = Agent(  
  'anthropic:claude-sonnet-4-5',
)

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
    
@logseq_agent.tool
async def query_logseq(self, request: QueryRequest) -> QueryResult:
    vector_db_adapter = ChromaDBAdapter(COLLECTION_NAME, CHROMADB_PATH)
    results = vector_db_adapter.query(request.query, request.limit)
    blocks = [QueryResultBlock(uuid=block.uuid, content=block.content) for block in results]
        
    return QueryResult(
        count=len(blocks),
        blocks=blocks
    )
