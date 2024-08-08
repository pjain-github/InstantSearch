from VectorDB.pinecone import Pinecone_db
from VectorDB.vector_store import VectorStore
from VectorDB.vector_store import TextSplitter
from langchain_core.documents import Document
from DataProcessing.docx import WordReader
from DataProcessing.pdf import PDF_Reader
from DataProcessing.webscrapping import WebScrapper
import logging

class DataProcessing:

    def __init__(self, pinecone_api_key, index_name, openai_api_key=None, google_api_key=None):
        
        pinecone_db = Pinecone_db(api_key=pinecone_api_key, openai_api_key=openai_api_key, google_api_key=google_api_key)       
        pc = pinecone_db.get_vector_store(index_name)

        self.vs = VectorStore(pc)

        # Logging
        logging.info("Pinecone and Vector Store Initiated")

    def add_data(self, text, metadata):

        ts = TextSplitter(chunk_size=500, chunk_overlap=50)

        text_list = ts.split_text(text)

        docs = []

        for texts in text_list:
            docs.append(Document(page_content=texts, metadata=metadata))
            self.vs.add_documents([Document(page_content=texts, metadata=metadata)])

        #print(docs)

        #self.vs.add_documents(documents = docs)

class Extraction:
    def __init__(self):
        pass

    def extract_extractor(self, path):
        if ".pdf" in str(path):
            return PDF_Reader()
        elif ".docx" in str(path):
            return WordReader()
        elif "https:" in str(path):
            return WebScrapper()
        
    def extract_text(self, path):

        extractor = self.extract_extractor(path)

        text = extractor.get_text(path)

        return text
    



