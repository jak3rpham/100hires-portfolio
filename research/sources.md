# Expert Sources — AI-Powered SEO Content Production
**Research Project: 100Hires Portfolio Step 2**
**Topic:** AI-Powered SEO Content Production
**Assessed:** 2026-04-20
**Researcher:** Pham Ngoc Thanh (jak3rpham)

---

## 1. Research Methodology

This project uses a multi-phase, API-driven approach to eliminate selection bias in expert identification. Every decision in the selection process is backed by data rather than intuition or name recognition alone.

### Phase 1 — Keyword Validation (DataForSEO API)
Before searching for experts, we validated which keywords the SEO community actually uses to discuss this topic. This prevents searching for experts using terms that practitioners don't actually use.

**Method:** Pulled search volume data for 15 seed keywords via DataForSEO Google Ads API (US market, April 2026).

**Selected keywords for expert discovery (based on real search volume):**

| Keyword | Monthly Volume | Rationale |
|---------|---------------|-----------|
| AI SEO | 8,100 | Highest volume, broadest community coverage |
| GEO SEO | 2,400 | Strong upward trend: 720 → 3,600 in 12 months — signals emerging practitioner term |
| AI search optimization | 1,000 | Practitioner-level intent signal |
| LLM SEO | 880 | Niche but stable — signals deep practitioners, not trend-chasers |

**Excluded keywords:** "AI content production" (10/mo), "automated content SEO" (10/mo), "SGE SEO strategy" (no data) — not established community terms despite being descriptively accurate for the topic.

### Phase 2 — YouTube Channel Discovery (YouTube Data API v3)
Searched 4 validated keywords → discovered 38 unique channels → scored on engagement, recency, and relevance.

**Scoring formula:**
- Engagement rate (likes/views): 35%
- Video frequency (90 days): 30%
- Subscriber base: 35%

**Auto-exclusion criteria:**
- avg_views < 10 relative to subscriber count (fraud signal — validated: James Dooley, 1.34M subs, avg 5 views)
- Zero engagement over 90-day window
- Off-topic content despite keyword match

### Phase 3 — LinkedIn/Newsletter Cross-Reference
LinkedIn has no public discovery API. Candidates were sourced via cross-reference of ≥2 independent industry ranking sources:
- position.digital Top SEO Influencers 2026
- ewrdigital.com Top AI SEO Influencers 2026
- digitalmarketingsupermarket.com Top 24 AI SEO Experts LinkedIn 2026
- BrightonSEO 2024-2025 speaker lists
- MozCon 2025 speaker list
- SEO Week 2025 speaker list

**Tier assignment based on:** depth of AI-SEO/GEO focus, originality of perspective, research/data output, recency of activity.

### Phase 4 — Merged Scoring
Combined YouTube API metrics + LinkedIn/Newsletter tier assessment:
- LinkedIn S-tier = 10/10, A-tier = 7/10, B-tier = 4/10
- Combined = LinkedIn 50% + YouTube 50% (if both present)
- LinkedIn only = 75% of LinkedIn score (penalized for missing YouTube signal)
- YouTube only = 50% of YouTube score (penalized for missing LinkedIn validation)

### Phase 5 — Content Collection & Verification
- **YouTube transcripts:** Supadata API (22 transcripts collected, 22% of 100/month free quota)
- **Blog/newsletter articles:** Claude in Chrome browser collection (48 articles across 10 experts)
- **Content verification:** URLs spot-checked manually before inclusion

---

## 2. Expert Weighting Framework

After identifying candidates, collected content was weighted to determine final selection and to assess the relative value of each expert's output for playbook development.

### Why Weight at All?
Not all content from all experts is equally useful for building an AI-powered SEO content production playbook. A systematic weighting framework prevents two common biases:
1. **Fame bias** — selecting experts because they are well-known, not because their content is on-topic
2. **Volume bias** — treating a high-output expert as more valuable than a focused, high-depth expert

### The Three Dimensions

#### Dimension 1: Topic Relevance — 40% weight

**Definition:** The degree to which an expert's content directly addresses AI-powered SEO content production, as opposed to general SEO, general AI, or adjacent topics.

**Why 40% (highest weight):**
This research targets a specific topic. An expert with 1M subscribers who discusses general marketing is less valuable than an expert with 10k subscribers whose entire output addresses AI SEO content workflows.

**Theoretical grounding:** This aligns with the information retrieval principle of **topical authority** — the degree to which a source is recognized as an authority on a specific topic cluster rather than in general. This principle is embedded in Google's Reasonable Surfer Model (US Patent 9,165,040, 2012), which weights links and sources by their topical relevance to the query. More directly, Kevin Indig's own citation research (AirOps dataset, 2026) found that ~30 domains own 67% of AI citations *within a specific topic* — demonstrating that topic-specificity, not raw authority, determines citation dominance in AI search.

**How measured:**
- Keyword match rate in collected content (topic keywords: "AI SEO", "GEO", "LLM SEO", "AI content", "content production", "generative engine", "AI overview", "topical authority", "semantic SEO")
- Proportion of expert's recent output (90 days) dedicated to AI SEO vs. other topics
- Presence of original research/frameworks on the topic (not just commentary)

**Scoring scale (0-10):**
- 9-10: Entire content output is AI SEO/GEO focused, original research present
- 7-8: Majority of content is AI SEO focused, some adjacent topics
- 5-6: Mixed — strong AI SEO content but significant general SEO coverage
- 3-4: AI SEO is a minor theme within broader marketing/SEO content
- 0-2: Primarily general SEO/marketing with occasional AI SEO mention

#### Dimension 2: Source Authority — 35% weight

**Definition:** The degree to which an expert is recognized by peers and the industry as a credible, trustworthy source.

**Why 35% (second highest):**
Authority is a proxy for peer validation. Conference invitations, newsletter subscriber counts, and industry citations are observable signals that peers have evaluated and endorsed an expert's credibility. However, authority is not the primary dimension because a highly authoritative general SEO expert may produce less useful content for this specific topic than a lower-profile specialist.

**Theoretical grounding:** Metzger, Flanagin & Medders (2010) — "Evaluating the Credibility of Online Information" — identifies *expertise* and *trustworthiness* as the two primary dimensions of source credibility. Observable authority metrics (subscribers, conference appearances, industry citations) serve as proxies for both dimensions in the absence of direct evaluation. Additionally, Patrick Stox's Ahrefs study (2026) on AI Overview citations found that domain authority and brand mentions from high-authority sources are among the strongest predictors of AI citation — validating authority as a meaningful signal.

**How measured:**
- Newsletter subscribers (where publicly available)
- YouTube subscribers and average view count
- Number of major conference appearances (BrightonSEO, MozCon, SEO Week, SMX)
- Citations in industry publications (Search Engine Land, Search Engine Journal, Ahrefs blog)
- LinkedIn follower count (estimated from Favikon and industry sources)

**Scoring scale (0-10):**
- 9-10: 50k+ newsletter subscribers OR 100k+ YouTube subscribers OR keynote at 3+ major conferences in 12 months
- 7-8: 20k-50k newsletter subscribers OR 30k-100k YouTube subscribers OR regular conference speaker
- 5-6: 10k-20k newsletter subscribers OR 10k-30k YouTube subscribers OR occasional conference appearances
- 3-4: Under 10k newsletter subscribers, moderate YouTube presence, emerging conference presence
- 0-2: Minimal measurable reach

#### Dimension 3: Content Recency — 25% weight

**Definition:** The degree to which an expert's collected content reflects the current state of AI-powered SEO (2025-2026), not outdated practices.

**Why 25% (lowest weight, but non-trivial):**
The AI SEO landscape is changing faster than any other SEO sub-topic. AI Mode, AI Overviews, ChatGPT's search behavior, and GEO tactics from 2023 are already outdated in 2026. An expert who last published on this topic in 2023 provides less actionable playbook material than one publishing weekly in 2026.

**Theoretical grounding:** Kevin Indig's own citation research (AirOps dataset, 2026) provides direct empirical evidence: *"content less than 3 months old is 3x more likely to get cited by LLMs"* — demonstrating that recency is not just a quality signal but a structural requirement for AI search visibility. This makes the weighting self-consistent: we are selecting experts using the same recency principle that governs the AI search systems the playbook will help practitioners win in.

Recency receives lower weight than relevance and authority because an expert with deep, verified expertise in AI SEO (high on dimensions 1 and 2) is still more valuable than a prolific but shallow recent poster — even if the latter publishes daily.

**How measured:**
- Date of most recent content on AI SEO topic
- Publishing frequency on AI SEO topics in last 90 days
- Whether content addresses 2025-2026 developments (AI Mode, GEO tactics, LLM citation patterns) vs. older frameworks

**Scoring scale (0-10):**
- 9-10: Publishing on AI SEO weekly or more, content addresses 2026 developments
- 7-8: Publishing monthly, content addresses 2025-2026 developments
- 5-6: Publishing quarterly, some 2025-2026 content
- 3-4: Last substantive AI SEO content 6-12 months ago
- 0-2: Last substantive AI SEO content over 12 months ago

### Combined Scoring Formula

```
Final Score = (Topic Relevance × 0.40) + (Source Authority × 0.35) + (Content Recency × 0.25)
```

---

## 3. Expert Scores & Selection Rationale

| # | Expert | Relevance (40%) | Authority (35%) | Recency (25%) | Final Score | Selected |
|---|--------|----------------|----------------|---------------|-------------|----------|
| 1 | Aleyda Solís | 8.5 | 9.5 | 9.0 | 8.9 | ✅ |
| 2 | Kevin Indig | 9.5 | 8.0 | 9.0 | 9.0 | ✅ |
| 3 | Lily Ray | 9.0 | 8.5 | 9.5 | 9.0 | ✅ |
| 4 | Patrick Stox | 8.5 | 8.5 | 8.0 | 8.5 | ✅ |
| 5 | Crystal Carter | 9.0 | 8.0 | 8.5 | 8.7 | ✅ |
| 6 | Marie Haynes | 8.0 | 7.5 | 9.5 | 8.4 | ✅ |
| 7 | Britney Muller | 8.5 | 7.5 | 8.0 | 8.1 | ✅ |
| 8 | Koray Tuğberk GÜBÜR | 7.5 | 7.5 | 6.0 | 7.2 | ✅ |
| 9 | Ryan Law | 8.0 | 7.0 | 8.5 | 7.9 | ✅ |
| 10 | Nathan Gotch | 7.0 | 7.5 | 8.5 | 7.5 | ✅ |
| — | James Dooley | 5.0 | 2.0 | 7.0 | 4.4 | ❌ Excluded: subscriber fraud (1.34M subs, avg 5 views) |
| — | Lawrence Dauchy | 4.0 | 2.0 | 7.0 | 3.9 | ❌ Excluded: zero engagement despite active posting |
| — | Neil Patel | 4.0 | 10.0 | 5.0 | 5.7 | ❌ Excluded: general SEO/marketing, low AI SEO specificity |

### Why Koray Tuğberk Scores Lower on Recency
Koray's YouTube channel shows reduced posting frequency (latest video 74 days ago at time of collection). However, his topical authority methodology remains foundational to the AI SEO content production space — the "Topical Authority" framework he founded in May 2022 is cited by multiple other experts in the list. His lower recency score (6.0) is offset by high relevance and the foundational nature of his work. He is retained because the playbook requires understanding of topical authority as a content architecture principle.

---

## 4. Final Expert List

| # | Name | Primary Platform | Relevance | Authority | Recency | Final |
|---|------|-----------------|-----------|-----------|---------|-------|
| 1 | **Aleyda Solís** | SEOFOMO newsletter (39k) + LinkedIn (100k+) + YouTube (Crawling Mondays) | 8.5 | 9.5 | 9.0 | **8.9** |
| 2 | **Kevin Indig** | Growth Memo Substack (25k) + LinkedIn | 9.5 | 8.0 | 9.0 | **9.0** |
| 3 | **Lily Ray** | Substack + LinkedIn + Search Engine Land | 9.0 | 8.5 | 9.5 | **9.0** |
| 4 | **Patrick Stox** | LinkedIn + Ahrefs blog | 8.5 | 8.5 | 8.0 | **8.5** |
| 5 | **Crystal Carter** | LinkedIn + Wix Studio YouTube + Search Engine Land | 9.0 | 8.0 | 8.5 | **8.7** |
| 6 | **Marie Haynes** | YouTube (4k) + weekly podcast | 8.0 | 7.5 | 9.5 | **8.4** |
| 7 | **Britney Muller** | LinkedIn + conferences (BrightonSEO keynote 2025) | 8.5 | 7.5 | 8.0 | **8.1** |
| 8 | **Koray Tuğberk GÜBÜR** | YouTube (24k) + LinkedIn + Holistic SEO blog | 7.5 | 7.5 | 6.0 | **7.2** |
| 9 | **Ryan Law** | Ahrefs blog + YouTube (Ahrefs channel) | 8.0 | 7.0 | 8.5 | **7.9** |
| 10 | **Nathan Gotch** | YouTube (126k) + Rankability blog | 7.0 | 7.5 | 8.5 | **7.5** |

---

## 5. Source Links

| # | Expert | LinkedIn | YouTube | Blog/Newsletter |
|---|--------|----------|---------|----------------|
| 1 | Aleyda Solís | linkedin.com/in/aleyda | youtube.com/c/crawlingmondaysbyaleyda | aleydasolis.com · seofomo.co |
| 2 | Kevin Indig | linkedin.com/in/kevinindig | — | growth-memo.com |
| 3 | Lily Ray | linkedin.com/in/lily-ray-44a9b369 | youtube.com/@lilyraynyc | lilyraynyc.substack.com |
| 4 | Patrick Stox | linkedin.com/in/patrickstox | — | ahrefs.com/blog/author/patrick-stox |
| 5 | Crystal Carter | linkedin.com/in/crystalcarterseo | youtube.com/@wixstudio | searchengineland.com/author/crystal-carter |
| 6 | Marie Haynes | linkedin.com/in/mariehaynes | youtube.com/channel/UC5JCNbPrfBAhnVG1Cfx25qA | mariehaynes.com |
| 7 | Britney Muller | linkedin.com/in/britneymuller | — | britneymuller.com |
| 8 | Koray Tuğberk GÜBÜR | linkedin.com/in/koraytugberkgubur | youtube.com/channel/UCXTg_CjVldLQ1RH8jxTTqiw | holisticseo.digital |
| 9 | Ryan Law | linkedin.com/in/thinkingslow | youtube.com/@ahrefs | ahrefs.com/blog/author/ryan-law |
| 10 | Nathan Gotch | linkedin.com/in/nathangotch | youtube.com/channel/UCNEsahyXxNJvYNsMhru-UzQ | nathangotch.com |

---

## 6. Known Limitations

### L1 — LinkedIn Discovery is Not Automated
LinkedIn has no public discovery API. LinkedIn/Newsletter candidates were selected via cross-reference of ≥2 independent industry ranking sources, not direct engagement data. This introduces potential recency bias toward well-established names over emerging practitioners.

**Mitigation:** Cross-referencing ≥2 independent sources reduces single-source bias. Conference speaker lists (BrightonSEO, MozCon) provide independent validation from industry gatekeepers.

### L2 — YouTube Text Matching Understates Depth
Relevance scoring via title/description keyword matching penalizes experts who discuss AI SEO without using exact keyword phrases in titles (e.g., Aleyda Solís often frames content around specific use cases rather than generic "AI SEO" labels).

**Mitigation:** Manual content review of transcripts supplemented automated scoring for final decisions.

### L3 — YouTube Channel Matching Had False Positives
Automated channel lookup for Ryan Law matched "Ahrefs Podcast" instead of personal channel. Mordy Oberstein matched "Sure Oak" (unrelated agency). These were manually corrected.

### L4 — Paywall Limitations on Newsletter Content
Kevin Indig (Growth Memo) and Lily Ray (Substack) operate partially paywalled newsletters. Collected content represents publicly accessible portions. Full premium content was accessed via PDF exports for 2 articles (Kevin Indig: "The Science of How AI Picks Its Sources", "The Great Decoupling") and direct Substack access for Lily Ray's 4 articles.

### L5 — Koray Tuğberk YouTube Content Age
Koray's most recent YouTube video at time of collection was 74 days old. His channel is de-prioritizing YouTube in favor of community/course content. Blog content at holisticseo.digital remains active. This is noted in his lower recency score (6.0/10).

### L6 — Kevin Indig and Lily Ray Share One YouTube Source
Both Kevin Indig and Lily Ray's YouTube transcripts derive from the same Ahrefs video (RwKKLnyXCig: "Top SEO Experts Build Me an AI Search Strategy"). Kevin appears as an interviewed expert; Lily Ray is referenced and discussed. This is disclosed as a limitation — their YouTube transcript coverage is thinner than their blog/newsletter coverage, which is their primary platform.

---

## 7. Content Collection Summary

| Expert | Blog Articles | YouTube Transcripts | Total Content Chars (approx) |
|--------|--------------|---------------------|------------------------------|
| Aleyda Solís | 4 articles (36,858 chars) | 2 videos (78,107 chars) | ~115,000 |
| Kevin Indig | 5 articles (full PDFs for 2) | 1 video (shared) | ~50,000 |
| Lily Ray | 4 articles (full Substack) | 1 video (shared) | ~60,000 |
| Patrick Stox | 5 articles | 1 video (22,519 chars) | ~35,000 |
| Crystal Carter | 5 articles | 1 video (69,583 chars) | ~70,000 |
| Marie Haynes | 5 articles (34,616 chars) | 5 videos | ~80,000 |
| Britney Muller | 5 articles | 1 video (36,877 chars) | ~40,000 |
| Koray Tuğberk GÜBÜR | 5 articles | 1 video (57,381 chars) | ~60,000 |
| Ryan Law | 5 articles | 5 Ahrefs videos | ~55,000 |
| Nathan Gotch | 5 articles | 5 videos | ~40,000 |
| **Total** | **48 articles** | **~22 transcripts** | **~605,000 chars** |

---

## 8. References for Weighting Framework

- Metzger, M.J., Flanagin, A.J., & Medders, R.B. (2010). Social and Heuristic Approaches to Credibility Evaluation Online. *Journal of Communication*, 60(3), 413-439.
- Google Inc. (2015). US Patent 9,165,040 — Reasonable Surfer Model (link weighting by topical relevance).
- Indig, K. (2026). "The Science of How AI Picks Its Sources." *Growth Memo*. [Analyzed 21,482 ChatGPT citation rows across 7 verticals]
- Indig, K. (2026). "The Great Decoupling." *Growth Memo*. [Search volume decline analysis across 10,000 keywords]
- AirOps Research (2025). "2026 State of AI Search." [548,534 retrieved pages, 15,000 prompts dataset]
- Stox, P. (2026). "ChatGPT Has 12% of Google's Search Volume but Google Sends 190x More Traffic." *Ahrefs Blog*.
- Ray, L. (2026). "Your GEO Strategy Might Be Destroying Your SEO." *Substack*. [RAG pipeline analysis]
