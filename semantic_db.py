import chromadb
from chromadb.config import Settings


class ChromaDBManager:
    """
    A class to manage writing operations to a filesystem-hosted ChromaDB instance.
    """

    def __init__(self, persist_directory: str):
        """
        Initialize the ChromaDB manager with a persistence directory.

        Args:
            persist_directory (str): Path to the directory where ChromaDB data will be stored.
        """
        self.persist_directory = persist_directory
        self.client = None

    def create_client(self):
        """
        Create and return a persistent ChromaDB client.
        """
        if self.client is None:
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
        return self.client

    def create_collection(self, name: str, metadata: dict = None):
        """
        Create a new collection in ChromaDB.

        Args:
            name (str): Name of the collection.
            metadata (dict, optional): Metadata for the collection.

        Returns:
            chromadb.Collection: The created collection.
        """
        client = self.create_client()
        collection = client.get_or_create_collection(name=name, metadata=metadata)
        return collection

    def add_documents(self, collection_name: str, documents: list[str], metadatas: list[dict] = None, ids: list[str] = None):
        """
        Add documents to a collection.

        Args:
            collection_name (str): Name of the collection.
            documents (list[str]): List of document texts.
            metadatas (list[dict], optional): List of metadata dictionaries for each document.
            ids (list[str], optional): List of unique IDs for each document. If None, auto-generated.
        """
        collection = self.create_collection(collection_name)
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def upsert_documents(self, collection_name: str, documents: list[str], metadatas: list[dict] = None, ids: list[str] = None):
        """
        Upsert documents to a collection (add or update).

        Args:
            collection_name (str): Name of the collection.
            documents (list[str]): List of document texts.
            metadatas (list[dict], optional): List of metadata dictionaries for each document.
            ids (list[str]): List of unique IDs for each document. Required for upsert.
        """
        if ids is None:
            raise ValueError("IDs are required for upsert operations.")
        collection = self.create_collection(collection_name)
        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def update_documents(self, collection_name: str, documents: list[str] = None, metadatas: list[dict] = None, ids: list[str] = None):
        """
        Update existing documents in a collection.

        Args:
            collection_name (str): Name of the collection.
            documents (list[str], optional): List of updated document texts.
            metadatas (list[dict], optional): List of updated metadata dictionaries.
            ids (list[str]): List of IDs of documents to update.
        """
        if ids is None:
            raise ValueError("IDs are required for update operations.")
        collection = self.create_collection(collection_name)
        collection.update(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def delete_documents(self, collection_name: str, ids: list[str] = None, where: dict = None, where_document: dict = None):
        """
        Delete documents from a collection.

        Args:
            collection_name (str): Name of the collection.
            ids (list[str], optional): List of IDs to delete.
            where (dict, optional): Metadata filter for deletion.
            where_document (dict, optional): Document filter for deletion.
        """
        collection = self.create_collection(collection_name)
        collection.delete(
            ids=ids,
            where=where,
            where_document=where_document
        )
