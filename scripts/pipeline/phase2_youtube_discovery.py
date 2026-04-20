import os
import requests
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from datetime import datetime, timedelta

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

SEARCH_KEYWORDS = [
    "AI SEO",
    "GEO SEO generative engine optimization",
    "AI search optimization",
    "LLM SEO"
]

def search_youtube_channels(query, max_results=15):
    request = youtube.search().list(
        q=query,
        type="video",
        part="snippet",
        maxResults=max_results,
        order="relevance",
        publishedAfter=(datetime.utcnow() - timedelta(days=180)).strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    response = request.execute()
    
    channels = {}
    for item in response["items"]:
        channel_id = item["snippet"]["channelId"]
        channel_title = item["snippet"]["channelTitle"]
        if channel_id not in channels:
            channels[channel_id] = {
                "channel_id": channel_id,
                "channel_name": channel_title,
                "search_keyword": query,
                "sample_video_title": item["snippet"]["title"],
                "published_at": item["snippet"]["publishedAt"]
            }
    return list(channels.values())

def get_channel_stats(channel_ids):
    request = youtube.channels().list(
        part="statistics,snippet",
        id=",".join(channel_ids)
    )
    response = request.execute()
    
    stats = {}
    for item in response["items"]:
        cid = item["id"]
        stats[cid] = {
            "subscribers": int(item["statistics"].get("subscriberCount", 0)),
            "total_videos": int(item["statistics"].get("videoCount", 0)),
            "total_views": int(item["statistics"].get("viewCount", 0)),
            "description": item["snippet"].get("description", "")[:200]
        }
    return stats

if __name__ == "__main__":
    print("Searching YouTube for AI SEO creators...\n")
    
    all_channels = []
    
    for keyword in SEARCH_KEYWORDS:
        print(f"Searching: '{keyword}'")
        results = search_youtube_channels(keyword)
        all_channels.extend(results)
        print(f"  Found {len(results)} channels")
    
    # Deduplicate by channel_id
    seen = set()
    unique_channels = []
    for ch in all_channels:
        if ch["channel_id"] not in seen:
            seen.add(ch["channel_id"])
            unique_channels.append(ch)
    
    print(f"\nTotal unique channels found: {len(unique_channels)}")
    
    # Get stats for all channels
    print("Fetching channel statistics...")
    channel_ids = [ch["channel_id"] for ch in unique_channels]
    
    # YouTube API accepts max 50 IDs at once
    all_stats = {}
    for i in range(0, len(channel_ids), 50):
        batch = channel_ids[i:i+50]
        stats = get_channel_stats(batch)
        all_stats.update(stats)
    
    # Merge
    for ch in unique_channels:
        cid = ch["channel_id"]
        if cid in all_stats:
            ch.update(all_stats[cid])
    
    # Build DataFrame
    df = pd.DataFrame(unique_channels)
    df = df.sort_values("subscribers", ascending=False)
    
    print("\n=== CHANNELS DISCOVERED ===")
    print(df[["channel_name", "subscribers", "total_videos", "search_keyword"]].to_string(index=False))
    
    os.makedirs("research", exist_ok=True)
    df.to_csv("research/youtube_candidates.csv", index=False)
    print("\nSaved to research/youtube_candidates.csv")