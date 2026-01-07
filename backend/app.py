import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/generate_ideas/"

st.title("🎬 AI-Powered YouTube Idea Generator")

topic = st.text_input("Enter a topic", "")
audience = st.selectbox("Target Audience", ["Beginners", "Intermediate", "Experts"])
region = st.text_input("YouTube Region (e.g., US, IN, UK)", "US")

if st.button("Generate Video Ideas"):
    try:
        response = requests.get(
            API_URL,
            params={
                "topic": topic,
                "audience": audience,
                "region": region
            },
            timeout=30
        )

        if response.status_code != 200:
            st.error("❌ Backend returned an error.")
            st.stop()

        data = response.json()

    except Exception as e:
        st.error(f"❌ API Error: {e}")
        st.stop()

    # 🔥 Trending Keywords
    st.subheader("🔥 Trending Keywords")
    keywords = data.get("trending_keywords") or []
    if keywords:
        st.write(", ".join(keywords))
    else:
        st.write("No trending keywords found.")

    # 🎥 Trending YouTube Videos
    st.subheader("🎥 Learning YouTube Videos")
    videos = data.get("trending_videos") or []
    if videos:
        for video in videos:
            st.markdown(f"📌 [{video.get('title','No title')}]({video.get('url','#')})")
    else:
        st.write("No learning videos found.")

    # ✨ AI-Generated Video Ideas
    st.subheader("✨ AI-Generated Video Ideas")

    ideas = data.get("ideas", "")

    # ✅ FIX: preprocess before f-string (NO backslash error)
    formatted_ideas = ideas.replace("\n", "<br>")

    st.markdown(
        f"""
<div style="
    background-color:#e9f7ef;
    padding:20px;
    border-radius:10px;
    font-size:16px;
    line-height:1.7;
    color:#1f2937;
">
{formatted_ideas}
</div>
""",
        unsafe_allow_html=True
    )
