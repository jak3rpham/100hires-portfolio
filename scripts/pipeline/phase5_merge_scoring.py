import os
import json
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# All candidates: LinkedIn/Newsletter experts + YouTube-discovered
LINKEDIN_EXPERTS = [
    # S-tier
    {"name": "Aleyda Solís", "linkedin_tier": "S", "tier_score": 10, "search_query": "Aleyda Solis SEO"},
    {"name": "Kevin Indig", "linkedin_tier": "S", "tier_score": 10, "search_query": "Kevin Indig Growth Memo SEO"},
    {"name": "Lily Ray", "linkedin_tier": "S", "tier_score": 10, "search_query": "Lily Ray SEO"},
    {"name": "Patrick Stox", "linkedin_tier": "S", "tier_score": 10, "search_query": "Patrick Stox Ahrefs SEO"},
    {"name": "Crystal Carter", "linkedin_tier": "S", "tier_score": 10, "search_query": "Crystal Carter SEO Wix"},
    {"name": "Marie Haynes", "linkedin_tier": "S", "tier_score": 10, "search_query": "Marie Haynes SEO"},
    {"name": "Britney Muller", "linkedin_tier": "S", "tier_score": 10, "search_query": "Britney Muller SEO AI"},
    {"name": "Koray Tuğberk GÜBÜR", "linkedin_tier": "S", "tier_score": 10, "search_query": "Koray Tugberk semantic SEO"},
    # A-tier
    {"name": "Ryan Law", "linkedin_tier": "A", "tier_score": 7, "search_query": "Ryan Law Ahrefs content marketing"},
    {"name": "Mark Williams-Cook", "linkedin_tier": "A", "tier_score": 7, "search_query": "Mark Williams-Cook SEO AlsoAsked"},
    {"name": "Mordy Oberstein", "linkedin_tier": "A", "tier_score": 7, "search_query": "Mordy Oberstein SEO"},
]

# YouTube-only candidates (already scored, pull from CSV)
YOUTUBE_ONLY = [
    "Ahrefs", "Nathan Gotch", "Julia McCoy", "Edward Sturm",
    "Vasco's SEO Tips", "Exposure Ninja", "Zubair Trabzada | AI Workshop",
    "Caleb Ulku", "Neil Patel", "Rankknar"
]

def find_youtube_channel(query):
    try:
        request = youtube.search().list(
            q=query,
            type="channel",
            part="snippet",
            maxResults=3
        )
        response = request.execute()
        items = response.get("items", [])
        if not items:
            return None, None, None
        # Take first result
        item = items[0]
        return (
            item["snippet"]["channelId"],
            item["snippet"]["title"],
            item["snippet"].get("description", "")[:200]
        )
    except Exception as e:
        print(f"  Search error: {e}")
        return None, None, None

def get_channel_metrics(channel_id):
    try:
        # Channel stats
        ch_request = youtube.channels().list(
            part="statistics",
            id=channel_id
        )
        ch_response = ch_request.execute()
        items = ch_response.get("items", [])
        if not items:
            return 0, 0, 0, 0

        stats = items[0]["statistics"]
        subscribers = int(stats.get("subscriberCount", 0))
        total_videos = int(stats.get("videoCount", 0))

        # Recent videos (90 days)
        cutoff = (datetime.now(timezone.utc) - timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
        search_request = youtube.search().list(
            channelId=channel_id,
            part="snippet",
            type="video",
            order="date",
            publishedAfter=cutoff,
            maxResults=20
        )
        search_response = search_request.execute()
        recent_items = search_response.get("items", [])
        video_count_90d = len(recent_items)

        # Get video stats for engagement
        video_ids = [v["id"]["videoId"] for v in recent_items if "videoId" in v.get("id", {})]
        avg_views = 0
        avg_likes = 0
        if video_ids:
            vid_request = youtube.videos().list(
                part="statistics",
                id=",".join(video_ids[:10])
            )
            vid_response = vid_request.execute()
            views_list = [int(v["statistics"].get("viewCount", 0)) for v in vid_response.get("items", [])]
            likes_list = [int(v["statistics"].get("likeCount", 0)) for v in vid_response.get("items", [])]
            avg_views = sum(views_list) / len(views_list) if views_list else 0
            avg_likes = sum(likes_list) / len(likes_list) if likes_list else 0

        return subscribers, video_count_90d, avg_views, avg_likes

    except Exception as e:
        print(f"  Metrics error: {e}")
        return 0, 0, 0, 0

def compute_youtube_score(subscribers, video_count_90d, avg_views, avg_likes):
    engagement_rate = (avg_likes / avg_views * 100) if avg_views > 0 else 0
    recency_score = min(10, video_count_90d / 2)
    engagement_score = min(10, engagement_rate * 20)
    sub_score = min(10, (subscribers / 200000) * 10)
    youtube_score = (engagement_score * 0.35 + recency_score * 0.30 + sub_score * 0.35)
    return round(youtube_score, 2), round(engagement_rate, 3)

def combined_score(linkedin_tier_score, youtube_score, has_youtube):
    if has_youtube:
        # Both signals: LinkedIn 50% + YouTube 50%
        return round((linkedin_tier_score * 0.5) + (youtube_score * 0.5), 2)
    else:
        # LinkedIn only: full weight but penalize slightly for no YouTube presence
        return round(linkedin_tier_score * 0.75, 2)

if __name__ == "__main__":
    results = []

    # --- Process LinkedIn experts ---
    print("=== Processing LinkedIn/Newsletter Experts ===\n")
    for expert in LINKEDIN_EXPERTS:
        name = expert["name"]
        print(f"  Finding YouTube for: {name}")
        channel_id, channel_title, channel_desc = find_youtube_channel(expert["search_query"])

        if channel_id:
            print(f"    Found: {channel_title} — fetching metrics...")
            subs, vid_count, avg_views, avg_likes = get_channel_metrics(channel_id)
            yt_score, eng_rate = compute_youtube_score(subs, vid_count, avg_views, avg_likes)
            has_yt = subs > 1000  # ignore noise channels
        else:
            subs, vid_count, avg_views, avg_likes, yt_score, eng_rate = 0, 0, 0, 0, 0, 0
            has_yt = False

        c_score = combined_score(expert["tier_score"], yt_score, has_yt)

        results.append({
            "name": name,
            "source": "LinkedIn+YouTube" if has_yt else "LinkedIn only",
            "linkedin_tier": expert["linkedin_tier"],
            "linkedin_tier_score": expert["tier_score"],
            "youtube_channel": channel_title if has_yt else "—",
            "yt_subscribers": subs,
            "yt_video_count_90d": vid_count,
            "yt_avg_views": round(avg_views),
            "yt_engagement_rate": eng_rate,
            "yt_score": yt_score,
            "combined_score": c_score
        })

    # --- Process YouTube-only candidates ---
    print("\n=== Processing YouTube-only Candidates ===\n")
    yt_df = pd.read_csv("research/channel_relevance.csv")

    for _, row in yt_df.iterrows():
        if row["channel_name"] not in YOUTUBE_ONLY:
            continue
        print(f"  Adding: {row['channel_name']}")

        # No LinkedIn tier = score 0 for that dimension
        yt_score_raw, _ = compute_youtube_score(
            row["subscribers"],
            row.get("video_count_90d", 10),
            row["avg_views"],
            row["avg_views"] * row["engagement_rate"] / 100 if row["avg_views"] > 0 else 0
        )
        c_score = combined_score(0, yt_score_raw, True)

        results.append({
            "name": row["channel_name"],
            "source": "YouTube only",
            "linkedin_tier": "—",
            "linkedin_tier_score": 0,
            "youtube_channel": row["channel_name"],
            "yt_subscribers": row["subscribers"],
            "yt_video_count_90d": row.get("video_count_90d", 0),
            "yt_avg_views": row["avg_views"],
            "yt_engagement_rate": row["engagement_rate"],
            "yt_score": round(yt_score_raw, 2),
            "combined_score": c_score
        })

    # --- Final output ---
    final_df = pd.DataFrame(results)
    final_df = final_df.sort_values("combined_score", ascending=False)

    print("\n=== FINAL COMBINED RANKING ===\n")
    display_cols = ["name", "source", "linkedin_tier", "yt_subscribers", "yt_avg_views", "yt_score", "linkedin_tier_score", "combined_score"]
    print(final_df[display_cols].to_string(index=False))

    os.makedirs("research", exist_ok=True)
    final_df.to_csv("research/final_candidates.csv", index=False)
    print("\nSaved to research/final_candidates.csv")

    print("\n=== TOP 10 RECOMMENDED ===\n")
    top10 = final_df.head(10)
    for i, (_, row) in enumerate(top10.iterrows(), 1):
        print(f"{i:2}. {row['name']:<30} combined: {row['combined_score']} | tier: {row['linkedin_tier']} | yt_subs: {row['yt_subscribers']:,}")