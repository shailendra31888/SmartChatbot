import os
import requests
from dotenv import load_dotenv

load_dotenv()
fmp_api_key = os.getenv("fmp_api_key")

def search(query: str) -> dict | None:
    parts = query.strip().split()
    if len(parts) != 2:
        return {"error": "Please use format: '<command> <ticker>' (e.g., 'quote AAPL')"}

    command, ticker = parts[0].lower(), parts[1].upper()
    base_url = "https://www.alphavantage.co/query"
    result = {}

    try:
        if command == "quote":
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": ticker,
                "apikey": fmp_api_key
            }
            res = requests.get(base_url, params=params).json()
            data = res.get("Global Quote", {})
            if data:
                result = {
                    "symbol": ticker,
                    "price": data.get("05. price"),
                    "change": data.get("09. change"),
                    "change_percent": data.get("10. change percent"),
                    "volume": data.get("06. volume")
                }
            else:
                result = {"error": "No data found or invalid ticker."}

        elif command == "fundamentals":
            params = {
                "function": "OVERVIEW",
                "symbol": ticker,
                "apikey": fmp_api_key
            }
            res = requests.get(base_url, params=params).json()
            if res and "Name" in res:
                result = {
                    "name": res.get("Name"),
                    "market_cap": res.get("MarketCapitalization"),
                    "pe_ratio": res.get("PERatio"),
                    "eps": res.get("EPS")
                }
            else:
                result = {"error": "Could not retrieve fundamentals."}

        elif command == "news":
            params = {
                "function": "NEWS_SENTIMENT",
                "tickers": ticker,
                "apikey": fmp_api_key
            }
            res = requests.get(base_url, params=params).json()
            feed = res.get("feed", [])
            if feed:
                result = [
                    {
                        "title": item["title"],
                        "published": item["time_published"],
                        "url": item["url"]
                    }
                    for item in feed[:5]
                ]
            else:
                result = {"error": "News may require a premium account."}
        else:
            result = {"error": "Unknown command! Use one of: quote, fundamentals, news"}

        return result

    except Exception as e:
        return {"error": f"API call failed: {e}"}
