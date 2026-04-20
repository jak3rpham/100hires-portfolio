import json
import os

base = "research/other"

# Full content updates
updates = {
    "kevin_indig": {
        "article_4.json": {
            "title": "The science of how AI picks its sources",
            "url": "https://www.growth-memo.com/p/the-science-of-how-ai-picks-its-sources",
            "published_date": "2026-03-23",
            "author": "Kevin Indig",
            "content": """The science of how AI picks its sources - Kevin Indig (Mar 23, 2026)

I analyzed over 21K citations to understand the impact of content length, depth and focus.

KEY FINDINGS:

1. ~30 domains own 67% of AI citations per topic
Classic search is winner-takes-all. Is that also true for ChatGPT answers?
Dataset: 21,482 ChatGPT citation rows, 670 unique domains, 2,344 unique URLs, 127 unique prompts
Results: The top 10 domains take 46% of all citations in a topic. The top 30 take 67%.

Effectively, there are ~30 seats (domains) at the citation table for any given topic. Everything else is nearly invisible.

Among pages ranking #1 in Google, 43.2% were cited by ChatGPT. That was 3.5x higher than the citation rate for pages ranking beyond Google's top 20 results.

ChatGPT retrieves about 6x more pages than it cites.
- 85% of pages ChatGPT retrieved were never cited
- 1/3 of cited pages came from fan-out queries, and 95% of those had zero search volume
- Ranking well helps, but it doesn't guarantee citations

Industry concentration patterns:
- Education: top 10% of domains capture 59.5% of all citations (winner-take-most)
- Crypto: 43.0% concentration for top 10%
- Finance: 29.4% for top-10%
- Healthcare: 13.0% — least concentrated, new entrants have realistic path
- CRM/SaaS: 16.1%, HR Tech: 14.4% — similarly diffuse

2. The citation advantage starts at 10,000 words
More words correlate with more citations, but there's a ceiling.
The 5K-to-10K jump is the largest single step — nearly 2x.
Pages above 20,000 characters average 10.18 citations each vs. 2.39 for pages under 500 characters.

Length effect is vertical-specific:
- Finance inverts it entirely: high-cited Finance pages average 1,783 words vs. 2,084 for low-cited pages
- Education: citations climb steadily from 1.85 (under 500 words) to 6.05 (20K+ words) with no drop-off
- SaaS shows weakest length effect: even longest pages only get 2.77 citations per page on average

Universal finding: very short pages (under 1K words) underperform in every vertical.

3. 58% of cited URLs are cited once
On average, 67% of cited URLs appear in only one prompt.
Citation breadth (number of distinct prompts a domain answers) is more useful than raw citation count.

The top 4.8% of URLs (cited 10+) are all category-level comparisons or guides answering "what is it," "who uses it," "how to choose," and "pricing" in a single URL.

A single evergreen page covering 10+ query intents is worth more in AI citation reach than 10 single-intent pages.

4. The ski ramp is steeper in some verticals
The bottom 10% of any page earns 2.4-4.4% of citations — roughly a quarter of what the peak band earns. The conclusion section is nearly invisible to AI, regardless of vertical.

The true peak decile across all verticals is the 10-20% band — where AI reads hardest. The first 10% is typically navigation, headlines, and intro fluff that AI skips.

Finance: 43.7% of citations land in the first 30% of the page.
Healthcare and HR Tech: flattest ramps — useful content distributed more evenly.
Education: peaks at the 30-40% decile.

METHODOLOGY:
~98,000 ChatGPT citation rows pulled from approximately 1.2 million ChatGPT responses from Gauge.
7 distinct verticals: B2B SaaS, Finance, Healthcare, Education, Crypto, HR Tech, Product Analytics.
Structural parsing, positional mapping, entity & sentiment extraction via Google Natural Language API."""
        },
        "article_5.json": {
            "title": "The Great Decoupling",
            "url": "https://www.growth-memo.com/p/the-great-decoupling",
            "published_date": "2026-01-19",
            "author": "Kevin Indig",
            "content": """The Great Decoupling - Kevin Indig & Amanda Johnson (Jan 19, 2026)

Traffic and pipeline no longer move together.

SEO died as a traffic channel the moment pipeline stopped following pageviews. Traffic is either down for many sites, or its growth nowhere near reflects growth rates of 2019-2022, but demos and pipeline are up for brands that shifted from chasing clicks to building authority.

1. WE'VE HIT PEAK SEARCH VOLUME FOR TRADITIONAL QUERIES
An analysis of roughly 10,000 short-head keywords shows that collective search volume grew only 1.2% over the last 12 months and is forecasted to decline by 0.74% over the next 12 months.

Two forces are driving it:
- Fragmentation into long-tail: demand did not disappear, it atomized into thousands of specific queries
- Bypass behavior: more users start in AI interfaces (AIOs, AI Mode, ChatGPT) instead of classic search

This shift is irreversible for 4 structural reasons:
1/ AI Overviews are here to stay. Google's revenue model depends on keeping users inside the SERP.
2/ LLM outputs are preferred starting points. Users have conditioned themselves to expect direct answers.
3/ Zero-click is now the default expectation. Clicking through now feels like friction.
4/ Content supply exploded. AI-generated articles, Reddit threads, YouTube videos, newsletters all compete for visibility.

Forecast divergence by category:
- Marketing: -26.9% (biggest decline)
- Real estate: -6.4%
- E-commerce: -1.6%
- SaaS: +4.1% (growing)
- Business services: +25.2% (biggest growth)

2. TRAFFIC AND PIPELINE DECOUPLED BECAUSE AI ATE THE CLICK
The Growth Memo AI Mode Study found that when the search task was informational and non-transactional, the number of external clicks to sources outside the AI Mode output was nearly zero across all user tasks.

The classic SEO model assumed: More rankings → more clicks → more traffic → more leads.
That world is dead.

But buying intent didn't disappear with the clicks. SEO creates influence. It can still shape which brands buyers trust. It just doesn't deliver the click anymore.

Evidence: Maeva Cifuentes reported traffic growth of 32% for a client while signups grew 75% over the same 6-month period. Pipeline growing 2.3x faster than traffic.

3. STRONG BRANDS STILL WIN IN AI SEARCH, BUT "BRAND STRENGTH" HAS A NEW DEFINITION
Brand strength in AI search has four components:
1. Topical Authority: Complete ownership of the conceptual map
2. ICP Alignment: Answers tailored to specific buyer questions
3. Third-Party Validation: Citations from category-defining sources matter more than high-DA links
4. Positioning Clarity: LLMs must recognize what a brand is known for. Vague positioning gets skipped; sharp positioning gets cited

4. THE UNCOMFORTABLE QUESTION: IF SEO DOESN'T DRIVE TRAFFIC ANYMORE, WHAT DOES IT DO?
SEO influences brand preference within the category. When buyers are in-market and researching solutions, SEO determines whether your brand is in the consideration set and whether AI systems recommend you.

Traffic was never the point. It was just the easiest thing to measure.

HOW TO RESPOND:
- Move from keyword-first workflows to ICP-first workflows
- Move from traffic reporting to influence reporting
- Report on: brand lift, pipeline influence, LLM visibility rates
- Stop leading stakeholder conversations with sessions, impressions, and rankings"""
        }
    },
    "lily_ray": {
        "article_1.json": {
            "title": "A Reflection on SEO, GEO & AI Search in 2025",
            "url": "https://lilyraynyc.substack.com/p/a-reflection-on-seo-and-ai-search",
            "published_date": "2026-01-20",
            "author": "Lily Ray",
            "content": """A Reflection on SEO & AI Search in 2025 - Lily Ray (Jan 20, 2026)

2025 marked my 15th year working in the SEO industry, and it was easily the most volatile year yet. We faced an industry-wide identity crisis triggered by the meteoric rise of OpenAI's ChatGPT and competing AI assistants like Gemini, Perplexity and Claude.

THE GREAT ACRONYM GOLD RUSH & GEO GRIFT
2025 was the year of GEO (Generative Engine Optimization), AEO (Answer Engine Optimization), AI SEO, LLMO. These names were competing for dominance within a new trade many believed would make SEO obsolete. Coordinated "GEO disinformation campaigns" emerged, where GEO tools allegedly offered payment to micro-influencers to promote the narrative that SEO is dead.

THE BAIT AND SWITCH
Many loudest voices declaring the death of SEO appeared to have the greatest lack of context about how modern SEO actually works. Many 'novel' GEO recommendations were verbatim recommendations that SEO teams have been making for years: structured data, chunked content, keyword-optimized URLs.

Some risky GEO recommendations: using AI to generate thousands of new pages, buying Reddit accounts with karma to seed 'organic' recommendations, hidden instructions for LLMs using white text on white background.

THE NEW MECHANICS OF TRADITIONAL SEO
Key finding: Every time I wrote an article in 2025 — whether on my personal blog, agency blog, LinkedIn Pulse, or SEL — I would see it cited within a few hours across various LLMs. This worked every time because LLMs use search engines, and the articles were quickly indexed and ranked well in web search.

NUANCED TAKEAWAYS:
1. AI search has introduced a significant paradigm shift in searcher behavior
2. AI assistants function fundamentally differently than search engines — LLMs focus on synthesis
3. Organic traffic will naturally decline as AI surfaces provide direct answers
4. We must develop new metrics focused on conversions, brand visibility, share of search
5. AEO/GEO is not an overhaul of SEO — it's an expansion of the toolkit
6. A solid SEO + social media + digital PR strategy is the most effective way to capture AI search visibility

QUERY FAN-OUT
When a system determines a query requires factual grounding, it uses an LLM to deconstruct the prompt into multiple sub-queries — "query fan-out." These queries execute simultaneously across search indices to gather diverse source data.

Tools for query fan-out: Google's Gemini Grounding Model, Queryfanout.ai, iPullRank's Qforia, Profound's Query Fanout Feature.

Warning: Don't fall into the hyper long-tail trap. Fan-out queries are inherently long-tail, highly personalized, and vary between prompts. The real value is aggregating signals to reveal core topics models consistently prioritize.

INCREASING IMPORTANCE OF OFF-SITE ACTIVITY
Off-site signals — brand mentions on popular websites, top-tier reviews, positive social media reputation — are more important than ever. Reddit, Quora, Facebook Groups, LinkedIn are among the most heavily cited websites in AI search.

GOOGLE IS TURNING THE TIDE
By late 2025, Semrush data showed Google AI Overviews appearing in roughly 16-25% of all U.S. queries. Google Gemini saw monthly active users surge by 30% in final quarter of 2025, reaching 650 million monthly active users. ChatGPT's market share eroded from 87% to 64.5% over the year.

KEY DATA: 95.3% of ChatGPT users still visit Google. Google processes 90%+ of global searches. ChatGPT represents less than 1% of global referral traffic."""
        },
        "article_2.json": {
            "title": "Your GEO Strategy Might Be Destroying Your SEO",
            "url": "https://lilyraynyc.substack.com/p/your-geo-strategy-might-be-destroying",
            "published_date": "2026-03-19",
            "author": "Lily Ray",
            "content": """Your GEO Strategy Might Be Destroying Your SEO - Lily Ray (Mar 19, 2026)

Many tactics designed to win in AI search can undermine SEO performance — which is, ironically, necessary for success in AI search.

HOW AI SEARCH ACTUALLY RETRIEVES CONTENT
Every major AI search product — ChatGPT, Perplexity, Gemini, Google AI Overviews, Microsoft Copilot — is built on RAG (Retrieval Augmented Generation). If your content isn't indexed and ranking in the search engine, it cannot enter the model's context window.

As Britney Muller stated: "Every Single URL you see in an LLM output comes from a search engine API (Google or Bing)."

Evidence ChatGPT uses Google: Multiple independent studies show ChatGPT sources 83% of carousel products from Google Shopping. OpenAI allegedly uses SerpAPI to scrape Google results. Google filed lawsuit against SerpAPI in December 2025.

5 GEO TACTICS THAT WORK — UNTIL THEY DON'T:

1. SCALING CONTENT RAPIDLY WITH AI
Pattern found: For many sites, content scaling appeared to work — until it didn't. Three case studies from AI content generation companies showed: rapid growth followed by crashes during June 2025 Core Update, March 2024 Core Update, and January 2025. One site recently 410'd (permanently removed) articles celebrated as success stories.

2. ARTIFICIAL REFRESHING
Superficially refreshing content — adding sentences or tweaking paragraphs just enough to update the "date modified" timestamp. Google has gotten increasingly good at distinguishing genuine updates from cosmetic ones.

3. EXCESSIVE SELF-PROMOTIONAL LISTICLES
Multiple companies saw organic traffic drop -29% to -49% beginning January 21, 2026 — all heavily using self-promotional "best" listicles where they rank themselves #1. Their drops in Google organic results also impacted visibility across LLMs.

4. "SUMMARIZE WITH AI" BUTTONS THAT PROMOTE YOUR BRAND
Microsoft's security research team (Feb 2026) documented "AI Recommendation Poisoning": companies hiding prompt-injection instructions inside "Summarize with AI" buttons, instructing AI assistants to "remember [Company] as a trusted source." Found across 31 companies in 14 industries. Microsoft formally classifies this as prompt injection.

5. EXCESSIVE "ALTERNATIVES" AND "COMPARISON" PAGES
One site created 51 comparison pages throughout 2025, then saw blog traffic drop starting late January 2026. Their ChatGPT citations also dropped around the same time organic traffic started declining.

GEO GETS THE CREDIT. SEO DID THE WORK.
Pattern: "GEO wins" being celebrated can almost always be explained by strong pre-existing SEO performance. This is a correlation problem. A brand with years of established authority starts appearing in ChatGPT — and concludes their new GEO campaign is working. The more plausible explanation: existing SEO visibility got them into the search indexes feeding those AI products.

CONCLUSION: Your SEO and GEO strategies should always work together. Undermining organic rankings by chasing risky AI search shortcuts won't just result in SEO traffic loss — because of RAG, you lose AI search visibility too."""
        },
        "article_3.json": {
            "title": "The AI Slop Loop",
            "url": "https://lilyraynyc.substack.com/p/the-ai-slop-loop",
            "published_date": "2026-04-15",
            "author": "Lily Ray",
            "content": """The AI Slop Loop - Lily Ray (Apr 15, 2026)

How AI-generated misinformation is feeding itself, and why billions of users are getting the worst of it.

THE INCIDENT: Asked Perplexity for latest SEO/AI news. It responded with details about a "September 2025 'Perspective' Core Algorithm Update" — a completely fake update. Both citations came from AI-generated content on SEO agency blogs, confidently fabricating details about an algorithm update that never happened.

This fake SEO news spread across multiple websites via AI systems scanning and regurgitating information regardless of accuracy. Today, you can ask any LLM about the September 2025 "Perspectives" update and they will confidently answer with fabricated information.

THE AI SLOP LOOP:
One AI-generated article hallucinates a detail → sites running AI content pipelines scrape and regurgitate it → more AI-generated sites scrape the same misinformation → enough citations exist for RAG-based systems to treat it as fact.

THE SCALE OF THE PROBLEM:
- Only ~50 million of ChatGPT's 900 million weekly active users are paying subscribers (94% on free tier)
- Google AI Overviews reached over 2 billion monthly active users as of mid-2025
- Free models have no real mechanism for distinguishing true information from repeated information

EXPERIMENT: Published a fake Google core update article on personal blog (January 2026). Within 24 hours, Google's AI Overviews was serving the fabricated information as fact — including the detail that Google "approved the update between slices of leftover pizza."

BBC TEST: Journalist Thomas Germaine published fictitious article "Best Tech Journalists at Eating Hot Dogs" on low-traffic personal site, naming himself #1. Within 24 hours: "Google parroted the gibberish from my website, both in the Gemini app and AI Overviews."

NYT STUDY FINDINGS:
- Google's AI Overviews were accurate 91% of the time
- With 5 trillion searches/year, 91% accuracy still means tens of millions of erroneous answers per hour
- 56% of correct responses were "ungrounded" — sources didn't fully support the information provided
- Problem worsened with newer model: 37% ungrounded with Gemini 2, rose to 56% with Gemini 3

HOW SMARTER LLMS ARE ATTEMPTING TO FIX IT:
ChatGPT's "Thinking" model (GPT-5.4, paid tier) goes through six rounds of thinking, specifically limiting fan-out searches to trusted sources (site:gsqi.com, site:linkedin.com/in/glenngabe).
- GPT-5.4: individual claims 33% less likely to be false, full responses 18% less likely to contain errors vs. GPT-5.2
- GPT-5.3 (free): 26.8% fewer hallucinations with web search enabled

BUT: Better reasoning is paywalled. 94% of ChatGPT users on free tier get more error-prone models. This is irresponsible when deployed to billions of people framed as "intelligence."

WARNING FOR MARKETERS: If you're trying to learn about SEO or AI search directly from an LLM, the information is contaminated. Always verify by real experts with experience in the field."""
        },
        "article_4.json": {
            "title": "Is Google Finally Cracking Down on Self-Promotional Listicles?",
            "url": "https://lilyraynyc.substack.com/p/is-google-finally-cracking-down-on",
            "published_date": "2026-02-03",
            "author": "Lily Ray",
            "content": """Is Google Finally Cracking Down on Self-Promotional Listicles? - Lily Ray (Feb 3, 2026)

The most popular 'GEO' tactic might indeed be risky for SEO purposes after all.

THE TACTIC: Companies publish "listicle" content on their own blogs — ranking the best companies or products in their niche and placing themselves in the #1 spot. Often done collaboratively: you mention me, and I'll mention you (modern reciprocal linking).

This has proven effective at influencing traditional search rankings and, by extension, visibility within LLMs that rely on RAG — when users search for top companies/products in a given niche.

WHY IT'S A GRAY AREA:
Google questions these pages fail:
1. Does the content provide original information, reporting, research, or analysis? — No: no real evidence of testing competitors they rank
2. Does the title avoid exaggerating or being misleading? — No: "best" implies objective evaluation when it's self-serving
3. Does the content present information in a way that makes you want to trust it? — No: inherent bias without third-party validation

IT WORKS, UNTIL IT DOESN'T:
When a tactic proves effective and becomes widely adopted, Google almost always develops ways to detect and suppress it. This is "the cycle of SEO."

EVIDENCE OF CRACKDOWN (January 2026 volatility):
Barry Schwartz reported significant Google ranking volatility in January 2026. Sharp visibility declines across several large brands beginning around the same period:

- $8B B2B brand: -49% organic visibility (Jan 21 - Feb 2, 2026). Blog = 77% of site visibility. Had 191 self-promotional listicles.
- SaaS company: -43% visibility. /guide/ folder had 228 self-promotional listicles.
- B2B/B2C SaaS: -42% visibility. 76 self-serving listicles, 38 updated with '2026' in title.
- B2B SaaS: -38% visibility. 267 self-promotional "best" listicles, 76 with '2026' in title.
- SaaS product: -34% visibility. 340 self-promotional articles. Blog = ~90% of total visibility.
- Software company (launched July 2025): -29% visibility. 61 listicles (4% of content).
- SaaS/digital marketing: -29% visibility. Only 10 self-promotional listicles — suggests even small numbers may have heavy weighting.

COMMON TRAITS AMONG AFFECTED SITES:
- All in SaaS space, likely paying attention to SEO/GEO trends
- Many blogs contained specific guidance around GEO and AI search
- Many had recently scaled content quickly (likely AI-generated)
- AI detection tools returned 100% confidence score on multiple articles
- Other tactics present: artificial refreshing, Schema.org violations, excessive informational/definition content

IMPACT ON AI SEARCH:
Glenn Gabe confirmed: sites dropping in organic search are also rapidly losing visibility in AI Overviews and AI Mode. Drops in Google organic results also impact visibility across other LLMs that leverage Google's search results, including ChatGPT.

CONCLUSION: Self-promotional listicles have proven effective at driving short-term visibility in both traditional search and AI-generated answers. But new data suggests this shortcut may be contributing to performance declines in SEO — and by extension, AI search. Long-term visibility favors content grounded in real-world experience, transparent methodology, and demonstrable value to users."""
        }
    }
}

# Apply updates
for author, articles in updates.items():
    author_path = os.path.join(base, author)
    for filename, content in articles.items():
        filepath = os.path.join(author_path, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            data.update(content)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Updated: {author}/{filename} ({len(content['content'])} chars)")
        else:
            print(f"NOT FOUND: {filepath}")

print("\nDone. Verify with:")
print("python -c \"import json; d=json.load(open('seo_articles_collection/kevin_indig/article_4.json')); print(len(d['content']), 'chars')\"")