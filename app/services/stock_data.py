import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the API key from environment
fmp_api_key = os.getenv("fmp_api_key")  # Make sure it's named like this in your .env

def search(query):
    parts = query.strip().split()
    if len(parts) != 2:
        print("⚠️ Please use format: '<command> <ticker>' (e.g., 'quote AAPL')")
        return

    command, ticker = parts[0].lower(), parts[1].upper()
    base_url = "https://www.alphavantage.co/query"

    if command == "quote":
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": fmp_api_key
        }
        response = requests.get(base_url, params=params)
        data = response.json().get("Global Quote", {})
        if data:
            print(f"\n📈 Real-time Quote for {ticker}:")
            print(f"Price: {data.get('05. price')}")
            print(f"Change: {data.get('09. change')} ({data.get('10. change percent')})")
            print(f"Volume: {data.get('06. volume')}")
        else:
            print("❌ No data found or invalid ticker.")

    elif command == "fundamentals":
        params = {
            "function": "OVERVIEW",
            "symbol": ticker,
            "apikey": fmp_api_key
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        if data:
            print(f"\n🏢 Fundamentals for {ticker}:")
            print(f"Name: {data.get('Name')}")
            print(f"Market Cap: {data.get('MarketCapitalization')}")
            print(f"PE Ratio: {data.get('PERatio')}")
            print(f"EPS: {data.get('EPS')}")
        else:
            print("❌ Could not retrieve fundamentals.")

    elif command == "news":
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": ticker,
            "apikey": fmp_api_key
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        feed = data.get("feed", [])
        if feed:
            print(f"\n📰 News for {ticker}:")
            for i, item in enumerate(feed[:5], 1):
                print(f"{i}. {item['title']}")
                print(f"   📅 {item['time_published']}")
                print(f"   🔗 {item['url']}\n")
        else:
            print("⚠️ News is likely restricted to premium accounts.")

    else:
        print("⚠️ Unknown command! Use one of: quote, fundamentals, news")
