from VectorDB.pinecone import Pinecone_db
from VectorDB.vector_store import VectorStore
from DataProcessing.cleaning import clean_folder
import os
from dotenv import load_dotenv

load_dotenv()

pinecone_api_key = os.getenv('PINECONE_API_KEY')
openai_api_key = None
google_api_key = os.getenv('GOOGLE_API_KEY')

pinecone_db = Pinecone_db(api_key=pinecone_api_key, openai_api_key=openai_api_key, google_api_key=google_api_key)

### Creating a new index
def create_new_index(index_name="temp-index"):
    pinecone_db.create_index(index_name=index_name)

### Deleting Index
def delete_index(index_name="temp-index"):
    pinecone_db.delete_index(index_name=index_name)

### Checking Data

def get_data(index_name="temp-index", query="All"):
    # Assignming Vector Store
    vs = pinecone_db.get_vector_store(index_name=index_name)
    vector_store = VectorStore(vs)
    output = vector_store.similarity_search(query=query)
    print(output)


###########################
# Run all that is necessary
###########################

# delete_index()
# create_new_index() 
# get_data()
#clean_folder("Data")





