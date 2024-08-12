import requests
import json

with open('../env.json') as f:
    config = json.load(f)


def call_gpt_api(text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {config['provider']['gpt']['key']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{
            "role": "user",
            "content": f"Is the following SMS message a voice phishing scam? \n\n{text}"
        }],
        "max_tokens": 10,
        "n": 1,
        "stop": None,
        "temperature": 0.5
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()