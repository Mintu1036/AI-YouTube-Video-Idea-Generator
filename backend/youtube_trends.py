import requests
import os
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def get_youtube_trending_videos(topic: str, region: str, audience: str):
    """
    GUARANTEES different learning videos for Beginners / Intermediate / Experts
    and excludes YouTube Shorts.
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
