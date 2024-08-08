from docx import Document
from datetime import datetime

class WordReader:

    def __init__(self):
        pass

    def get_text(self, file_path):

        document = Document(file_path)
        
        full_text = []

        for paragraph in document.paragraphs:
            full_text.append(paragraph.text)

        metadata = {
            'SOURCE': file_path,  # You might want to add the file path as the source
            'DATE': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format the date as per your preference
        }

        return '\n'.join(full_text), metadata
