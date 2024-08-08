import tiktoken
from langchain.docstore.document import Document

def prepare_text(chunks, token_limit, model):
    combined_text = []
    combined_sources = []

    text = ""
    sources = ""

    # Initialize the tokenizer
    tokenizer = tiktoken.get_encoding(model)  # Replace with the appropriate model tokenizer

    def token_count(text):
        return len(tokenizer.encode(text))

    for i in range(len(chunks)):

        chunk = chunks[i][0]

        chunk_text = f"Chunk #{i}: {chunk.page_content}\n"
        chunk_source = chunk.metadata.get('SOURCE', '') + "\n"

        # Check if adding this chunk would exceed the token limit
        if token_count(text + chunk_text) > token_limit:
            # Append current text and sources to their respective lists
            combined_text.append(text.strip())
            combined_sources.append(sources.strip())

            # Reset text and sources
            text = ""
            sources = ""

        # Add chunk text and source
        text += chunk_text
        sources += chunk_source

    # Append any remaining text and sources
    if text:
        combined_text.append(text.strip())
        combined_sources.append(sources.strip())

    return combined_text, combined_sources