import os

from mcp.server.fastmcp import FastMCP

from adapter.logseq_semantic_search_adapter import LogseqSemanticSearchAdapter
from agents.logseq_agent import LogseqAgent
from service.indexer_service import CHROMADB_PATH, COLLECTION_NAME

port = os.getenv("PORT", 8000)
server = FastMCP('Pydantic AI Server', port=int(port))
logseq_search = LogseqSemanticSearchAdapter(COLLECTION_NAME, CHROMADB_PATH)
agent = LogseqAgent.load(logseq_search)

@server.tool()
async def query_logseq(search: str) -> str:
    r = await agent.run(search)
    return r.output