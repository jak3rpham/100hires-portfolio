import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
SUPADATA_API_KEY = os.getenv("SUPADATA_API_KEY")

VIDEOS = [
    {"id": "tiW6xRYSXmM", "title": "SEO in 2026: How I'd Rank in Google in the AI Era"},
    {"id": "KjK5-L-wDVg", "title": "Keyword Research Tutorial for Google and AI SEO"},
    {"id": "3iNJeArrUu4", "title": "I Outsourced our Digital Marketing to AI. Here's What Happened"},
    {"id": "lgUrHqaPrhU", "title": "How they use YouTube SEO to Get Millions of Views"},
]

def get_transcript(video_id):
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
        return content
    print(f"  Error {r.status_code}: {r.text[:100]}")
    return None

os.makedirs("research/youtube-transcripts", exist_ok=True)

# Load existing Ahrefs file if exists
ahrefs_file = "research/youtube-transcripts/Ahrefs_GEO_Strategy.json"
if os.path.exists(ahrefs_file):
    with open(ahrefs_file, "r", encoding="utf-8") as f:
        ahrefs_data = json.load(f)
    # Convert to multi-video format
    if "videos" not in ahrefs_data:
        ahrefs_data = {
            "expert": "Ahrefs",
            "channel_id": "UCWquNQV8Y0_defMKnGKrFOQ",
            "channel_url": "https://www.youtube.com/@AhrefsCom",
            "videos": [{
                "title": ahrefs_data.get("video_title", ""),
                "url": ahrefs_data.get("url", ""),
                "experts_featured": ahrefs_data.get("experts_featured", []),
                "transcript_chars": len(ahrefs_data.get("transcript", "")),
                "transcript": ahrefs_data.get("transcript", "")
            }]
        }
else:
    ahrefs_data = {
        "expert": "Ahrefs",
        "channel_id": "UCWquNQV8Y0_defMKnGKrFOQ",
        "channel_url": "https://www.youtube.com/@AhrefsCom",
        "videos": []
    }

print("Collecting Ahrefs video transcripts...\n")
quota_used = 0

for video in VIDEOS:
    print(f"-> {video['title']}")
    transcript = get_transcript(video["id"])
    quota_used += 1

    if transcript:
        print(f"   OK {len(transcript):,} chars")
        ahrefs_data["videos"].append({
            "title": video["title"],
            "url": f"https://www.youtube.com/watch?v={video['id']}",
            "transcript_chars": len(transcript),
            "transcript": transcript
        })
    else:
        print(f"   No transcript")
        ahrefs_data["videos"].append({
            "title": video["title"],
            "url": f"https://www.youtube.com/watch?v={video['id']}",
            "transcript_chars": 0,
            "transcript": "[No captions available]"
        })

with open("research/youtube-transcripts/Ahrefs.json", "w", encoding="utf-8") as f:
    json.dump(ahrefs_data, f, indent=2, ensure_ascii=False)

print(f"\nSaved to research/youtube-transcripts/Ahrefs.json")
print(f"Total videos: {len(ahrefs_data['videos'])}")
print(f"Supadata quota used this run: ~{quota_used}")