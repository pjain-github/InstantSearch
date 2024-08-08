from langchain_community.document_loaders.pdf import PyMuPDFLoader
from datetime import datetime

class PDF_Reader:

    def __init__(self):
        pass

    def get_text(self, file_path):

        loader = PyMuPDFLoader(file_path)

        pages = loader.load_and_split()

        text = ''
        for page in pages:
            text = text + page.page_content

        metadata = {
            'SOURCE': file_path,  # You might want to add the file path as the source
            'DATE': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format the date as per your preference
        }

        return text, metadata

    # def read_adobe(self, file_path):
    #     loader = PyMuPDFLoader(file_path)