import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DATAFORSEO_LOGIN = os.getenv("DATAFORSEO_LOGIN")
DATAFORSEO_PASSWORD = os.getenv("DATAFORSEO_PASSWORD")

SEED_KEYWORDS = [
    "AI SEO",
    "AI content production",
    "programmatic SEO",
    "AI powered SEO",
    "generative engine optimization",
    "GEO SEO",
    "LLM SEO",
    "AI content strategy B2B",
    "topical authority SEO",
    "semantic SEO",
    "AI SEO content workflow",
    "automated content SEO",
    "AI search optimization",
    "AEO optimization",
    "SGE SEO strategy"
]

def get_keyword_volume(keywords):
    url = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
    payload = [{"keywords": keywords, "location_code": 2840, "language_code": "en"}]
    response = requests.post(
        url,
        auth=(DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD),
        json=payload
    )
    return response.json()

def parse_results(data):
    results = []
    try:
        items = data["tasks"][0]["result"]
        for item in items:
            if item.get("search_volume") is not None:
                results.append({
                    "keyword": item["keyword"],
                    "search_volume": item["search_volume"],
                    "competition": item.get("competition", "N/A"),
                    "competition_index": item.get("competition_index", 0),
                    "cpc": item.get("cpc", 0)
                })
    except Exception as e:
        print(f"Parse error: {e}")
    return results

if __name__ == "__main__":
    print("Fetching keyword volumes from DataForSEO...")
    data = get_keyword_volume(SEED_KEYWORDS)
    results = parse_results(data)

    if results:
        df = pd.DataFrame(results)
        df = df.sort_values("search_volume", ascending=False)

        print("\n=== KEYWORD VOLUME RESULTS ===")
        print(df.to_string(index=False))

        os.makedirs("research", exist_ok=True)
        df.to_csv("research/keyword_volumes.csv", index=False)
        print("\nSaved to research/keyword_volumes.csv")
    else:
        print("No results returned.")