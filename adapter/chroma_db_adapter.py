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

    def upsert(self, block: Block):
        if block.content is not None:
            print(f"Upserting block with id: {block.uuid} and content: {block.content}")
            self.collection.upsert(documents=[block.content], ids=[block.uuid])

    def query(self, query_string: str):
        results = self.collection.query(
            query_texts=[query_string],
            n_results=10
        )
        return results