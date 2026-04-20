import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Julia McCoy's blog sources to check
JULIA_SOURCES = [
    "https://juliamccoy.com/blog/",
    "https://www.contentatscale.ai/blog/author/julia-mccoy/",
    "https://www.searchenginejournal.com/author/julia-mccoy/",
]

TOPIC_KEYWORDS = [
    "ai seo", "ai content", "geo", "llm", "ai search",
    "content production", "content workflow", "aeo",
    "ai writing", "content strategy", "ai tools seo",
    "programmatic", "topical authority", "semantic"
]

def fetch_page(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        if r.status_code == 200:
            return r.text
        return None
    except:
        return None

def extract_links_and_titles(html, base_keyword=""):
    """Simple extraction of article links and titles from HTML"""
    import re
    # Find article titles and URLs
    pattern = r'href=["\']([^"\']*)["\'][^>]*>([^<]{10,100})</a>'
    matches = re.findall(pattern, html)
    results = []
    for url, title in matches:
        title = title.strip()
        if any(kw in title.lower() for kw in TOPIC_KEYWORDS):
            if url.startswith("http") or url.startswith("/"):
                results.append({"url": url, "title": title})
    return results[:10]

def audit_julia_full(content):
    prompt = f"""You are evaluating Julia McCoy as an expert for a research project on "AI-powered SEO content production."

Below is a comprehensive sample of her recent content:

---
{content[:7000]}
---

Key question: Is Julia McCoy's CURRENT focus (2025-2026) on AI-powered SEO content production specifically, or has she pivoted to general AI/personal branding content?

Return JSON only:
{{
  "CURRENT_FOCUS": "AI SEO content production / General AI / Personal brand / Mixed",
  "TOPIC_RELEVANCE_SCORE": 0-10,
  "TOPIC_RELEVANCE_EVIDENCE": ["example1", "example2"],
  "CONTENT_PIVOT_DETECTED": true/false,
  "PIVOT_EVIDENCE": "description if pivot detected",
  "ORIGINAL_RESEARCH": "yes/no/partial",
  "DEPTH_SCORE": 0-10,
  "UNIQUE_ANGLE": "1-2 sentences",
  "PLAYBOOK_VALUE": 0-10,
  "VALIDATION_VERDICT": "CONFIRM/BORDERLINE/REPLACE",
  "VERDICT_REASONING": "2-3 sentences — specifically address whether she should replace Patrick Stox"
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
    print("JULIA McCOY — Full Content Validation")
    print("="*60)

    content_parts = []

    # Load existing YouTube transcript
    yt_file = "research/youtube-transcripts/Julia_McCoy.json"
    if os.path.exists(yt_file):
        with open(yt_file) as f:
            yt_data = json.load(f)
        for v in yt_data.get("videos", []):
            t = v.get("transcript", "")
            if t and t != "[No captions]":
                content_parts.append(f"[YOUTUBE] {v['title']}\n{t[:2000]}")
        print(f"YouTube: {len(yt_data.get('videos', []))} videos loaded")

    # Try fetching blog content
    print("\nFetching blog content...")
    for source_url in JULIA_SOURCES:
        print(f"  Trying: {source_url}")
        html = fetch_page(source_url)
        if html:
            links = extract_links_and_titles(html)
            print(f"  Found {len(links)} relevant article links")
            for link in links[:3]:
                print(f"    - {link['title'][:60]}")
                # Try to fetch article content
                art_url = link["url"] if link["url"].startswith("http") else f"https://juliamccoy.com{link['url']}"
                art_html = fetch_page(art_url)
                if art_html:
                    # Extract text roughly
                    import re
                    text = re.sub(r'<[^>]+>', ' ', art_html)
                    text = re.sub(r'\s+', ' ', text).strip()[:2000]
                    content_parts.append(f"[BLOG] {link['title']}\nURL: {art_url}\n{text}")
        else:
            print(f"  Could not fetch (bot protection)")

    # Add YouTube video titles as signal even without full transcripts
    print("\nYouTube video titles (last 90 days) as topic signal:")
    recent_titles = [
        "Scientists Just Cut AI Energy Use By 100x",
        "AI Layoffs Are About to 9X",
        "God over AI",
        "I Cloned Myself — And It Freed Me From the Hustle",
        "The 2027 Founder — Why Your Personal Brand Is Your Most Valuable",
        "I Gave Replit Agent 4 One Idea. It Built Me an Entire Business.",
        "The 3 AI Skills That Will Be Worth $500K in 2027",
        "Recall: Everyone Has the Same AI — So What's the Edge?",
        "AI Just Triggered 15,341 Layoffs in One Month",
        "Why Your Business Will Be Invisible by 2027 (The AI Search Apocalypse)",
        "AI Layoffs Are About to 9X",
        "See you in Phoenix Saturday?"
    ]

    titles_text = "Recent YouTube video titles (April 2026):\n" + "\n".join(f"- {t}" for t in recent_titles)
    content_parts.append(f"[YOUTUBE TITLES SIGNAL]\n{titles_text}")

    print(f"\nTotal content assembled: {sum(len(p) for p in content_parts):,} chars")

    # Run full audit
    print("\nRunning full audit...")
    full_content = "\n\n---\n\n".join(content_parts)
    audit = audit_julia_full(full_content)

    if audit:
        print(f"\n{'='*60}")
        print("FULL AUDIT RESULTS")
        print(f"{'='*60}")
        print(f"Current Focus: {audit.get('CURRENT_FOCUS')}")
        print(f"Content Pivot Detected: {audit.get('CONTENT_PIVOT_DETECTED')}")
        print(f"Pivot Evidence: {audit.get('PIVOT_EVIDENCE')}")
        print(f"Topic Relevance: {audit.get('TOPIC_RELEVANCE_SCORE')}/10")
        print(f"Depth: {audit.get('DEPTH_SCORE')}/10")
        print(f"Original Research: {audit.get('ORIGINAL_RESEARCH')}")
        print(f"Playbook Value: {audit.get('PLAYBOOK_VALUE')}/10")
        print(f"Verdict: {audit.get('VALIDATION_VERDICT')}")
        print(f"Reasoning: {audit.get('VERDICT_REASONING')}")

        print(f"\n{'='*60}")
        print("FINAL SWAP DECISION")
        print(f"{'='*60}")
        julia_pv = audit.get("PLAYBOOK_VALUE", 0)
        julia_tr = audit.get("TOPIC_RELEVANCE_SCORE", 0)

        if julia_tr >= 7 and julia_pv >= 7 and not audit.get("CONTENT_PIVOT_DETECTED"):
            print("✅ SWAP CONFIRMED — Julia McCoy replaces Patrick Stox")
        elif audit.get("CONTENT_PIVOT_DETECTED"):
            print("❌ SWAP REJECTED — Content pivot detected. Julia McCoy has moved away from AI SEO content production.")
            print("   Keeping Patrick Stox with BORDERLINE re-framing (Role 4: AI Search Behavior Data).")
        else:
            print(f"⚠️  BORDERLINE — Julia TR: {julia_tr}/10, PV: {julia_pv}/10. Manual review recommended.")

        # Save final decision
        with open("research/swap_decision_final.json", "w", encoding="utf-8") as f:
            json.dump({
                "decision_date": datetime.now().isoformat(),
                "julia_full_audit": audit,
                "patrick_stox_audit": {
                    "TOPIC_RELEVANCE_SCORE": 3,
                    "PLAYBOOK_VALUE": 4,
                    "VERDICT": "REPLACE"
                }
            }, f, indent=2, ensure_ascii=False)
        print("\nSaved to research/swap_decision_final.json")