"""Class to intract including add and return from vector store"""
from langchain_text_splitters import TokenTextSplitter
import logging

class TextSplitter:
    """
    A class for splitting text and documents into smaller chunks based on specified chunk size and overlap.

    Attributes:
        chunk_size: The size of each chunk in terms of tokens.
        chunk_overlap: The number of tokens that overlap between chunks.
        text_splitter: An instance of TokenTextSplitter that performs the actual splitting.
    """

    def __init__(self, chunk_size=1000, chunk_overlap=0):
        """
        Initializes the TextSplitter with the given chunk size and overlap.

        Args:
            chunk_size: The number of tokens per chunk (default is 1000).
            chunk_overlap: The number of overlapping tokens between chunks (default is 0).
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = TokenTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

        # Logging
        logging.info("Text Splitter Initiated")
    
    def split_text(self, text):
        """
        Splits the given text into chunks.

        Args:
            text: The text to be split.

        Returns:
            A list of text chunks.
        """
        return self.text_splitter.split_text(text)

    def split_documents(self, documents):
        """
        Splits a list of documents into chunks.

        Args:
            documents: A list of documents to be split.

        Returns:
            A list of documents, each split into smaller chunks.
        """
        return self.text_splitter.split_documents(documents)

    async def atransform_documents(self, documents):
        """
        Asynchronously transforms (splits) a list of documents into chunks.

        Args:
            documents: A list of documents to be asynchronously split.

        Returns:
            A list of documents, each split into smaller chunks.
        """
        return await self.text_splitter.atransform_documents(documents)
    

class VectorStore:
    """
    A wrapper class for a vector store, providing synchronous and asynchronous methods
    for adding documents and performing similarity searches.

    Attributes:
        vector_store: An instance of the underlying vector store.
    """

    def __init__(self, vector_store):
        """
        Initializes the VectorStore with the given vector store instance.

        Args:
            vector_store: The underlying vector store instance.
        """
        self.vector_store = vector_store

        # Logging
        logging.info("Vector Store Initiated")

    def add_documents(self, documents):
        """
        Adds documents to the vector store.

        Args:
            documents: A list of documents to be added to the vector store.
        """
        self.vector_store.add_documents(documents)

        # Logging
        logging.info("Documents added in vector store")

    async def aadd_documents(self, documents):
        """
        Asynchronously adds documents to the vector store.

        Args:
            documents: A list of documents to be added to the vector store.
        """
        await self.vector_store.aadd_documents(documents)

        # Logging
        logging.info("Documents added in vector store")

    def similarity_search(self, query, k=5, filter=None):
        """
        Performs a similarity search on the vector store.

        Args:
            query: The query to search for.
            k: The number of top results to return (default is 5).
            filter: An optional filter to apply to the search.

        Returns:
            A list of tuples containing the search results and their similarity scores.
        """
        return self.vector_store.similarity_search_with_score(query, k=k, filter=filter)

    async def asimilarity_search(self, query, k=5, filter=None):
        """
        Asynchronously performs a similarity search on the vector store.

        Args:
            query: The query to search for.
            k: The number of top results to return (default is 5).
            filter: An optional filter to apply to the search.

        Returns:
            A list of tuples containing the search results and their similarity scores.
        """
        return await self.vector_store.asimilarity_search_with_score(query, k=k, filter=filter)