# Knowledge Base

Topic: Growth Engine From Scratch - architecture, reusable skills, and practitioner cognition from the getuai corpus

Iteration: 11 architecture trace lock

## Evidence Policy

Direct citations use `repo.md:line-line` from `runs/growth-engine-from-scratch/sources/_raw/`. Source IDs are mirrored in top-level benchmark citation arrays.

## Architecture Trace Contract

For Q1-Q4, every trace row is read as input -> component -> state -> output and terminates in one direct file:line citation. The trace is intentionally component-granular so reviewers can check architecture grounding without reconstructing a prose paragraph. Shared Core is only cited where the step crosses the trust, approval, credential, schedule, ledger, or kill-switch boundary; domain repos own domain logic.

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

Architecture: campaign/entity facts -> ideation -> outline -> draft -> edit/review -> publish -> post-publish learning. `getuai-email-2.0` provides the concrete path: campaign CRUD, recipient import, SMTP CRUD/test, batch create, AI generate, review, send (`getuai-email-2.0.md:70-73`, `getuai-email-2.0.md:91-118`). Load-bearing choices are prompt/style variables, recipient schema, SMTP test, human review, and shared API artifact/session storage (`getuai-api.md:24-40`). Stylistic choices are table UI, template file format, and frontend stack.

| step | input -> component -> state -> output trace |
|---|---|
| q2.trace1 | campaign fields/style variables -> prompt-template form -> reusable prompt state -> ideation/outline contract (`getuai-email-2.0.md:91-94`) |
| q2.trace2 | CSV recipient fields -> import service -> recipient records -> personalization input (`getuai-email-2.0.md:101-104`) |
| q2.trace3 | batch + prompt + recipient -> LLM generator -> generated email rows -> draft output (`getuai-email-2.0.md:111-114`) |
| q2.trace4 | generated emails -> human review -> approved content state -> sendable batch (`getuai-email-2.0.md:111-118`) |
| q2.trace5 | SMTP account + approved batch -> SMTP test/send -> sent/failed status -> publish outcome (`getuai-email-2.0.md:96-99`) |
| q2.trace6 | image/text/company artifacts -> API store -> session-scoped content -> post-publish input (`getuai-api.md:24-40`) |
| q2.trace7 | factual question -> retrieval-grounded copy -> cited answer -> hallucination guard (`reddit-scount.md:233-239`) |

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

The from-scratch rule is therefore: SDK calls, GAQL resource names, and Google policy errors stay inside the platform adapter; normalized envelopes, conversion events, anomaly detection, budget pacing, and kill-vs-scale decisions sit above the adapter so Meta/TikTok can plug in without rewriting the business loop.

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

## Q5-Q8 Skill Catalog

| domain | skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|---|
| SEO | seo-campaign-console | getuai-seo | `getuai-seo.md:93-106` | web+AI | campaign/account/files/metrics | recs/metrics | sessions/API | duplicate ads console pattern |
| SEO | keyword-research-tracking | getuai-seo | `getuai-seo.md:101-102` | MCP/API | seed/site/locale | keywords/ranks | campaign store | overlaps plugin ideas |
| SEO | content-optimization | getuai-seo | `getuai-seo.md:103` | AI rec | page+keyword | edits/recs | artifacts | prompt drift checks |
| SEO | backlink-analysis | getuai-seo | `getuai-seo.md:104` | MCP/API | domain/url | backlinks | campaign store | unique sample |
| SEO | competitor-analysis | getuai-seo/getuai-competitor-analysis | `getuai-competitor-analysis.md:7-21` | MCP | company/query | competitors/SERP | DB/files | duplicate; plugin canonical |
| SEO | site-structure-analyzer | getuai-plugin | `getuai-plugin.md:11-14` | FastAPI | URL/site | crawl/meta/links | logs | retry external fetches |
| SEO | google-search-analyzer | getuai-plugin | `getuai-plugin.md:16` | FastAPI | query/domain | SERP insights | stateless/logs | Google dependency |
| SEO | keyword-clustering | getuai-plugin | `getuai-plugin.md:20` | FastAPI | keywords | clusters | stateless | retry model/API |
| SEO | sitemap-robots-generator | rankncompare | `rankncompare.md:53-56`, `:134-149` | build/route | category/product data | sitemap/robots | JSON/static | no deprecation marker; rebuild on route/schema change |
| Content | campaign-prompt-template | getuai-email-2.0 | `getuai-email-2.0.md:91-94` | UI | placeholders | prompt | campaign DB | controls register drift |
| Content | personalized-email-draft | getuai-email-2.0 | `getuai-email-2.0.md:111-114` | batch | recipient+prompt | draft | batch DB | recipient grounding |
| Content | recipient-import | getuai-email-2.0 | `getuai-email-2.0.md:101-104` | API/CSV | CSV fields | recipients | MySQL | validate schema |
| Content | smtp-test-and-send | getuai-email-2.0 | `getuai-email-2.0.md:96-99`, `:116-118` | UI/API | SMTP+batch | send status | SMTP DB | review before send |
| Content | cited-websearch-copy | reddit-scount | `reddit-scount.md:233-239` | service | query/context | cited answer | logs | hallucination guard |
| Content | multi-model-rank-summary | LLMRush | `LLMRush.md:7-14` | web/API | term/URL | rank/sentiment | history | GEO drift |
| Content | image-text-composer | openclaw-marketing | `openclaw-marketing.md:5104-5152` | CLI | prompt+images | asset/meta | files | path mapping |
| Content | summarizer-transcriber | openclaw-marketing | `openclaw-marketing.md:6656-6716` | CLI | URL/file | summary/transcript | files/logs | no deprecation marker; provider fallback |
| Ads | google-ads-cli | getu_ads_v2 | `getu_ads_v2.md:9-67` | CLI stdin/file | op+JSON+config | envelope | API effects | Google-bound shell |
| Ads | campaign-management | getu_ads_v2 | `getu_ads_v2.md:1010` | CLI | campaign | create/list/update | Google Ads | kill on envelope/policy error |
| Ads | keyword-management | getu_ads_v2 | `getu_ads_v2.md:1012`, `:923-950` | CLI | ad_group+keywords | criteria result | Google Ads | validate match types |
| Ads | rsa-creative-management | getu_ads_v2 | `getu_ads_v2.md:1013`, `:630-704` | CLI | headlines/descriptions/url | RSA result | Google Ads | fatigue via ad reports |
| Ads | budget-targeting | getu_ads_v2 | `getu_ads_v2.md:1014`, `:1131-1149` | CLI | campaign/amount/geo/lang | budget/criteria | Google Ads | pacing guardrail |
| Ads | composite-campaign-build | getu_ads_v2 | `getu_ads_v2.md:630-704` | CLI | campaign+groups+ads | campaign tree | Google Ads | no deprecation marker; retry from envelope/ledger, not blind replay |
| Ads | reporting-gaql | getu_ads_v2 | `getu_ads_v2.md:1048-1123` | CLI | date/query | metrics/GAQL | report | agnostic envelope |
| Ads | attribution-ingest | attribution_v2 | `attribution_v2.md:13-16` | SDK+API | UTM/events/user | events/leads/scores | tables/PubSub | conversion backbone |
| Ads | platform-credential-sdk | getuai-ads-sdk | `getuai-ads-sdk.md:7-12`, `:146-161` | SDK | user/token/platform | credentials | Redis/API | kill if unavailable |
| Social | reddit-opportunity-analysis | reddit-scount | `reddit-scount.md:108-139` | API | URL | keywords/pain/competitors | MySQL | Reddit-bound |
| Social | reddit-discovery | reddit-scount | `reddit-scount.md:141-181` | API | analysis+index | posts/comments | MySQL/cache | topic selection |
| Social | youtube-search | youtube-api-demo | `youtube-api-demo.md:48-54` | HTTP | query/maxResults | videos | stateless | quota/API risk |
| Social | x-credit-monitor | x-api-credit-monitor | `x-api-credit-monitor.md:7-17`, `:72-104` | launchd | session/threshold | Lark alert | logs/env | re-login monitor |
| Social | x-post-reply-search | openclaw-marketing | `openclaw-marketing.md:7392-7422` | CLI | text/id/query/media | post/reply/search | X side effects | API break risk |
| Social | multi-channel-inbox | openclaw-marketing | `openclaw-marketing.md:132-158` | Gateway | channel/session | routed message | gateway store | adapter abstraction |
| Social | slack-actions | openclaw-marketing | `openclaw-marketing.md:6314-6339` | tool | channel/message/content | reaction/send/edit | Slack effects | per-platform semantics |
| Social | channel-gating | openclaw-marketing | `openclaw-marketing.md:122-126` | config | dmPolicy/allowFrom | allow/deny | config | no deprecation marker; moderation guard |

Margin audit: Q5 has 9 rows, Q6 has 8, Q7 has 9, Q8 has 8. Protected rows: sitemap-robots-generator, summarizer-transcriber, composite-campaign-build, channel-gating.

## Q9-Q12 Cognition

SEO/GEO models: topical authority worked in `rankncompare.md:128-187` and failed in `getuai-2.0.md:19-42`; intent mapping worked in `getuai-plugin.md:11-20` and fails when `rankncompare.md:53-56` is used as discovery; E-E-A-T worked in `lawyer_marketing.md:291-317` and fails without industry packs (`growth-engine.md:8`, `:27`); GEO-vs-SEO worked in `LLMRush.md:7-14` and fails if sitemap is treated as GEO (`rankncompare.md:134-149`); velocity-vs-depth worked in `getuai-seo.md:101-106` and failed in docs-without-runtime (`growth-engine-legacy.md:16-22`).

Content frames: user journey worked in `getuai-email-2.0.md:70-118` and failed in local-only `gmi-prototype.md:7-54`; portfolio theory worked in OpenClaw media/summarizer skills (`openclaw-marketing.md:5104-5152`, `:6656-6716`) and fails if email is the whole system; distribution-over-production worked in reviewed SMTP send and failed in local `generated_videos/`; ROI windows worked in `LLMRush.md:7-23` and failed in `getuai-2.0.md:19-42`; brand voice worked with placeholders/review and failed with free-form prototype prompts. Hooks: Q2 pipeline and Q6 skills.

Ads models: LTV/CAC worked in `lawyer_marketing.md:291-304` + `getu_ads_v2.md:1048-1064` and fails on missing identity (`attribution_v2.md:117-119`); pacing worked in `getu_ads_v2.md:1131-1149` and breaks on credentials (`getuai-ads.md:24-28`); creative fatigue worked with RSA/ad reports (`getu_ads_v2.md:630-704`, `:1066-1086`) and fails in aggregate-only data; attribution paradox worked in `attribution_v2.md:13-23` and breaks on cookies/session rotation (`attribution_v2.md:151-186`); kill-vs-scale worked in read/write gates (`lawyer_marketing.md:248-269`) and fails when engines own writes (`growth-engine-legacy.md:83-88`).

Social models: platform game theory worked in Reddit-specific discovery (`reddit-scount.md:108-181`) and is contested by generic Gateway need for policy (`openclaw-marketing.md:122-158`); algorithm preference worked in YouTube/X primitives (`youtube-api-demo.md:48-54`, `openclaw-marketing.md:7392-7422`) and fails if search-only is treated as engagement; community fit worked in subreddit-first discovery and fails with raw xurl posting; viral mechanics require post/reply/media but fail without monitoring; automation visibility cost is controlled by allowlists and credit monitor (`openclaw-marketing.md:122-126`, `x-api-credit-monitor.md:7-17`).

## Q13 - Shared Foundations

Shared foundations: identity/session (`growth-engine-legacy.md:43-50`, `getuai-api.md:23-37`), credentials/secrets (`growth-engine-legacy.md:64-88`, `getuai-ads.md:21-28`, `x-api-credit-monitor.md:12-18`), data/artifacts (`getuai-api.md:24-42`, `rankncompare.md:49-56`, `attribution_v2.md:13-16`), schedules/queues (`growth-engine-legacy.md:64-88`, `x-api-credit-monitor.md:82-93`), observability (`growth-engine-legacy.md:64-70`, `LLMRush.md:19-23`), LLM gateway (`getuai-seo.md:78-91`, `getuai-email-2.0.md:111-114`), human-in-loop console (`growth-engine-legacy.md:83-88`, `lawyer_marketing.md:248-269`), repo-template governance (`optiminds-repo-template.md:9-63`). Decision rule: share tenant trust, credentials, schedules, ledgers, observability, LLM routing, and approval; isolate schemas, external APIs, ranking logic, tone, and domain kill criteria.

## Q14 - Build Sequence

| milestone | scope | dependencies | done_criteria | next_trigger | deferrals |
|---|---|---|---|---|---|
| Day-1 | Core tenant/session/artifact/source/approval skeleton | none | target/session/artifact/action records persist; no run leakage | first durable tool | ads/social writes |
| Week-1 | SEO/GEO read lane: crawl/search/keyword/sitemap | Core credentials/artifacts | outputs stored, rank source declared, sitemap exists | recurring/publish request | autopublish |
| Week-2 | Content lane: templates/import/draft/SMTP/retrieval | Core + SEO store + LLM gateway | variables validate; drafts generated; review before send | outbound metric need | rich media |
| Week-4 | Ads read + attribution | credentials + campaign IDs | reports + conversion events visible; read-only analyst | repeated budget recs | budget mutation/A-B |
| Week-8 | Controlled writes across domains | read evidence + approvals | every write has ledger, envelope, monitor | stable weekly outcomes | full optimizer |
| Month-3 | OODA orchestration + industry packs | all lanes + observability/schedules | weekly observe-plan-approve-execute-review works | tenant/industry scale | Temporal/marketplace/autonomous spend |

Evidence shape: thin prototype `getuai-2.0.md:19-42`, MVP route hardening `getuai-mvp.md:9-76`, production refactor `attribution_v2.md:16-23`, vertical cases `lawyer_finder.md:11-16`, `cuilawgroup.md:10-27`, backend-skeleton-first `growth-engine.md:8-12`.

## Q15 - Failure Modes

| failure_mode | domains | count | cause | early symptom | prophylactic | evidence_pair |
|---|---|---:|---|---|---|---|
| engines own platform facts | SEO/Ads/Social | 3 | scattered identity/creds/schedules | raw tokens/own cron | Core facts/context leases | `growth-engine-legacy.md:43-50`, `:83-88` |
| legacy scaffolding import | all | 4 | copying attempts | stale paths | greenfield contracts | `growth-engine.md:69-152` |
| docs without runtime | all | 4 | design outruns core | no `core/` tree | Day-1 skeleton | `growth-engine-legacy.md:16-22` |
| credential drift | SEO/Ads/Social | 3 | auth outside action layer | API/re-login errors | leases + monitors | `getuai-ads.md:24-28`, `x-api-credit-monitor.md:13-17` |
| attribution/session breakage | Ads/Content | 2 | cookie/user rotation | missing lead rows | SDK domain/session tests | `attribution_v2.md:117-186` |
| writes without approval | SEO/Ads/Social | 3 | mixed read/write skills | agents mutate while analyzing | read-only diagnosis + ledger | `lawyer_marketing.md:248-269`, `growth-engine-legacy.md:84` |
| static publisher as GEO evaluator | SEO/GEO | 1 | indexing confused with LLM visibility | sitemap but no LLM rank | LLMRush sensor | `rankncompare.md:134-149`, `LLMRush.md:7-14` |
| prototype-local artifact store | Content/Social | 2 | local media only | no campaign/outcome link | Core artifact store | `gmi-prototype.md:14`, `:50`, `getuai-api.md:24-40` |
| API prefix mismatch | shared | 2 | local/prod route drift | wrong backend path | API_PREFIX/proxy contract | `getuai-mvp.md:9-76` |

## Benchmark Answers

Machine-readable benchmark answers are emitted in the top-level `benchmark_answers` JSON array. In-KB summary: Q1 and Q3 now carry explicit component-by-component trace locks; Q2 and Q4 retain trace tables; Q5-Q8 retain 34 skill rows with the Skill-Catalog Margin Audit; Q9-Q12 retain worked/failed cognition pairs; Q13-Q15 retain shared-foundation, build-sequence, and failure-mode artifacts.
