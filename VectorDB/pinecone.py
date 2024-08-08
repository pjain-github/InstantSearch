"""Pinecone Vector Database"""

# Pinecone Lib
from pinecone import Pinecone, ServerlessSpec

# Langchain
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import logging

class Pinecone_db:
    """
    A class for managing Pinecone indexes and embedding models for vector storage and similarity searches.

    Attributes:
        pc: The Pinecone instance.
        pc_key: The Pinecone API key.
        embedding_model: The embedding model instance used for generating embeddings.
    """

    #def __init__(self, api_key, embedding_model="google_genai", openai_api_key=None, google_api_key=None):
    def __init__(self, api_key, openai_api_key=None, google_api_key=None):
        """
        Initializes the Pinecone_db with the given API key and embedding model.

        Args:
            api_key: The API key for Pinecone.
            openai_api_key: The API key for OpenAI (if using OpenAI embeddings).
            google_api_key: The API key for Google Generative AI (if using Google GenAI embeddings).
        """
        # Pinecone
        self.pc = Pinecone(api_key=api_key)
        self.pc_key = api_key

        # Embedding Model
        if openai_api_key:
            self.embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

            #Logging
            logging.info("OpenAI Embedding model initiated in Pinecone DB")

        elif google_api_key:
            self.embedding_model = GoogleGenerativeAIEmbeddings(google_api_key=google_api_key, model="models/text-embedding-004")

            #Logging
            logging.info("Google Embedding model initiated in Pinecone DB")

        else:
            raise ValueError("Invalid embedding model")

    def create_index(self, index_name='temp-index', metric="cosine", spec=None):
        """
        Creates a Pinecone index with the given specifications.

        Args:
            index_name: The name of the index to create (default is 'temp-index').
            metric: The similarity metric to use (default is "cosine").
            spec: The serverless specification for the index (default is None).

        Returns:
            The name of the created index.
        """
        if spec is None:
            spec = ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )

        if index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=index_name,
                dimension=768,
                metric=metric,
                spec=spec)
            
            #Logging
            logging.info(f"New index crated in pinecone with name {index_name}")
            return index_name
        else:
            self.pc.delete_index(index_name)
            logging.info(f"Alrady had index on name {index_name}, so deleted index in pinecone with name {index_name}")

            self.pc.create_index(
                name=index_name,
                dimension=768,
                metric=metric,
                spec=spec)
            
            #Logging
            logging.info(f"New index crated in pinecone with name {index_name}")

            return index_name

    def get_vector_store(self, index_name):
        """
        Retrieves a Pinecone vector store for the specified index.

        Args:
            index_name: The name of the index to retrieve the vector store for.

        Returns:
            An instance of PineconeVectorStore.
        """
        return PineconeVectorStore(index_name=index_name, embedding=self.embedding_model, pinecone_api_key=self.pc_key)

    def delete_index(self, index_name):
        """
        Deletes the specified Pinecone index.

        Args:
            index_name: The name of the index to delete.
        """
        self.pc.delete_index(index_name)

        #Logging
        logging.info(f"Index deleted in pinecone with name {index_name}")

    def reset_index(self, index_name):
        """
        Reset the specified Pinecone index.

        Args:
            index_name: The name of the index to delete.
        """
        self.delete_index(index_name)
        self.create_index(index_name = index_name)
