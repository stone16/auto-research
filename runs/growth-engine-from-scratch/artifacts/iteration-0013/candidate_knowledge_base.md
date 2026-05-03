# Knowledge Base

Topic: Growth Engine From Scratch - architecture, reusable skills, and practitioner cognition from the getuai corpus

Iteration: 15 compact architecture-grounding patch

## Evidence Policy

Direct citations use `repo.md:line-line` from `runs/growth-engine-from-scratch/sources/_raw/`. Source IDs are mirrored in top-level benchmark citation arrays. Stable IDs are contractual: Q1-Q4 `q*.trace*`; Q5-Q8 `seo.skill*`, `content.skill*`, `ads.skill*`, `social.skill*`; Q9-Q12 `q*.cog*`; Q13 `q13.f1`-`q13.f8`; Q14 `q14.m1`-`q14.m6`; Q15 `q15.fm1`-`q15.fm9`.

## Q1 - SEO/GEO Architecture

Converged pattern: crawler/search adapter -> ranking signal source -> GEO evaluator -> content store -> generator/publisher -> Core approval/ledger/kill-switch. Evidence: `getuai-plugin.md:11-20`, `getuai-seo.md:101-106`, `LLMRush.md:7-14`, `rankncompare.md:53-56`, `rankncompare.md:128-149`, `growth-engine-legacy.md:83-88`. Packaging disagreement is now direct: `getuai-seo` declares UI/MCP/AI layers and three simultaneous runtime components (`getuai-seo.md:7-11`, `getuai-seo.md:52-83`), while `growth-engine-legacy` rejects browser-facing engine ownership by requiring Browser -> Core only and Core ownership of platform facts (`growth-engine-legacy.md:43-50`, `growth-engine-legacy.md:45-49`).

| step | input -> component -> state -> output trace |
|---|---|
| q1.trace1 | URL/site -> site-structure analyzer -> crawl/meta/link state -> discovery artifact (`getuai-plugin.md:11-14`) |
| q1.trace2 | query/domain -> search/competitor/keyword tools -> SERP/competitor/keyword state -> intent map (`getuai-plugin.md:16-20`) |
| q1.trace3 | term/company -> keyword/rank metrics -> campaign-rank state -> ranking signal source (`getuai-seo.md:101-106`) |
| q1.trace4 | term/company/model set -> LLMRush evaluator -> rank/sentiment/history -> GEO signal (`LLMRush.md:7-14`) |
| q1.trace5 | product/category JSON -> content store -> metadata/routes -> publishable corpus (`rankncompare.md:128-149`) |
| q1.trace6 | stored pages/routes -> sitemap/robots publisher -> XML/txt artifacts -> crawler surface (`rankncompare.md:53-56`) |
| q1.trace7 | publish/check request -> Core approval/ledger/kill-switch -> approved/stopped action -> audit trail (`growth-engine-legacy.md:83-88`) |
| q1.trace8 | page+keyword+rank gap -> optimization generator -> recommendation artifact -> human review candidate (`getuai-seo.md:103-106`) |

External dependencies: search APIs, Google Ads/Custom Search credentials, LLM providers, CMS/static publishing, and Core credential leases. Failure handling: adapter retry/logging, artifact replay, and stopped actions at Core. Recommendation: keep crawler/evaluator/publisher domain-specific; share credentials, approvals, schedules, ledgers, and kill-switches.

## Q2 - Content Writing Architecture

Architecture: ideation -> outline -> draft -> edit/review -> publish -> post-publish learning. `getuai-email-2.0` gives the concrete campaign/recipient/SMTP/batch/AI-review-send path (`getuai-email-2.0.md:70-73`, `getuai-email-2.0.md:91-118`). Load-bearing choices: prompt/style variables, recipient schema, SMTP test, human review, and shared artifact/session storage (`getuai-api.md:24-40`). Stylistic choices: table UI, template format, frontend stack.

| step | input -> component -> state -> output trace |
|---|---|
| q2.trace1 | campaign fields/style variables -> prompt-template form -> reusable prompt -> ideation/outline contract (`getuai-email-2.0.md:91-94`) |
| q2.trace2 | CSV fields -> recipient import -> recipient records -> personalization input (`getuai-email-2.0.md:101-104`) |
| q2.trace3 | batch+prompt+recipient -> LLM generator -> generated rows -> draft (`getuai-email-2.0.md:111-114`) |
| q2.trace4 | generated emails -> human review -> approved state -> sendable batch (`getuai-email-2.0.md:111-118`) |
| q2.trace5 | SMTP account+batch -> SMTP test/send -> sent/failed status -> publish outcome (`getuai-email-2.0.md:96-99`) |
| q2.trace6 | image/text/company artifacts -> API store -> session content -> learning input (`getuai-api.md:24-40`) |
| q2.trace7 | factual question -> retrieval-grounded copy -> cited answer -> hallucination guard (`reddit-scount.md:233-239`) |

## Q3 - Ads Architecture

Architecture: campaign feed -> bidding/budget/targeting -> reporting -> attribution -> optimization. Platform-bound code lives in Google Ads CLI/SDK operations; platform-agnostic logic is ResultEnvelope, reporting lake, attribution event model, anomaly detection, pacing analysis, approval ledger, and kill criteria (`getu_ads_v2.md:9-67`, `getu_ads_v2.md:1010-1149`, `attribution_v2.md:13-16`, `getuai-ads-data.md:216-250`).

| step | input -> component -> state -> output trace |
|---|---|
| q3.trace1 | credentials+brief -> Ads UI/MCP/AI -> campaign feed/recs -> operator workbench (`getuai-ads.md:7-11`) |
| q3.trace2 | operation JSON -> google-ads-cli exec -> ResultEnvelope -> agent-readable output (`getu_ads_v2.md:9-67`) |
| q3.trace3 | campaign/adgroup/keyword/RSA/budget payload -> 38 ops -> platform tree -> mutation/list result (`getu_ads_v2.md:1010-1017`) |
| q3.trace4 | date range/GAQL -> reports -> metrics -> optimization input (`getu_ads_v2.md:1048-1123`) |
| q3.trace5 | SDK event+UTM+session -> attribution ingress/consumer -> events/leads/scores -> conversion event (`attribution_v2.md:13-16`) |
| q3.trace6 | Google/Meta/TikTok rows -> ads data platform -> campaign/conversion tables -> anomaly/pacing candidate (`getuai-ads-data.md:216-250`) |
| q3.trace7 | budget/targeting rec -> approval boundary -> blocked/approved action -> action log (`lawyer_marketing.md:248-269`) |
| q3.trace8 | unsafe write/lost attribution/envelope error -> Core kill-switch -> freeze/pause/reduce -> audited stop (`growth-engine-legacy.md:83-88`) |

## Q4 - Social Architecture

Architecture: listen, post, schedule, engage, monitor as platform adapters behind Gateway routing, not a fake universal adapter. Reddit listens/discovers (`reddit-scount.md:108-181`), YouTube monitors (`youtube-api-demo.md:48-54`), X posts/replies/searches (`openclaw-marketing.md:7392-7422`), OpenClaw attempts a universal Gateway/control plane (`openclaw-marketing.md:132-158`), but the flat API breaks on per-channel policy: `dmPolicy="pairing"`, explicit `allowFrom`, mention gating, reply tags, per-channel chunking (`openclaw-marketing.md:124-126`, `openclaw-marketing.md:158`) and X-specific credit accounting (`x-api-credit-monitor.md:7-17`, `x-api-credit-monitor.md:72-104`). Moderation inserts at the DM allowlist/pairing gate.

| step | input -> component -> state -> output trace |
|---|---|
| q4.trace1 | company URL -> Reddit analysis -> keywords/pain/competitors/subreddits -> listen state (`reddit-scount.md:108-139`) |
| q4.trace2 | analysis+keyword index -> Reddit discovery -> posts/comments -> engagement cache (`reddit-scount.md:141-181`) |
| q4.trace3 | query+maxResults -> YouTube adapter -> video list -> monitor candidates (`youtube-api-demo.md:48-54`) |
| q4.trace4 | text/post_id/query/media -> X skill -> side effect/platform JSON -> post/reply/search output (`openclaw-marketing.md:7392-7422`) |
| q4.trace5 | channel message -> Gateway -> routed session/inbox -> engage surface constrained by policies (`openclaw-marketing.md:124-158`) |
| q4.trace6 | schedule+Chrome session+threshold -> launchd credit monitor -> heartbeat/alert -> quota output (`x-api-credit-monitor.md:72-104`) |
| q4.trace7 | generated reply -> dmPolicy/allowFrom -> allow/deny -> moderated automation (`openclaw-marketing.md:122-126`) |

## Q5-Q8 Skill Catalog

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
| content.skill1 | Content | campaign-prompt-template | getuai-email-2.0 | `getuai-email-2.0.md:91-94` | UI | placeholders | prompt | campaign DB | controls register drift |
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
| ads.skill6 | Ads | composite-campaign-build | getu_ads_v2 | `getu_ads_v2.md:630-704` | CLI | campaign+groups+ads | campaign tree | Google Ads | retry from envelope/ledger |
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
| social.skill8 | Social | channel-gating | openclaw-marketing | `openclaw-marketing.md:122-126` | config | dmPolicy/allowFrom | allow/deny | config | moderation guard |

## Q9-Q12 Cognition Evidence Table

| row_id | domain | model_name | trigger | worked_here | failed_here | anti_pattern | hook |
|---|---|---|---|---|---|---|---|
| q9.cog1 | SEO/GEO | topical authority | durable corpus needed | `rankncompare.md:128-187` | `getuai-2.0.md:19-42` | thin AI-Studio as corpus | `seo.skill9`, `q15.fm8` |
| q9.cog2 | SEO/GEO | intent mapping | term/site -> target map | `getuai-plugin.md:11-20` | `rankncompare.md:53-56` | sitemap as discovery | `seo.skill7`, `seo.skill8` |
| q9.cog3 | SEO/GEO | E-E-A-T / vertical expertise | YMYL/legal claims | `lawyer_marketing.md:291-317` | `growth-engine.md:7-30` | generic industry labels | `q13.f8`, `q14.m6` |
| q9.cog4 | SEO/GEO | GEO vs SEO pivot | LLM visibility question | `LLMRush.md:7-14` | `rankncompare.md:134-149` | sitemap as GEO evaluator | `content.skill6`, `q15.fm7` |
| q9.cog5 | SEO/GEO | content velocity vs depth | rec frequency vs durable assets | `getuai-seo.md:101-106` | `growth-engine-legacy.md:16-22` | docs without runtime | `q14.m2`, `q15.fm3` |
| q10.cog1 | Content | user journey mapping | audience state drives stages | `getuai-email-2.0.md:70-118` | `gmi-prototype.md:7-54` | local artifact detached | Q2, `content.skill1` |
| q10.cog2 | Content | content portfolio theory | multiple media types | `openclaw-marketing.md:5104-5152` | `getuai-email-2.0.md:70-73` | email-only system | `content.skill7` |
| q10.cog3 | Content | distribution over production | draft needs send/publish | `getuai-email-2.0.md:111-118` | `gmi-prototype.md:50` | folder output no ledger | `content.skill4` |
| q10.cog4 | Content | ROI time window | measurable outcome needed | `LLMRush.md:7-23` | `getuai-2.0.md:19-42` | no metric loop | `content.skill6` |
| q10.cog5 | Content | brand voice as forcing function | tone before send | `getuai-email-2.0.md:91-118` | `gmi-prototype.md:37-54` | free prompt as brand | `content.skill1` |
| q11.cog1 | Ads | LTV/CAC discipline | spend needs business value | `lawyer_marketing.md:291-304`, `getu_ads_v2.md:1048-1064` | `attribution_v2.md:117-119` | spend with missing session | `ads.skill7`, `ads.skill8` |
| q11.cog2 | Ads | pacing logic | budget/geo changes | `getu_ads_v2.md:1131-1149` | `getuai-ads.md:24-28` | credentials assumed | `ads.skill5` |
| q11.cog3 | Ads | creative fatigue curves | ad-level performance | `getu_ads_v2.md:630-704` | `getuai-ads-data.md:216-250` | aggregate hides creative | `ads.skill4` |
| q11.cog4 | Ads | attribution paradox | better measurement fragility | `attribution_v2.md:13-23` | `attribution_v2.md:151-186` | SDK once solves all | `q15.fm5` |
| q11.cog5 | Ads | kill-vs-scale criteria | write recommendation | `lawyer_marketing.md:248-269` | `growth-engine-legacy.md:83-88` | engines own writes | `q15.fm6` |
| q12.cog1 | Social | platform-as-game-theory | community-native rules | `reddit-scount.md:108-181` | `openclaw-marketing.md:122-158` | universal adapter | `social.skill8` |
| q12.cog2 | Social | algorithm preference modeling | search/feed/reply/video | `youtube-api-demo.md:48-54`, `openclaw-marketing.md:7392-7422` | `reddit-scount.md:141-181` | search-only engagement | `social.skill3` |
| q12.cog3 | Social | community fit before brand voice | context before reply | `reddit-scount.md:108-139` | `openclaw-marketing.md:7392-7422` | raw posting | `social.skill2` |
| q12.cog4 | Social | viral mechanics | post/reply/media loop | `openclaw-marketing.md:7392-7422` | `youtube-api-demo.md:48-54` | video search as viral loop | `q14.m5` |
| q12.cog5 | Social | automation visibility cost | public/private automation | `openclaw-marketing.md:122-126`, `x-api-credit-monitor.md:7-17` | `openclaw-marketing.md:132-158` | no moderation/quota visibility | `q15.fm4`, `q15.fm6` |

## Q13 - Shared Foundations

Decision rule: share tenant, money, secret, queue, audit, and operator-control boundaries; keep ranking logic, creative/tone judgment, platform semantics, industry facts, content schema, and channel-specific kill criteria domain-isolated.

| row_id | foundation | shared_contract | corpus_evidence | domain_isolated_boundary | hooks_to_q14_q15 |
|---|---|---|---|---|---|
| q13.f1 | identity/session | Core validates tenant/user/session; token/context schema migrates in Core | `growth-engine-legacy.md:43-50`; `getuai-api.md:23-37`; `getuai-ui.md:18-32` | audience/campaign/channel state only | `q14.m1`, `q14.m3`, `q14.m4`; prevents `q15.fm1`, `q15.fm5` |
| q13.f2 | credentials/secrets | central credential records and scoped leases; additive provider schema | `growth-engine-legacy.md:64-88`; `getuai-ads.md:21-28`; `getuai-ads-sdk.md:7-12`; `x-api-credit-monitor.md:12-18` | platform OAuth/API SDKs | `q14.m1`, `q14.m2`, `q14.m4`, `q14.m5`; prevents `q15.fm1`, `q15.fm4`, `q15.fm6` |
| q13.f3 | data/artifacts | artifact ledger for inputs/assets/reports/citations/replay; append-only metadata | `getuai-api.md:24-42`; `rankncompare.md:49-56`; `attribution_v2.md:13-16`; `gmi-prototype.md:14-50` | rank/draft/ad/social schemas | `q14.m1`-`q14.m4`; prevents `q15.fm3`, `q15.fm8`, `q15.fm9` |
| q13.f4 | schedules/queues | Core schedules/queues/retries/terminal stops; stable op names/envelopes | `growth-engine-legacy.md:64-88`; `x-api-credit-monitor.md:72-104`; `openfang.md:42-52` | cadence interpretation | `q14.m1`, `q14.m5`, `q14.m6`; prevents `q15.fm1`, `q15.fm3`, `q15.fm4` |
| q13.f5 | observability | shared run events/request IDs/cost/trace/redaction; additive fields | `growth-engine-legacy.md:64-70`; `LLMRush.md:19-23`; `x-api-credit-monitor.md:7-17`; `attribution_v2.md:13-23` | domain dashboards/metrics | `q14.m1`, `q14.m4`, `q14.m6`; prevents `q15.fm3`, `q15.fm4`, `q15.fm5` |
| q13.f6 | LLM gateway | model routing, prompt/cost guardrails, fallback, response envelopes | `getuai-seo.md:78-91`; `getuai-email-2.0.md:111-114`; `LLMRush.md:7-14`; `reddit-scount.md:233-239` | prompts/tone/ranking/retrieval corpus | `q14.m2`, `q14.m3`, `q14.m6`; prevents `q15.fm7`, `q15.fm8` |
| q13.f7 | human-in-loop console | review/approval/override/kill-switch/action ledger; explicit stop reasons | `growth-engine-legacy.md:83-88`; `lawyer_marketing.md:248-269`; `openclaw-marketing.md:122-126` | domain proposals only | `q14.m1`, `q14.m5`, `q14.m6`; prevents `q15.fm1`, `q15.fm3`, `q15.fm6` |
| q13.f8 | repo-template governance | AGENTS/CLAUDE, skills, CI gates, version drift; idempotent re-apply | `optiminds-repo-template.md:9-63`; `optiminds-org-config.md:7-47`; `lawyer_finder.md:69-72` | business logic and vertical facts | `q14.m1`, `q14.m6`; prevents `q15.fm2`, `q15.fm3`, `q15.fm9` |

## Q14 - Build Sequence

| row_id | milestone | scope | dependencies | done_criteria | next_trigger | deferrals |
|---|---|---|---|---|---|---|
| q14.m1 | Day-1 | Core tenant/session/artifact/source/approval skeleton | `q13.f1`, `q13.f2`, `q13.f3`, `q13.f4`, `q13.f5`, `q13.f7`, `q13.f8` | records persist; no run leakage; terminal stop explicit | first durable tool | ads/social writes; rich media; autonomous schedules beyond smoke |
| q14.m2 | Week-1 | SEO/GEO read lane via `seo.skill6`-`seo.skill9` | `q13.f2`, `q13.f3`, `q13.f5`, `q13.f6`, `q13.f7` | outputs stored; rank source declared; sitemap exists; evaluator boundary named | recurring/publish request | autopublish; GEO-as-sitemap |
| q14.m3 | Week-2 | Content templates/import/draft/SMTP/retrieval | `q13.f1`, `q13.f2`, `q13.f3`, `q13.f6`, `q13.f7` plus SEO store | variables validate; drafts; citations/recipient grounding; review before send | outbound metric need | rich media; multilingual; auto-send |
| q14.m4 | Week-4 | Ads read + attribution; no spend mutation | `q13.f1`, `q13.f2`, `q13.f3`, `q13.f5` plus campaign IDs | reports and conversion events visible; read-only kill-vs-scale recs | repeated budget recs | budget mutation; A/B; autonomous bidding |
| q14.m5 | Week-8 | Controlled writes across domains | `q13.f2`, `q13.f3`, `q13.f4`, `q13.f5`, `q13.f7`; evidence from `q14.m2`-`q14.m4` | every write has ledger, envelope, quota/credit monitor, rollback/pause | stable weekly outcomes | full optimizer; cross-platform rewrite marketplace |
| q14.m6 | Month-3 | OODA orchestration + industry packs | `q13.f1`, `q13.f3`, `q13.f4`, `q13.f5`, `q13.f6`, `q13.f7`, `q13.f8`; all lanes | weekly observe-plan-approve-execute-review; vertical pack has evidence and kill criteria | tenant/industry scale | Temporal marketplace; autonomous spend; generic industry labels |

Evidence from corpus evolution: thin prototype `getuai-2.0.md:19-42`, MVP API-prefix hardening `getuai-mvp.md:9-76`, production attribution refactor `attribution_v2.md:16-23`, vertical cases `lawyer_finder.md:11-16`, `cuilawgroup.md:10-27`, backend skeleton `growth-engine.md:8-12`.

## Q15 - Failure Modes

| row_id | failure_mode | domains | count | cause | early symptom | prophylactic | evidence_pair |
|---|---|---|---:|---|---|---|---|
| q15.fm1 | engines own platform facts | SEO/Ads/Social | 3 | scattered identity/creds/schedules | raw tokens/own cron | `q13.f1`, `q13.f2`, `q13.f4`, `q13.f7` | `growth-engine-legacy.md:43-50`, `growth-engine-legacy.md:83-88` |
| q15.fm2 | legacy scaffolding import | all | 4 | copying attempts | stale paths | `q13.f8` + `q9.cog3` | `growth-engine.md:69-152` |
| q15.fm3 | docs without runtime | all | 4 | design outruns core | no `core/` tree | `q13.f3`, `q13.f4`, `q13.f5`, `q13.f7`, `q13.f8`, `q14.m1` | `growth-engine-legacy.md:16-22` |
| q15.fm4 | credential drift | SEO/Ads/Social | 3 | auth outside action layer | API/re-login errors | `q13.f2`, `q13.f4`, `q13.f5`, `social.skill4` | `getuai-ads.md:24-28`, `x-api-credit-monitor.md:13-17` |
| q15.fm5 | attribution/session breakage | Ads/Content | 2 | cookie/user rotation | missing lead rows | `q13.f1`, `q13.f3`, `q13.f5`, `ads.skill8` | `attribution_v2.md:117-186` |
| q15.fm6 | writes without approval | SEO/Ads/Social | 3 | mixed read/write skills | agents mutate while analyzing | `q13.f2`, `q13.f3`, `q13.f7`, `q11.cog5`, `q12.cog1`, `q12.cog5` | `lawyer_marketing.md:248-269`, `growth-engine-legacy.md:84` |
| q15.fm7 | static publisher as GEO evaluator | SEO/GEO | 1 | indexing confused with LLM visibility | sitemap but no LLM rank | `q13.f3`, `q13.f5`, `q13.f6`, `content.skill6` | `rankncompare.md:134-149`, `LLMRush.md:7-14` |
| q15.fm8 | prototype-local artifact store | Content/Social | 2 | local media only | no campaign/outcome link | `q13.f3`, `q13.f6`, `q13.f7` | `gmi-prototype.md:14`, `gmi-prototype.md:50`, `getuai-api.md:24-40` |
| q15.fm9 | API prefix mismatch | shared | 2 | local/prod route drift | wrong backend path | `q13.f3`, `q13.f5`, `q13.f8` | `getuai-mvp.md:9-76` |
