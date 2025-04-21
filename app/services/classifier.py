import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("groq_api_key")

def classify_with_llm(question: str) -> str | None:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""You are a smart classifier. Classify the following user question into one of these categories:
1. Trades
2. News
3. llm
4. FMP Data
5. Google Search
only give me one word answer as the name of the category.
I DONT WANT ANY OTHER WORDS OR EXPLANATIONS.ONLY ANSWER WITH THE NAME OF THE CATEGORY.GIVEN CATEGORY MUST BE ONE OF THESE:
1. Trades
2. News
3. llm
4. FMP Data
5. Google Search

Question: "{question}"
Category:"""

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    return None
