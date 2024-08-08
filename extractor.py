from DataProcessing.data_processing import Extraction
from DataProcessing.data_processing import DataProcessing
import os

def Database(path, pinecone_api_key=None, google_api_key=None, openai_api_key=None):
    extractor = Extraction()
    
    # Check if the path is a folder
    if os.path.isdir(path):
        # Loop over each file in the folder
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path):  # Ensure it's a file and not a subfolder
                text, metadata = extractor.extract_text(file_path)

                processor = DataProcessing(
                    pinecone_api_key=pinecone_api_key, 
                    index_name="temp-index", 
                    openai_api_key=openai_api_key, 
                    google_api_key=google_api_key
                )
                processor.add_data(text, metadata)
    else:
        # If path is a single file
        text, metadata = extractor.extract_text(path)

        processor = DataProcessing(
            pinecone_api_key=pinecone_api_key, 
            index_name="temp-index", 
            openai_api_key=openai_api_key, 
            google_api_key=google_api_key
        )
        processor.add_data(text, metadata)

    print("Upload Successful")
