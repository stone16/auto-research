# Knowledge Base

Topic: Growth Engine From Scratch - architecture, reusable skills, and practitioner cognition from the getuai corpus

Iteration: 3 cognition-pairing patch

## Evidence Policy
Citations use run-local raw extracts as direct file:line evidence, for example `runs/growth-engine-from-scratch/sources/_raw/getuai-seo.md:7-11` (tier: file:line). Benchmark answers cite required source IDs.

## Q1 - SEO/GEO Architecture
SEO/GEO converges on UI -> domain tools/adapters -> AI recommendation service, with Core owning identity, sessions, credentials, schedules, ledgers, approvals, and kill-switches. Components: crawler/sensor, ranking sensor, content store, generator, publisher, evaluator. Data enters through site structure, Google Search, competitor, keyword, URL-content, and clustering tools (`getuai-plugin.md:11-20`, `:117-126`); ranking comes from SEO metrics/keyword tracking (`getuai-seo.md:101-106`) and GEO rank/sentiment sensors (`LLMRush.md:7-17`); content store/publisher evidence comes from JSON category/product storage plus sitemap/robots/canonical generation (`rankncompare.md:49-56`, `:128-149`). Repos disagree: `getuai-seo` is a three-service product shell (`getuai-seo.md:7-11`), `rankncompare` is static SEO publishing, and `growth-engine-legacy` requires Browser -> Core only and engines never owning raw platform facts (`growth-engine-legacy.md:43-50`, `:83-88`). Recommendation: keep SEO/GEO tools domain-isolated but require Core approval, override, and kill-switch before publish or recurring checks.

## Q2 - Content Writing Architecture
Content Writing runs ideation -> outline -> draft -> edit/review -> publish/send -> post-publish iteration. `getuai-email-2.0` is the concrete pipeline: Campaign, Recipients/CSV, SMTP test, Batch create, AI generate, review, send (`getuai-email-2.0.md:70-73`, `:91-118`). LLM role is generator for personalized drafts, retriever/critic when citations are required, and orchestrator only for batch/recipient selection. Load-bearing choices: prompt template variables, recipient schema, mandatory SMTP test, human review before send, and shared session/artifact storage (`getuai-email-2.0.md:91-99`, `:111-118`; `getuai-api.md:24-40`). Stylistic choices: exact UI, template format, and model vendor.

## Q3 - Ads Architecture
Ads converges on campaign feed -> bidding/budget/targeting -> reporting -> attribution -> optimization. `getuai-ads` provides UI/MCP/AI split and Google Ads credentials (`getuai-ads.md:7-11`, `:21-28`); `getu_ads_v2` provides agent-safe stdin/file JSON, `exec run`, ResultEnvelope, failure envelopes, and 38 operations (`getu_ads_v2.md:9-72`, `:1010-1017`). Data model spans campaigns, ad groups, keywords, creatives, budgets, reports, and conversions (`getuai-ads-data.md:216-250`). Attribution is isolated as browser SDK + event ingress + dashboard API (`attribution_v2.md:13-16`). Platform-specific code lives in Google/Meta/TikTok/X SDKs and mutation commands; platform-agnostic logic is envelope, attribution event schema, reporting metrics, read/write split, pacing, anomaly, and kill-vs-scale rules. Human-in-loop comes from `lawyer_marketing` read-only analysis and write enforcement (`lawyer_marketing.md:248-269`).

## Q4 - Social Architecture
Social decomposes into listen, post, schedule, engage, monitor. Listen is strongest in `reddit-scount`: analyze URL, derive keywords/pain points/competitors/subreddits, discover posts, fetch comments (`reddit-scount.md:108-181`). YouTube is a thin query/maxResults search adapter (`youtube-api-demo.md:7-20`, `:52-54`). X post/reply/search exists through `xurl` (`openclaw-marketing.md:7392-7422`, `:7502-7507`). The closest shared abstraction is OpenClaw Gateway: sessions, channels, tools, cron/webhooks, group routing, channel adapters (`openclaw-marketing.md:132-158`). Rate/credit monitoring is explicit in `x-api-credit-monitor` balance, burn, days remaining, low-balance, and re-login alerts (`x-api-credit-monitor.md:7-17`, `:117-125`). Moderation sits before post/reply via DM pairing, allowlists, mention gating, and per-channel chunking (`openclaw-marketing.md:122-126`, `:157-158`).

## Q5 - SEO/GEO Skill Catalog
| skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|
| seo-campaign-console | getuai-seo | `getuai-seo.md:93-106` | web UI + AI backend | campaign/account/files/metrics | recommendations/metrics | sessions/API store | canonical product shell |
| keyword-research-tracking | getuai-seo | `getuai-seo.md:101-102` | MCP/API | seed/site/locale | keywords/ranks | campaign store | overlaps plugin keyword ideas |
| content-optimization | getuai-seo | `getuai-seo.md:103` | AI recommendation | page/content/keyword | edits/recs | content artifacts | prompt drift checks |
| backlink-analysis | getuai-seo | `getuai-seo.md:104` | MCP/API | domain/url | backlink report | campaign store | unique in sample |
| competitor-analysis | getuai-seo/getuai-competitor-analysis | `getuai-seo.md:105`; `getuai-competitor-analysis.md:7-21` | MCP service | company/query | competitors/SERP/keywords | service DB/files | duplicate; canonical plugin/MCP |
| site-structure-analyzer | getuai-plugin | `getuai-plugin.md:11-14` | FastAPI/Dify | URL/site | crawl/internal-link/meta | plugin logs | canonical crawl skill |
| google-search-analyzer | getuai-plugin | `getuai-plugin.md:16`, `:124` | FastAPI plugin | query/domain | SERP insights | stateless/logs | Google CSE dependency |
| keyword-clustering | getuai-plugin | `getuai-plugin.md:20`, `:126` | FastAPI plugin | keywords | semantic clusters | stateless | retry external API |
| sitemap-robots-generator | rankncompare | `rankncompare.md:53-56`, `:134-149` | build/server route | category/product data | sitemap.xml/robots.txt | JSON/static files | canonical publisher |
Canonical pick: `getuai-plugin` for reusable tools, `getuai-seo` for product shell, `rankncompare` for static indexability.

## Q6 - Content Writing Skill Catalog
| skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|
| campaign-prompt-template | getuai-email-2.0 | `getuai-email-2.0.md:91-94` | UI form | name/description/placeholders | prompt template | campaign DB | mitigates register drift |
| personalized-email-draft | getuai-email-2.0 | `getuai-email-2.0.md:14`, `:111-114` | batch action | recipient + prompt | email draft | batch DB | recipient grounding |
| recipient-import | getuai-email-2.0 | `getuai-email-2.0.md:70-73`, `:101-104` | API + CSV | CSV columns | recipient records | MySQL | schema validation |
| smtp-test-and-send | getuai-email-2.0 | `getuai-email-2.0.md:96-99`, `:116-118` | UI/API | SMTP account/batch | sent status | SMTP/account DB | human review before send |
| cited-websearch-copy | reddit-scount | `reddit-scount.md:233-239` | service call | query/context | answer with citations | logs/results | retrieval grounding |
| multi-model-rank-summary | LLMRush | `LLMRush.md:7-17` | web/API | term/company URL | rank/sentiment/reviews | search history | GEO drift sensor |
| image-text-composer | openclaw-marketing | `openclaw-marketing.md:153`, `:5104-5152` | skill CLI | prompt/images | asset/metadata | files/gallery | prompt/path mapping |
| summarizer-transcriber | openclaw-marketing | `openclaw-marketing.md:6656-6716` | CLI skill | URL/file/YouTube | summary/transcript | file/log | retrieval fallback |
Controls: templates, variables, retrieval grounding, recipient schemas, and review gates are load-bearing; UI and exact model choice are stylistic.

## Q7 - Ads Skill Catalog
| skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|
| google-ads-cli | getu_ads_v2 | `getu_ads_v2.md:9-72` | CLI stdin/file | operation + JSON + config | ResultEnvelope | API side effects | platform-bound Google shell |
| campaign-management | getu_ads_v2 | `getu_ads_v2.md:1010` | CLI op | campaign config/id | create/list/update | Google Ads | kill on envelope error |
| keyword-management | getu_ads_v2 | `getu_ads_v2.md:1012`, `:923-950` | CLI op | ad_group_ids/keywords | criteria mutations/list | Google Ads | validate match types |
| rsa-creative-management | getu_ads_v2 | `getu_ads_v2.md:1013`, `:211-271` | CLI op | headlines/descriptions/url | RSA result | Google Ads | fatigue via report.ad |
| budget-targeting | getu_ads_v2 | `getu_ads_v2.md:1014`, `:1131-1149` | CLI op | campaign_id/amount/geo/lang | budget/criteria result | Google Ads | pacing guardrail |
| composite-campaign-build | getu_ads_v2 | `getu_ads_v2.md:634-704` | CLI op | campaign/groups/ads | campaign tree | Google Ads | partial failure tolerant |
| reporting-gaql | getu_ads_v2 | `getu_ads_v2.md:1048-1123` | CLI op | date_range/query | metrics/raw GAQL | report artifact | platform-bound query |
| attribution-ingest | attribution_v2 | `attribution_v2.md:13-16` | SDK + FastAPI | UTM/events/user ids | events/leads/scores | event tables/PubSub | agnostic conversion backbone |
| platform-credential-sdk | getuai-ads-sdk | `getuai-ads-sdk.md:7-12`, `:146-161` | Python SDK | user_id/token/platform | scoped credentials | Redis/API cache | kill if unavailable |
Abstraction contract: platform-bound skills mutate/read external APIs; platform-agnostic layer owns envelope, metrics, attribution events, and kill criteria.

## Q8 - Social Skill Catalog
| skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|
| reddit-opportunity-analysis | reddit-scount | `reddit-scount.md:108-139` | API | company URL | keywords/pain points/competitors | MySQL | Reddit/SteadyAPI bound |
| reddit-discovery | reddit-scount | `reddit-scount.md:141-181` | API | analysis + keyword index | posts/comments | MySQL/cache | topic selection |
| youtube-search | youtube-api-demo | `youtube-api-demo.md:7-20`, `:52-54` | HTTP API | query/maxResults | video list | stateless | quota/API risk |
| x-credit-monitor | x-api-credit-monitor | `x-api-credit-monitor.md:7-17`, `:72-104` | launchd | Chrome session/thresholds | Lark heartbeat/alert | logs/env | credit/re-login monitor |
| x-post-reply-search | openclaw-marketing | `openclaw-marketing.md:7392-7422`, `:7502-7507` | xurl CLI | text/post_id/query/media | post/reply/search JSON | X side effects | API change risk |
| multi-channel-inbox | openclaw-marketing | `openclaw-marketing.md:132-158` | Gateway adapters | channel/account/session | routed message/session | gateway store | closest shared abstraction |
| slack-actions | openclaw-marketing | `openclaw-marketing.md:6314-6339` | tool/skill | channelId/messageId/content | reaction/send/edit/delete | Slack side effects | per-platform semantics |
| channel-gating | openclaw-marketing | `openclaw-marketing.md:122-126` | config policy | dmPolicy/allowFrom | allow/deny | gateway config | moderation guardrail |
Parameterization: expose length, media, hashtag/mention semantics, reply/thread ID, auth profile, quota threshold, and platform API failure mode.

## Q9 - SEO/GEO Cognition
1. Topical authority. Decision: build durable entities/categories before generation. Trigger: stable search demand. Worked here: `rankncompare` uses category/product data, sitemap, robots, canonical metadata, schema, and data consistency (`rankncompare.md:128-187`, `:346-390`). Failed here: `getuai-2.0` is only AI Studio/Vite/Gemini scaffolding with no crawlable content store or ranking sensor (`getuai-2.0.md:19-42`).
2. Intent mapping. Decision: route work to crawl, SERP, competitor, keyword, URL content, or clustering tools. Trigger: before outline/draft/publish. Worked here: `getuai-plugin` separates Google Search, competitor discovery, keyword ideas, URL content, and clustering with schemas (`getuai-plugin.md:15-20`, `:121-136`). Failed here: `getuai-seo` names broad feature areas but lacks those typed intent interfaces at the product-shell level (`getuai-seo.md:101-106`).
3. E-E-A-T via domain evidence. Decision: inject vertical evidence and constraints. Trigger: regulated/expertise-heavy targets. Worked here: `lawyer_marketing` adds court opinions, demographics, SEO keywords, competitor analysis, compliance, budget, and legal benchmarks (`lawyer_marketing.md:7-14`, `:291-317`). Failed here: `growth-engine` treats industry pack mechanism as separate from engines, proving generic SEO is incomplete until the pack is injected (`growth-engine.md:8`, `:25-29`).
4. GEO vs SEO pivot. Decision: distinguish search indexability from LLM-answer visibility. Trigger: question is AI answer inclusion/sentiment. Worked here: LLMRush measures rank and sentiment across ChatGPT, DeepSeek, Claude, Gemini, token usage, and search history (`LLMRush.md:7-17`). Failed here: `rankncompare` sitemap/robots/canonical work cannot measure LLM answer inclusion (`rankncompare.md:134-157`).
5. Content velocity vs depth. Decision: scale output only after entity consistency/evaluator coverage. Trigger: generator can produce more than the ranking system can validate. Worked here: `rankncompare` validates categories, product IDs, ratings, positions, and trending consistency (`rankncompare.md:346-390`). Failed here: `gmi-prototype` generates local videos without search intent, rank, or outcome loop (`gmi-prototype.md:11-14`, `:46-54`).
Anti-patterns: tool-first SEO with no content store; sitemap-only GEO; generic content velocity without vertical evidence; prompt generation without ranking sensors.

## Q10 - Content Writing Cognition
1. User journey mapping. Decision: content must belong to recipient/campaign/send/review path. Trigger: outbound or lifecycle content. Worked here: `getuai-email-2.0` runs Campaign -> SMTP -> Recipients -> Batch -> generate -> review -> send, directly supporting Q2 and Q6 (`getuai-email-2.0.md:91-118`). Failed here: `gmi-prototype` saves generated videos locally with no recipient, campaign, distribution, or outcome loop (`gmi-prototype.md:7-14`, `:50-54`).
2. Content portfolio theory. Decision: manage campaigns, recipients, batches, assets, and history, not single prompts. Trigger: reuse or later comparison. Worked here: email APIs persist campaigns/recipients/batches, and LLMRush preserves search history/user data (`getuai-email-2.0.md:70-73`; `LLMRush.md:17`, `:206-210`). Failed here: `gmi-prototype` stores outputs as local generated-video files with implicit target/performance (`gmi-prototype.md:14`, `:96-111`).
3. Distribution over production. Decision: build send/publish path before scaling drafts. Trigger: generation volume exceeds review/routing capacity. Worked here: SMTP test is mandatory and send happens after review (`getuai-email-2.0.md:96-99`, `:115-118`). Failed here: `gmi-prototype` optimizes model choice/count/prompt/local generation but stops at saved files (`gmi-prototype.md:36-54`).
4. ROI window. Decision: judge content after rank, sentiment, replies, or conversion can be observed. Trigger: keep/iterate/stop decision. Worked here: LLMRush tracks rank, sentiment, reviews, token use, and search history (`LLMRush.md:7-17`, `:206-214`). Failed here: `gmi-prototype` confirms generation/local save but defines no later evaluation window (`gmi-prototype.md:91-96`, `:126-133`).
5. Brand voice as forcing function. Decision: force generation through variables and templates. Trigger: many recipients/channels need consistent register. Worked here: email prompt template supports `{email}`, `{first_name}`, `{last_name}`, `{company}`, `{position}` and personalized generation (`getuai-email-2.0.md:91-94`, `:111-114`). Failed here: `gmi-prototype` uses a free-text prompt after model/count selection, with no voice variables or review metadata (`gmi-prototype.md:40-50`, `:91-96`).
Anti-patterns: production over distribution; portfolio without state; ROI judged at generation time; prompt-only brand voice; skipping review before publish.

## Q11 - Ads Cognition
1. LTV/CAC discipline. Decision: keep/pause/scale only when spend, conversion, and economics agree. Trigger: enough cost/conversion signal exists. Worked here: `lawyer_marketing` injects budget strategy and CPC/CTR/CVR benchmarks; `getu_ads_v2` reports cost, conversions, avg_cpc, cost_per_conversion (`lawyer_marketing.md:291-304`; `getu_ads_v2.md:1048-1064`). Failed here: LTV/CAC breaks when lead rows are missing or `setUserId`/session rotation splits identity (`attribution_v2.md:117-119`, `:153-162`).
2. Pacing logic. Decision: adjust daily budget gradually with limits. Trigger: spend drift vs evidence window. Worked here: `search.budget.update` updates campaign daily budgets and lawyer skill stores budget strategy (`getu_ads_v2.md:1131-1149`; `lawyer_marketing.md:297-300`). Failed here: pacing fails when Ads credentials/developer tokens drift; operators are told to check API credentials/token (`getuai-ads.md:21-28`, `:113-115`).
3. Creative fatigue curves. Decision: refresh/copy/pause/remove ads using ad-level performance. Trigger: campaign aggregate hides ad decay. Worked here: RSA operations and ad-level reports exist (`getu_ads_v2.md:211-271`, `:1066-1086`). Failed here: creative automation can hit policy/platform failure; composite create preserves campaign/groups if ad creation fails (`getu_ads_v2.md:634-704`).
4. Attribution paradox. Decision: distrust both platform-only reporting and unstable attribution. Trigger: platform conversions disagree with downstream leads. Worked here: attribution SDK, ingress, dashboard API, lead, attribution, and session contracts exist (`attribution_v2.md:13-16`, `:160-162`). Failed here: public suffix cookies and `setUserId` rotation can break sessions/windows (`attribution_v2.md:117-119`, `:153-155`).
5. Kill-vs-scale criteria. Decision: analysts recommend; writes happen only after evidence and guardrails. Trigger: budget/targeting/keyword/creative change. Worked here: ResultEnvelope has success/errors and `lawyer_marketing` separates analysis, validation, execution, logging, and read/write skills (`getu_ads_v2.md:61-72`; `lawyer_marketing.md:248-269`). Failed here: ignoring non-success envelopes or policy failures scales broken campaigns (`getu_ads_v2.md:72`, `:704`).
Kill criteria: envelope errors, credential drift, attribution loss, policy failure, cost_per_conversion drift, or low data confidence. Scale criteria: increase only after reporting, attribution, and vertical benchmarks agree.

## Q12 - Social Cognition
1. Platform game theory. Decision: each platform has its own discovery surface and norms. Trigger: cross-platform post/reply/listen. Worked here: Reddit Scout starts from company, audience, pain points, competitors, and subreddits (`reddit-scount.md:124-139`). Failed here: YouTube demo is only query/maxResults search; treating it as full social strategy misses community/reply dynamics (`youtube-api-demo.md:7-20`, `:52-54`).
2. Algorithm preference modeling. Decision: use platform ranking inputs, not generic content score. Trigger: topic selection/evaluation. Worked here: Reddit sort supports relevance/hot/top/new/comments; YouTube exposes query/maxResults and metadata (`reddit-scount.md:256-265`; `youtube-api-demo.md:11-14`). Failed here: `xurl` post/reply/search commands do not encode algorithm-quality rubric (`openclaw-marketing.md:7502-7507`, `:7550-7581`).
3. Community fit before brand voice. Decision: find where users gather before tone/posting. Trigger: entering Reddit/X/Slack/Discord. Worked here: Reddit Scout derives target subreddits, then rotates keyword/competitor searches to real posts/comments (`reddit-scount.md:135-139`, `:141-181`). Failed here: `xurl` can post/reply from text and IDs with no community-fit check (`openclaw-marketing.md:7392-7422`, `:7502-7507`).
4. Viral mechanics. Decision: amplification needs quote/repost/reply/follow/mentions plus quota monitoring. Trigger: shift from listening to amplification. Worked here: `xurl` exposes quote/repost/follow/mentions/media and credit monitor tracks balance, burn, days remaining (`openclaw-marketing.md:7502-7531`; `x-api-credit-monitor.md:13-17`). Failed here: low balance or expired cookies require alert/re-login before viral loops continue (`x-api-credit-monitor.md:57`, `:117-125`).
5. Automation visibility cost. Decision: automation must be opt-in, gated, and channel-aware. Trigger: bot receives DMs/groups/replies/events. Worked here: OpenClaw uses DM pairing, allowlists, group routing, mention gating, reply tags, and per-channel chunking (`openclaw-marketing.md:122-126`, `:157-158`). Failed here: public inbound DMs need explicit opt-in, and bare X post/reply can bypass moderation (`openclaw-marketing.md:126`, `:7550-7568`).
Anti-patterns: one tone across platforms; search API as community understanding; amplification without quota/session monitoring; posting before moderation/approval.

## Q13 - Shared Foundations
| foundation | contract/interface | evidence | share vs isolate decision |
|---|---|---|---|
| identity/session | tenant/user/session IDs, Core RequestContext or signed envelope | `growth-engine-legacy.md:43-50`; `getuai-api.md:23-37`; `attribution_v2.md:153-162` | share; engines never own raw identity |
| credentials/secrets | scoped leases, env sync, re-login/low-balance monitor | `growth-engine-legacy.md:64-88`; `getuai-ads.md:21-28`; `x-api-credit-monitor.md:12-18` | share trust/rotation; isolate SDK calls |
| data lake/artifact store | artifacts/events/results keyed by tenant/target/run/action/source | `getuai-api.md:24-42`; `rankncompare.md:49-56`; `attribution_v2.md:13-16`; `gmi-prototype.md:11-16` | share ownership/retention; isolate schemas |
| task queue/schedules | schedule registry, cron/launchd adapters, queue/dead-letter | `growth-engine-legacy.md:64-88`; `x-api-credit-monitor.md:20`, `:82-93`; `attribution_v2.md:49-52` | share lifecycle; isolate quota cadence |
| observability | run_event, request IDs, Sentry/Langfuse/Grafana, redaction | `growth-engine-legacy.md:64-70`; `LLMRush.md:19-23`; `attribution_v2.md:107-119` | share traces; isolate dashboards |
| LLM gateway | provider/model routing, prompt policy, token/cost tracking | `getuai-seo.md:78-91`; `getuai-email-2.0.md:14`; `openclaw-marketing.md:175-180`; `cuilawgroup.md:25-27` | share cost/failover; isolate prompts |
| human-in-loop console | approvals, overrides, kill-switches, action ledger, read/write split | `growth-engine-legacy.md:83-88`; `lawyer_marketing.md:248-269`; `getuai-email-2.0.md:115-118`; `openclaw-marketing.md:122-126` | share workflow/audit; isolate validation |
| repo-template conventions | AGENTS/CLAUDE, skills, CI, version check, idempotent apply | `optiminds-repo-template.md:9-30`, `:55-63`, `:156-177` | share governance; isolate product logic |
Decision rule: share tenant trust, credentials, ledgers, approvals, schedules, observability, LLM routing; isolate schema, API, ranking logic, tone, and kill criteria. Worked example: attribution events are shared (`attribution_v2.md:13-16`, `:153-162`), but SEO ranking logic stays isolated between sitemap publishing (`rankncompare.md:128-157`) and LLM answer sensing (`LLMRush.md:7-14`).

## Q14 - Build Sequence
| milestone | scope | dependencies | done_criteria | next_trigger | deferrals |
|---|---|---|---|---|---|
| Day-1 | Core tenant/session/artifact/source registry/repo-template/approval stub; implements Q13 before Q1-Q8 | none; `growth-engine.md:8-12` and repo-template governance | target can be created; sessions/artifacts/approvals persist; no `runs/` leakage | first durable artifact/credential need | defer ads mutations/social posting due Q15 approval risk |
| Week-1 | SEO/GEO read-only using Q5 site/search/keyword/sitemap skills; implements Q1 | Day-1 Core + Q13 credentials/artifacts | crawl/search/keyword artifacts stored; ranking source declared; review point exists | recurring checks or publish need | defer auto-publish until GEO evaluator + kill-switch exist |
| Week-2 | Content lane using Q6 template/import/draft/SMTP/retrieval; implements Q2/Q10 | Core + content store + LLM gateway | variables validate; recipients import; drafts generated; review before send; SMTP test passes | first outbound campaign or metric request | defer rich media until artifact-store issue solved |
| Week-4 | Ads read-only + attribution using Q7 credential/report/attribution and Q11 CAC/pacing | Core credentials + Content campaign IDs + Q13 attribution contract | reports and conversion events visible; session tests pass; analysts read-only | repeated manual budget recommendations | defer budget mutation/A-B automation |
| Week-8 | Controlled writes for SEO/email/ads/social behind approval; uses Q7 envelopes and Q8 gating/credit/post skills | read-only evidence + Q13 human-in-loop + Q15 write prophylactic | every write has approval, ledger, rollback/kill-switch, quota/session monitor | stable weekly outcomes and repeated approvals | defer cross-platform optimizer |
| Week-12 / Month-3 | OODA orchestration across all domains with industry pack injection and Q9-Q12 guardrails | all lanes + observability + schedules + vertical case lessons | one tenant runs weekly observe-plan-approve-execute-review with override and kill criteria | scale tenants/industries | defer Temporal-scale workflow, marketplace, autonomous spend |
Evidence: prototype scaffolds (`getuai-2.0.md:19-42`), MVP routing (`getuai-mvp.md:9-76`), production attribution migration (`attribution_v2.md:16-23`), vertical hardening (`lawyer_finder.md:11-16`; `cuilawgroup.md:10-27`), and `growth-engine` backend-skeleton-first sequence (`growth-engine.md:8-12`).

## Q15 - Cross-Domain Failure Modes
| failure_mode | affected_domains | recurrence_count | structural_cause | early_symptom | prophylactic | evidence_pair |
|---|---|---:|---|---|---|---|
| Domain engines own platform facts | SEO, Ads, Social | 3 | identity/credentials/schedules scattered | engines ask for raw tokens/run own cron | Core owns facts; engines get context/leases. Enforced by Q13 + Q7 credential + Q8 credit monitor | `growth-engine-legacy.md:43-50`, `:83-88` |
| Legacy scaffolding import | all | 4 | copying old attempt instead of contracts | stale paths/missing runtime | greenfield rewrite; references read-only. Enforced by Q13 templates + Q14 Day-1 | `growth-engine.md:69-100`, `:138-152` |
| Missing runtime core after docs | all | 4 | docs exist but core tree absent | docs mention Core, no runtime | Day-1 skeleton before domains. Enforced by Q14 done criteria | `growth-engine-legacy.md:16-22`, `growth-engine.md:11-12` |
| Platform API credential drift | SEO, Ads, Social | 3 | env/session/auth outside action layer | API errors/re-login alerts | credential leases + monitors. Enforced by Q7/Q8/Q5 | `getuai-ads.md:24-28`, `x-api-credit-monitor.md:13-17`, `growth-engine-legacy.md:85` |
| Attribution/session breakage | Ads, Content | 2 | cookies/user rotation misunderstood | missing lead rows; SDK cookies not shared | SDK domain config + session tests. Enforced by Q7 attribution + Q6 campaigns + Q13 event contract | `attribution_v2.md:117-119`, `:153-155`, `:184-186` |
| Write operations without approval | SEO, Ads, Social | 3 | read/write mixed | agents mutate while analyzing | read-only analysis, write hooks, ledger. Enforced by Q7, Q8, Q6, Q13 | `lawyer_marketing.md:248-269`, `growth-engine-legacy.md:84` |
| Static publisher treated as GEO evaluator | SEO/GEO | 1 | sitemap confused with LLM visibility | sitemap exists but no LLM rank signal | add LLMRush sensor. Enforced by Q5 sitemap + Q6 rank summary | `rankncompare.md:134-149`, `LLMRush.md:7-14` |
| Prototype-local artifact store | Content, Social | 2 | media saved locally only | outputs no campaign/outcome link | Core artifact store with owner/run/action IDs. Enforced by Q13 + Q6 image composer | `gmi-prototype.md:14`, `:50`, `getuai-api.md:24-40` |
| API prefix/proxy mismatch | shared infra | 2 | local/prod routes diverge | frontend calls wrong backend path | configurable API_PREFIX/proxy. Enforced by Q13 config + Q14 env contract | `getuai-mvp.md:9-76` |
Strongest prophylactic: shared Core for trust/ledgers, isolated adapters for APIs, human approval before writes, and monitors for quotas, sessions, and attribution.
