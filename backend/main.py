from fastapi import FastAPI, Query
from google_trends import get_trending_keywords
from youtube_trends import get_youtube_trending_videos
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY missing in .env file")

# ✅ Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

app = FastAPI()


@app.get("/generate_ideas/")
def generate_video_ideas(
    topic: str = Query(..., description="Video topic"),
    audience: str = Query("Beginners", description="Target audience"),
    region: str = Query("US", description="YouTube region")
):
    # 🔥 Trending Keywords
    trending_keywords = get_trending_keywords(topic)
    if not trending_keywords:
        trending_keywords = ["No trending keywords found"]

    # 🎥 Learning-focused YouTube videos (audience aware)
    trending_videos = get_youtube_trending_videos(topic, region, audience)
    if not trending_videos:
        trending_videos = [{"title": "No learning videos found", "url": "#"}]

    # 🧠 CREATOR-STYLE PROMPT (KEY FIX)
    prompt = f"""
You are an experienced YouTube creator known for making ORIGINAL and ENGAGING content.

Generate EXACTLY 5 UNIQUE YouTube video ideas about "{topic}" for a "{audience}" audience.

GOAL:
These ideas must feel like REAL CONTENT IDEAS a YouTuber would actually upload.
They should NOT feel like generic tutorials or textbook explanations.

VERY IMPORTANT RULES:
- Do NOT generate generic "introduction", "roadmap", or "what is" videos
- Do NOT repeat the same idea structure
- Each idea must use a DIFFERENT creative angle
- Think like a creator, not a teacher

CREATIVE ANGLES TO MIX:
- experiments
- challenges
- comparisons
- myths & mistakes
- real-world builds
- trends & opinions
- case studies
- personal experience style content

FORMAT (FOLLOW STRICTLY):

1. "VIDEO TITLE" Description: Write a creative 3–4 sentence description explaining what the video is about, 
why someone would click on it, and what makes this idea unique.

2. "VIDEO TITLE" Description: ...

(Repeat until 5 ideas)

TRENDING KEYWORDS (USE NATURALLY, DO NOT FORCE):
{", ".join(trending_keywords)}

REFERENCE THESE EXISTING YOUTUBE VIDEOS FOR CONTEXT (DO NOT COPY THEM):
{", ".join(v["title"] for v in trending_videos)}

Now generate 5 DISTINCT, CREATOR-STYLE video ideas.
"""

    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        ideas = response.text.strip()

    except Exception as e:
        # ✅ Intelligent fallback (still creator-style)
        ideas = f"""
1. "I Tried Learning {topic} in 7 Days — Here’s What Actually Happened" Description: This video documents a real learning experiment, showing what progress can realistically be made in a short time and what challenges appear along the way.

2. "5 Beginner Mistakes People Make When Starting {topic}" Description: This video highlights common mistakes beginners make, helping viewers avoid wasted time and confusion early in their learning journey.

3. "Is {topic} Overhyped? An Honest Beginner’s Perspective" Description: This opinion-style video explores expectations vs reality, breaking down what beginners should realistically expect from learning {topic}.

4. "Building My First {topic} Project — Full Process & Lessons Learned" Description: This project-based video walks through creating a simple real-world project, focusing on practical lessons rather than theory.

5. "What Nobody Tells Beginners About {topic}" Description: This video reveals hidden challenges, misconceptions, and truths that beginners usually discover the hard way.
"""

    return {
        "trending_keywords": trending_keywords,
        "trending_videos": trending_videos,
        "ideas": ideas
    }
