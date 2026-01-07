import requests
import os
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def get_youtube_trending_videos(topic: str, region: str, audience: str):
    """
    Selects learning-focused YouTube videos for a given topic, region, and audience level.
    
    Filters search results to exclude Shorts and obvious non-learning content, prioritizes titles containing audience-relevant keywords, and returns up to six matching videos (or a single fallback entry if none match).
    
    Parameters:
        topic (str): Topic to search for (used to build the query).
        region (str): Region code to scope results (ISO 3166-1 alpha-2).
        audience (str): Target learning level; expected values are "beginners", "intermediate", or "experts" (case-insensitive). Values other than "beginners" and "intermediate" are treated as experts.
    
    Returns:
        list[dict]: A list of dictionaries with keys:
            - "title" (str): Video title.
            - "url" (str): Full YouTube watch URL.
        If no suitable videos are found, returns a single-item list containing a fallback entry whose "url" is "#".
    """

    audience = audience.lower()

    # 🎯 Audience-specific search queries (KEY FIX)
    if audience == "beginners":
        query = f"{topic} tutorial for beginners explained"
        relevance_words = ["beginner", "basics", "explained", "step by step"]

    elif audience == "intermediate":
        query = f"{topic} project tutorial implementation"
        relevance_words = ["project", "tutorial", "build", "implementation"]

    else:  # Experts
        query = f"{topic} advanced deep dive architecture"
        relevance_words = ["advanced", "deep dive", "architecture", "internals"]

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "regionCode": region,
        "maxResults": 15,
        "order": "relevance",
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    videos = []

    for item in data.get("items", []):
        title = item["snippet"]["title"]
        title_lower = title.lower()

        # 🚫 Remove Shorts
        if "shorts" in title_lower or "#shorts" in title_lower:
            continue

        # 🚫 Remove non-learning content
        if any(x in title_lower for x in ["song", "music", "trailer", "clip"]):
            continue

        # 🎯 Keep only audience-relevant videos
        if not any(word in title_lower for word in relevance_words):
            continue

        videos.append({
            "title": title,
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        })

    # 🔥 Final safety fallback
    if not videos:
        return [{
            "title": f"No {audience.capitalize()} learning videos found for {topic}",
            "url": "#"
        }]

    return videos[:6]