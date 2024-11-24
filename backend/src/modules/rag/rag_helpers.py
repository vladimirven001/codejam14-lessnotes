from langchain_chroma import Chroma
from typing import Optional
import os

from langchain_ollama import OllamaEmbeddings
import time

from langchain_unstructured import UnstructuredLoader

def vector_db(id):
    embeddings = OllamaEmbeddings(
        model="mxbai-embed-large",
    )
    vectorstore = Chroma(
        collection_name=f"user{id}",
        embedding_function=embeddings,
        persist_directory="./db/chroma_db",  
    )
    return vectorstore

def delete_documents_by_source(
    vector_store: Chroma,
    source_path: str,
    collection_name: Optional[str] = None
) -> None:
    """
    Delete all documents from a Chroma vector store that match a specific source path.
    
    Args:
        vector_store: The Chroma vector store instance
        source_path: The source path to match (e.g., "files/file1.pdf")
        collection_name: Optional name of the collection to use
    """
    # Get all documents with their metadata
    collection = vector_store._collection
    
    # Get all document IDs and their metadata
    docs = collection.get(
        include=['metadatas', 'ids']
    )
    
    if not docs or not docs['ids']:
        print("No documents found in the collection.")
        return
    
    # Find documents with matching source
    ids_to_delete = []
    for idx, metadata in enumerate(docs['metadatas']):
        if metadata and 'source' in metadata and metadata['source'] == source_path:
            ids_to_delete.append(docs['ids'][idx])
    
    # Delete the matching documents
    if ids_to_delete:
        collection.delete(ids_to_delete)
        print(f"Deleted {len(ids_to_delete)} documents from source: {source_path}")
    else:
        print(f"No documents found with source: {source_path}")


    
if __name__ == '__main__':
    # Add a file to the vector database
    vectorstore = vector_db(1)
    path = os.path.join(os.getcwd(), "files/1/data/messi.txt")
    print(path)
    # converth file to document
    loader = UnstructuredLoader([path])
    doc = loader.load()
    print(doc)
    vectorstore.add_documents(doc)

    time.sleep(2)
    collection = vectorstore._collection
    docs = collection.get(
        include=['metadatas', 'ids']
    )
    print(docs)
    time.sleep(2)

    delete_documents_by_source(vectorstore, "./files/1/data/messi.txt")
    