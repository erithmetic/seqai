from pydantic import BaseModel, Field
from pydantic_ai import Agent

from adapter.chroma_db_adapter import ChromaDBAdapter
from model.logseq import Block
from service.indexer_service import CHROMADB_PATH, COLLECTION_NAME
from service.query_service import QueryService

INSTRUCTIONS = '''
    You are a helpful assistant for querying a user's logseq notes.
    You have access to the query_logseq tool that allows you to search the user's notes and retrieve relevant information.
    The results include a URL to the source that should be included in your answer to the user.
    The URL is prefixed with "logseq://".
    Always include the source URL in your response.
    If you cannot find the answer in the notes, say you don't know instead of making something up.
'''

class QueryRequest(BaseModel):
    query: str = Field(..., description="The query string to search for in logseq")
    limit: int = Field(10, description="Maximum number of results to return", ge=1, le=100)

class QueryResultBlock(BaseModel):
    uuid: str = Field(..., description="Unique identifier of the block")
    url: str = Field(..., description="URL to the matching block in Logseq")
    content: str = Field(..., description="Notes content")

class QueryResult(BaseModel):
    count: int = Field(..., description="Number of results returned")
    blocks: list[QueryResultBlock] = Field(..., description="Matching notes")

class Result:
    def __init__(self, count: int, blocks: list[Block]):
        self.count = count
        self.blocks = blocks

class LogseqAgent():
    @staticmethod
    def load():
        me = LogseqAgent(ChromaDBAdapter(COLLECTION_NAME, CHROMADB_PATH))
        return Agent(
            'anthropic:claude-sonnet-4-5',
            instructions=INSTRUCTIONS,
            instrument=True,
            tools=[me.query_logseq]
        )

    def __init__(self, vector_db_adapter: ChromaDBAdapter):
        self.query_service = QueryService(vector_db_adapter)

    def query_logseq(self, request: QueryRequest) -> QueryRequest:
        blocks = self.query_service.query(request.query, request.limit)
        result_blocks = [
            QueryResultBlock(uuid=block.uuid, content=block.content, url=block.url()) for block in blocks
        ]

        return QueryResult(
            count=len(result_blocks),
            blocks=result_blocks
        )

