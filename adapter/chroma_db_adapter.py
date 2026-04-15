import chromadb
from model.logseq import Block

class ChromaDBAdapter:
    collection: chromadb.Collection = None

    def __init__(self, collection_name: str, db_path: str):
        self.db = chromadb.PersistentClient(path=db_path)
        self.collection_name = collection_name
    
    def connect(self):
        try:
            self.collection = self.db.create_collection(self.collection_name)
        except Exception as e:
            print(f"Collection '{self.collection_name}' already exists. Using existing collection.")
            self.collection = self.db.get_collection(self.collection_name)
    
    def destroy(self):
        try:
            self.db.delete_collection(self.collection_name)
        except Exception as e:
            pass

    def upsert(self, blocks: list[Block]):
        params = self.add_params(blocks)
        self.collection.upsert(ids=params['ids'], documents=params['documents'])

    def query(self, query_string: str, limit: int = 10) -> list[Block]:
        results = self.collection.query(
            query_texts=[query_string],
            n_results=limit
        )

        blocks = []
        for i in range(len(results['ids'])):
            block = Block(
                uuid=results['ids'][0][i],
                content=results['documents'][0][i],
                match_value=results['distances'][0][i],
            )
            blocks.append(block)

        return blocks
    
    def add_params(self, blocks: list[Block]) -> dict:
        return {
            "ids": [block.uuid for block in blocks],
            "documents": [block.content for block in blocks],
        }