import requests
import os
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def get_trending_keywords(topic: str):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_trends",
        "q": topic,
        "hl": "en",
        "date": "today 12-m",
        "data_type": "RELATED_QUERIES",
        "api_key": SERPAPI_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "related_queries" in data and "top" in data["related_queries"]:
        return [item["query"] for item in data["related_queries"]["top"][:10]]

    return []
