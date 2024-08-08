"""Py test file to test module"""
from main import streaming_instant_search
from dotenv import load_dotenv
import os

load_dotenv()

pinecone_api_key = os.getenv('PINECONE_API_KEY')
openai_api_key = None
google_api_key = os.getenv('GOOGLE_API_KEY')


def test_pytest():  # Any test case should have test_ before the function name  

    answer = ""
    chunks = streaming_instant_search("Hi", pinecone_api_key=pinecone_api_key, sources=False, openai_api_key=openai_api_key, google_api_key=google_api_key)
    for chunk in chunks:
        answer = answer+chunk

    if answer:
        assert 1