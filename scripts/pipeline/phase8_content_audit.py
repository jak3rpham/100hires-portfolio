import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Use Anthropic API key - need to add to .env
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

EXPERTS = [
    "aleyda_solis",
    "kevin_indig", 
    "lily_ray",
    "patrick_stox",
    "crystal_carter",
    "marie_haynes",
    "britney_muller",
    "koray_tugberk",
    "ryan_law",
    "nathan_gotch"
]

EXPERT_NAME_MAP = {
    "aleyda_solis": "Aleyda Solís",
    "kevin_indig": "Kevin Indig",
    "lily_ray": "Lily Ray",
    "patrick_stox": "Patrick Stox",
    "crystal_carter": "Crystal Carter",
    "marie_haynes": "Marie Haynes",
    "britney_muller": "Britney Muller",
    "koray_tugberk": "Koray Tuğberk GÜBÜR",
    "ryan_law": "Ryan Law",
    "nathan_gotch": "Nathan Gotch"
}

def load_expert_content(expert_key):
    """Load all collected content for an expert"""
    content_parts = []

    # Load blog articles
    blog_path = f"research/other/{expert_key}"
    if os.path.exists(blog_path):
        for fname in sorted(os.listdir(blog_path)):
            if fname.endswith(".json"):
                fpath = f"{blog_path}/{fname}"
                try:
                    with open(fpath, encoding="utf-8") as f:
                        data = json.load(f)
                    title = data.get("title", "")
                    url = data.get("url", "")
                    text = data.get("content", data.get("text", ""))[:3000]  # cap at 3000 chars per article
                    if text:
                        content_parts.append(f"[BLOG] {title}\nURL: {url}\n{text}")
                except:
                    pass

    # Load LinkedIn posts
    linkedin_files = [
        f"research/linkedin-posts/{expert_key.replace('_', '-')}.json",
        f"research/linkedin-posts/linkedin-posts/{expert_key.replace('_', '-')}.json",
        f"research/linkedin-posts/linkedin-posts/{expert_key.replace('_tugberk', '-tugberk-gubur').replace('_', '-')}.json",
        f"research/linkedin-posts/linkedin-posts/ryan-law-thinkingslow.json" if expert_key == "ryan_law" else None,
    ]
    for lpath in linkedin_files:
        if lpath and os.path.exists(lpath):
            try:
                with open(lpath, encoding="utf-8") as f:
                    data = json.load(f)
                posts = data if isinstance(data, list) else data.get("posts", [])
                for post in posts[:5]:
                    text = post.get("text", post.get("content", ""))[:500]
                    url = post.get("url", "")
                    date = post.get("date", "")
                    if text:
                        content_parts.append(f"[LINKEDIN] {date}\nURL: {url}\n{text}")
            except:
                pass
            break

    # Load YouTube transcripts
    yt_files = [
        f"research/youtube-transcripts/{EXPERT_NAME_MAP.get(expert_key, '').replace(' ', '_').replace('ğ', 'g').replace('Ğ', 'G').replace('ü', 'u').replace('Ü', 'U')}.json",
        f"research/youtube-transcripts/{expert_key.replace('_', '_').title()}_interviews.json",
        f"research/youtube-transcripts/{expert_key}_interviews.json",
    ]

    # Also check specific files
    specific_files = {
        "marie_haynes": "research/youtube-transcripts/Marie_Haynes.json",
        "nathan_gotch": "research/youtube-transcripts/Nathan_Gotch.json",
        "koray_tugberk": "research/youtube-transcripts/Koray_Tugberk_GUBUR.json",
        "aleyda_solis": "research/youtube-transcripts/Aleyda_Solis_interviews.json",
        "kevin_indig": "research/youtube-transcripts/Kevin_Indig_interviews.json",
        "lily_ray": "research/youtube-transcripts/Lily_Ray_interviews.json",
        "patrick_stox": "research/youtube-transcripts/Patrick_Stox_interviews.json",
        "crystal_carter": "research/youtube-transcripts/Crystal_Carter_interviews.json",
        "britney_muller": "research/youtube-transcripts/Britney_Muller_interviews.json",
        "ryan_law": "research/youtube-transcripts/Ahrefs.json",
    }

    yt_path = specific_files.get(expert_key)
    if yt_path and os.path.exists(yt_path):
        try:
            with open(yt_path, encoding="utf-8") as f:
                data = json.load(f)
            videos = data.get("videos", [])
            for video in videos[:2]:  # max 2 videos, first 2000 chars each
                title = video.get("title", "")
                transcript = video.get("transcript", "")[:2000]
                if transcript and transcript != "[No captions available]":
                    content_parts.append(f"[YOUTUBE] {title}\n{transcript}")
        except:
            pass

    return "\n\n---\n\n".join(content_parts[:8])  # max 8 content pieces


def analyze_expert(expert_key, expert_name, content):
    """Call Claude API to analyze expert content quality"""

    prompt = f"""You are evaluating an expert for a research project on "AI-powered SEO content production."

Expert: {expert_name}

Below is a sample of their recent content (blog articles, LinkedIn posts, YouTube transcripts):

---
{content[:6000]}
---

Please analyze this expert's content and provide a structured assessment with these exact fields:

1. TOPIC_RELEVANCE_SCORE (0-10): How specifically does this content address AI-powered SEO content production? Not general SEO, not general AI — specifically the intersection of AI tools and SEO content workflows.

2. TOPIC_RELEVANCE_EVIDENCE: 2-3 specific examples from the content that demonstrate their focus (or lack thereof) on this specific topic. Quote or paraphrase directly.

3. ORIGINAL_RESEARCH (yes/no/partial): Does this expert produce original data, studies, or frameworks — or primarily commentary on others' work?

4. ORIGINAL_RESEARCH_EVIDENCE: Specific example of original research/framework if present.

5. DEPTH_SCORE (0-10): How deep and actionable is the content? Does it go beyond surface-level observations?

6. DEPTH_EVIDENCE: Specific example of depth or shallowness.

7. UNIQUE_ANGLE: What perspective or angle does this expert bring that others in the list likely don't? (1-2 sentences)

8. PLAYBOOK_VALUE (0-10): How valuable would this expert's content be for building an AI-powered SEO content production playbook?

9. VALIDATION_VERDICT: CONFIRM (keep in final list) / BORDERLINE (keep but note limitations) / REPLACE (suggest replacing)

10. VERDICT_REASONING: 2-3 sentences explaining the verdict.

Format your response as JSON only, no other text."""

    response = requests.post(
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

    if response.status_code == 200:
        data = response.json()
        text = data["content"][0]["text"]
        # Clean JSON
        text = text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    else:
        print(f"  API error {response.status_code}: {response.text[:200]}")
        return None


if __name__ == "__main__":
    if not ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not found in .env")
        print("Add this line to your .env file:")
        print("ANTHROPIC_API_KEY=your_key_here")
        exit(1)

    os.makedirs("research", exist_ok=True)
    results = []

    print("="*60)
    print("PHASE 8 — Content Quality Audit via Claude API")
    print("="*60)

    for expert_key in EXPERTS:
        expert_name = EXPERT_NAME_MAP[expert_key]
        print(f"\nAnalyzing: {expert_name}")

        content = load_expert_content(expert_key)
        if not content:
            print(f"  WARNING: No content found for {expert_key}")
            continue

        print(f"  Content loaded: {len(content):,} chars")

        assessment = analyze_expert(expert_key, expert_name, content)

        if assessment:
            assessment["expert"] = expert_name
            assessment["expert_key"] = expert_key
            results.append(assessment)

            verdict = assessment.get("VALIDATION_VERDICT", "N/A")
            tr = assessment.get("TOPIC_RELEVANCE_SCORE", "N/A")
            pv = assessment.get("PLAYBOOK_VALUE", "N/A")
            print(f"  Verdict: {verdict} | Topic Relevance: {tr}/10 | Playbook Value: {pv}/10")
        else:
            print(f"  Failed to get assessment")

        time.sleep(2)  # Rate limiting

    # Save results
    output_file = "research/content_quality_audit.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print("AUDIT COMPLETE")
    print(f"{'='*60}")
    print(f"\n{'Expert':<25} {'TR':>4} {'PV':>4} {'Verdict'}")
    print("-" * 55)
    for r in sorted(results, key=lambda x: x.get("PLAYBOOK_VALUE", 0), reverse=True):
        print(f"{r['expert']:<25} {str(r.get('TOPIC_RELEVANCE_SCORE','?')):>4} {str(r.get('PLAYBOOK_VALUE','?')):>4}  {r.get('VALIDATION_VERDICT','?')}")

    print(f"\nFull results saved to: {output_file}")