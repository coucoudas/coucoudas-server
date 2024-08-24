from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()

gpt_api_key = os.getenv('GPT_API')

client = OpenAI(
    api_key = gpt_api_key
)

def get_gpt_response(prompt):
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {
                "role": "user",
                "content": "Hello World"
            }
        ]
    )

    answer = response.choices[0].message.content

    return answer