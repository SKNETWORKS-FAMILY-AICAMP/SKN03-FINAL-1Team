import openai
import os
import boto3


class openaiHandler:
    def __init__(self) -> None:
        self._set_openai_api_key()

    def _set_openai_api_key(self) -> None:
        """
        Sets the OpenAI API key from environment variables or AWS SSM Parameter Store.
        """

        #in local
        print("Fetching API key from AWS SSM Parameter Store...")
        ssm = boto3.client("ssm")
        parameter = ssm.get_parameter(
            Name="/DOCUMENTO/KEY/OPENAI_API_KEY/TRANSFORMATION", WithDecryption=True
        )
        os.environ["OPENAI_API_KEY"] = parameter["Parameter"]["Value"]
        openai.api_key = os.environ["OPENAI_API_KEY"]

        # api_key = os.environ.get("OPENAI_API_KEY")
        # if not api_key:
        #     print("Fetching API key from AWS SSM Parameter Store...")
        #     ssm = boto3.client("ssm")
        #     parameter = ssm.get_parameter(
        #         Name="/DOCUMENTO/KEY/OPENAI_API_KEY/TRANSFORMATION", WithDecryption=True
        #     )
        #     os.environ["OPENAI_API_KEY"] = parameter["Parameter"]["Value"]
        # openai.api_key = os.environ["OPENAI_API_KEY"]

    def create_system_prompt(self, user_prompt) -> str:
        """
        Creates a keyword prompt for the OpenAI Chat API.
        """
        system_prompt = (
            "You are an expert in identifying highly relevant research papers. "
            "When the user provides a specific topic or question, your task is to recommend 10 precise, research-friendly keywords related to the query. "
            "These keywords should be specific, consist of three or more words, and cater to advanced research purposes. "
            "Additionally, provide translations for the keywords in both English and Korean in the following structured format:\n\n"
            "[\n"
            '{"eng": "<English Keyword 1>", "kor": "<Korean Translation 1>"},\n'
            '{"eng": "<English Keyword 2>", "kor": "<Korean Translation 2>"},\n'
            "...]\n\n"
            f"Here’s the user query:\n‘{user_prompt}’\nGenerate 5 specific and highly relevant keywords that align with this topic."
        )
        return system_prompt

    def get_keywords(self, user_prompt) -> str:
        """
        Sends a query to OpenAI and streams the response.
        """
        try:
            self.query = self.create_system_prompt(user_prompt)
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.query},
                ],
                # stream=True
            )

            # print("Assistant: ", end="", flush=True)
            # for chunk in response:
            #     content = chunk['choices'][0].get('delta', {}).get('content')
            #     if content:
            #         print(content, end="", flush=True)
            content = response["choices"][0]["message"]["content"]
            
            return content
        except Exception as e:
            print(f"Error occurred: {str(e)}")


# # Example usage:
# if __name__ == "__main__":
#     chatbot = Chatbot()
#     chatbot.get_keywords("대형 언어 모델(LLM) 사용 시 높은 성능을 유지하면서 비용과 리소스를 어떻게 최적화할 것인가?")
