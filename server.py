import os

from mcp.server.fastmcp import FastMCP

from adapter.chroma_db_adapter import ChromaDBAdapter
from agents.logseq_agent import LogseqAgent
from service.indexer_service import CHROMADB_PATH, COLLECTION_NAME

port = os.getenv("PORT", 8000)
server = FastMCP('Pydantic AI Server', log_level="INFO", port=int(port))
vector_db = ChromaDBAdapter(COLLECTION_NAME, CHROMADB_PATH)
agent = LogseqAgent.load(vector_db)

@server.tool()
async def query_logseq(search: str) -> str:
    r = await agent.run(search)
    return r.output