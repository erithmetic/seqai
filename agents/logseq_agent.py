from pydantic import BaseModel, Field
from pydantic_ai import Agent

from adapter.logseq_semantic_search_adapter import LogseqSemanticSearchAdapter
from model.logseq import Block
from service.indexer_service import CHROMADB_PATH, COLLECTION_NAME
from service.query_service import QueryService

INSTRUCTIONS = '''
You are a reporter who searches and summarizes a user's logseq notes.
Always include the content and source URLs in your response.
If you cannot find the answer in the notes, say you don't know instead of making something up.
Do not add any extra information to the search results.
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
    def load(logseq_search_adapter: LogseqSemanticSearchAdapter) -> Agent:
        me = LogseqAgent(logseq_search_adapter)
        return Agent(
            'anthropic:claude-haiku-4-5',
            instructions=INSTRUCTIONS,
            instrument=True,
            tools=[me.query_logseq],
            history_processors=[]
        )

    def __init__(self, logseq_search_adapter: LogseqSemanticSearchAdapter):
        self.query_service = QueryService(logseq_search_adapter)

    def query_logseq(self, request: QueryRequest) -> QueryRequest:
        blocks = self.query_service.query(request.query, request.limit)
        result_blocks = [
            QueryResultBlock(uuid=block.uuid, content=block.content, url=block.url()) for block in blocks
        ]

        return QueryResult(
            count=len(result_blocks),
            blocks=result_blocks
        )
