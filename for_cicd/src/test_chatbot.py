from openai import OpenAI
import boto3
import os

class dummy_chatbot:
    
    def __init__(self, ask_query:str) -> None:
        self._get_ID()
        self.query = ask_query
    
    def _get_ID(self):
        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', None)
        if not OPENAI_API_KEY:
            print("get PARAM store")
            ssm = boto3.client('ssm')
            parameter = ssm.get_parameter(Name='/DOCUMENTO/KEY/OPENAI_API_KEY', WithDecryption=True)
            os.environ['OPENAI_API_KEY'] = parameter['Parameter']['Value']
        

    def _get_client(self):
        return OpenAI()

    
    def reuturn_ANS(self) -> str:
        

        completion = self._get_client().chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. You must answer in Korean."},
                {
                    "role": "user",
                    "content": f"{self.query}"
                }
            ]
        )
        return completion.choices[0].message
