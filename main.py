
from VectorDB.pinecone import Pinecone_db
from VectorDB.vector_store import VectorStore
from Answer.text_prep import prepare_text
from LLM.llm import Gemini, OpenAI
from Answer.answer import Answer
import logging
import os
from dotenv import load_dotenv

load_dotenv()


def streaming_instant_search(user_query, pinecone_api_key, sources=False, openai_api_key=None, google_api_key=None):
    try:
        # Initialize the Pinecone database and vector store
        logging.info("Initializing Pinecone database and vector store...")
        pinecone_db = Pinecone_db(api_key=pinecone_api_key, openai_api_key=openai_api_key, google_api_key=google_api_key)
        vector_store = VectorStore(pinecone_db.get_vector_store("temp-index"))
        logging.info("Successfully initialized Pinecone and vector store.")
        
    except Exception as e:
        logging.error(f"Unable to access vector store: {e}")
        yield "Sorry, unable to access the database. Please try again later."
        return

    try:
        # Retrieve similar documents
        logging.info(f"Performing similarity search for query: {user_query}")
        retrieved_documents = vector_store.similarity_search(query=user_query)
        logging.info(f"Retrieved {len(retrieved_documents)} documents.")
        
    except Exception as e:
        logging.error(f"Document retrieval failed: {e}")
        yield "Sorry, unable to retrieve documents. Please try again later."
        return

    try:
        # Prepare the text and sources for the answer
        logging.info("Preparing text and sources...")
        combined_text, combined_sources = prepare_text(chunks=retrieved_documents, token_limit=500, model="gpt2")
        logging.info("Text preparation successful.")
        
    except Exception as e:
        logging.error(f"Preparing text failed: {e}")
        yield "Sorry, unable to prepare the text. Please try again later."
        return

    try:
        # Choose the language model based on the available API key
        if openai_api_key:
            logging.info("Using OpenAI model for generating the response...")
            llm = OpenAI(api_key=openai_api_key, model="gpt-4o-mini")
        else:
            logging.info("Using Gemini model for generating the response...")
            llm = Gemini(api_key=google_api_key, model="gemini-pro")
        
    except Exception as e:
        logging.error(f"Model load failed: {e}")
        yield "Sorry, unable to load the model. Please check your API keys and try again."
        return

    try:
        # Create an answer generator and stream the response
        logging.info("Generating response...")
        answer_generator = Answer(llm)
        for chunk in answer_generator.stream_user_query(combined_text, user_query):
            yield chunk
            
        # if sources:
        #     yield "\nSources:\n" + "\n".join(combined_sources)
            
    except Exception as e:
        logging.error(f"Failed to generate or stream the response: {e}")
        yield "Sorry, an error occurred while generating the response. Please try again later."
    # if sources:
    #     yield "\n".join(combined_sources)
   
    
def instant_search(user_query, pinecone_api_key, sources=False, openai_api_key=None, google_api_key=None):
    # Initialize the Pinecone database and vector store
    pinecone_db = Pinecone_db(api_key=pinecone_api_key, openai_api_key=openai_api_key, google_api_key=google_api_key)
    vector_store = VectorStore(pinecone_db.get_vector_store("temp-index"))

    # Retrieve similar documents
    retrieved_documents = vector_store.similarity_search(query=user_query)

    # Prepare the text and sources for the answer
    combined_text, combined_sources = prepare_text(chunks=retrieved_documents, token_limit=500, model="gpt2")

    # Choose the language model based on the available API key
    if openai_api_key:
        llm = OpenAI(api_key=openai_api_key, model="gpt-4o-mini")
    else:
        llm = Gemini(api_key=google_api_key, model="gemini-pro")

    # Create an answer generator
    answer_generator = Answer(llm)

    answer = answer_generator.answer_user_query(combined_text, user_query)
    
    if sources:
        answer += "\n" + "\n".join(combined_sources)
        answer = answer
    return answer
    

def main():
    # Example inputs
    user_query = "Hi"
    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    openai_api_key = None
    google_api_key = os.getenv('GOOGLE_API_KEY')
    sources = False  # Set to True if you want sources included in the answer
    stream = False  # Set to True if you want to stream the response

    try:

        if stream:
            response = streaming_instant_search(
                user_query=user_query, 
                pinecone_api_key=pinecone_api_key, 
                sources=sources, 
                openai_api_key=openai_api_key, 
                google_api_key=google_api_key,
            )
            # Handle streaming response
            for chunk in response:
                if chunk:
                    print(chunk, end='')  # Print each chunk as it arrives
                else:
                    print("Received empty chunk.")
        else:
            response = instant_search(
                user_query=user_query, 
                pinecone_api_key=pinecone_api_key, 
                sources=sources, 
                openai_api_key=openai_api_key, 
                google_api_key=google_api_key
            )
            # Handle non-streaming response
            if response:
                print("Answer:", response)
            else:
                print("No answer returned.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the main function
if __name__ == "__main__":
    main()













