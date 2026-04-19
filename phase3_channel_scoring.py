import os
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def get_recent_videos(channel_id, days=90):
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    try:
        request = youtube.search().list(
            channelId=channel_id,
            part="snippet",
            type="video",
            order="date",
            publishedAfter=cutoff,
            maxResults=20
        )
        response = request.execute()
        return response.get("items", [])
    except Exception as e:
        print(f"  Error fetching videos for {channel_id}: {e}")
        return []

def get_video_stats(video_ids):
    if not video_ids:
        return []
    try:
        request = youtube.videos().list(
            part="statistics",
            id=",".join(video_ids)
        )
        response = request.execute()
        return response.get("items", [])
    except Exception as e:
        print(f"  Error fetching video stats: {e}")
        return []

def score_channel(channel_id, channel_name, subscribers):
    print(f"  Scoring: {channel_name}")
    
    recent_videos = get_recent_videos(channel_id)
    video_count_90d = len(recent_videos)
    
    if video_count_90d == 0:
        return {
            "video_count_90d": 0,
            "avg_views": 0,
            "avg_likes": 0,
            "engagement_rate": 0,
            "recency_score": 0,
            "consistency_score": 0,
            "final_score": 0
        }
    
    video_ids = [v["id"]["videoId"] for v in recent_videos if "videoId" in v.get("id", {})]
    stats = get_video_stats(video_ids)
    
    views_list = []
    likes_list = []
    for s in stats:
        v = int(s["statistics"].get("viewCount", 0))
        l = int(s["statistics"].get("likeCount", 0))
        views_list.append(v)
        likes_list.append(l)
    
    avg_views = sum(views_list) / len(views_list) if views_list else 0
    avg_likes = sum(likes_list) / len(likes_list) if likes_list else 0
    engagement_rate = (avg_likes / avg_views * 100) if avg_views > 0 else 0
    
    # Scores (0-10)
    recency_score = min(10, video_count_90d / 2)  # 20 videos in 90d = 10/10
    consistency_score = min(10, video_count_90d / 1.5)  # consistent posting
    engagement_score = min(10, engagement_rate * 20)  # 0.5% engagement = 10/10
    
    # Weighted final score
    # Engagement 30%, Recency 20%, Consistency 25%, Subscriber base 25%
    sub_score = min(10, (subscribers / 200000) * 10)
    final_score = (
        engagement_score * 0.30 +
        recency_score * 0.20 +
        consistency_score * 0.25 +
        sub_score * 0.25
    )
    
    return {
        "video_count_90d": video_count_90d,
        "avg_views": round(avg_views),
        "avg_likes": round(avg_likes),
        "engagement_rate": round(engagement_rate, 3),
        "recency_score": round(recency_score, 2),
        "consistency_score": round(consistency_score, 2),
        "engagement_score": round(engagement_score, 2),
        "sub_score": round(sub_score, 2),
        "final_score": round(final_score, 2)
    }

if __name__ == "__main__":
    df = pd.read_csv("research/youtube_candidates.csv")
    
    # Pre-filter: remove obvious non-relevant channels
    exclude = [
        "HubSpot Marketing",
        "AI Master",
        "The Rise of Intelligence", 
        "JVZoo WSO Launch Review",
        "Get Certificate Online",
        "AI Innovations With Maria Johnsen",
        "Ahrefs Tutorials",  # keep main Ahrefs channel
        "Ahrefs Podcast"
    ]
    df = df[~df["channel_name"].isin(exclude)]
    print(f"Scoring {len(df)} channels after pre-filter...\n")
    
    scored = []
    for _, row in df.iterrows():
        scores = score_channel(row["channel_id"], row["channel_name"], row["subscribers"])
        result = {
            "channel_name": row["channel_name"],
            "subscribers": row["subscribers"],
            "search_keyword": row["search_keyword"],
            **scores
        }
        scored.append(result)
    
    scored_df = pd.DataFrame(scored)
    scored_df = scored_df.sort_values("final_score", ascending=False)
    
    print("\n=== CHANNEL SCORES (sorted by final score) ===")
    cols = ["channel_name", "subscribers", "video_count_90d", "avg_views", "engagement_rate", "final_score"]
    print(scored_df[cols].to_string(index=False))
    
    scored_df.to_csv("research/channel_scores.csv", index=False)
    print("\nSaved to research/channel_scores.csv")