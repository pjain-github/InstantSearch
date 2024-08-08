import logging
import re

class SmallTalk:

    def __init__(self, llm):
        self.llm = llm

    def small_talk(self, query):

        prompt = f"""
        You are an AI chatbot expert in data that the I have added. You can answer based on my question from the data.
        Your name is Instant Search.

        If the user is trying to make small talk, answer is small talk only.
        Small talk includes - Hi, Hello, How are you etc.
        Small talks also include general topics like - who are you, what can you do etc.
        Return if the query is small talk or not.

        If the user is asking a specific question, where we need to search, reply:
        "Sure, let me try and fetch the answer for you. Please wait for a few seconds."

        Output should be in the following format:
        Small-talk: True/Flase,
        Answer: Sample Answer

        For example:
        user querry - 
            Hi, what up?
        answer - 
            Small-talk:True
            Answer: Hi, how can I help you?

        For example:
        uer_query - 
            What is the new law?
        asnwer -
            Small-talk:False
            Answer- Sure, let me try and fetch the answer for you. Please wait for a few seconds.

        user_query = {query}
        """

        output = self.llm.call_llm(prompt)

        small_talk, answer = self.extract_fields(output)

        if small_talk == None:
            small_talk = False
            answer = "Sure, will try and answer you question. Give me a few minutes."

        return small_talk, answer

    def extract_fields(self, text):
        # Regular expression to match "Small-talk: <value>" and "Answer: <value>"
        small_talk_pattern = r"Small-talk:\s*(True|False)"
        answer_pattern = r"Answer:\s*(.*)"
        
        # Find the matches
        small_talk_match = re.search(small_talk_pattern, text)
        answer_match = re.search(answer_pattern, text)
        
        # Extract the values
        small_talk = small_talk_match.group(1) if small_talk_match else None
        answer = answer_match.group(1).strip() if answer_match else None
        
        return small_talk, answer


        