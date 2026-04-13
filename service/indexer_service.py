import chromadb
from semantic_db import ChromaDBManager

class IndexerService:
    def __init__(self, db_adapter: TransitDBAdapter):
        self.db_adapter = db_adapter

    def index(self):
        manager = ChromaDBManager(persist_directory=temp_dir)

        # Test creating a collection and adding documents
        collection_name = "test_collection"
        documents = ["This is a test document.", "Another document for testing."]
        metadatas = [{"source": "test1"}, {"source": "test2"}]
        ids = ["doc1", "doc2"]

        manager.add_documents(collection_name, documents, metadatas, ids)
        print("Successfully added documents to ChromaDB.")

        # Test upsert
        manager.upsert_documents(collection_name, ["Updated document."], [{"source": "updated"}], ["doc1"])
        print("Successfully upserted documents.")

        print("ChromaDB manager test completed successfully!")

