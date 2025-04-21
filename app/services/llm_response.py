import os
import requests
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("groq_api_key")

def get_answer_from_groq(query: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "user",
                "content": f"Answer the query asked by the user.\nQuestion: \"{query}\"\nCategory:"
            }
        ],
        "temperature": 0
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()

    except requests.exceptions.RequestException as e:
        return f"❌ Error: {e}"
