import streamlit as st
from main import streaming_instant_search
from extractor import Database
import os
import tempfile
import env
from dotenv import load_dotenv

load_dotenv()

pinecone_api_key = os.getenv('PINECONE_API_KEY')
openai_api_key = None
google_api_key = os.getenv('GOOGLE_API_KEY')

st.title("Instant Search")

# #Cleaning Folder
# clean_folder("Data")

# Add the "API Keys" button to the sidebar
with st.sidebar:
    st.header("Chat Menu")

    # # API Keys
    # with st.expander("API Keys", expanded=False):
    #     st.markdown("Enter your API keys for security and individual access")
    #     pinecone_api_key_input = st.text_input("Pinecone API Key", value="", type="password")
    #     openai_api_key_input = st.text_input("OpenAI API Key", value="", type="password")
    #     google_api_key_input = st.text_input("Google API Key", value="", type="password")

    #     pinecone_api_key = ""
    #     openai_api_key = None
    #     google_api_key = ""

    #     if st.button("Submit Keys"):

    #         pinecone_api_key = pinecone_api_key_input
    #         openai_api_key = openai_api_key_input
    #         google_api_key = google_api_key_input
    
    # st.write("---")


    #Upload Files:

    with st.expander("Upload Files", expanded=True):

        uploaded_files = st.file_uploader("Choose a file(s)", accept_multiple_files=True)

        for uploaded_file in uploaded_files:
            # Save uploaded file to "Data" folder
            file_path = os.path.join("Data", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())            
            st.write(f"File {uploaded_file.name} saved to Data folder.")

            Database(path = file_path, pinecone_api_key=pinecone_api_key, google_api_key=google_api_key, openai_api_key=openai_api_key)

        # with tempfile.TemporaryDirectory() as temp_dir:
        #     for uploaded_file in uploaded_files:
        #     # Save uploaded file to the temporary folder
        #         file_path = os.path.join(temp_dir, uploaded_file.name)
        #         with open(file_path, "wb") as f:
        #             f.write(uploaded_file.getbuffer())
        #         st.write(f"File {uploaded_file.name} saved to temporary folder.")

        #         # Process the file with the Database class
        #         Database(path=file_path, pinecone_api_key=pinecone_api_key, google_api_key=google_api_key, openai_api_key=openai_api_key)


    st.write("---")  # Creates a horizontal line to separate the sections

    # URL input section
    with st.expander("Adding Webpage", expanded=True):
        url = st.text_input("Paste a link to a website")

        if st.button("Submit"):
        
            if url:

                Database(path = url, pinecone_api_key=pinecone_api_key, google_api_key=google_api_key, openai_api_key=openai_api_key)
                st.write(f"File downloaded from {url} and saved to Data folder.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant's message as it streams
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # Placeholder for streaming content
        streamed_text = ""  # Accumulator for the streamed text

        # Call your custom streaming function
        response = streaming_instant_search(
            user_query=prompt, 
            pinecone_api_key=pinecone_api_key, 
            sources=True, 
            openai_api_key=openai_api_key, 
            google_api_key=google_api_key
        )

        complete_response = ''
        # Stream each chunk of the response
        for chunk in response:
            if chunk:
                streamed_text += chunk  # Accumulate the chunk
                message_placeholder.markdown(streamed_text)  # Update placeholder with streamed content
                complete_response += chunk
            else:
                message_placeholder.markdown("Received empty chunk.")  # Handle empty chunks (optional)
    st.session_state.messages.append({"role": "assistant", "content": complete_response})

