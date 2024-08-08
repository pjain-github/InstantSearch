from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


class Gemini:
    def __init__(self, api_key, model="gemini-pro"):
        self.model = model
        self.api_key = api_key

        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
            api_key=self.api_key,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
            )

    def stream_llm(self, messages, stream=False):
        if stream:
            response = ""
            for chunk in self.llm.stream(messages):
                response += chunk.content
                yield chunk.content  # Stream each chunk
    
    def call_llm(self, messages, stream=False):
        response = self.llm.invoke(messages).content
        return response


class OpenAI:
    def __init__(self, api_key, model ="gpt-4o-mini"):
        self.model = model
        self.api_key = api_key

        self.llm = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
            )

    def stream_llm(self, messages, stream=False):
        if stream:
            response = ""
            for chunk in self.llm.stream(messages):
                response += chunk.content
                yield chunk.content  # Stream each chunk
    
    def call_llm(self, messages, stream=False):
        response = self.llm.invoke(messages).content
        return response
        
