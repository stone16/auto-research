# Knowledge Base

Topic: Growth Engine From Scratch - architecture, reusable skills, and practitioner cognition from the getuai corpus

Iteration: 14 Q13 foundation IDs plus Q2/Q4 architecture trace parity

## Evidence Policy

Direct citations use `repo.md:line-line` from `runs/growth-engine-from-scratch/sources/_raw/`. Source IDs are mirrored in top-level benchmark citation arrays.

## Stable Artifact ID Contract

Cross-model evaluability depends on stable row IDs, not prose position. Q1-Q4 architecture trace rows use `q1.trace*` through `q4.trace*`; Q13 shared foundations use `q13.f1` through `q13.f8`; Q5-Q8 skill rows use `seo.skill*`, `content.skill*`, `ads.skill*`, and `social.skill*`; Q9-Q12 cognition rows use `q9.cog*` through `q12.cog*`; Q14 milestones use `q14.m1` through `q14.m6`; Q15 failure modes use `q15.fm1` through `q15.fm9`. Benchmark answers and cross-question hooks should cite these IDs when they depend on a specific artifact row.

## Architecture Trace Contract

For Q1-Q4, every trace row is read as input -> component -> state -> output and terminates in one direct file:line citation. Each domain also has a component-order table with the schema `order | component | input | state | output | citation`, so reviewers can score architecture grounding symmetrically across SEO/GEO, Content, Ads, and Social. Shared Core is cited only where the step crosses the trust, approval, credential, schedule, ledger, observability, or kill-switch boundary; domain repos own domain logic.

## Q1 - SEO/GEO Architecture

Converged architecture: UI/product shell -> SEO/GEO tool adapters -> AI/recommendation layer -> Core-owned identity, credentials, artifacts, schedules, approvals, ledgers, and kill-switch. Evidence: `getuai-seo.md:7-11`, `getuai-seo.md:93-97`, `getuai-api.md:7-28`, `growth-engine-legacy.md:43-50`, `growth-engine-legacy.md:83-88`. Repos disagree on packaging: `getuai-seo` is a three-service product, `rankncompare` is a static publisher/content store, and `growth-engine-legacy` makes Core the only browser-facing owner of platform facts.

| step | input -> component -> state -> output trace |
|---|---|
| q1.trace1 | URL/site -> site-structure analyzer -> crawl/meta/link state -> artifact candidate (`getuai-plugin.md:11-14`) |
| q1.trace2 | query/domain -> search/competitor/keyword tools -> SERP/competitor/keyword state -> intent input (`getuai-plugin.md:16-20`) |
| q1.trace3 | term/company -> SEO keyword/rank metrics -> campaign-rank state -> SEO signal (`getuai-seo.md:101-106`) |
| q1.trace4 | term/company -> LLMRush multi-model rank/sentiment -> rank/sentiment state -> GEO signal (`LLMRush.md:7-14`) |
| q1.trace5 | category/product JSON -> content store -> product/category/metadata state -> publishable corpus (`rankncompare.md:128-149`) |
| q1.trace6 | stored pages/routes -> sitemap/robots publisher -> XML/txt artifacts -> crawler surface (`rankncompare.md:53-56`) |
| q1.trace7 | publish/check request -> Core approval/ledger/kill-switch -> approved or stopped action -> audit trail (`growth-engine-legacy.md:83-88`) |
| q1.trace8 | page + keyword + rank gap -> content optimization generator -> recommendation artifact -> human review candidate (`getuai-seo.md:103-106`) |

Trace lock: SEO/GEO is not a single service. It is a reviewable chain: crawl/search inputs feed ranking sensors, ranking signals feed a content store and generator, published crawler surfaces feed evaluators, and any write crosses Core approval and kill-switch. External dependencies are search APIs, Google Ads/Custom Search credentials, LLM providers, CMS/static publishing, and Core credential leases; failure handling is retry/logging at adapters, stored artifacts for replay, and stopped actions at Core.

| order | component | input | state | output | citation |
|---:|---|---|---|---|---|
| 1 | crawler/search adapter | URL, site, query, domain | crawl/meta/link/SERP state | discovery artifact | `getuai-plugin.md:11-20` |
| 2 | ranking signal source | term, company, campaign | keyword/rank metrics | SEO ranking signal | `getuai-seo.md:101-106` |
| 3 | GEO evaluator sensor | term, URL, model set | rank/sentiment/history | LLM visibility signal | `LLMRush.md:7-14` |
| 4 | content store | category/product JSON | products/categories/metadata | publishable corpus | `rankncompare.md:128-149` |
| 5 | publisher | stored routes/pages | sitemap.xml/robots.txt | crawler-facing surface | `rankncompare.md:53-56` |
| 6 | human-in-loop Core control | publish or optimization request | action ledger/approval state | approved, overridden, or killed action | `growth-engine-legacy.md:83-88` |

Disagreement is architectural, not cosmetic: `getuai-seo` converges on a UI/MCP/AI product shell, `rankncompare` keeps a static publisher/content store, and `growth-engine-legacy` rejects engines owning platform facts. The trade-off is speed versus auditability: direct publishers ship quickly, but the from-scratch design should keep crawler/evaluator/publisher domain-specific while putting credentials, approvals, schedules, ledgers, and kill-switches in Core.

## Q2 - Content Writing Architecture

Architecture: campaign/entity facts -> ideation -> outline -> draft -> edit/review -> publish -> post-publish learning. `getuai-email-2.0` provides the concrete path: campaign CRUD, recipient import, SMTP CRUD/test, batch create, AI generate, review, send (`getuai-email-2.0.md:70-73`, `getuai-email-2.0.md:91-118`). Load-bearing choices are style guide injection through prompt variables, recipient schema, SMTP test, human review, and shared API artifact/session storage (`getuai-api.md:24-40`). Stylistic choices are table UI, template file format, and frontend stack.

| step | input -> component -> state -> output trace |
|---|---|
| q2.trace1 | campaign fields/style variables -> prompt-template form -> reusable prompt state -> ideation/outline contract (`getuai-email-2.0.md:91-94`) |
| q2.trace2 | CSV recipient fields -> import service -> recipient records -> personalization input (`getuai-email-2.0.md:101-104`) |
| q2.trace3 | batch + prompt + recipient -> LLM generator -> generated email rows -> draft output (`getuai-email-2.0.md:111-114`) |
| q2.trace4 | generated emails -> human review -> approved content state -> sendable batch (`getuai-email-2.0.md:111-118`) |
| q2.trace5 | SMTP account + approved batch -> SMTP test/send -> sent/failed status -> publish outcome (`getuai-email-2.0.md:96-99`) |
| q2.trace6 | image/text/company artifacts -> API store -> session-scoped content -> post-publish input (`getuai-api.md:24-40`) |
| q2.trace7 | factual question -> retrieval-grounded copy -> cited answer -> hallucination guard (`reddit-scount.md:233-239`) |

Trace lock: Content is a staged workflow, not a generic writer agent. Ideation and outline are constrained by campaign fields and style variables; draft generation is LLM-owned; edit/review and SMTP testing are human/control-plane owned; publish is a send or artifact write; post-publish learning comes from sent/failed status, retrieval citations, and rank/sentiment sensors. Style guide injection, recipient grounding, SMTP validation, review-before-send, and retrieval grounding are load-bearing because removing them breaks correctness; spreadsheet styling and UI layout are stylistic.

| order | component | input | state | output | citation |
|---:|---|---|---|---|---|
| 1 | campaign and prompt workspace | campaign name, description, style variables | campaign/prompt-template state | ideation and outline contract | `getuai-email-2.0.md:70-73`, `getuai-email-2.0.md:91-94` |
| 2 | recipient import | CSV email, first_name, last_name, company, position | recipient records | personalization input | `getuai-email-2.0.md:101-104` |
| 3 | SMTP account validator | SMTP host/account/test action | tested sender state | send eligibility | `getuai-email-2.0.md:96-99` |
| 4 | batch planner | campaign, recipients, selection strategy, quantity | batch state | generation queue | `getuai-email-2.0.md:107-114` |
| 5 | LLM draft generator | prompt template plus recipient facts | generated email rows | draft copy | `getuai-email-2.0.md:111-114` |
| 6 | human review/edit gate | generated emails | approved or revised content state | sendable batch | `getuai-email-2.0.md:111-118` |
| 7 | publish/send adapter | approved batch plus active SMTP account | sent/failed status | outbound outcome | `getuai-email-2.0.md:116-118` |
| 8 | retrieval/factual guard | factual question and web context | cited answer artifact | hallucination-controlled copy | `reddit-scount.md:233-239` |

## Q3 - Ads Architecture

Architecture: campaign feed -> bidding/budget/targeting -> reporting -> attribution -> optimization. `getuai-ads` shows the UI/MCP/AI product and credential dependencies (`getuai-ads.md:7-11`, `getuai-ads.md:24-28`). `getu_ads_v2` is the agent-safe Google Ads adapter: stdin/file JSON, `exec run`, compact `ResultEnvelope`, and 38 operations (`getu_ads_v2.md:9-67`, `getu_ads_v2.md:1010-1017`). Platform SDKs and mutations stay platform-bound; ResultEnvelope, attribution events, reporting lake, anomaly/pacing checks, and kill criteria are platform-agnostic. `getuai-ads-data` supplies cross-platform campaign/conversion tables (`getuai-ads-data.md:216-250`). `attribution_v2` supplies browser SDK -> ingress/consumer -> Pub/Sub -> events/leads/scores (`attribution_v2.md:13-16`).

| step | input -> component -> state -> output trace |
|---|---|
| q3.trace1 | credentials + campaign brief -> Ads UI/MCP/AI -> campaign feed/recs -> operator workbench (`getuai-ads.md:7-11`) |
| q3.trace2 | operation JSON -> google-ads-cli exec -> ResultEnvelope state -> agent-readable output (`getu_ads_v2.md:9-67`) |
| q3.trace3 | campaign/adgroup/keyword/RSA/budget payload -> 38 ops -> platform campaign tree -> mutation/list result (`getu_ads_v2.md:1010-1017`) |
| q3.trace4 | date range/GAQL -> reports -> campaign/ad/search-term metrics -> optimization input (`getu_ads_v2.md:1048-1123`) |
| q3.trace5 | SDK event + UTM + user/session -> attribution ingress/consumer -> event-table state -> conversion/lead score (`attribution_v2.md:13-16`) |
| q3.trace6 | Google/Meta/TikTok report rows -> ads data platform -> campaign/conversion model -> trend/anomaly candidate (`getuai-ads-data.md:216-250`) |
| q3.trace7 | budget/targeting rec -> read/write approval boundary -> blocked or approved action -> action log (`lawyer_marketing.md:248-269`) |
| q3.trace8 | unsafe write/lost attribution/envelope error -> Core kill-switch -> freeze/pause/reduce -> audited stop (`growth-engine-legacy.md:83-88`) |
| q3.trace9 | Google/Meta/TikTok normalized rows -> platform-agnostic analyst -> anomaly/pacing state -> kill-vs-scale recommendation (`getuai-ads-data.md:216-250`) |

Trace lock: Ads has two boundaries. Platform-bound code is the Google Ads operation adapter and credentialed mutations; platform-agnostic logic is the ResultEnvelope, reporting lake, attribution event model, anomaly detection over trends, budget pacing, approval ledger, and kill criteria. Bidding is a controlled mutation, not a background optimizer; the first safe version reads reports and attribution, emits a recommendation, and requires human-in-loop approval before a budget or bidding write.

| order | component | input | state | output | citation |
|---:|---|---|---|---|---|
| 1 | campaign feed workbench | credentials, brief, uploaded data | campaign/account/session context | recommendations and operator queue | `getuai-ads.md:7-11` |
| 2 | platform API adapter | operation JSON via stdin/file | ResultEnvelope | agent-readable success/errors | `getu_ads_v2.md:9-67` |
| 3 | campaign data model | campaign/ad group/keyword/RSA/budget payload | Google campaign tree | mutation or list result | `getu_ads_v2.md:1010-1017` |
| 4 | bidding and budget pacing | campaign id, amount, geo, language, bidding op | budget/criteria state | pacing or bid-change candidate | `getu_ads_v2.md:1131-1149` |
| 5 | reporting and anomaly detection input | date range or GAQL | campaign/ad/search-term metrics | trend/anomaly signal | `getu_ads_v2.md:1048-1123` |
| 6 | attribution model | SDK event, UTM, user/session | events/leads/scores tables | conversion event and lead score | `attribution_v2.md:13-16` |
| 7 | cross-platform reporting lake | Google/Meta/TikTok rows | campaign/conversion tables | platform-agnostic analysis surface | `getuai-ads-data.md:216-250` |
| 8 | human-in-loop approval and kill criteria | budget/targeting/write recommendation | read/write gate and action log | blocked, approved, paused, or reduced spend | `lawyer_marketing.md:248-269` |
| 9 | Core kill-switch | unsafe write, lost attribution, envelope error | action ledger/stop state | audited stop | `growth-engine-legacy.md:83-88` |

## Q4 - Social Architecture

Architecture: listen, post, schedule, engage, monitor as platform adapters behind a Gateway-style control plane, not a fake universal adapter. Reddit listening/topic selection: `reddit-scount.md:108-181`. YouTube search adapter: `youtube-api-demo.md:48-54`. X post/reply/search: `openclaw-marketing.md:7392-7422`. OpenClaw multi-channel Gateway: `openclaw-marketing.md:132-158`. Credit/rate monitoring: `x-api-credit-monitor.md:7-17`, `x-api-credit-monitor.md:72-104`. Moderation gate: `openclaw-marketing.md:122-126`.

| step | input -> component -> state -> output trace |
|---|---|
| q4.trace1 | company URL -> Reddit analysis -> keywords/pain/competitors/subreddits -> listen state (`reddit-scount.md:108-139`) |
| q4.trace2 | analysis + keyword/competitor index -> Reddit discovery -> posts/comments -> engagement cache (`reddit-scount.md:141-181`) |
| q4.trace3 | query + maxResults -> YouTube adapter -> video list -> monitor candidates (`youtube-api-demo.md:48-54`) |
| q4.trace4 | text/post_id/query/media -> X skill -> platform JSON/side effect -> post/reply/search output (`openclaw-marketing.md:7392-7422`) |
| q4.trace5 | channel message -> Gateway adapter -> routed session/inbox -> engage surface (`openclaw-marketing.md:132-158`) |
| q4.trace6 | schedule + Chrome session + threshold -> launchd credit monitor -> heartbeat/alert state -> quota output (`x-api-credit-monitor.md:72-104`) |
| q4.trace7 | generated reply -> DM allowlist policy -> allow/deny state -> moderated automation (`openclaw-marketing.md:122-126`) |

Trace lock: Social has a shared control plane but not a shared platform semantics layer. Gateway unifies session routing and channel inboxing; Reddit, YouTube, X, Slack, and credit monitors remain per-platform adapters because each platform exposes different search, reply, media, rate-limit, and moderation constraints. The correct abstraction is message/session/approval/monitor state, not a pretend universal post object. Content moderation belongs before public or DM side effects, and credit accounting belongs in scheduled monitors with operator-visible alerts.

| order | component | input | state | output | citation |
|---:|---|---|---|---|---|
| 1 | Reddit listen analyzer | company URL | keywords, pain points, competitors, subreddits | listen state | `reddit-scount.md:108-139` |
| 2 | Reddit discovery/topic selector | analysis plus keyword or competitor index | posts/comments cache | engagement candidates | `reddit-scount.md:141-181` |
| 3 | YouTube monitor adapter | query and maxResults | video result list | monitor candidates | `youtube-api-demo.md:48-54` |
| 4 | X post/reply/search adapter | text, post_id, query, media | X side effects and JSON response | post, reply, or search output | `openclaw-marketing.md:7392-7422` |
| 5 | multi-channel Gateway | channel message and session | routed inbox/session state | engage surface | `openclaw-marketing.md:132-158` |
| 6 | credit and rate monitor | schedule, Chrome session, threshold | heartbeat, spend, low-balance state | quota alert | `x-api-credit-monitor.md:7-17`, `x-api-credit-monitor.md:72-104` |
| 7 | moderation and allowlist gate | generated reply or DM action | allow/deny policy state | constrained automation | `openclaw-marketing.md:122-126` |

## Q5-Q8 Skill Catalog

Schema note: the artifact keeps the original 8 contract columns and adds stable `row_id` plus domain so each row can be scored independently. IDs are canonical and must not be renumbered after future insertions; add suffixes instead.

| row_id | domain | skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|---|---|
| seo.skill1 | SEO | seo-campaign-console | getuai-seo | `getuai-seo.md:93-106` | web+AI | campaign/account/files/metrics | recs/metrics | sessions/API | duplicate ads console pattern |
| seo.skill2 | SEO | keyword-research-tracking | getuai-seo | `getuai-seo.md:101-102` | MCP/API | seed/site/locale | keywords/ranks | campaign store | overlaps plugin ideas |
| seo.skill3 | SEO | content-optimization | getuai-seo | `getuai-seo.md:103` | AI rec | page+keyword | edits/recs | artifacts | prompt drift checks |
| seo.skill4 | SEO | backlink-analysis | getuai-seo | `getuai-seo.md:104` | MCP/API | domain/url | backlinks | campaign store | unique sample |
| seo.skill5 | SEO | competitor-analysis | getuai-seo/getuai-competitor-analysis | `getuai-competitor-analysis.md:7-21` | MCP | company/query | competitors/SERP | DB/files | duplicate; plugin canonical |
| seo.skill6 | SEO | site-structure-analyzer | getuai-plugin | `getuai-plugin.md:11-14` | FastAPI | URL/site | crawl/meta/links | logs | retry external fetches |
| seo.skill7 | SEO | google-search-analyzer | getuai-plugin | `getuai-plugin.md:16` | FastAPI | query/domain | SERP insights | stateless/logs | Google dependency |
| seo.skill8 | SEO | keyword-clustering | getuai-plugin | `getuai-plugin.md:20` | FastAPI | keywords | clusters | stateless | retry model/API |
| seo.skill9 | SEO | sitemap-robots-generator | rankncompare | `rankncompare.md:53-56`, `rankncompare.md:134-149` | build/route | category/product data | sitemap/robots | JSON/static | no deprecation marker; rebuild on route/schema change |
| content.skill1 | Content | campaign-prompt-template | getuai-email-2.0 | `getuai-email-2.0.md:91-94` | UI | placeholders/style variables | prompt | campaign DB | controls register drift |
| content.skill2 | Content | personalized-email-draft | getuai-email-2.0 | `getuai-email-2.0.md:111-114` | batch | recipient+prompt | draft | batch DB | recipient grounding |
| content.skill3 | Content | recipient-import | getuai-email-2.0 | `getuai-email-2.0.md:101-104` | API/CSV | CSV fields | recipients | MySQL | validate schema |
| content.skill4 | Content | smtp-test-and-send | getuai-email-2.0 | `getuai-email-2.0.md:96-99`, `getuai-email-2.0.md:116-118` | UI/API | SMTP+batch | send status | SMTP DB | review before send |
| content.skill5 | Content | cited-websearch-copy | reddit-scount | `reddit-scount.md:233-239` | service | query/context | cited answer | logs | hallucination guard |
| content.skill6 | Content | multi-model-rank-summary | LLMRush | `LLMRush.md:7-14` | web/API | term/URL | rank/sentiment | history | GEO drift |
| content.skill7 | Content | image-text-composer | openclaw-marketing | `openclaw-marketing.md:5104-5152` | CLI | prompt+images | asset/meta | files | path mapping |
| content.skill8 | Content | summarizer-transcriber | openclaw-marketing | `openclaw-marketing.md:6656-6716` | CLI | URL/file | summary/transcript | files/logs | no deprecation marker; provider fallback |
| ads.skill1 | Ads | google-ads-cli | getu_ads_v2 | `getu_ads_v2.md:9-67` | CLI stdin/file | op+JSON+config | envelope | API effects | Google-bound shell |
| ads.skill2 | Ads | campaign-management | getu_ads_v2 | `getu_ads_v2.md:1010` | CLI | campaign | create/list/update | Google Ads | kill on envelope/policy error |
| ads.skill3 | Ads | keyword-management | getu_ads_v2 | `getu_ads_v2.md:1012`, `getu_ads_v2.md:923-950` | CLI | ad_group+keywords | criteria result | Google Ads | validate match types |
| ads.skill4 | Ads | rsa-creative-management | getu_ads_v2 | `getu_ads_v2.md:1013`, `getu_ads_v2.md:630-704` | CLI | headlines/descriptions/url | RSA result | Google Ads | fatigue via ad reports |
| ads.skill5 | Ads | budget-targeting | getu_ads_v2 | `getu_ads_v2.md:1014`, `getu_ads_v2.md:1131-1149` | CLI | campaign/amount/geo/lang | budget/criteria | Google Ads | pacing guardrail |
| ads.skill6 | Ads | composite-campaign-build | getu_ads_v2 | `getu_ads_v2.md:630-704` | CLI | campaign+groups+ads | campaign tree | Google Ads | no deprecation marker; retry from envelope/ledger, not blind replay |
| ads.skill7 | Ads | reporting-gaql | getu_ads_v2 | `getu_ads_v2.md:1048-1123` | CLI | date/query | metrics/GAQL | report | agnostic envelope |
| ads.skill8 | Ads | attribution-ingest | attribution_v2 | `attribution_v2.md:13-16` | SDK+API | UTM/events/user | events/leads/scores | tables/PubSub | conversion backbone |
| ads.skill9 | Ads | platform-credential-sdk | getuai-ads-sdk | `getuai-ads-sdk.md:7-12`, `getuai-ads-sdk.md:146-161` | SDK | user/token/platform | credentials | Redis/API | kill if unavailable |
| social.skill1 | Social | reddit-opportunity-analysis | reddit-scount | `reddit-scount.md:108-139` | API | URL | keywords/pain/competitors | MySQL | Reddit-bound |
| social.skill2 | Social | reddit-discovery | reddit-scount | `reddit-scount.md:141-181` | API | analysis+index | posts/comments | MySQL/cache | topic selection |
| social.skill3 | Social | youtube-search | youtube-api-demo | `youtube-api-demo.md:48-54` | HTTP | query/maxResults | videos | stateless | quota/API risk |
| social.skill4 | Social | x-credit-monitor | x-api-credit-monitor | `x-api-credit-monitor.md:7-17`, `x-api-credit-monitor.md:72-104` | launchd | session/threshold | Lark alert | logs/env | re-login monitor |
| social.skill5 | Social | x-post-reply-search | openclaw-marketing | `openclaw-marketing.md:7392-7422` | CLI | text/id/query/media | post/reply/search | X side effects | API break risk |
| social.skill6 | Social | multi-channel-inbox | openclaw-marketing | `openclaw-marketing.md:132-158` | Gateway | channel/session | routed message | gateway store | adapter abstraction |
| social.skill7 | Social | slack-actions | openclaw-marketing | `openclaw-marketing.md:6314-6339` | tool | channel/message/content | reaction/send/edit | Slack effects | per-platform semantics |
| social.skill8 | Social | channel-gating | openclaw-marketing | `openclaw-marketing.md:122-126` | config | dmPolicy/allowFrom | allow/deny | config | no deprecation marker; moderation guard |

Margin audit: Q5 has 9 rows (`seo.skill1`-`seo.skill9`), Q6 has 8 (`content.skill1`-`content.skill8`), Q7 has 9 (`ads.skill1`-`ads.skill9`), Q8 has 8 (`social.skill1`-`social.skill8`). Protected rows: `seo.skill9`, `content.skill8`, `ads.skill6`, `social.skill8`.

## Q9-Q12 Cognition Evidence Table

Read each row as: stable row ID -> model -> trigger -> worked-here evidence -> failed-here evidence -> anti-pattern -> hook to architecture, skill, or failure-mode sections. Every model is paired; unsupported cognition claims are intentionally excluded. Stable `q9.cog*` through `q12.cog*` IDs are part of the evaluation contract, mirroring `q1.trace*`, skill row IDs, `q13.f*`, and `q15.fm*` so judges can score cognition row-by-row.

| row_id | domain | model_name | trigger | worked_here (file:line) | failed_here (file:line) | anti_pattern | hook_to_skill_or_failure_mode |
|---|---|---|---|---|---|---|---|
| q9.cog1 | SEO/GEO | topical authority | Category or product corpus needs searchable depth, not one-off pages | `rankncompare.md:128-187` | `getuai-2.0.md:19-42` | Thin AI-Studio prototype treated as durable SEO corpus | Q1 content store + `seo.skill9`; `q15.fm8` prototype-local artifact store |
| q9.cog2 | SEO/GEO | intent mapping | Search term, competitor, or site URL must become a structured target map | `getuai-plugin.md:11-20` | `rankncompare.md:53-56` | Using sitemap generation as discovery or intent research | Q1 crawler/search adapter; `seo.skill7`/`seo.skill8` |
| q9.cog3 | SEO/GEO | E-E-A-T / vertical expertise | YMYL or legal domain claims require industry facts and reviewable authority | `lawyer_marketing.md:291-317` | `growth-engine.md:7-13`, `growth-engine.md:23-30` | Generic industry labels instead of product-vertical packs | Q13 domain-isolated industry packs; `q14.m6`; `q15.fm2` |
| q9.cog4 | SEO/GEO | GEO vs SEO pivot | Visibility question shifts from crawler indexability to LLM answer ranking/sentiment | `LLMRush.md:7-14` | `rankncompare.md:134-149` | Treating sitemap/robots output as a GEO evaluator | Q1 GEO evaluator sensor; `content.skill6`; `q15.fm7` |
| q9.cog5 | SEO/GEO | content velocity vs depth | Frequent optimization suggestions compete with durable, reviewed content assets | `getuai-seo.md:101-106` | `growth-engine-legacy.md:16-22` | Docs-heavy runtime plan with no executable Core tree | Q1 `q1.trace8`; `q14.m2`/`q14.m5`; `q15.fm3` |
| q10.cog1 | Content | user journey mapping | Recipient or audience state must drive ideation -> draft -> send | `getuai-email-2.0.md:70-118` | `gmi-prototype.md:7-54` | Local artifact generation detached from campaign/outcome state | Q2 staged content pipeline; `content.skill1`; `q15.fm8` |
| q10.cog2 | Content | content portfolio theory | Growth surface needs multiple media/content types, not only one channel | `openclaw-marketing.md:5104-5152`, `openclaw-marketing.md:6656-6716` | `getuai-email-2.0.md:70-73` | Treating email batch generation as the whole content system | `content.skill7`/`content.skill8`; `q14.m3` rich-media deferral |
| q10.cog3 | Content | distribution over production | Draft value is realized only when review, send, or publish path exists | `getuai-email-2.0.md:111-118` | `gmi-prototype.md:50` | Generating content into local folders without distribution ledger | Q2 human review/send; `content.skill4`; `q15.fm6` |
| q10.cog4 | Content | ROI time window | Content work should create measurable ranking/sentiment or outbound outcomes | `LLMRush.md:7-23` | `getuai-2.0.md:19-42` | Prototype UI with no metric loop | Q2 post-publish learning; `content.skill6`; `q14.m4` |
| q10.cog5 | Content | brand voice as forcing function | Prompt variables and review gates must constrain tone/register before send | `getuai-email-2.0.md:91-118` | `gmi-prototype.md:37-54` | Free-form prompt as brand system | `content.skill1` and human-review skills; `q15.fm6` |
| q11.cog1 | Ads | LTV/CAC discipline | Spend decision needs campaign metrics and vertical business value | `lawyer_marketing.md:291-304`, `getu_ads_v2.md:1048-1064` | `attribution_v2.md:117-119` | Optimizing spend while identity/session is missing | Q3 reporting + attribution model; `ads.skill7`/`ads.skill8`; `q15.fm5` |
| q11.cog2 | Ads | pacing logic | Budget or geo/language targeting changes are requested | `getu_ads_v2.md:1131-1149` | `getuai-ads.md:24-28` | Treating credential-dependent mutations as always available | Q3 bidding/budget pacing; `ads.skill5`; `q15.fm4` |
| q11.cog3 | Ads | creative fatigue curves | RSA/ad creative needs refresh based on ad-level performance | `getu_ads_v2.md:630-704`, `getu_ads_v2.md:1066-1086` | `getuai-ads-data.md:216-250` | Aggregate cross-platform rows used without ad-level creative diagnosis | Q3 reporting/anomaly input; `ads.skill4`; `q15.fm1` |
| q11.cog4 | Ads | attribution paradox | Better measurement increases operational fragility around session/cookie semantics | `attribution_v2.md:13-23` | `attribution_v2.md:151-186` | Believing attribution is solved by installing an SDK once | Q3 attribution model; `ads.skill8`; `q15.fm5` |
| q11.cog5 | Ads | kill-vs-scale criteria | Recommendation crosses read-only analysis into spend/write action | `lawyer_marketing.md:248-269` | `growth-engine-legacy.md:83-88` | Engines own writes or auto-restart spend loops after stop state | Q3 human-in-loop approval and Core kill-switch; `ads.skill2`/`ads.skill5`; `q15.fm6` |
| q12.cog1 | Social | platform-as-game-theory | Discovery or engagement depends on platform-native community rules | `reddit-scount.md:108-181` | `openclaw-marketing.md:122-158` | Universal social adapter without per-channel policy/gating | Q4 Reddit listen/discover + Gateway; `social.skill1`/`social.skill8`; `q15.fm6` guardrail |
| q12.cog2 | Social | algorithm preference modeling | Platform distribution mechanism is search, feed, reply, or video result | `youtube-api-demo.md:48-54`, `openclaw-marketing.md:7392-7422` | `reddit-scount.md:141-181` | Search-only monitor treated as engagement engine | Q4 YouTube/X adapters; `social.skill3`/`social.skill5`; `q15.fm7` analog |
| q12.cog3 | Social | community fit before brand voice | Topic/subreddit/competitor context must precede generated reply voice | `reddit-scount.md:108-139` | `openclaw-marketing.md:7392-7422` | Raw xurl/text posting before community-fit analysis | Q4 listen before post; `social.skill2`/`social.skill5`; `q15.fm6` |
| q12.cog4 | Social | viral mechanics | Post/reply/media affordances exist but need monitor loop to learn | `openclaw-marketing.md:7392-7422` | `youtube-api-demo.md:48-54` | Video search result treated as viral loop | Q4 post/monitor split; `social.skill5`/`social.skill3`; `q14.m5` |
| q12.cog5 | Social | automation visibility cost | Automation touches public/private channels and must be visibly constrained | `openclaw-marketing.md:122-126`, `x-api-credit-monitor.md:7-17` | `openclaw-marketing.md:132-158` | Always-on multi-channel assistant without explicit moderation and quota visibility | Q4 moderation + credit monitor; `social.skill8`/`social.skill4`; `q15.fm4` and `q15.fm6` |

Cognition synthesis: the recurring practitioner move is trigger discipline. Use a model only when its trigger is present, attach a worked/failed evidence pair, and route the resulting control to the matching skill or failure mode. That makes Q13-Q15 mechanical: shared infrastructure owns trust, schedules, ledgers, credentials, observability, LLM routing, and kill-switches; domain cognition owns interpretation of ranking, tone, spend, and community context.

## Q13 - Shared Foundations

Q13 is now a stable-ID table so Q14/Q15 hooks resolve to exact shared-foundation rows rather than a prose paragraph.

| row_id | foundation | shared_or_isolated_decision | owner_layer | citation | hooks_to_q14_q15 |
|---|---|---|---|---|---|
| q13.f1 | identity/session | Share tenant/user/session verification and internal context envelopes; isolate domain audience, lead, and profile schemas. Contract: session ID or RequestContext with versioned auth claims. | Core identity/session | `growth-engine-legacy.md:43-50`, `getuai-api.md:23-37`, `getuai-ui.md:23-50` | `q14.m1`; prevents `q15.fm1` and supports `q15.fm5` |
| q13.f2 | credentials/secrets | Share credential records, secret storage, rotation, scoped leases, and credential health; isolate provider-specific token use inside adapters. Contract: time-bound credential lease plus audit record. | Core credentials | `growth-engine-legacy.md:64-88`, `getuai-ads.md:21-28`, `x-api-credit-monitor.md:12-18` | `q14.m1`, `q14.m4`, `q14.m5`; prevents `q15.fm1` and `q15.fm4` |
| q13.f3 | data/artifacts | Share artifact IDs, source references, run ledgers, and data-lake joins; isolate domain tables such as products, recipients, campaign rows, posts, and events. Contract: typed artifact pointer plus domain payload schema. | Core artifacts/data lake with domain stores | `getuai-api.md:24-42`, `rankncompare.md:49-56`, `attribution_v2.md:13-16` | `q14.m1`, `q14.m2`, `q14.m4`; prevents `q15.fm5` and `q15.fm8` |
| q13.f4 | schedules/queues | Share workflow schedules, queues, run caps, stop reasons, and retry policy; isolate domain cadence and platform polling details. Contract: scheduled job envelope with terminal-stop semantics. | Core schedules/queues | `growth-engine-legacy.md:64-88`, `x-api-credit-monitor.md:72-104`, `attribution_v2.md:13-16` | `q14.m5`, `q14.m6`; prevents `q15.fm1`, `q15.fm3`, and `q15.fm4` |
| q13.f5 | observability | Share run events, logs, redaction, cost/trace correlation, and alert plumbing; isolate domain metric interpretation such as rank, spend, sentiment, and engagement. Contract: redacted event schema with request/run IDs. | Core observability plus domain sensors | `growth-engine-legacy.md:64-70`, `LLMRush.md:19-23`, `x-api-credit-monitor.md:7-17` | `q14.m6`; prevents `q15.fm1`, `q15.fm3`, and `q15.fm7` |
| q13.f6 | LLM gateway | Share provider routing, model credentials, cost controls, prompt envelopes, and citation enforcement; isolate domain prompts, evaluators, and recommendation logic. Contract: model invocation envelope plus citation/result metadata. | Core LLM gateway with domain skills | `getuai-seo.md:78-91`, `getuai-email-2.0.md:111-114`, `LLMRush.md:7-14` | `q14.m3`, `q14.m6`; prevents `q15.fm6` and `q15.fm7` |
| q13.f7 | human-in-loop console | Share approval, override, action ledger, and kill-switch controls; isolate domain-specific read/write policy and kill-vs-scale thresholds. Contract: proposed action -> approval state -> ledgered execution. | Core console/action ledger | `growth-engine-legacy.md:83-88`, `lawyer_marketing.md:248-269`, `openclaw-marketing.md:122-126` | `q14.m5`; prevents `q15.fm1` and `q15.fm6` |
| q13.f8 | repo-template governance | Share AGENTS/CLAUDE rules, CI, CODEOWNERS, template version checks, and org rulesets; isolate product logic and vertical packs. Contract: versioned repo baseline with read-only drift checks. | Repo governance layer | `optiminds-repo-template.md:9-63`, `optiminds-org-config.md:7-63`, `Pi.md:26-47` | `q14.m1`, `q14.m6`; prevents `q15.fm2` and `q15.fm9` |

Decision rule: put a component in shared Core when it controls tenant trust, credentials, durable artifacts, schedules/queues, observability, LLM provider routing, human approval, kill-switches, or repo governance. Keep it domain-isolated when it encodes platform API semantics, ranking logic, copy tone, bidding strategy, community rules, industry packs, or schema fields whose meaning changes by growth domain. New components must name their `q13.f*` dependency before they can be wired into `q14.m*`; if no row fits, the default is a domain adapter until two domains independently need the same contract.

## Q14 - Build Sequence

| row_id | milestone | scope | dependencies | done_criteria | next_trigger | deferrals |
|---|---|---|---|---|---|---|
| q14.m1 | Day-1 | Core tenant/session/artifact/source/approval skeleton from `q13.f1`, `q13.f3`, `q13.f7`, plus governance from `q13.f8` | none | target/session/artifact/action records persist; no run leakage | first durable tool | ads/social writes |
| q14.m2 | Week-1 | SEO/GEO read lane: Q1 crawl/search/keyword/sitemap via `seo.skill6`-`seo.skill9` | Core credentials/artifacts `q13.f2`/`q13.f3` | outputs stored, rank source declared, sitemap exists | recurring/publish request | autopublish |
| q14.m3 | Week-2 | Content lane: Q2 templates/import/draft/SMTP/retrieval via `content.skill1`-`content.skill5` | Core + SEO store + LLM gateway `q13.f6` | variables validate; drafts generated; review before send | outbound metric need | rich media |
| q14.m4 | Week-4 | Ads read + attribution via `ads.skill7`/`ads.skill8`; no spend mutation | credentials + campaign IDs + data lake `q13.f2`/`q13.f3` | reports + conversion events visible; read-only analyst | repeated budget recs | budget mutation/A-B |
| q14.m5 | Week-8 | Controlled writes across domains using Q3/Q4 approval and moderation guardrails | read evidence + approvals + `q13.f7` | every write has ledger, envelope, monitor | stable weekly outcomes | full optimizer |
| q14.m6 | Month-3 | OODA orchestration + industry packs, especially `q9.cog3` vertical expertise | all lanes + observability/schedules `q13.f4`/`q13.f5` | weekly observe-plan-approve-execute-review works | tenant/industry scale | Temporal/marketplace/autonomous spend |

Evidence shape: thin prototype `getuai-2.0.md:19-42`, MVP route hardening `getuai-mvp.md:9-76`, production refactor `attribution_v2.md:16-23`, vertical cases `lawyer_finder.md:11-16`, `cuilawgroup.md:10-27`, backend-skeleton-first `growth-engine.md:8-12`. Deferral logic is failure-informed: do not build autopublish before `q14.m2` has rank/source evidence; do not build budget mutation or A/B before `q14.m4` proves attribution; do not build autonomous spend before `q14.m6` proves OODA review and industry packs.

## Q15 - Failure Modes

| row_id | failure_mode | domains | count | cause | early symptom | prophylactic | evidence_pair |
|---|---|---|---:|---|---|---|---|
| q15.fm1 | engines own platform facts | SEO/Ads/Social | 3 | scattered identity/creds/schedules | raw tokens/own cron | Core facts/context leases via `q13.f1`, `q13.f2`, `q13.f4`, `q13.f7` | `growth-engine-legacy.md:43-50`, `growth-engine-legacy.md:83-88` |
| q15.fm2 | legacy scaffolding import | all | 4 | copying attempts | stale paths | greenfield contracts and repo governance `q13.f8`; `q9.cog3` vertical specificity | `growth-engine.md:69-152` |
| q15.fm3 | docs without runtime | all | 4 | design outruns core | no `core/` tree | Day-1 skeleton `q14.m1`; schedules/events via `q13.f4`/`q13.f5` | `growth-engine-legacy.md:16-22` |
| q15.fm4 | credential drift | SEO/Ads/Social | 3 | auth outside action layer | API/re-login errors | leases + monitors via `q13.f2`; `social.skill4` | `getuai-ads.md:24-28`, `x-api-credit-monitor.md:13-17` |
| q15.fm5 | attribution/session breakage | Ads/Content | 2 | cookie/user rotation | missing lead rows | SDK domain/session tests; identity/data contracts `q13.f1`/`q13.f3`; `ads.skill8` | `attribution_v2.md:117-186` |
| q15.fm6 | writes without approval | SEO/Ads/Social | 3 | mixed read/write skills | agents mutate while analyzing | read-only diagnosis + ledger via `q13.f7`; `q11.cog5`, `q12.cog1`, and `q12.cog5` guard public actions | `lawyer_marketing.md:248-269`, `growth-engine-legacy.md:84` |
| q15.fm7 | static publisher as GEO evaluator | SEO/GEO | 1 | indexing confused with LLM visibility | sitemap but no LLM rank | LLMRush sensor and gateway `q13.f6`; `content.skill6` | `rankncompare.md:134-149`, `LLMRush.md:7-14` |
| q15.fm8 | prototype-local artifact store | Content/Social | 2 | local media only | no campaign/outcome link | Core artifact store `q13.f3` | `gmi-prototype.md:14`, `gmi-prototype.md:50`, `getuai-api.md:24-40` |
| q15.fm9 | API prefix mismatch | shared | 2 | local/prod route drift | wrong backend path | API_PREFIX/proxy contract plus repo governance `q13.f8` | `getuai-mvp.md:9-76` |

ID lock: `q15.fm1`-`q15.fm9` are the canonical failure-mode rows. When a benchmark answer claims a prophylactic, it should cite the relevant `q15.fm*` row plus the cognition row and Q13 foundation row that prevents misapplication; for example `q15.fm6` uses `q13.f7` and `q12.cog1` to stop a universal social adapter from bypassing per-platform moderation.

## Benchmark Answers

Machine-readable benchmark answers are emitted in the top-level `benchmark_answers` JSON array. In-KB summary: Q1-Q4 now carry both trace rows and component-order tables; Q13 carries exact shared-foundation IDs (`q13.f1`-`q13.f8`); Q5-Q8 retain 34 skill rows with stable IDs (`seo.skill1`-`social.skill8`); Q9-Q12 carry stable cognition row IDs (`q9.cog1`-`q12.cog5`) and worked/failed evidence pairs; Q14 carries milestone IDs (`q14.m1`-`q14.m6`); Q15 carries failure-mode IDs (`q15.fm1`-`q15.fm9`).
