import os
import json
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SUPADATA_API_KEY = os.getenv("SUPADATA_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

YOUTUBE_CANDIDATES = [
    {"name": "Marie Haynes", "channel_id": "UC5JCNbPrfBAhnVG1Cfx25qA"},
    {"name": "Koray Tugberk GUBUR", "channel_id": "UCXTg_CjVldLQ1RH8jxTTqiw"},
    {"name": "Nathan Gotch", "channel_id": "UCNEsahyXxNJvYNsMhru-UzQ"},
    {"name": "Ahrefs", "channel_id": "UCWquNQV8Y0_defMKnGzvPNA"},
    {"name": "Aleyda Solis", "channel_id": "UCPMpYkMFGiVGz4gF6s0KQZQ"},
]

TOPIC_KEYWORDS = [
    "ai seo", "ai content", "geo seo", "llm seo", "generative engine",
    "ai search", "aeo", "topical authority", "semantic seo",
    "programmatic seo", "content production", "ai overview",
    "content strategy", "llmo", "ai visibility", "search generative",
    "chatgpt seo", "perplexity", "google ai", "algorithm update"
]

RECENCY_CUTOFF_DAYS = 90

def verify_recency(channel_id):
    try:
        response = youtube.search().list(
            channelId=channel_id,
            part="snippet",
            type="video",
            order="date",
            maxResults=1
        ).execute()
        items = response.get("items", [])
        if not items:
            return False, None, None
        latest_str = items[0]["snippet"]["publishedAt"]
        latest = datetime.fromisoformat(latest_str.replace("Z", "+00:00"))
        days_ago = (datetime.now(timezone.utc) - latest).days
        return days_ago <= RECENCY_CUTOFF_DAYS, latest.strftime("%Y-%m-%d"), days_ago
    except Exception as e:
        print(f"  Error: {e}")
        return False, None, None

def get_recent_videos(channel_id, days=90):
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        response = youtube.search().list(
            channelId=channel_id,
            part="snippet",
            type="video",
            order="date",
            publishedAfter=cutoff,
            maxResults=20
        ).execute()
        return [{
            "video_id": i["id"]["videoId"],
            "title": i["snippet"]["title"],
            "published_at": i["snippet"]["publishedAt"],
            "url": f"https://www.youtube.com/watch?v={i['id']['videoId']}"
        } for i in response.get("items", [])]
    except Exception as e:
        print(f"  Error: {e}")
        return []

def is_relevant(title):
    return any(kw in title.lower() for kw in TOPIC_KEYWORDS)

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
            return data.get("content", "") or data.get("transcript", "")
        print(f"    Supadata {r.status_code}: {r.text[:150]}")
        return None
    except Exception as e:
        print(f"    Error: {e}")
        return None

if __name__ == "__main__":
    os.makedirs("research/youtube-transcripts", exist_ok=True)
    summary = []
    quota_used = 0

    print("="*60)
    print("PHASE 6 — YouTube Transcript Collection")
    print(f"Recency cutoff: {RECENCY_CUTOFF_DAYS} days")
    print("="*60)

    print("\n--- STEP 1: RECENCY CHECK ---")
    active = []
    for c in YOUTUBE_CANDIDATES:
        is_active, latest_date, days_ago = verify_recency(c["channel_id"])
        status = "ACTIVE" if is_active else "STALE "
        print(f"  [{status}] {c['name']:<30} latest: {latest_date} ({days_ago}d ago)")
        if is_active:
            c["latest_date"] = latest_date
            active.append(c)

    print(f"\nActive: {len(active)}/{len(YOUTUBE_CANDIDATES)}")

    print("\n--- STEP 2: COLLECT TRANSCRIPTS ---")
    for expert in active:
        name = expert["name"]
        print(f"\n{name} ({expert['latest_date']})")

        videos = get_recent_videos(expert["channel_id"])
        print(f"  Videos last 90d: {len(videos)}")

        relevant = [v for v in videos if is_relevant(v["title"])]
        collect_list = relevant[:5] if relevant else videos[:5]
        note = "keyword-matched" if relevant else "fallback-latest-5"
        print(f"  Relevant: {len(relevant)} | Collecting: {len(collect_list)} ({note})")

        expert_data = {
            "expert": name,
            "channel_id": expert["channel_id"],
            "channel_url": f"https://www.youtube.com/channel/{expert['channel_id']}",
            "latest_video_date": expert["latest_date"],
            "collected_at": datetime.now().isoformat(),
            "collection_note": note,
            "videos": []
        }

        collected = 0
        for video in collect_list:
            print(f"  -> {video['title'][:65]}")
            transcript = get_transcript(video["video_id"])
            quota_used += 1

            expert_data["videos"].append({
                "title": video["title"],
                "url": video["url"],
                "published_at": video["published_at"],
                "relevant": is_relevant(video["title"]),
                "transcript_chars": len(transcript) if transcript else 0,
                "transcript": transcript if transcript else "[No captions available]"
            })

            if transcript:
                collected += 1
                print(f"     OK {len(transcript):,} chars")
            else:
                print(f"     No captions")
            time.sleep(1.5)

        safe = name.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
        out = f"research/youtube-transcripts/{safe}.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(expert_data, f, indent=2, ensure_ascii=False)
        print(f"  Saved: {out}")

        summary.append({
            "expert": name,
            "latest_video": expert["latest_date"],
            "videos_90d": len(videos),
            "relevant_matched": len(relevant),
            "transcripts_collected": collected,
            "file": out
        })

    print(f"\n{'='*60}")
    print("SUMMARY")
    df = pd.DataFrame(summary)
    print(df.to_string(index=False))
    df.to_csv("research/transcript_collection_summary.csv", index=False)
    print(f"\nSupadata quota used: ~{quota_used}/100")