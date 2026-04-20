import os
import json
import time
import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SUPADATA_API_KEY = os.getenv("SUPADATA_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Targeted videos found via web research
# Only including videos where expert is actually speaking, not about them
TARGETED_VIDEOS = {
    "Aleyda_Solis": [
        {"id": "-4cu882OJ8E", "title": "Traditional SEO vs AI Search Optimization (GEO, AEO) - Crawling Mondays", "channel": "Crawling Mondays by Aleyda", "date": "2025-06-09"},
        {"id": "BjyF_4UhoOM", "title": "The AI Search Optimization Roadmap - Aleyda Solis", "channel": "Ahrefs", "date": "2025-09-09"},
    ],
    "Kevin_Indig": [
        # Kevin appears in Ahrefs GEO video - already collected as RwKKLnyXCig
        # Clearscope roundtable Jan 28 2026 - need to find ID
        {"id": "RwKKLnyXCig", "title": "Top SEO Experts Build Me an AI Search Strategy (GEO) - Kevin featured", "channel": "Ahrefs", "date": "2026-01-21"},
    ],
    "Lily_Ray": [
        # Lily Ray appears in Ahrefs GEO video context (referenced by Lily herself)
        # Her own YouTube channel - check
        {"id": "RwKKLnyXCig", "title": "Top SEO Experts Build Me an AI Search Strategy - Lily Ray context", "channel": "Ahrefs", "date": "2026-01-21"},
    ],
    "Britney_Muller": [
        # BrightonSEO San Diego 2025 keynote
        {"id": "YZD2lmcbryo", "title": "SEO is Changing: Why Brand Mentions are the New Backlinks - Britney Muller", "channel": "Britney Muller", "date": "2026-02"},
    ]
}

# Koray fix - search his own channel only
KORAY_CHANNEL_ID = "UCXTg_CjVldLQ1RH8jxTTqiw"

def get_transcript(video_id):
    try:
        r = requests.get(
            "https://api.supadata.ai/v1/youtube/transcript",
            headers={"x-api-key": SUPADATA_API_KEY},
            params={"videoId": video_id, "text": True},
            timeout=30
        )
        if r.status_code == 200:
            data = r.json()
            content = data.get("content", [])
            if isinstance(content, list):
                return " ".join([s.get("text", "") for s in content])
            return str(content)
        print(f"    Supadata {r.status_code}: {r.text[:100]}")
        return None
    except Exception as e:
        print(f"    Error: {e}")
        return None

def search_channel_videos(channel_id, query, days=365):
    """Search within a specific channel"""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        r = youtube.search().list(
            channelId=channel_id,
            q=query,
            part="snippet",
            type="video",
            order="relevance",
            publishedAfter=cutoff,
            maxResults=5
        ).execute()
        return [{
            "video_id": i["id"]["videoId"],
            "title": i["snippet"]["title"],
            "published_at": i["snippet"]["publishedAt"],
            "url": f"https://www.youtube.com/watch?v={i['id']['videoId']}"
        } for i in r.get("items", [])]
    except Exception as e:
        print(f"  Error: {e}")
        return []

if __name__ == "__main__":
    os.makedirs("research/youtube-transcripts", exist_ok=True)
    quota_used = 0

    print("="*60)
    print("PHASE 7B — Targeted transcript collection")
    print("="*60)

    # 1. Collect targeted videos for Aleyda, Kevin, Lily, Britney
    for expert, videos in TARGETED_VIDEOS.items():
        print(f"\n--- {expert} ---")
        expert_data = {
            "expert": expert,
            "note": "Targeted video collection — expert speaking directly",
            "collected_at": datetime.now().isoformat(),
            "videos": []
        }

        seen_ids = set()
        for video in videos:
            vid_id = video["id"]
            if vid_id in seen_ids:
                print(f"  Skip duplicate: {vid_id}")
                continue
            seen_ids.add(vid_id)

            print(f"  -> {video['title'][:60]}")
            transcript = get_transcript(vid_id)
            quota_used += 1

            expert_data["videos"].append({
                "title": video["title"],
                "url": f"https://www.youtube.com/watch?v={vid_id}",
                "channel": video.get("channel", ""),
                "published_at": video.get("date", ""),
                "transcript_chars": len(transcript) if transcript else 0,
                "transcript": transcript if transcript else "[No captions available]"
            })

            if transcript:
                print(f"     OK {len(transcript):,} chars")
            else:
                print(f"     No captions")
            time.sleep(1.5)

        out = f"research/youtube-transcripts/{expert}_interviews.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(expert_data, f, indent=2, ensure_ascii=False)
        print(f"  Saved: {out}")

    # 2. Fix Koray — search his own channel with expanded date range
    print(f"\n--- Koray_Tugberk (own channel, 365 days) ---")
    koray_videos = search_channel_videos(KORAY_CHANNEL_ID, "SEO AI topical authority", days=365)

    if koray_videos:
        print(f"  Found {len(koray_videos)} videos:")
        for v in koray_videos:
            print(f"  [{v['published_at'][:10]}] {v['title'][:60]} | {v['video_id']}")

        koray_data = {
            "expert": "Koray_Tugberk",
            "note": "Own channel — expanded to 365 days due to reduced posting frequency",
            "channel_id": KORAY_CHANNEL_ID,
            "collected_at": datetime.now().isoformat(),
            "videos": []
        }

        for video in koray_videos[:3]:
            print(f"\n  Collecting: {video['title'][:55]}")
            transcript = get_transcript(video["video_id"])
            quota_used += 1

            koray_data["videos"].append({
                "title": video["title"],
                "url": video["url"],
                "published_at": video["published_at"],
                "transcript_chars": len(transcript) if transcript else 0,
                "transcript": transcript if transcript else "[No captions available]"
            })

            if transcript:
                print(f"    OK {len(transcript):,} chars")
            else:
                print(f"    No captions")
            time.sleep(1.5)

        # Overwrite previous Koray file with correct data
        out = "research/youtube-transcripts/Koray_Tugberk_GUBUR.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(koray_data, f, indent=2, ensure_ascii=False)
        print(f"  Saved: {out}")
    else:
        print("  No videos found on own channel in 365 days")

    print(f"\nSupadata quota used this run: ~{quota_used}")
    print(f"Total quota used so far: ~{11 + 5 + quota_used}/100")