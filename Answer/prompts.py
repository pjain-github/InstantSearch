def get_message(chunks, question):

    messages = [
        (
            "system",
            f"""You are an assistant for question-answering tasks.
            Use the chunks of retrieved context to answerthe question.
            If you don't know the answer, say - Sorry, I cannot answer your question from the given documents.
            Use five sentences maximum and keep the answer concise.
            {chunks}"""
        ),
        ("human", f"""{question}"""),
      ]
    
    return messages

def get_message_simple(chunks, question):

    messages = f"""You are an assistant for question-answering tasks.
            Use the chunks of retrieved context to answerthe question.
            If you don't know the answer, say - "Sorry, I cannot answer your question from the given documents."
            Use five sentences maximum and keep the answer concise.
            Chunks:
            {chunks}
            User Question:
            {question}  """
    
    return messages

def get_message_rolling(chunks, question, previous_answer = ''):

    messages = [
        (
            "system", f"""You are an assistant for question-answering tasks.
            You are shared with a answer from other chunks.
            Use the answer and the new chunks to answer the user question.
            If you don't know the answer, say - "Sorry, I cannot answer your question from the given documents."
            Use five sentences maximum and keep the answer concise.
            Previous Answer:
            {previous_answer}
            New Chunks:
            {chunks}"""
        ),
        ("human", f"""{question}"""),
    ]
    
    return messages

def get_message_rolling_simple(chunks, question, previous_answer = ''):

    messages = f"""You are an assistant for question-answering tasks.
            You are shared with a answer from other chunks.
            Use the answer and the new chunks to answer the user question.
            If you don't know the answer, say - "Sorry, I cannot answer your question from the given documents".
            Use five sentences maximum and keep the answer concise.
            Previous Answer:
            {previous_answer}
            New Chunks:
            {chunks}
            User Question:
            {question}"""
    
    
    return messages
