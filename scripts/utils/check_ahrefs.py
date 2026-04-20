import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone

load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")
print(f"API Key loaded: {api_key[:10]}..." if api_key else "ERROR: No API key found")

yt = build("youtube", "v3", developerKey=api_key)

channel_id = "UCWquNQV8Y0_defMKnGKrFOQ"
cutoff = (datetime.now(timezone.utc) - timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
print(f"Cutoff: {cutoff}")
print(f"Channel: {channel_id}")

r = yt.search().list(
    channelId=channel_id,
    part="snippet",
    type="video",
    order="date",
    publishedAfter=cutoff,
    maxResults=20
).execute()

print(f"Total results: {r.get('pageInfo', {}).get('totalResults', 0)}")
print(f"Items returned: {len(r.get('items', []))}")

for item in r.get("items", []):
    print(f"  {item['snippet']['publishedAt'][:10]} | {item['id']['videoId']} | {item['snippet']['title']}")