from Answer.prompts import get_message, get_message_rolling, get_message_simple, get_message_rolling_simple
import logging

class Answer:

    def __init__(self, llm):
        self.llm = llm
    
    def stream_user_query(self, text_list, user_query):
        answer = ""

        try:

            for i in range(len(text_list)):
                if i == 0:
                    message = get_message_simple(text_list[i], user_query)
                else:
                    message = get_message_rolling_simple(text_list[i], user_query, answer)

                # If streaming, gather the response chunk by chunk
                for chunk in self.llm.stream_llm(messages=message, stream=True):
                    answer += chunk

                    if i+1==len(text_list): # Remove this if you want to all the chunks
                        yield chunk  # Yield the response chunk for streaming
        except Exception as e:
            loggging.info("LLM failed")
            return """LLM is not reponding, possible reasons could be:
            1. Server issue.
            2. Token limit reached.
            3. Rate limit reached(in that case wait for a couple of minutes before retrying)."""

    def answer_user_query(self, text_list, user_query):
        answer = ""

        for i in range(len(text_list)):
            if i == 0:
                message = get_message_simple(text_list[i], user_query)
            else:
                message = get_message_rolling_simple(text_list[i], user_query, answer)

            # Non-streaming mode
            answer = self.llm.call_llm(messages=message)

        return answer
        
# class Answer:

#     def __init__(self, llm):
#         self.llm = llm

#     def answer_user_query_simple(self, text_list, user_query):
#         answer = ""

#         for i in range(len(text_list)):
#             if i == 0:
#                 message = get_message_simple(text_list[i], user_query)
#             else:
#                 message = get_message_rolling_simple(text_list[i], user_query, answer)

#             # Non-streaming mode
#             answer = self.llm.call_llm(messages=message)
#             # all_responses.append(answer)

#         return answer