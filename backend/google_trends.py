import requests
import os
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def get_trending_keywords(topic: str):
    """
    Retrieve up to 10 top related Google Trends queries for the given topic using SerpAPI.
    
    Parameters:
        topic (str): Search topic to fetch related trending queries for.
    
    Returns:
        list[str]: A list of up to 10 related query strings from Google Trends; an empty list if none are available.
    """
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