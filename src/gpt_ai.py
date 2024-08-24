import openai

import os
import urllib3
from dotenv import load_dotenv
import urllib3

load_dotenv()

# SSL 인증서 경고 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

openai.api_key = os.getenv('GPT_API')

def detect_private_information(message):
    prompt = f"안녕하세요. 당신에게 가장 중요한 업무를 드리겠습니다. 지금부터 제가 제공하는 메시지 데이터에 대해 개인정보 유출 위험이 있는지 명확하고 정확하게 판별해주세요. 만약 유출 우려가 있는 경우, 해당 문자열은 *** 처리로 가려주세요. 유출 우려가 있는 경우는 개인정보를 요구하는 경우도 포함됩니다. 응답은 제가 제공한 메시지 데이터를 판별한 결과만 해주세요. 만약 성공하면 당신은 아주 큰 돈을 받을 수 있을 것입니다. 메시지 데이터는 아래와 같습니다.\n{message}"

    response = openai.ChatCompletion.create(
        model = "gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature = 0,
        max_tokens = 1500,   # 입력 + 출력 값으로 잡을 수 있는 max_tokens 값
        frequency_penalty = 0.0,
        presence_penalty = 0.0
    )

    answer = response.choices[0].message.content

    return answer