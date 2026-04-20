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
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

JULIA_CHANNEL_ID = "UCqzK60-oUOEq36uU9B1MMUg"

TOPIC_KEYWORDS = [
    "ai seo", "ai content", "geo", "llm seo", "generative engine",
    "ai search", "aeo", "topical authority", "semantic seo",
    "programmatic seo", "content production", "ai overview",
    "content strategy", "llmo", "ai visibility", "content creation",
    "ai writing", "content workflow", "ai tools"
]

def get_recent_videos(channel_id, days=90):
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        r = youtube.search().list(
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
        } for i in r.get("items", [])]
    except Exception as e:
        print(f"Error: {e}")
        return []

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

def is_relevant(title):
    return any(kw in title.lower() for kw in TOPIC_KEYWORDS)

def audit_expert(name, content):
    prompt = f"""You are evaluating an expert for a research project on "AI-powered SEO content production."

Expert: {name}

Below is a sample of their recent content:

---
{content[:6000]}
---

Analyze and return JSON only with these fields:

{{
  "TOPIC_RELEVANCE_SCORE": 0-10,
  "TOPIC_RELEVANCE_EVIDENCE": ["example1", "example2", "example3"],
  "ORIGINAL_RESEARCH": "yes/no/partial",
  "DEPTH_SCORE": 0-10,
  "UNIQUE_ANGLE": "1-2 sentences",
  "PLAYBOOK_VALUE": 0-10,
  "VALIDATION_VERDICT": "CONFIRM/BORDERLINE/REPLACE",
  "VERDICT_REASONING": "2-3 sentences"
}}"""

    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01"
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=60
    )

    if r.status_code == 200:
        text = r.json()["content"][0]["text"].strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    return None

if __name__ == "__main__":
    print("="*60)
    print("JULIA McCOY vs PATRICK STOX — Swap Decision")
    print("="*60)

    # Step 1: Check recency
    print("\n--- Step 1: Julia McCoy Channel Recency ---")
    videos = get_recent_videos(JULIA_CHANNEL_ID, days=90)
    print(f"Videos last 90 days: {len(videos)}")

    if not videos:
        print("Channel STALE — checking 180 days...")
        videos = get_recent_videos(JULIA_CHANNEL_ID, days=180)
        print(f"Videos last 180 days: {len(videos)}")

    for v in videos[:10]:
        relevant = "★" if is_relevant(v["title"]) else "○"
        print(f"  {relevant} [{v['published_at'][:10]}] {v['title'][:65]}")

    if not videos:
        print("No videos found. Julia McCoy channel inactive. Keeping Patrick Stox.")
        exit()

    # Step 2: Collect transcripts
    print("\n--- Step 2: Collecting Transcripts ---")
    relevant_videos = [v for v in videos if is_relevant(v["title"])]
    collect_list = relevant_videos[:5] if relevant_videos else videos[:5]

    julia_data = {
        "expert": "Julia McCoy",
        "channel_id": JULIA_CHANNEL_ID,
        "collected_at": datetime.now().isoformat(),
        "videos_90d": len(videos),
        "relevant_videos": len(relevant_videos),
        "videos": []
    }

    content_parts = []
    quota_used = 0

    for video in collect_list:
        print(f"  -> {video['title'][:60]}")
        transcript = get_transcript(video["video_id"])
        quota_used += 1

        julia_data["videos"].append({
            "title": video["title"],
            "url": video["url"],
            "published_at": video["published_at"],
            "transcript_chars": len(transcript) if transcript else 0,
            "transcript": transcript if transcript else "[No captions]"
        })

        if transcript:
            print(f"     OK {len(transcript):,} chars")
            content_parts.append(f"[YOUTUBE] {video['title']}\n{transcript[:2000]}")
        else:
            print(f"     No captions")
        time.sleep(1.5)

    # Save Julia's transcripts
    os.makedirs("research/youtube-transcripts", exist_ok=True)
    with open("research/youtube-transcripts/Julia_McCoy.json", "w", encoding="utf-8") as f:
        json.dump(julia_data, f, indent=2, ensure_ascii=False)

    print(f"\nSupadata quota used: ~{quota_used}")

    # Step 3: Run audit on Julia
    print("\n--- Step 3: Content Quality Audit ---")
    julia_content = "\n\n---\n\n".join(content_parts)

    if not julia_content.strip():
        print("Insufficient content for audit. Keeping Patrick Stox.")
        exit()

    print(f"Auditing Julia McCoy ({len(julia_content):,} chars)...")
    julia_audit = audit_expert("Julia McCoy", julia_content)

    if julia_audit:
        print(f"\nJulia McCoy Audit Results:")
        print(f"  Topic Relevance: {julia_audit['TOPIC_RELEVANCE_SCORE']}/10")
        print(f"  Depth: {julia_audit['DEPTH_SCORE']}/10")
        print(f"  Original Research: {julia_audit['ORIGINAL_RESEARCH']}")
        print(f"  Playbook Value: {julia_audit['PLAYBOOK_VALUE']}/10")
        print(f"  Verdict: {julia_audit['VALIDATION_VERDICT']}")
        print(f"  Reasoning: {julia_audit['VERDICT_REASONING']}")
        print(f"  Unique Angle: {julia_audit['UNIQUE_ANGLE']}")

    # Step 4: Compare with Patrick Stox
    print("\n--- Step 4: Swap Decision ---")
    print("\nPatrick Stox (from previous audit):")
    print("  Topic Relevance: 3/10")
    print("  Depth: 8/10")
    print("  Playbook Value: 4/10")
    print("  Verdict: REPLACE")

    if julia_audit:
        julia_tr = julia_audit.get("TOPIC_RELEVANCE_SCORE", 0)
        julia_pv = julia_audit.get("PLAYBOOK_VALUE", 0)
        patrick_tr = 3
        patrick_pv = 4

        print(f"\nComparison:")
        print(f"  {'Metric':<20} {'Julia McCoy':>12} {'Patrick Stox':>14}")
        print(f"  {'-'*46}")
        print(f"  {'Topic Relevance':<20} {julia_tr:>12}/10 {patrick_tr:>12}/10")
        print(f"  {'Playbook Value':<20} {julia_pv:>12}/10 {patrick_pv:>12}/10")

        if julia_tr > patrick_tr and julia_pv > patrick_pv:
            print(f"\n✅ DECISION: SWAP — Julia McCoy replaces Patrick Stox")
            print(f"   Julia scores higher on both Topic Relevance ({julia_tr} vs {patrick_tr}) and Playbook Value ({julia_pv} vs {patrick_pv})")
        elif julia_tr > patrick_tr:
            print(f"\n⚠️  BORDERLINE: Julia higher on relevance but check playbook value")
        else:
            print(f"\n❌ KEEP Patrick Stox — Julia does not score higher on key metrics")

    # Save comparison
    comparison = {
        "decision_date": datetime.now().isoformat(),
        "julia_mccoy_audit": julia_audit,
        "patrick_stox_audit": {
            "TOPIC_RELEVANCE_SCORE": 3,
            "DEPTH_SCORE": 8,
            "PLAYBOOK_VALUE": 4,
            "VALIDATION_VERDICT": "REPLACE",
            "VERDICT_REASONING": "Content focuses on AI impact on search traffic metrics rather than AI-powered content production workflows."
        }
    }

    with open("research/swap_decision.json", "w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2, ensure_ascii=False)
    print(f"\nComparison saved to research/swap_decision.json")