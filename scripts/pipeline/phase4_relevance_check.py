import os
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Channels còn lại sau khi auto-loại
EXCLUDE = [
    "James Dooley",
    "Lawrence Dauchy ~ GEO Expert",
    "Lawrence Dauchy ~ AI Visibility",
    "George Vlasyev",
    "Waltz Chen",
    "SeoGri",
    "Lorraine Pawell - SEO & Content Strategy Services",
    "StrategeMarketing",
    "Saket Wahi",
    "Flow Agency"
]

# Keywords để score relevance từ titles/descriptions
RELEVANT_KEYWORDS = [
    "ai seo", "llm seo", "geo seo", "generative engine",
    "ai content", "content production", "programmatic seo",
    "semantic seo", "topical authority", "ai search",
    "search generative", "aeo", "content strategy",
    "content workflow", "ai writing", "content at scale"
]

def get_recent_video_details(channel_id, max_results=10):
    cutoff = (datetime.now(timezone.utc) - timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        search_response = youtube.search().list(
            channelId=channel_id,
            part="snippet",
            type="video",
            order="date",
            publishedAfter=cutoff,
            maxResults=max_results
        ).execute()
        
        videos = []
        for item in search_response.get("items", []):
            videos.append({
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"][:300],
                "published_at": item["snippet"]["publishedAt"]
            })
        return videos
    except Exception as e:
        print(f"  Error: {e}")
        return []

def score_relevance(videos):
    if not videos:
        return 0, []
    
    matched_titles = []
    total_score = 0
    
    for v in videos:
        text = (v["title"] + " " + v["description"]).lower()
        matches = [kw for kw in RELEVANT_KEYWORDS if kw in text]
        if matches:
            total_score += len(matches)
            matched_titles.append(f"{v['title']} [{', '.join(matches)}]")
    
    relevance_score = min(10, total_score / len(videos) * 3)
    return round(relevance_score, 2), matched_titles[:3]

if __name__ == "__main__":
    df = pd.read_csv("research/channel_scores.csv")
    df = df[~df["channel_name"].isin(EXCLUDE)]
    print(f"Checking relevance for {len(df)} channels...\n")
    
    results = []
    for _, row in df.iterrows():
        channel_id = None
        
        # Get channel_id from youtube_candidates.csv
        candidates = pd.read_csv("research/youtube_candidates.csv")
        match = candidates[candidates["channel_name"] == row["channel_name"]]
        if match.empty:
            continue
        channel_id = match.iloc[0]["channel_id"]
        
        print(f"  Checking: {row['channel_name']}")
        videos = get_recent_video_details(channel_id)
        relevance_score, sample_titles = score_relevance(videos)
        
        results.append({
            "channel_name": row["channel_name"],
            "subscribers": row["subscribers"],
            "final_score": row["final_score"],
            "avg_views": row["avg_views"],
            "engagement_rate": row["engagement_rate"],
            "relevance_score": relevance_score,
            "combined_score": round((row["final_score"] * 0.5) + (relevance_score * 0.5), 2),
            "sample_titles": " | ".join(sample_titles)
        })
    
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("combined_score", ascending=False)
    
    print("\n=== RELEVANCE + PERFORMANCE COMBINED SCORE ===")
    cols = ["channel_name", "subscribers", "avg_views", "relevance_score", "final_score", "combined_score"]
    print(results_df[cols].to_string(index=False))
    
    results_df.to_csv("research/channel_relevance.csv", index=False)
    print("\nSaved to research/channel_relevance.csv")
    
    print("\n=== SAMPLE TITLES (relevance evidence) ===")
    for _, row in results_df.head(15).iterrows():
        print(f"\n{row['channel_name']} (score: {row['combined_score']})")
        print(f"  {row['sample_titles']}")