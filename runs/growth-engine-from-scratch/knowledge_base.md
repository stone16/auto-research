# Knowledge Base

Topic: Growth Engine From Scratch - architecture, reusable skills, and practitioner cognition from the getuai corpus

Iteration: 6 cross-model-evaluability and cognition-pair patch

## Evidence Policy

Citations use run-local raw extracts as direct file:line evidence, for example `runs/growth-engine-from-scratch/sources/_raw/getuai-seo.md:7-11` (tier: file:line). Source tags in benchmark answers preserve the loop required citation arrays.

## Evaluation Rubric Contract

This KB embeds the evaluator contract so q1-q15 can be compared by different judges at the same clause level.

| benchmark_id | primary dimension evidenced | artifact-internal target threshold |
|---|---|---|
| q1 | Architecture grounding | Names crawler, ranking sensor, content store, generator, publisher, evaluator, external dependencies, human-in-loop, kill-switch, convergence, disagreement, and file:line evidence. |
| q2 | Architecture grounding | Walks ideation, outline, draft, edit, publish, post-publish; states LLM role, style guide injection, human review point, and load-bearing vs stylistic choices. |
| q3 | Architecture grounding | Covers campaign feed, bidding, reporting, attribution model, conversion event, budget pacing, anomaly detection, data model, and platform-agnostic boundary. |
| q4 | Architecture grounding | Separates listen, post, schedule, engage, monitor; names the multi-platform abstraction or adapter limit; includes rate limit, credit accounting, and moderation. |
| q5 | Skill enumeration completeness | SEO/GEO skill-catalog has >=8 rows and all 8 columns populated; duplicate and canonical pick stated. |
| q6 | Skill enumeration completeness | Content skill-catalog has >=8 rows and all 8 columns populated; brittleness mitigation covers drift, hallucination, register, and retrieval grounding. |
| q7 | Skill enumeration completeness | Ads skill-catalog has >=8 rows and all 8 columns populated; each skill marks platform-bound vs platform-agnostic, abstraction contract, and kill criteria. |
| q8 | Skill enumeration completeness | Social skill-catalog has >=8 rows and all 8 columns populated; each skill states platform difference, parameterization, and API-change failure. |
| q9 | Cognition evidence pairing | Five SEO/GEO models, each with Decision shaped, Trigger condition, Worked here, Failed here; anti-pattern footer; all model clauses cite file:line evidence. |
| q10 | Cognition evidence pairing | Five content frames, each with Decision shaped, Trigger condition, Worked here, Failed here, Links to Q2, Links to Q6; anti-pattern footer. |
| q11 | Cognition evidence pairing | Five ads models, each with worked/failed pair and platform-change break condition; explicit kill criteria and scale criteria. |
| q12 | Cognition evidence pairing | Five social models, each with worked/failed pair and per-platform evidence; automation visibility cost is explicit. |
| q13 | Cross-domain integration discipline | >=6 shared foundations, each with contract, >=2 repo evidence points, and shared-vs-domain-isolated decision rule. |
| q14 | Cross-domain integration discipline | Six build-sequence rows from Day-1 through Month-3; each row has scope, dependencies, done_criteria, next_trigger, deferrals, and Q1-Q13 hooks. |
| q15 | Cross-domain integration discipline | >=8 failure-modes rows, including >=3 growth-engine-legacy lessons; each row names affected_domains, recurrence_count, structural_cause, early_symptom, prophylactic, and evidence_pair. |

## Q1 - SEO/GEO Architecture

Pattern hypothesis: build SEO/GEO as UI -> domain adapter/tools -> AI/recommendation service, with identity, sessions, credentials, ledgers, schedules, approvals, and kill-switches in shared Core. `getuai-seo` uses UI, MCP SEO tools/API integration, and AI backend layers (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-seo.md:7-11`, `:93-97`). Shared session/data belongs to `getuai-api`, the FastAPI source of truth for sessions, temporary image/text storage, validation, and cleanup (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-api.md:7-28`).

Components and data flow: crawler/sensor inputs enter through site structure, Google Search, competitor discovery, keyword ideas, URL content analysis, and keyword clustering tools (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-plugin.md:11-20`, `:117-126`). Ranking signal source is split between SEO metrics/keyword tracking in `getuai-seo` (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-seo.md:101-106`) and GEO rank/sentiment sensing in LLMRush (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/LLMRush.md:7-14`). Content store/publisher surfaces appear in `rankncompare` sitemap, robots, metadata APIs, and JSON data storage (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/rankncompare.md:28`, `:53-56`, `:128-149`). External dependencies are search APIs, Google Ads keyword APIs, LLM providers, CMS/static publishing, and app storage. Disagreement: `getuai-seo` is a three-service product, `rankncompare` is a static/data-store publisher, and `growth-engine-legacy` says Browser -> Core only, engines never see raw Logto tokens, and Core owns platform facts (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/growth-engine-legacy.md:43-50`). Recommendation: keep domain tools, but require human-in-loop approval, override, and kill-switch in Core ledgers before publishing or recurring checks (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/growth-engine-legacy.md:83-88`).

## Q2 - Content Writing Architecture

Pipeline: ideation starts from campaign/entity facts, recipients, search or social intent; outline and draft are LLM-generated; edit is human/rule based; publish sends email, web, or channel output; post-publish reads outcomes into the next run. `getuai-email-2.0` has the clearest concrete pipeline: Campaign CRUD, Recipients CRUD/CSV import, SMTP account CRUD/test, Batch create + AI generate + send (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-email-2.0.md:70-73`). Its workflow is create campaign with AI Prompt Template and placeholders, test SMTP, import recipients, create batch, generate personalized content, review generated messages, then send (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-email-2.0.md:91-118`).

LLM role by stage: generator for personalized drafts, critic/retriever where citations are required, and orchestrator only when selecting recipients/batches. Load-bearing choices are style guide injection through prompt variables, recipient schema, mandatory SMTP test, human review before send, and storage/session contracts inherited from `getuai-api` (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-email-2.0.md:14`, `:91-99`, `:111-118`; `runs/growth-engine-from-scratch/sources/_raw/getuai-api.md:24-40`). Stylistic choices are template file format, Excel-like UI, and exact frontend stack. Disagreement: email content is recipient/SMTP centered; OpenClaw-style skills support multi-modal generation, transcription, and summarization as reusable channel skills (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:153`, `:5104-5152`, `:6656-6716`).

## Q3 - Ads Architecture

The converged ads loop is campaign feed -> bidding/budget/targeting -> reporting -> attribution -> optimization. `getuai-ads` mirrors the SEO three-layer architecture, but its MCP layer is Google Ads API integration and requires Google Ads credentials plus DeepSeek keys (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-ads.md:7-11`, `:24-28`, `:66-100`). `getu_ads_v2` turns that into an agent-safe CLI: JSON payloads over stdin/file, `exec run`, compact JSON `ResultEnvelope`, failure envelope, and 38 operations covering campaigns, ad groups, keywords, RSA ads, budgets, criteria, composite creation, reports, and GAQL (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getu_ads_v2.md:9-67`, `:1010-1017`).

Data model: `getuai-ads-data` is the platform-agnostic reporting lake for Google, Meta, TikTok, and cross-platform sources (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-ads-data.md:7`, `:15`, `:159-164`). It names campaign fields and conversions across platform tables (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-ads-data.md:216-250`). Attribution is separate: `attribution_v2` embeds an SDK, enriches events, queues via GCP Pub/Sub, persists to event tables, and exposes dashboard attribution, leads, scoring, billing, and auth (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/attribution_v2.md:13-16`). Boundary: platform SDKs and mutation commands stay platform-bound; query schemas, ResultEnvelope, attribution events, anomaly banners, pacing decisions, and kill-vs-scale criteria are platform-agnostic. Human-in-loop is the read/write boundary in `lawyer_marketing`, where analysis agents get read-only query skills and write operations are blocked by skill docs plus code hooks (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/lawyer_marketing.md:248-269`).

## Q4 - Social Architecture

Social decomposes into listen, post, schedule, engage, and monitor, but the corpus has adapters more than a single clean social abstraction. Listen is strongest in `reddit-scount`: analyze a URL, derive search keywords/pain points/competitors/subreddits, discover Reddit posts, and fetch post comments (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/reddit-scount.md:108-121`, `:124-181`). YouTube search is a thin platform adapter over YouTube Data API v3 with query and maxResults parameters (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/youtube-api-demo.md:7-20`, `:48-54`). X/Twitter post/reply/search exists as OpenClaw `xurl` skill (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:7392-7422`, `:7502-7507`).

OpenClaw is the closest multi-platform abstraction: Gateway control plane, multi-channel inbox, routing, sessions, tools, cron/webhooks, and per-channel adapters for WhatsApp, Telegram, Slack, Discord, Google Chat, Signal, Teams, Matrix, Feishu, LINE, Twitch, X-like tools, and WebChat (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:132-158`). Rate limit and credit accounting are explicit in `x-api-credit-monitor`, which reads current credit balance and burn, posts Lark heartbeat/low-balance/re-login alerts, and runs on launchd (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/x-api-credit-monitor.md:7-17`, `:72-104`). Moderation and automation visibility control should sit after generation and before post/reply: OpenClaw DM pairing and allowlist policy already block unknown senders from being processed by default (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:122-126`).

## Q5 - SEO/GEO Skill Catalog

| skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|
| seo-campaign-console | getuai-seo | `runs/growth-engine-from-scratch/sources/_raw/getuai-seo.md:93-106` | web UI + AI backend | campaign/account, files, metrics | recommendations, metrics | sessions/API store | canonical UI/MCP/AI split; duplicate of ads console pattern |
| keyword-research-tracking | getuai-seo | `runs/growth-engine-from-scratch/sources/_raw/getuai-seo.md:101-102` | MCP/API call | seed keyword, site, locale | keyword list/ranks | campaign store | canonical for SEO; overlaps plugin keyword ideas |
| content-optimization | getuai-seo | `runs/growth-engine-from-scratch/sources/_raw/getuai-seo.md:103` | AI recommendation | page/content + keyword | edits/recs | content artifacts | maintain with LLM prompt drift checks |
| backlink-analysis | getuai-seo | `runs/growth-engine-from-scratch/sources/_raw/getuai-seo.md:104` | MCP/API | domain/url | backlink report | campaign store | unique in corpus sample |
| competitor-analysis | getuai-seo | `runs/growth-engine-from-scratch/sources/_raw/getuai-seo.md:105`; `runs/growth-engine-from-scratch/sources/_raw/getuai-competitor-analysis.md:7-21` | MCP services | company/search term | competitors, SERP/keywords | service DB/files | duplicate; canonical is plugin/MCP service |
| site-structure-analyzer | getuai-plugin | `runs/growth-engine-from-scratch/sources/_raw/getuai-plugin.md:11-14` | FastAPI/Dify plugin | URL/site | crawl/internal-link/meta result | plugin response/logs | canonical plugin form |
| google-search-analyzer | getuai-plugin | `runs/growth-engine-from-scratch/sources/_raw/getuai-plugin.md:16`, `:124` | FastAPI plugin | query/domain | structured SERP insights | stateless/plugin logs | depends on Google Custom Search |
| keyword-clustering | getuai-plugin | `runs/growth-engine-from-scratch/sources/_raw/getuai-plugin.md:20`, `:126` | FastAPI plugin | keywords | semantic clusters | stateless response | canonical clustering; retry external API |
| sitemap-robots-generator | rankncompare | `runs/growth-engine-from-scratch/sources/_raw/rankncompare.md:53-56`, `:134-149` | build/server route | category/product data | sitemap.xml, robots.txt | JSON/static files | canonical publisher; duplicate static SEO assets elsewhere |

Canonical pick: `getuai-plugin` for reusable SEO/GEO tools, `getuai-seo` for product shell, and `rankncompare` for static indexability publishing. Deprecate ad-hoc repo-local duplicates once the Core skill registry exists.

## Q6 - Content Writing Skill Catalog

| skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|
| campaign-prompt-template | getuai-email-2.0 | `runs/growth-engine-from-scratch/sources/_raw/getuai-email-2.0.md:91-94` | UI form | name, description, placeholders | reusable prompt template | campaign DB | mitigates register drift via variables |
| personalized-email-draft | getuai-email-2.0 | `runs/growth-engine-from-scratch/sources/_raw/getuai-email-2.0.md:14`, `:111-114` | batch action | recipient + prompt | per-recipient email draft | batch DB | hallucination risk; use recipient grounding |
| recipient-import | getuai-email-2.0 | `runs/growth-engine-from-scratch/sources/_raw/getuai-email-2.0.md:70-73`, `:101-104` | API + CSV | CSV columns | recipient records | MySQL | brittle schema; validate columns |
| smtp-test-and-send | getuai-email-2.0 | `runs/growth-engine-from-scratch/sources/_raw/getuai-email-2.0.md:96-99`, `:116-118` | UI/API | SMTP account, batch | sent email status | SMTP/account DB | human review point before send |
| cited-websearch-copy | reddit-scount | `runs/growth-engine-from-scratch/sources/_raw/reddit-scount.md:233-239` | service call | query/context | answer with citations | logs/results | retrieval grounding for hallucination |
| multi-model-rank-summary | LLMRush | `runs/growth-engine-from-scratch/sources/_raw/LLMRush.md:7-14` | web app/API | term/company URL | rank, sentiment, reviews | search history | detects GEO drift across models |
| image-text-composer | openclaw-marketing | `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:153`, `:5104-5152` | skill CLI | prompt + images | image asset + metadata | files/gallery | brittle assets; keep prompt + path mapping |
| summarizer-transcriber | openclaw-marketing | `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:6656-6716` | CLI skill | URL/file/YouTube | summary/transcript | file output/log | retrieval fallback, multi-provider keys |

Load-bearing content controls: prompt template injection, retrieval grounding, recipient data schemas, and human review before publish. Stylistic controls: exact UI pattern, markdown/template formatting, and model choice.

## Q7 - Ads Skill Catalog

| skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|
| google-ads-cli | getu_ads_v2 | `runs/growth-engine-from-scratch/sources/_raw/getu_ads_v2.md:9-67` | CLI stdin/file | operation + JSON + config | ResultEnvelope | none except API side effects | platform-bound Google; canonical mutation/query shell |
| campaign-management | getu_ads_v2 | `runs/growth-engine-from-scratch/sources/_raw/getu_ads_v2.md:1010` | CLI op | campaign config/id | created/listed/updated campaigns | Google Ads | kill if envelope errors or policy failure |
| keyword-management | getu_ads_v2 | `runs/growth-engine-from-scratch/sources/_raw/getu_ads_v2.md:1012`, `:923-950` | CLI op | ad_group_ids, keywords | criteria mutations/list | Google Ads | platform-bound; validate match types |
| rsa-creative-management | getu_ads_v2 | `runs/growth-engine-from-scratch/sources/_raw/getu_ads_v2.md:1013`, `:630-704` | CLI op | headlines, descriptions, final_url | RSA ad result | Google Ads | creative fatigue via report.ad |
| budget-targeting | getu_ads_v2 | `runs/growth-engine-from-scratch/sources/_raw/getu_ads_v2.md:1014`, `:1131-1149` | CLI op | campaign_id, amount, geo/lang | budget/criteria result | Google Ads | budget pacing guardrail |
| composite-campaign-build | getu_ads_v2 | `runs/growth-engine-from-scratch/sources/_raw/getu_ads_v2.md:630-704` | CLI op | campaign + groups + ads | full campaign tree | Google Ads | preserves campaign/groups if ad creation fails |
| reporting-gaql | getu_ads_v2 | `runs/growth-engine-from-scratch/sources/_raw/getu_ads_v2.md:1048-1123` | CLI op | date_range/query | metrics, raw GAQL | report artifact | platform-bound query, agnostic envelope |
| attribution-ingest | attribution_v2 | `runs/growth-engine-from-scratch/sources/_raw/attribution_v2.md:13-16` | browser SDK + FastAPI | UTM/events/user ids | events, leads, scores | event tables/PubSub | platform-agnostic conversion event backbone |
| platform-credential-sdk | getuai-ads-sdk | `runs/growth-engine-from-scratch/sources/_raw/getuai-ads-sdk.md:7-12`, `:146-161` | Python SDK | user_id/token/platform | scoped credentials | Redis/cache/API | kill if credentials unavailable |

Contract: platform-bound skills mutate/read Google, Meta, TikTok, or X APIs; platform-agnostic abstraction is the envelope, attribution event schema, campaign/conversion metrics, and kill criteria. A/B tests are represented as campaign/ad variants plus reports until a dedicated experiment service is built.

## Q8 - Social Skill Catalog

| skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|
| reddit-opportunity-analysis | reddit-scount | `runs/growth-engine-from-scratch/sources/_raw/reddit-scount.md:108-139` | API | company URL | keywords, pain points, competitors | MySQL | platform-bound Reddit/SteadyAPI |
| reddit-discovery | reddit-scount | `runs/growth-engine-from-scratch/sources/_raw/reddit-scount.md:141-181` | API | analysis + keyword/competitor index | posts/comments | MySQL/cache | handles topic selection/listening |
| youtube-search | youtube-api-demo | `runs/growth-engine-from-scratch/sources/_raw/youtube-api-demo.md:7-20`, `:48-54` | HTTP API | query, maxResults | video list | stateless | platform-bound YouTube quota risk |
| x-credit-monitor | x-api-credit-monitor | `runs/growth-engine-from-scratch/sources/_raw/x-api-credit-monitor.md:7-17`, `:72-104` | launchd job | Chrome session, thresholds | Lark heartbeat/alert | logs/env | credit accounting and re-login failure mode |
| x-post-reply-search | openclaw-marketing | `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:7392-7422`, `:7502-7507` | xurl CLI | text/post_id/query/media | post/reply/search JSON | X API side effects | API change failure if xurl breaks |
| multi-channel-inbox | openclaw-marketing | `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:132-158` | Gateway/channel adapters | channel/account/session | routed message/session | gateway session store | cross-platform abstraction |
| slack-actions | openclaw-marketing | `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:6314-6339` | tool/skill | channelId, messageId, content | reaction/send/edit/delete | Slack API side effects | per-platform semantics |
| channel-gating | openclaw-marketing | `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:122-126` | config policy | dmPolicy, allowFrom | allow/deny processing | gateway config | moderation/automation visibility guardrail |

Parameterization: each social skill must expose platform difference explicitly: max length, media requirements, mention semantics, hashtags, reply/thread ID, auth profile, and quota/credit threshold. Do not pretend platforms are interchangeable.

## Q9 - SEO/GEO Cognition

1. Topical authority.
- Decision shaped: Build durable entity/category/product pages and internal linking before chasing prompt volume.
- Trigger condition: The target has stable search demand and can be represented as crawlable entities.
- Worked here: `rankncompare` treats category/product data, sitemap, robots, canonical URLs, metadata, and data consistency as the foundation for indexability (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/rankncompare.md:128-187`, `:350`).
- Failed here: the seed `getuai-2.0` AI Studio app has frontend/Gemini scaffolding but no crawlable SEO/GEO data model or content store, so authority cannot compound (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-2.0.md:19-42`).

2. Intent mapping.
- Decision shaped: Route crawler/search/competitor/keyword inputs into a declared intent model before generation or clustering.
- Trigger condition: Users ask what to write or optimize before the engine has a SERP, competitor, or keyword frame.
- Worked here: `getuai-plugin` exposes site structure, Google Search, competitor discovery, keyword ideas, URL content analysis, and keyword clustering as separate tool surfaces (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-plugin.md:11-20`, `:117-126`).
- Failed here: static publisher logic in `rankncompare` can emit sitemap and robots outputs, but by itself it does not discover search intent or competitor demand (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/rankncompare.md:53-56`, `:134-149`).

3. E-E-A-T via domain evidence.
- Decision shaped: Inject vertical expertise packs before allowing generic SEO recommendations to publish.
- Trigger condition: The domain has regulated, high-CPC, or trust-sensitive claims.
- Worked here: `lawyer_marketing` injects legal market intelligence, court opinions, demographics, SEO competitors, and industry skills into ads/SEO decisions (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/lawyer_marketing.md:7-14`, `:291-317`).
- Failed here: a generic growth engine without industry packs is explicitly incomplete; `growth-engine` moves industry difference into industry packs rather than the base engine (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/growth-engine.md:8`, `:27`).

4. GEO vs SEO pivot.
- Decision shaped: Separate indexability assets from LLM-answer visibility sensors.
- Trigger condition: The metric target changes from search-page ranking to mention/rank/sentiment inside model answers.
- Worked here: LLMRush measures rank and sentiment across ChatGPT, DeepSeek, Claude, Gemini, and other LLM models rather than only search pages (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/LLMRush.md:7-14`).
- Failed here: sitemap/robots generation in `rankncompare` proves SEO publishing hygiene but cannot measure LLM answer inclusion; using it as a GEO evaluator is the Q15 static-publisher-vs-GEO-evaluator failure mode (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/rankncompare.md:134-149`; `runs/growth-engine-from-scratch/sources/_raw/LLMRush.md:7-14`).

5. Content velocity vs depth.
- Decision shaped: Increase publishing cadence only after content depth, data consistency, and ranking/LLM sensors exist.
- Trigger condition: The team wants to scale AI generation before the data model and evaluator are stable.
- Worked here: `getuai-seo` couples keyword research/tracking, content optimization, backlink analysis, competitor analysis, and SEO metrics so velocity remains tied to measurement (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-seo.md:101-106`).
- Failed here: `growth-engine-legacy` warns that architecture docs existed while the Growth Core runtime tree had not been created; more generated plans without runtime/evaluator depth create false progress (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/growth-engine-legacy.md:16-22`).

Anti-patterns: tool-first SEO with no content store; content velocity without ranking/LLM answer sensors; sitemap treated as GEO evidence; generic industry-free recommendations in trust-sensitive verticals.

## Q10 - Content Writing Cognition

1. User journey mapping.
- Decision shaped: Make content a campaign-stage object, not a standalone artifact.
- Trigger condition: The content has recipients, a channel, or an intended conversion event.
- Worked here: `getuai-email-2.0` ties campaign, recipients, SMTP account, batch, AI generation, review, and send into one workflow (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-email-2.0.md:70-73`, `:91-118`).
- Failed here: `gmi-prototype` generates videos locally with model selection and prompt input, but the saved asset has no campaign, recipient, publish, or outcome loop (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/gmi-prototype.md:7-14`, `:50-54`).
- Links to Q2: reinforces ideation -> draft -> review -> publish -> post-publish flow.
- Links to Q6: uses `campaign-prompt-template`, `recipient-import`, `personalized-email-draft`, and `smtp-test-and-send`.

2. Content portfolio theory.
- Decision shaped: Maintain a mix of SEO/GEO measurement content, outbound emails, social assets, and cited answers instead of over-optimizing one format.
- Trigger condition: The team is choosing between channel-specific generation and reusable content primitives.
- Worked here: OpenClaw-style skills cover image/text generation, summarization, transcription, and channel delivery primitives, giving a reusable portfolio layer (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:153`, `:5104-5152`, `:6656-6716`).
- Failed here: `getuai-email-2.0` is strong for outbound email but does not itself cover multi-modal or search/GEO content, so treating it as the whole content subsystem narrows the portfolio (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-email-2.0.md:70-73`, `:91-118`).
- Links to Q2: separates channel-specific publish surfaces from shared ideation/draft/review controls.
- Links to Q6: explains why `image-text-composer`, `summarizer-transcriber`, and `multi-model-rank-summary` coexist with email drafting.

3. Distribution over production.
- Decision shaped: Do not count an asset as done until a channel publish/send path and measurement loop exist.
- Trigger condition: New generation skills produce local files faster than the team can publish or evaluate them.
- Worked here: email content in `getuai-email-2.0` is not done at draft time; it moves through review and send via SMTP-tested batches (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-email-2.0.md:96-99`, `:111-118`).
- Failed here: `gmi-prototype` saves generated videos to `./generated_videos/`, proving production but not distribution, attribution, or retention under Core (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/gmi-prototype.md:14`, `:50`).
- Links to Q2: makes publish and post-publish mandatory pipeline stages.
- Links to Q6: makes `smtp-test-and-send` and retrieval/citation skills load-bearing.

4. ROI time window.
- Decision shaped: Assign content to near-term outbound, medium-term SEO, or long-term GEO measurement windows before judging success.
- Trigger condition: A content artifact appears weak because it is measured on the wrong horizon.
- Worked here: LLMRush records multi-model rank, sentiment, positive/negative reviews, token usage, and search history, creating a longer-window GEO measurement surface (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/LLMRush.md:7-23`).
- Failed here: prototype apps such as `getuai-2.0` can run a Gemini frontend but have no backend result history, source registry, or post-publish measurement, so ROI cannot be attributed (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-2.0.md:19-42`).
- Links to Q2: post-publish iteration is the stage that captures the ROI window.
- Links to Q6: `multi-model-rank-summary` and `cited-websearch-copy` protect against hallucination while creating evaluation traces.

5. Brand voice as forcing function.
- Decision shaped: Encode voice through prompt variables, recipient fields, retrieval context, and review gates rather than one-off prompt taste.
- Trigger condition: Multiple writers, models, or channels must sound like one operator without collapsing into generic copy.
- Worked here: `getuai-email-2.0` prompt templates expose placeholders such as email, first_name, last_name, company, and position, then require generated messages to be reviewed before send (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-email-2.0.md:91-99`, `:111-118`).
- Failed here: free-form generation prototypes such as `gmi-prototype` accept a custom prompt but do not persist a brand voice schema, reviewer decision, or campaign variables (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/gmi-prototype.md:29-54`).
- Links to Q2: style guide injection and human review are load-bearing choices.
- Links to Q6: `campaign-prompt-template`, `personalized-email-draft`, and `cited-websearch-copy` are the enforceable skills.

Anti-patterns: production-over-distribution; prompt-only voice without variables; portfolio collapse into one channel; judging GEO content on same-day email metrics; no post-publish measurement.

## Q11 - Ads Cognition

1. LTV/CAC discipline.
- Decision shaped: Scale spend only when acquisition cost and downstream lead/conversion evidence agree.
- Trigger condition: Campaign reports show cost and conversions, but lead quality or user identity is uncertain.
- Worked here: `lawyer_marketing` injects budget strategy, CPC/CTR/CVR benchmarks, and legal benchmarks, while `getu_ads_v2` reports cost, conversions, and cost_per_conversion per campaign (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/lawyer_marketing.md:291-304`; `runs/growth-engine-from-scratch/sources/_raw/getu_ads_v2.md:1048-1064`).
- Failed here: it fails as true LTV/CAC when attribution rows are missing or user identity is not bridged, because lead extraction depends on `setUserId` wiring and session semantics (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/attribution_v2.md:117-119`, `:151-155`).

2. Pacing logic.
- Decision shaped: Budget and targeting changes are gradual controls, not blind spend increases.
- Trigger condition: Daily spend, conversion cost, or platform delivery drifts from plan.
- Worked here: `getu_ads_v2` exposes budget and targeting operations with campaign_id, amount, geo, and language inputs, making pacing an explicit skill boundary (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getu_ads_v2.md:1014`, `:1131-1149`).
- Failed here: `getuai-ads` requires Google Ads credentials and DeepSeek keys at service startup; when platform credentials drift, pacing logic cannot run regardless of model quality (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-ads.md:24-28`).

3. Creative fatigue curves.
- Decision shaped: Refresh RSA assets when ad-level reporting shows declining performance instead of rewriting campaign structure first.
- Trigger condition: Campaign aggregate looks acceptable but individual ad or search-term metrics decay.
- Worked here: `getu_ads_v2` has RSA creative operations and ad-level reporting, so fatigue can be observed at the creative row rather than inferred from whole-campaign spend (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getu_ads_v2.md:1013`, `:630-704`, `:1066-1086`).
- Failed here: platform-agnostic reporting alone in `getuai-ads-data` names campaign fields and conversions, but without ad/creative grain it can hide fatigue under campaign averages (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-ads-data.md:216-250`).

4. Attribution paradox.
- Decision shaped: Treat attribution as both the source of truth for scale decisions and the easiest part of the system to break silently.
- Trigger condition: Ads reports look healthy while lead tables, SDK cookies, or cross-subdomain identity look incomplete.
- Worked here: `attribution_v2` splits SDK, ingress/consumer, Pub/Sub persistence, dashboard attribution, lead extraction, scoring, billing, and auth while preserving legacy parity during refactor (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/attribution_v2.md:13-23`).
- Failed here: the same repo documents failure edges around missing lead rows, `setUserId`, session rotation, and cross-domain cookies (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/attribution_v2.md:117-119`, `:151-155`, `:184-186`).

5. Kill-vs-scale criteria.
- Decision shaped: Freeze, pause, or reduce spend on envelope errors, attribution loss, conversion-cost drift, policy failures, or low data confidence; scale only after reports and attribution agree.
- Trigger condition: A write operation would mutate campaign, keyword, creative, budget, or targeting state.
- Worked here: `lawyer_marketing` separates analysis, validation, execution, and action logging and blocks write operations for analyst agents; `getu_ads_v2` wraps operations in success/error ResultEnvelope semantics (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/lawyer_marketing.md:248-269`; `runs/growth-engine-from-scratch/sources/_raw/getu_ads_v2.md:9-67`).
- Failed here: `growth-engine-legacy` makes approval, action ledgers, schedules, and kill-switches Core responsibilities because engines owning platform facts or write paths create unsafe restarts and mutations (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/growth-engine-legacy.md:43-50`, `:83-88`).

Anti-patterns: scaling from platform-reported conversions without attribution identity; budget mutation before read-only diagnosis; campaign-average reporting used as creative-fatigue evidence; treating platform credential failures as model failures.

## Q12 - Social Cognition

1. Platform-as-game-theory.
- Decision shaped: Each platform gets its own action grammar, quota assumptions, and engagement rules.
- Trigger condition: A post/reply/search workflow is reused across Reddit, YouTube, X, Slack, or chat channels.
- Worked here: `reddit-scount` models Reddit as opportunity discovery over target audience, pain points, competitors, subreddits, posts, and comments (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/reddit-scount.md:108-181`).
- Failed here: OpenClaw can route across many channels, but a generic gateway without channel-specific policy would blur platform games; the repo mitigates with per-channel adapters, DM pairing, allowlists, group routing, and chunking (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:122-158`, `:177-180`).

2. Algorithm preference modeling.
- Decision shaped: Encode platform-specific discovery primitives before writing content.
- Trigger condition: The engine needs to decide whether the next action is search/listen, post, reply, or monitor.
- Worked here: YouTube is represented as search over query and maxResults through YouTube Data API v3, while X uses post/reply/search primitives through `xurl` (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/youtube-api-demo.md:7-20`, `:48-54`; `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:7392-7422`, `:7502-7507`).
- Failed here: YouTube search alone is discovery-only; it has no schedule, reply, moderation, or credit monitor, so treating it as a full social engine would miss engagement and monitoring surfaces (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/youtube-api-demo.md:7-20`, `:48-54`).

3. Community fit before brand voice.
- Decision shaped: Learn the community context before adapting brand tone.
- Trigger condition: The brand wants to enter a subreddit, thread, or channel where norms differ from owned copy.
- Worked here: `reddit-scount` starts from target audience, pain points, competitor names, and target subreddits before discovering posts and comments (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/reddit-scount.md:124-181`).
- Failed here: `xurl` can post, reply, and search, but those primitives do not by themselves inspect community norms; without Q8 channel-gating and Q12 community fit, visible automation risk increases (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:7392-7422`, `:7502-7507`).

4. Viral mechanics.
- Decision shaped: Expose reply/thread/media primitives, but do not confuse virality mechanics with a validated content strategy.
- Trigger condition: The team wants high-reach social loops rather than only listening.
- Worked here: OpenClaw/X primitives include post, reply, media, and search, the minimum mechanics for propagation experiments (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:7392-7422`, `:7502-7507`).
- Failed here: `youtube-api-demo` demonstrates search and result rendering only; it cannot run a viral loop because it lacks posting, scheduling, reply, or outcome monitoring (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/youtube-api-demo.md:7-20`, `:48-54`).

5. Automation visibility cost.
- Decision shaped: Put moderation, allowlists, credit/rate monitors, and human approval before automated replies or posts.
- Trigger condition: Content is generated by an agent in a public or semi-public channel.
- Worked here: OpenClaw blocks unknown senders through DM pairing/allowlist policy, and `x-api-credit-monitor` posts heartbeat, low-balance, burn, and re-login alerts so automation does not silently overrun quota or session state (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:122-126`; `runs/growth-engine-from-scratch/sources/_raw/x-api-credit-monitor.md:7-17`, `:72-104`).
- Failed here: direct X post/reply primitives without a moderation insertion point can expose automation; Q8 `channel-gating` and Q13 human-in-loop console must precede social writes (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/openclaw-marketing.md:7392-7422`, `:7502-7507`).

Anti-patterns: one tone across platforms; no rate-limit or credit accounting; posting before listening; treating discovery APIs as engagement engines; hiding automation controls inside a platform adapter instead of Core.

## Q13 - Shared Foundations

| shared foundation | contract/interface | evidence from corpus | share vs isolate decision |
|---|---|---|---|
| identity/session | tenant/user/session IDs, browser-facing API only, Core-created RequestContext or signed context envelope | `growth-engine-legacy.md:43-50`; `getuai-api.md:23-37`; `attribution_v2.md:153-162` | shared because SEO, Content, Ads, and Social all need user/session continuity; domain engines never own raw identity |
| credentials/secrets | credential records, scoped leases, env sync policy, re-login/low-balance monitor | `growth-engine-legacy.md:64-88`; `getuai-ads.md:21-28`; `x-api-credit-monitor.md:12-18`; `lawyer_finder.md:481-488` | shared because credential rotation and lease expiry are tenant-trust concerns; platform SDK calls remain isolated |
| data lake/artifact store | artifacts/events/results keyed by tenant, target, run, action, and source | `getuai-api.md:24-42`; `rankncompare.md:49-56`; `attribution_v2.md:13-16`; `gmi-prototype.md:11-16` | shared for ownership and retention; isolated for domain-specific schemas like rank rows, ad reports, social threads |
| task queue/schedules | Core schedule registry, launchd/cron adapters, queue/dead-letter for events | `growth-engine-legacy.md:64-88`; `x-api-credit-monitor.md:20`, `:82-93`; `attribution_v2.md:49-52` | shared for schedule lifecycle and retries; isolated for platform cadence and quota windows |
| observability | run_event log, request IDs, Sentry/Langfuse/Grafana tracing, redaction | `growth-engine-legacy.md:64-70`, `:86`; `LLMRush.md:19-23`; `attribution_v2.md:107-119` | shared so traces correlate across domains; isolated dashboards can render domain metrics |
| LLM gateway | provider/model routing, prompt policy, token/cost tracking, AI service adapters | `getuai-seo.md:78-91`; `getuai-email-2.0.md:14`, `:111-114`; `openclaw-marketing.md:175-180`; `cuilawgroup.md:25-27` | shared for cost, routing, and model failover; isolated for prompts, ranking logic, and channel tone |
| human-in-loop console | approvals, overrides, kill-switches, action ledger, read/write skill split | `growth-engine-legacy.md:83-88`; `lawyer_marketing.md:248-269`; `getuai-email-2.0.md:115-118`; `openclaw-marketing.md:122-126` | shared for approval workflow and audit; isolated for domain action payload validation |
| repo-template conventions | AGENTS/CLAUDE rules, skills, CI, version check, idempotent apply | `optiminds-repo-template.md:9-30`, `:55-63`, `:156-177`; `lawyer_finder.md:71-86` | shared because governance must be uniform; product behavior remains in each domain repo |

Decision rule: share a component if it enforces tenant trust, credentials, schedules, ledger/audit, observability, LLM routing, or approval across more than one domain; isolate it when its schema, external API, ranking logic, tone, or kill criteria are domain-specific.

Worked example: attribution events are shared, while ranking logic stays domain-isolated. Attribution events are shared because the same browser SDK/session/event path turns ads clicks, content forms, and downstream leads into a cross-domain conversion record (`attribution_v2.md:13-16`, `:153-162`). Ads consumes it for CAC and scale/kill decisions (Q7 `attribution-ingest`), Content consumes it for post-publish outcome loops (Q6 campaign/email flow), and Core observes it for ledgers (Q15 attribution/session breakage). Ranking logic stays isolated because `rankncompare` implements sitemap/category/indexability publishing (`rankncompare.md:128-157`) while LLMRush implements multi-model rank/sentiment sensing (`LLMRush.md:7-14`). Core may standardize the metric envelope, but SEO/GEO owns rank interpretation.

## Q14 - Build Sequence

| milestone | scope | dependencies | done_criteria | next_trigger | deferrals |
|---|---|---|---|---|---|
| Day-1 | Core skeleton for tenant/session, artifact store, source registry, repo-template rules, and approval stub. Implements Q13 identity/session + artifact + repo-template foundations before Q1-Q8 domain skills run. | none; use `growth-engine` backend-skeleton-first pattern and `optiminds-repo-template` governance | one growth_target can be created; sessions/artifacts persist; approval/action records exist; no `runs/` leakage | first domain tool needs credentials or durable artifacts | defer ads mutations and social posting because Q15 write-without-approval is not yet controlled |
| Week-1 | SEO/GEO read-only lane consuming Q5 `site-structure-analyzer`, `google-search-analyzer`, `keyword-clustering`, and `sitemap-robots-generator`; implements Q1 crawler/ranking/content-store/publisher separation. | Day-1 Core plus Q13 credential leases and artifact store; monitor Q15 Platform API credential drift | crawler/search/keyword outputs stored; ranking signal source declared; sitemap/content-store artifact exists; human review point exists | recurring checks or content publishing is requested | defer auto-publish until Q15 static-publisher-vs-GEO-evaluator guardrail and kill-switch exist |
| Week-2 | Content lane using Q6 `campaign-prompt-template`, `recipient-import`, `personalized-email-draft`, `smtp-test-and-send`, plus retrieval grounding; implements Q2 ideation -> draft -> review -> send. | Core sessions/artifacts plus Week-1 content store; Q13 LLM gateway; Q10 user-journey and brand-voice frames | prompt variables validate; recipients import; AI draft generated per recipient; human review happens before send; SMTP test is mandatory | first outbound campaign or post-publish metric request | defer multi-image/video production because Q15 prototype-local-artifact-store remains unresolved for rich media |
| Week-4 | Ads read-only + attribution lane using Q7 `platform-credential-sdk`, `reporting-gaql`, `attribution-ingest`, and Q11 CAC/pacing rules; no ad-platform writes. | Core credentials/secrets, Content campaign IDs, Week-2 publish events; Q13 shared attribution-event contract | campaign feed/reporting/conversion events visible in one dashboard; attribution session tests pass; analyst has read-only skills only | analysts repeatedly make the same budget/targeting recommendations | defer budget mutation and A/B automation because Q15 read/write boundary and attribution/session breakage are still high risk |
| Week-8 | Controlled write lanes: SEO publish, email send, ads budget/targeting, and social replies behind approval. Uses Q7 ResultEnvelope/action ledger and Q8 `channel-gating`, `x-credit-monitor`, `x-post-reply-search`, `slack-actions`. | prior read-only evidence, Q13 human-in-loop console, Q15 write-without-approval prophylactic | every write path has approval, ResultEnvelope/action ledger, rollback or kill-switch, and quota/session monitor | stable weekly outcomes and repeated manual approvals | defer full cross-platform optimizer because platform-specific tone/API rules in Q8 and Q12 still need per-domain isolation |
| Week-12 / Month-3 | OODA orchestration across SEO/GEO, Content, Ads, Social with industry pack injection. Uses Q9-Q12 cognition as guardrails and Q15 failure table as launch checklist. | all domain lanes, Q13 observability + LLM gateway + schedules, vertical case deployment lessons from `lawyer_marketing`, `lawyer_finder`, and `cuilawgroup` | target has cross-domain loop, observability, attribution, human override, per-domain kill criteria, and vertical pack injection; Month-3 done when one tenant can run weekly observe-plan-approve-execute-review | scale to more tenants or industries | defer Temporal-scale workflow, plugin marketplace, and autonomous spend scaling until failure modes have monitors |

Evidence from corpus evolution: prototypes are thin local apps (`getuai-2.0` AI Studio frontend/Gemini, tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-2.0.md:19-42`), MVP hardens routing/env (`getuai-mvp`, tier: file:line `runs/growth-engine-from-scratch/sources/_raw/getuai-mvp.md:9-76`), production attribution keeps legacy parity while refactoring (`attribution_v2`, tier: file:line `runs/growth-engine-from-scratch/sources/_raw/attribution_v2.md:16-23`), vertical cases show public/admin/backend separation and production hardening (`lawyer_finder.md:11-16`, `:220-255`; `cuilawgroup.md:10-27`), and new `growth-engine` starts with backend skeleton then schema/auth/engine vertical slice (tier: file:line `runs/growth-engine-from-scratch/sources/_raw/growth-engine.md:8-12`).

## Q15 - Cross-Domain Failure Modes

| failure_mode | affected_domains | recurrence_count | structural_cause | early_symptom | prophylactic | evidence_pair |
|---|---|---:|---|---|---|---|
| Domain engines own platform facts | SEO, Ads, Social | 3 | identity/credentials/schedules scattered | engines ask for raw tokens or run own cron | Browser -> Core only; Core owns facts; engines get context/leases. Enforced by Q13 identity/credential foundations plus Q7 `platform-credential-sdk` and Q8 `x-credit-monitor`. | failure/prophylactic: `growth-engine-legacy.md:43-50`, `:83-88` |
| Legacy scaffolding import | all | 4 | copying previous attempt instead of extracting contracts | stale paths, missing core runtime | greenfield rewrite; references read-only. Enforced by Q13 repo-template conventions and Q14 Day-1 Core skeleton before domain expansion. | `growth-engine.md:69-100`, `:138-152` |
| Missing runtime core after docs | all | 4 | design exists but core tree absent | docs mention Core, no runtime | Day-1 skeleton before domain expansion. Enforced by Q14 Day-1 done criteria and Q13 Core ownership contract. | `growth-engine-legacy.md:16-22`, `growth-engine.md:11-12` |
| Platform API credential drift | SEO, Ads, Social | 3 | env/session/auth external to action layer | API access errors, re-login alerts | central credential leases + low-balance/re-login monitors. Enforced by Q7 `platform-credential-sdk`, Q8 `x-credit-monitor`, and Q5 Google API tool rows. | `getuai-ads.md:24-28`, `x-api-credit-monitor.md:13-17`, `growth-engine-legacy.md:85` |
| Attribution/session breakage | Ads, Content | 2 | cross-domain cookies/user rotation misunderstood | lead table missing rows; SDK cookies not shared | explicit SDK domain config and session-rotation tests. Enforced by Q7 `attribution-ingest`, Q6 campaign/outbound rows, and Q13 shared attribution-event example. | `attribution_v2.md:117-119`, `:153-155`, `:184-186` |
| Write operations without approval | SEO, Ads, Social | 3 | read/write skills mixed | agents mutate campaigns/posts while analyzing | read-only analysis skills, write hooks, action ledger. Enforced by Q7 `google-ads-cli` read/write split, Q8 `channel-gating`, Q6 `smtp-test-and-send`, and Q13 human-in-loop console. | `lawyer_marketing.md:248-269`, `growth-engine-legacy.md:84` |
| Static publisher treated as GEO evaluator | SEO/GEO | 1 | sitemap/indexing confused with LLM answer visibility | sitemap exists but no LLM rank signal | add LLMRush-style multi-model rank/sentiment sensor. Enforced by Q5 `sitemap-robots-generator` + Q6 `multi-model-rank-summary` split. | `rankncompare.md:134-149`, `LLMRush.md:7-14` |
| Prototype-local artifact store | Content, Social | 2 | generated media saved locally only | outputs exist but no campaign/outcome link | artifact store under Core with owner/run/action IDs. Enforced by Q13 data lake/artifact store and Q6 `image-text-composer` persistence requirement. | `gmi-prototype.md:14`, `:50`, `getuai-api.md:24-40` |
| API prefix/proxy mismatch | shared infra | 2 | local/prod routes diverge | frontend calls wrong backend path | configurable API_PREFIX + proxy contract. Enforced by Q13 repo-template/config conventions and Q14 Day-1 environment contract. | `getuai-mvp.md:9-76` |

The strongest prophylactic is boring: shared Core for trust and ledgers, domain-isolated adapters for external APIs, human approval before writes, and explicit monitors for quotas, sessions, and attribution. The table ties every prophylactic back to Q5-Q8 skill rows or Q13 shared foundations so the failure catalog is executable rather than only diagnostic.
