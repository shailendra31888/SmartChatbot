import os
import requests
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
google_search_api = os.getenv("google_search_api")
google_search_cx = os.getenv("GOOGLE_SEARCH_CX")

def google_search(query: str, num_results: int = 5) -> list[dict] | None:
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": google_search_api,
        "cx": google_search_cx,
        "q": query,
        "num": num_results
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        results = data.get("items", [])
        formatted_results = []
        for item in results:
            formatted_results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })

        return formatted_results if formatted_results else None

    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", e)
        return None
