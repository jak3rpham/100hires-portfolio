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

# Curated video list per expert
# Sources: own channels (if active) + interview appearances on other channels
EXPERT_VIDEOS = {
    "Aleyda_Solis": {
        "linkedin_tier": "S",
        "primary_platform": "Newsletter + LinkedIn",
        "videos": [
            # Own channel - Crawling Mondays (found active videos)
            {"id": "-4cu882OJ8E", "title": "Traditional SEO vs AI Search Optimization (GEO, AEO)", "source": "own_channel", "date": "2025-06-09"},
            {"id": "BjyF_4UhoOM", "title": "The AI Search Optimization Roadmap", "source": "conference_recording", "date": "2025-09-09"},
        ]
    },
    "Kevin_Indig": {
        "linkedin_tier": "S",
        "primary_platform": "Substack newsletter",
        "videos": [
            # Featured in Clearscope webinar Jan 2026 - Lily Ray + Kevin Indig roundtable
            # Also Ahrefs video had him as expert (RwKKLnyXCig - already collected)
            {"id": "RwKKLnyXCig", "title": "Top SEO Experts Build Me an AI Search Strategy (GEO) [featured]", "source": "ahrefs_channel", "date": "2026-01-21"},
        ]
    },
    "Lily_Ray": {
        "linkedin_tier": "S",
        "primary_platform": "Substack + conferences",
        "videos": [
            # Clearscope roundtable Jan 2026 - need to find YouTube ID
            {"id": "RwKKLnyXCig", "title": "Top SEO Experts Build Me an AI Search Strategy - mentions Lily Ray", "source": "ahrefs_channel", "date": "2026-01-21"},
        ]
    },
    "Patrick_Stox": {
        "linkedin_tier": "S",
        "primary_platform": "Ahrefs blog + LinkedIn",
        "videos": [
            # Ahrefs channel - Patrick Stox appears in Ahrefs content
            {"id": "tiW6xRYSXmM", "title": "SEO in 2026: How I'd Rank in Google in the AI Era [Ahrefs]", "source": "ahrefs_channel", "date": "2026-03-18"},
            {"id": "3iNJeArrUu4", "title": "I Outsourced our Digital Marketing to AI [Ahrefs]", "source": "ahrefs_channel", "date": "2026-02-04"},
        ]
    },
    "Crystal_Carter": {
        "linkedin_tier": "S",
        "primary_platform": "Wix + Search Engine Land",
        "videos": [
            # SERP's Up podcast - Crystal Carter co-hosts
            # Need to find specific recent episode YouTube IDs
        ]
    },
    "Marie_Haynes": {
        "linkedin_tier": "S",
        "primary_platform": "YouTube + podcast",
        "videos": [
            # Already collected in phase 6 - skip duplicates
        ]
    },
    "Britney_Muller": {
        "linkedin_tier": "S",
        "primary_platform": "Conferences + LinkedIn",
        "videos": [
            # BrightonSEO San Diego 2025 keynote - need YouTube ID
        ]
    },
    "Koray_Tugberk": {
        "linkedin_tier": "S",
        "primary_platform": "YouTube + LinkedIn",
        "videos": [
            # Channel is stale but has interview appearances
        ]
    },
    "Ryan_Law": {
        "linkedin_tier": "A",
        "primary_platform": "Ahrefs blog",
        "videos": [
            # Already collected via Ahrefs channel - skip
        ]
    },
    "Nathan_Gotch": {
        "linkedin_tier": "B",
        "primary_platform": "YouTube",
        "videos": [
            # Already collected in phase 6 - skip duplicates
        ]
    }
}

TOPIC_KEYWORDS = [
    "ai seo", "ai content", "geo", "llm seo", "generative engine",
    "ai search", "aeo", "topical authority", "semantic seo",
    "programmatic seo", "content production", "ai overview",
    "content strategy", "llmo", "ai visibility"
]

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
        return None
    except:
        return None

def search_expert_videos(expert_name, search_query, days=180):
    """Search YouTube for recent videos featuring an expert"""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        r = youtube.search().list(
            q=search_query,
            part="snippet",
            type="video",
            order="relevance",
            publishedAfter=cutoff,
            maxResults=5
        ).execute()
        return [{
            "video_id": i["id"]["videoId"],
            "title": i["snippet"]["title"],
            "channel": i["snippet"]["channelTitle"],
            "published_at": i["snippet"]["publishedAt"],
            "url": f"https://www.youtube.com/watch?v={i['id']['videoId']}"
        } for i in r.get("items", [])]
    except Exception as e:
        print(f"  Search error: {e}")
        return []

def is_relevant(title):
    return any(kw in title.lower() for kw in TOPIC_KEYWORDS)

if __name__ == "__main__":
    os.makedirs("research/youtube-transcripts", exist_ok=True)

    # Search for recent interview appearances for experts without own channel
    SEARCH_QUERIES = {
        "Aleyda_Solis": "Aleyda Solis AI SEO GEO interview 2025 2026",
        "Kevin_Indig": "Kevin Indig AI search SEO interview 2025 2026",
        "Lily_Ray": "Lily Ray AI SEO GEO interview 2025 2026",
        "Patrick_Stox": "Patrick Stox Ahrefs AI search 2025 2026",
        "Crystal_Carter": "Crystal Carter Wix AI search SEO 2025 2026",
        "Britney_Muller": "Britney Muller AI SEO LLM interview 2025 2026",
        "Koray_Tugberk": "Koray Tugberk topical authority semantic SEO 2025 2026",
    }

    print("="*60)
    print("PHASE 7 — Comprehensive YouTube Discovery & Transcript Collection")
    print("="*60)

    quota_used = 0
    results_summary = []

    for expert_name, query in SEARCH_QUERIES.items():
        print(f"\n--- {expert_name} ---")
        videos = search_expert_videos(expert_name, query)

        if not videos:
            print("  No videos found")
            continue

        print(f"  Found {len(videos)} videos:")
        for v in videos:
            relevant = is_relevant(v["title"])
            marker = "★" if relevant else "○"
            print(f"  {marker} [{v['published_at'][:10]}] {v['title'][:60]}")
            print(f"    Channel: {v['channel']} | ID: {v['video_id']}")

        # Collect transcripts for relevant videos (max 3 per expert)
        to_collect = [v for v in videos if is_relevant(v["title"])][:3]
        if not to_collect:
            to_collect = videos[:2]  # fallback

        expert_data = {
            "expert": expert_name,
            "note": "Interview appearances on other channels + own channel content",
            "collected_at": datetime.now().isoformat(),
            "videos": []
        }

        for video in to_collect:
            print(f"\n  Collecting: {video['title'][:55]}...")
            transcript = get_transcript(video["video_id"])
            quota_used += 1

            expert_data["videos"].append({
                "title": video["title"],
                "url": video["url"],
                "channel": video["channel"],
                "published_at": video["published_at"],
                "source_type": "interview_appearance",
                "transcript_chars": len(transcript) if transcript else 0,
                "transcript": transcript if transcript else "[No captions available]"
            })

            if transcript:
                print(f"    ✓ {len(transcript):,} chars")
            else:
                print(f"    ✗ No captions")
            time.sleep(1.5)

        if expert_data["videos"]:
            out = f"research/youtube-transcripts/{expert_name}_interviews.json"
            with open(out, "w", encoding="utf-8") as f:
                json.dump(expert_data, f, indent=2, ensure_ascii=False)
            print(f"  Saved: {out}")

            results_summary.append({
                "expert": expert_name,
                "videos_found": len(videos),
                "transcripts_collected": sum(1 for v in expert_data["videos"] if v["transcript_chars"] > 100),
                "file": out
            })

    print(f"\n{'='*60}")
    print("SUMMARY")
    for r in results_summary:
        print(f"  {r['expert']:<25} found: {r['videos_found']} | collected: {r['transcripts_collected']}")
    print(f"\nSupadata quota used this run: ~{quota_used}")