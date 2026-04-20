# AI-Powered SEO Content Production — Research Project
**100Hires Portfolio Project | Step 2**
**Researcher:** Pham Ngoc Thanh (jak3rpham)
**Completed:** April 20, 2026

---

## What This Project Is

This repository contains a data-driven research project identifying, validating, and collecting content from the top 10 experts in AI-powered SEO content production.

The goal: build a high-signal source library that can support a comprehensive playbook on how AI is transforming SEO content creation, distribution, and optimization.

**Topic chosen:** AI-Powered SEO Content Production — selected from the 8 options because it directly maps to practitioner experience (200%+ organic traffic growth using AI-assisted content workflows) and because it sits at the highest-demand intersection in the current search marketing landscape.

---

## Tools & APIs Used

| Tool | Purpose |
|------|---------|
| Python 3.14 | All scripting |
| YouTube Data API v3 | Channel discovery, video metrics, recency verification |
| DataForSEO API | Keyword volume validation |
| Supadata API | YouTube transcript extraction |
| Anthropic Claude API | Content quality audit (Phase 8) |
| Claude in Chrome | Blog article collection, LinkedIn post collection |
| Git + GitHub | Version control, regular commits |

---

## How the Expert List Was Built — Full Process

### Why a Process at All?
Selecting experts based on name recognition introduces fame bias. Someone with 1M subscribers who covers general AI is less useful for this specific topic than someone with 10k subscribers whose entire output is AI SEO content workflows. The selection process was designed to surface the latter.

### Phase 1 — Keyword Validation (DataForSEO API)
Before searching for experts, we validated which keywords the SEO practitioner community actually uses. This prevents searching for experts using terms that don't match real community usage.

15 seed keywords were pulled against Google Ads search volume data (US market). Results:

| Keyword | Monthly Volume | Decision |
|---------|---------------|----------|
| AI SEO | 8,100 | ✅ Use for discovery |
| GEO SEO | 2,400 | ✅ Use — strong upward trend |
| AI search optimization | 1,000 | ✅ Use |
| LLM SEO | 880 | ✅ Use — signals deep practitioners |
| AI content production | 10 | ❌ Exclude — not a community term |
| automated content SEO | 10 | ❌ Exclude |

Key insight: "AI content production" — the most descriptively accurate term — has essentially no search volume. Practitioners use "AI SEO" and "GEO SEO" instead. This shaped all downstream discovery.

### Phase 2 — YouTube Channel Discovery (YouTube Data API v3)
Searched 4 validated keywords → discovered 38 unique channels → scored each on:
- Engagement rate (likes/views): 35%
- Video frequency (90 days): 30%
- Subscriber base: 35%

**Auto-exclusions based on data:**
- James Dooley (1.34M subs, avg 5 views) — subscriber count fraud signal, excluded
- Lawrence Dauchy (36k subs, 0 engagement) — posting actively but no audience response
- Generic AI channels with SEO keyword matches but off-topic content

### Phase 3 — LinkedIn/Newsletter Cross-Reference
LinkedIn has no public discovery API. Candidates were sourced by cross-referencing ≥2 independent industry sources:
- Top SEO Influencers 2026 lists (position.digital, ewrdigital.com, digitalmarketingsupermarket.com)
- Conference speaker lists: BrightonSEO 2024-2025, MozCon 2025, SEO Week 2025
- Newsletter subscriber counts where publicly reported

### Phase 4 — Merged Scoring
Combined YouTube API metrics and LinkedIn/Newsletter tier scores into a single ranking. Experts with both YouTube presence and LinkedIn/Newsletter validation scored highest. YouTube-only experts were penalized 50% for missing LinkedIn signal; LinkedIn-only experts were penalized 25% for missing YouTube signal.

### Phase 5 — Content Collection (3 Sources)
For each candidate, content was collected from all available sources:

**YouTube transcripts** — Supadata API (22 transcripts, 22% of free quota used)
**Blog/newsletter articles** — Claude in Chrome browser collection (48 articles, 10 experts)
**LinkedIn posts** — Claude in Chrome browser collection (5 posts per expert, 10 experts)

Content collection revealed a key issue: several newsletter sources (Kevin Indig's Growth Memo, Lily Ray's Substack) are partially paywalled. Two Kevin Indig articles were accessed via PDF exports. Lily Ray's 4 articles were accessed via direct Substack session.

### Phase 6 — Expert Weighting Framework
Three dimensions were defined and weighted to score content value:

**Topic Relevance — 40%**
The highest weight because this research targets a specific topic. An expert with 1M subscribers covering general marketing is less valuable than a 10k-subscriber specialist whose entire output addresses AI SEO content workflows. Grounded in Google's Reasonable Surfer Model (US Patent 9,165,040) and Kevin Indig's own citation research showing ~30 domains own 67% of AI citations *within a specific topic*.

**Source Authority — 35%**
Conference invitations, newsletter subscribers, and industry citations are observable proxies for peer-validated expertise. Grounded in Metzger et al. (2010) — "Evaluating the Credibility of Online Information" — which identifies expertise and trustworthiness as the two primary dimensions of source credibility.

**Content Recency — 25%**
The AI SEO space changes faster than any other SEO sub-topic. Content from 2023 is already outdated in 2026. Grounded in Kevin Indig's own citation research (AirOps dataset, 2026): "content less than 3 months old is 3x more likely to get cited by LLMs" — making the weighting self-consistent with the research collected.

### Phase 7 — Content Quality Audit (Claude API)
After collecting content, a structured Claude API audit was run on each expert's material. The audit assessed: Topic Relevance, Original Research presence, Depth, Unique Angle, and Playbook Value.

Key audit findings:
- **Nathan Gotch** scored highest on Topic Relevance (9/10) — conducted original 487-result case study on AI-generated vs human content
- **Koray Tuğberk GÜBÜR** scored highest on Depth (9/10) — built 48 custom AI agents for semantic SEO workflows
- **Patrick Stox** scored lowest on Topic Relevance (3/10) — see Limitation section below

### Phase 8 — Swap Analysis (Patrick Stox vs Julia McCoy)
The audit flagged Patrick Stox for potential replacement. Julia McCoy (285k YouTube subscribers, highest avg_views/sub ratio in YouTube discovery phase) was evaluated as the leading replacement candidate.

Full validation was run: YouTube channel recency check, transcript collection, blog article collection, and Claude API audit.

**Result: SWAP REJECTED.** Julia McCoy's channel shows a clear content pivot — her 90-day video titles ("God over AI", "I Cloned Myself", "AI Layoffs Are About to 9X") indicate a move toward general AI/personal branding content, away from AI SEO content production. Her Playbook Value scored 3/10 vs Patrick Stox's 4/10.

Patrick Stox was retained with role re-framing (see Expert Roles section).

---

## Final Expert List

### Expert Roles
Experts cluster into 4 distinct roles. All 10 are retained because each covers a perspective the others don't — removing any creates a playbook blind spot.

**Role 1: AI Content Production Practitioners**
Direct expertise in using AI tools for SEO content creation workflows.
- Nathan Gotch, Koray Tuğberk GÜBÜR, Britney Muller, Ryan Law

**Role 2: AI Search Optimization Strategists**
Expertise in optimizing content for AI search visibility and LLM citation.
- Kevin Indig, Crystal Carter, Lily Ray

**Role 3: AI Search Infrastructure & Discovery**
Technical perspective on how AI systems crawl, discover, and surface content.
- Aleyda Solís, Marie Haynes

**Role 4: AI Search Behavior Data**
Large-scale empirical research on AI search behavior and traffic patterns.
- Patrick Stox

### Expert Profiles

**1. Kevin Indig** — Growth Memo Substack (25k subscribers)
*Role: AI Search Optimization Strategist*
Audit scores: Topic Relevance 7/10 | Playbook Value 9/10 | Original Research: Yes
Why selected: Produces original large-scale empirical research on how LLMs select and cite content. Key study: 21,482 ChatGPT citation rows analyzed to find that top 30 domains own 67% of AI citations per topic. His data-scientist approach provides the evidence base for content architecture decisions in the playbook.
Expected contribution: Frameworks for structuring content to maximize AI citation probability; data on content length, page positioning, and topical concentration effects on LLM visibility.

**2. Koray Tuğberk GÜBÜR** — YouTube (24k) + Holistic SEO blog
*Role: AI Content Production Practitioner*
Audit scores: Topic Relevance 8/10 | Playbook Value 9/10 | Original Research: Yes
Why selected: Founded the Topical Authority methodology (May 2022), now foundational to AI SEO content architecture. Built "Koray's Agents" — 48 custom ChatGPT tools for semantic SEO workflows covering linguistic analysis, entity mapping, and SEO auditing. Combines deep semantic SEO theory with practical AI tool development.
Expected contribution: Topical authority content architecture; semantic SEO implementation with AI tools; entity-based content optimization frameworks.

**3. Nathan Gotch** — YouTube (126k) + Rankability blog
*Role: AI Content Production Practitioner*
Audit scores: Topic Relevance 9/10 | Playbook Value 9/10 | Original Research: Yes
Why selected: Highest Topic Relevance score in the audit (9/10). Conducted original 487-result Google case study on whether AI content gets penalized; tested 15 AI SEO tools with structured evaluation criteria; published "AI SEO For Dummies" (Wiley, 2025). Most directly focused on AI content production workflows of all experts in the list.
Expected contribution: Practical AI content production workflows; tool comparisons with real performance data; multi-platform AI search optimization (ChatGPT, Gemini, Perplexity).

**4. Britney Muller** — Conferences + LinkedIn
*Role: AI Content Production Practitioner*
Audit scores: Topic Relevance 7/10 | Playbook Value 8/10 | Original Research: Yes
Why selected: Background combines Moz Senior SEO Scientist (technical SEO depth) with Hugging Face (ML/LLM expertise) — unique combination in the list. Builds practical AI tools for marketers (Google Colab notebooks for Reddit analysis, keyword insight extraction). BrightonSEO San Diego 2025 keynote. Argues that "LLMs are non-deterministic probability machines" and that practitioners are "rediscovering SEO through AI" — important critical framing.
Expected contribution: AI tool building for SEO workflows; ML-informed perspective on how LLMs actually process content; practical implementation with free/open tools.

**5. Ryan Law** — Ahrefs blog + YouTube (Ahrefs channel)
*Role: AI Content Production Practitioner*
Audit scores: Topic Relevance 7/10 | Playbook Value 8/10 | Original Research: Yes
Why selected: Director of Content Marketing at Ahrefs — produces AI content at enterprise scale with full transparency about methodology. Key content: "My Complete AI Content Process for Ahrefs" (workflow deep dive), 900K AI-generated pages study, AI Overviews click reduction research (58% CTR drop). Combines macro-level industry data with tactical implementation.
Expected contribution: Enterprise AI content production workflows; data on AI content quality thresholds; AI Overviews impact on content strategy.

**6. Crystal Carter** — Wix Studio YouTube + Search Engine Land + LinkedIn
*Role: AI Search Optimization Strategist*
Audit scores: Topic Relevance 7/10 | Playbook Value 7/10 | Original Research: Partial
Why selected: Role title "Head of AI Search & SEO Communications" at Wix — one of the few practitioners with an explicitly AI search-focused job title. Developed GEO framework with documented 15% LLM visibility uplift within one week. SEO Week 2025 talk on Deepseek and Generative Search Optimization. Enterprise-scale product lens from Wix's massive user base.
Expected contribution: GEO framework and implementation methodology; LLM visibility measurement; enterprise-scale AI search optimization.

**7. Lily Ray** — Substack + LinkedIn + Search Engine Land
*Role: AI Search Optimization Strategist*
Audit scores: Topic Relevance 6/10 | Playbook Value 7/10 | Original Research: Partial
Why selected: Led AEO/GEO/LLMO practice launch at Amsive (2025). MozCon 2025 speaker. Provides the critical quality control perspective absent from other experts — her research documents GEO tactics that *damage* SEO performance (scaled AI content, self-promotional listicles, artificial refreshing). Her "AI Slop Loop" analysis and GEO Strategy research are essential cautionary content for any responsible playbook.
Expected contribution: Risk assessment of AI SEO tactics; Google algorithm response to AI content at scale; RAG pipeline implications for content strategy.

**8. Aleyda Solís** — SEOFOMO newsletter (39k) + LinkedIn (100k+) + Crawling Mondays YouTube
*Role: AI Search Infrastructure & Discovery*
Audit scores: Topic Relevance 6/10 | Playbook Value 7/10 | Original Research: Partial
Note: Audit scored BORDERLINE. Retained because her technical SEO audit perspective on AI crawlability and content discoverability is not covered by other experts. Focuses on the "consumption side" — how AI systems find and surface content — which is necessary context for content production decisions.
Why selected: #1 SEO voice globally per Favikon (2026), 200+ conference appearances in 30+ countries, creator of LearningSEO.io and LearnAISearch.com. SEOFOMO newsletter is the most widely read SEO newsletter in the industry. Her 10-step AI Search Content Optimization Checklist is an industry reference document.
Expected contribution: Technical infrastructure for AI content discoverability; international/enterprise AI search optimization; comprehensive AI search optimization checklists and frameworks.

**9. Marie Haynes** — YouTube (4k) + weekly podcast + mariehaynes.com
*Role: AI Search Strategic Implications*
Audit scores: Topic Relevance 7/10 | Playbook Value 6/10 | Original Research: Partial
Note: Audit scored BORDERLINE. Retained because her agentic search strategic framing is not covered by other experts. Focuses on where AI search is going (agentic web, WebMCP, Google Agent2Agent) rather than where it is now.
Why selected: Former veterinarian turned SEO expert — background gives her an outsider's precision when examining Google's systems. Weekly "Search News You Can Use" podcast covering agentic AI developments. Built 50+ custom AI tools (Gems). Thesis: "the agentic web is replacing GEO as the frontier" — forward-looking perspective essential for a playbook with strategic relevance beyond 2026.
Expected contribution: Agentic search implications for content strategy; forward-looking AI search framework; practical AI tool building for SEO analysis.

**10. Patrick Stox** — LinkedIn + Ahrefs blog
*Role: AI Search Behavior Data*
Audit scores: Topic Relevance 3/10 | Playbook Value 4/10 | Original Research: Yes
⚠️ **Limitation note:** Patrick Stox received the lowest Topic Relevance score in the audit (3/10). His content focuses on AI's *impact on search traffic metrics* rather than AI-powered content production workflows. A REPLACE verdict was initially issued and Julia McCoy (285k YouTube subs) was evaluated as replacement. Swap was rejected after full validation revealed Julia McCoy has pivoted to general AI/personal branding content (Playbook Value 3/10, content pivot confirmed).
Why retained: Patrick's large-scale empirical research (55.8M AI Overviews study; ChatGPT vs Google traffic analysis showing ChatGPT has 12% of Google's search volume but Google sends 190x more traffic) provides the foundational measurement layer that practitioners in Roles 1-3 cite and build on. His data answers "does AI search actually matter for traffic?" — a prerequisite question for any content production investment decision.
Expected contribution: Empirical baseline data on AI search traffic; AI Overviews positioning analysis; ChatGPT vs Google search volume and traffic benchmarks.

---

## Repository Structure

```
100hires-portfolio/
├── README.md                          # This file
├── .gitignore                         # Excludes .env (API keys)
│
├── scripts/
│   ├── pipeline/                      # Core workflow — run in order
│   │   ├── phase1_keyword_research.py     # DataForSEO keyword validation
│   │   ├── phase2_youtube_discovery.py    # YouTube channel discovery (38 channels)
│   │   ├── phase3_channel_scoring.py      # Engagement + recency scoring
│   │   ├── phase4_relevance_check.py      # Keyword relevance scoring
│   │   ├── phase5_merge_scoring.py        # LinkedIn + YouTube merged scoring
│   │   ├── phase6_collect_transcripts.py  # YouTube transcript collection (Supadata)
│   │   ├── phase7_expand_transcripts.py   # Interview appearance discovery
│   │   ├── phase7b_targeted.py            # Targeted transcript collection
│   │   └── phase8_content_audit.py        # Claude API content quality audit
│   │
│   └── utils/                         # Auxiliary scripts (branch off main pipeline)
│       ├── check_ahrefs.py            # Phase 6: Ahrefs channel ID verification
│       ├── collect_ahrefs_videos.py   # Phase 6: Ahrefs targeted video collection
│       ├── update_content.py          # Phase 5: Full content update for blog articles
│       ├── julia_vs_patrick.py        # Phase 8: Swap candidate initial analysis
│       ├── julia_validation.py        # Phase 8: Julia McCoy full content validation
│       ├── print_audit.py             # Phase 8: Audit results display
│       └── add_anthropic_key.py       # Setup: API key configuration helper
│
└── research/
    ├── sources.md                     # Full methodology + weighting framework + expert scores
    ├── keyword_volumes.csv            # Phase 1: DataForSEO keyword data
    ├── youtube_candidates.csv         # Phase 2: 38 discovered channels
    ├── channel_scores.csv             # Phase 3: engagement + recency scores
    ├── channel_relevance.csv          # Phase 4: relevance scoring
    ├── final_candidates.csv           # Phase 5: merged LinkedIn + YouTube scores
    ├── transcript_collection_summary.csv
    ├── content_quality_audit.json     # Phase 8: Claude API audit results (all 10 experts)
    ├── swap_decision.json             # Phase 8: Julia vs Patrick initial comparison
    ├── swap_decision_final.json       # Phase 8: Julia vs Patrick final decision + evidence
    │
    ├── youtube-transcripts/           # YouTube + interview appearance transcripts
    │   ├── Ahrefs.json                # 5 videos incl. GEO strategy (Kevin Indig featured)
    │   ├── Aleyda_Solis_interviews.json   # Crawling Mondays + AI Search Roadmap talk
    │   ├── Britney_Muller_interviews.json
    │   ├── Crystal_Carter_interviews.json # Wix Studio: State of AI Search 2026
    │   ├── Kevin_Indig_interviews.json    # Featured in Ahrefs GEO expert video
    │   ├── Koray_Tugberk_GUBUR.json       # SEO Masterclass: Topical Authority
    │   ├── Lily_Ray_interviews.json       # Referenced in Ahrefs GEO expert video
    │   ├── Marie_Haynes.json              # 5 recent videos from own channel
    │   ├── Nathan_Gotch.json              # 5 AI SEO videos from own channel
    │   ├── Patrick_Stox_interviews.json   # Ahrefs Tutorials: GEO? AEO? LLMO?
    │   └── Julia_McCoy.json              # Swap analysis only — not in final list
    │
    ├── linkedin-posts/                # 5 recent AI SEO posts per expert
    │   ├── aleyda-solis.json
    │   ├── britney-muller.json
    │   ├── crystal-carter.json
    │   ├── kevin-indig.json
    │   ├── koray-tugberk-gubur.json
    │   ├── lily-ray.json
    │   ├── marie-haynes.json
    │   ├── nathan-gotch.json
    │   ├── patrick-stox.json
    │   └── ryan-law-thinkingslow.json
    │
    └── other/                         # Blog articles + newsletter posts per expert
        ├── aleyda_solis/              # 4 articles — aleydasolis.com
        ├── britney_muller/            # 5 articles — Search Engine Land
        ├── crystal_carter/            # 5 articles — Search Engine Land
        ├── kevin_indig/               # 5 articles — Growth Memo (2 full PDFs included)
        ├── koray_tugberk/             # 5 articles — holisticseo.digital + Medium
        ├── lily_ray/                  # 4 articles — Substack (full content)
        ├── marie_haynes/              # 5 articles — mariehaynes.com
        ├── nathan_gotch/              # 5 articles — rankability.com + gotchseo.com
        ├── patrick_stox/              # 5 articles — ahrefs.com
        └── ryan_law/                  # 5 articles — ahrefs.com
```

---

## Known Limitations

**L1 — LinkedIn discovery is not automated.** No public LinkedIn API exists. LinkedIn candidates were sourced via cross-reference of ≥2 independent industry sources, not direct engagement data.

**L2 — Kevin Indig and Lily Ray share one YouTube source.** Both experts' YouTube transcripts derive from the same Ahrefs video (RwKKLnyXCig). Kevin appears as an interviewed expert; Lily Ray is referenced in context. Their primary platforms are newsletter and Substack respectively — YouTube transcripts are supplementary.

**L3 — Patrick Stox Topic Relevance is low (3/10).** His content focuses on AI search traffic measurement rather than AI content production workflows. Retained as "AI Search Behavior Data" role after swap analysis rejected Julia McCoy as replacement. See swap_decision_final.json for full evidence trail.

**L4 — Koray Tuğberk YouTube posting frequency reduced.** Latest video was 74 days old at collection time. Blog content at holisticseo.digital remains active. Retained due to foundational nature of Topical Authority methodology.

**L5 — Paywall limitations.** Kevin Indig Growth Memo and Lily Ray Substack are partially paywalled. Full content accessed via PDF export (2 articles) and direct session (4 articles). Remaining articles contain partial content (snippets/previews).

**L6 — Britney Muller and Crystal Carter Search Engine Land articles are snippets.** Search Engine Land blocks automated collection. Articles contain 470-770 chars of preview text. Full content available at source URLs.

---

## Setup Completed (Step 1)

- Cursor IDE installed
- Claude Code for VS Code (Anthropic) + Codex (OpenAI) extensions installed
- Git for Windows configured
- Python 3.14 with: google-api-python-client, pandas, requests, python-dotenv, anthropic

---

## References

- Metzger, M.J., Flanagin, A.J., & Medders, R.B. (2010). Social and Heuristic Approaches to Credibility Evaluation Online. *Journal of Communication*, 60(3), 413-439.
- Google Inc. (2015). US Patent 9,165,040 — Reasonable Surfer Model.
- Indig, K. (2026). "The Science of How AI Picks Its Sources." *Growth Memo*.
- Indig, K. (2026). "The Great Decoupling." *Growth Memo*.
- AirOps Research (2025). "2026 State of AI Search." 548,534 retrieved pages dataset.
- Stox, P. (2026). "ChatGPT Has 12% of Google's Search Volume." *Ahrefs Blog*.
- Ray, L. (2026). "Your GEO Strategy Might Be Destroying Your SEO." *Substack*.
- Ray, L. (2026). "Is Google Finally Cracking Down on Self-Promotional Listicles?" *Substack*.