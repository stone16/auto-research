# Knowledge Base

Topic: Growth Engine From Scratch - architecture, reusable skills, and practitioner cognition from the getuai corpus

Iteration: 9 citation-restored Q13 dependency audit

## Evidence Policy

Direct citations use `repo.md:line-line` from `runs/growth-engine-from-scratch/sources/_raw/`. Source IDs and the load-bearing file:line anchors are mirrored in top-level benchmark citation arrays. This pass preserves the retained iter-5 stable IDs, absorbs the discarded Q2/Q4 component-order tables, keeps `q13.f1`-`q13.f8`, and restores answer-level file:line citation discipline.

## Stable Artifact ID Contract

Stable IDs are part of the evaluation contract: Q1-Q4 architecture rows use `q1.trace*`-`q4.trace*`; Q5-Q8 skill rows use `seo.skill*`, `content.skill*`, `ads.skill*`, `social.skill*`; Q9-Q12 cognition rows use `q9.cog*`-`q12.cog*`; Q13 foundations use `q13.f1`-`q13.f8`; Q14 milestones use `q14.m1`-`q14.m6`; Q15 failure modes use `q15.fm1`-`q15.fm9`.

## Q1-Q4 Architecture Trace

| row_id | domain | component order and data flow | shared boundary | file:line anchors |
|---|---|---|---|---|
| q1.trace1 | SEO/GEO | crawler/search adapter -> ranking signal source -> GEO evaluator -> content store -> publisher -> generator/recommendation -> human review | Core owns identity, credential leases, artifact ledger, approval, schedule, and kill-switch | `getuai-plugin.md:11-20`, `getuai-seo.md:7-11`, `getuai-seo.md:93-106`, `LLMRush.md:7-14`, `rankncompare.md:53-56`, `rankncompare.md:128-149`, `growth-engine-legacy.md:43-50`, `growth-engine-legacy.md:83-88` |
| q2.trace1 | Content | campaign/style facts -> ideation/outline prompt -> recipient import -> draft generation -> edit/review -> SMTP publish -> artifact/post-publish learning -> retrieval-grounded factual copy | Core owns sessions/artifacts, LLM gateway, SMTP credential lease, review ledger | `getuai-email-2.0.md:70-73`, `getuai-email-2.0.md:91-118`, `getuai-email-2.0.md:101-104`, `getuai-api.md:24-40`, `reddit-scount.md:233-239` |
| q3.trace1 | Ads | campaign feed -> platform adapter -> campaign/adgroup/keyword/RSA/budget data model -> reporting/GAQL -> attribution event/lead score -> anomaly/pacing recommendation -> approval/kill | Platform-bound mutations stay in Google Ads adapter; platform-agnostic layer is ResultEnvelope, report lake, attribution model, anomaly/pacing, action ledger | `getuai-ads.md:7-11`, `getu_ads_v2.md:9-67`, `getu_ads_v2.md:1010-1017`, `getu_ads_v2.md:1048-1123`, `getu_ads_v2.md:1131-1149`, `attribution_v2.md:13-16`, `getuai-ads-data.md:216-250`, `lawyer_marketing.md:248-269`, `growth-engine-legacy.md:83-88` |
| q4.trace1 | Social | listen -> topic selection -> monitor -> post/reply/search -> engage -> schedule/credit accounting -> content moderation | Gateway routes sessions/channels; platform payload semantics, quotas, tone, and moderation stay adapter-specific | `reddit-scount.md:108-181`, `youtube-api-demo.md:48-54`, `openclaw-marketing.md:122-158`, `openclaw-marketing.md:7392-7422`, `x-api-credit-monitor.md:7-17`, `x-api-credit-monitor.md:72-104` |

Convergence rule: shared Core handles tenant trust, credentials, schedules, observability, ledgers, approvals, and kill-switches; domain systems own ranking, tone, platform API shape, campaign mutations, and community semantics. Disagreement is real: `getuai-seo` favors UI/MCP/AI services, `rankncompare` favors static publishing, and `growth-engine-legacy` rejects engines owning platform facts.

## Q5-Q8 Skill Catalog

| row_id | domain | skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|---|---|
| seo.skill1 | SEO | seo-campaign-console | getuai-seo | `getuai-seo.md:93-106` | web+AI | campaign/account/files/metrics | recs/metrics | sessions/API | duplicate ads console pattern |
| seo.skill2 | SEO | keyword-research-tracking | getuai-seo | `getuai-seo.md:101-102` | MCP/API | seed/site/locale | keywords/ranks | campaign store | overlaps plugin ideas |
| seo.skill3 | SEO | content-optimization | getuai-seo | `getuai-seo.md:103` | AI rec | page+keyword | edits/recs | artifacts | prompt drift checks |
| seo.skill4 | SEO | backlink-analysis | getuai-seo | `getuai-seo.md:104` | MCP/API | domain/url | backlinks | campaign store | unique sample |
| seo.skill5 | SEO | competitor-analysis | getuai-seo/plugin | `getuai-competitor-analysis.md:7-21` | MCP | company/query | competitors/SERP | DB/files | duplicate; plugin canonical |
| seo.skill6 | SEO | site-structure-analyzer | getuai-plugin | `getuai-plugin.md:11-14` | FastAPI | URL/site | crawl/meta/links | logs | retry fetches |
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
| ads.skill3 | Ads | keyword-management | getu_ads_v2 | `getu_ads_v2.md:923-950` | CLI | ad_group+keywords | criteria result | Google Ads | validate match types |
| ads.skill4 | Ads | rsa-creative-management | getu_ads_v2 | `getu_ads_v2.md:630-704` | CLI | headlines/descriptions/url | RSA result | Google Ads | fatigue via reports |
| ads.skill5 | Ads | budget-targeting | getu_ads_v2 | `getu_ads_v2.md:1131-1149` | CLI | campaign/amount/geo/lang | budget/criteria | Google Ads | pacing guardrail |
| ads.skill6 | Ads | composite-campaign-build | getu_ads_v2 | `getu_ads_v2.md:630-704` | CLI | campaign+groups+ads | campaign tree | Google Ads | no deprecation marker; retry from envelope/ledger |
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

Margin audit: Q5 has 9 rows, Q6 has 8, Q7 has 9, Q8 has 8. Protected rows: `seo.skill9`, `content.skill8`, `ads.skill6`, `social.skill8`.

## Q9-Q12 Cognition Evidence Table

| row_id | domain | model_name | trigger | worked_here | failed_here | anti_pattern | hook |
|---|---|---|---|---|---|---|---|
| q9.cog1 | SEO/GEO | topical authority | corpus depth needed | `rankncompare.md:128-187` | `getuai-2.0.md:19-42` | thin prototype as corpus | Q1 + `seo.skill9`; `q15.fm8` |
| q9.cog2 | SEO/GEO | intent mapping | search term/site needs target map | `getuai-plugin.md:11-20` | `rankncompare.md:53-56` | sitemap as intent research | `seo.skill7`/`seo.skill8` |
| q9.cog3 | SEO/GEO | E-E-A-T / vertical expertise | legal/YMYL claims | `lawyer_marketing.md:291-317` | `growth-engine.md:7-13`, `growth-engine.md:23-30` | generic industry labels | `q13.f8`; `q14.m6`; `q15.fm2` |
| q9.cog4 | SEO/GEO | GEO vs SEO pivot | LLM answer visibility needed | `LLMRush.md:7-14` | `rankncompare.md:134-149` | sitemap as GEO evaluator | `content.skill6`; `q15.fm7` |
| q9.cog5 | SEO/GEO | content velocity vs depth | rec frequency vs durable assets | `getuai-seo.md:101-106` | `growth-engine-legacy.md:16-22` | docs without runtime | `q14.m2`; `q15.fm3` |
| q10.cog1 | Content | user journey mapping | recipient state drives draft | `getuai-email-2.0.md:70-118` | `gmi-prototype.md:7-54` | local artifact detached | Q2; `content.skill1`; `q15.fm8` |
| q10.cog2 | Content | content portfolio | multiple media needed | `openclaw-marketing.md:5104-5152`, `openclaw-marketing.md:6656-6716` | `getuai-email-2.0.md:70-73` | email as whole system | `content.skill7`/`content.skill8` |
| q10.cog3 | Content | distribution over production | draft needs send/publish | `getuai-email-2.0.md:111-118` | `gmi-prototype.md:50` | generation without ledger | `content.skill4`; `q15.fm6` |
| q10.cog4 | Content | ROI time window | outcome loop needed | `LLMRush.md:7-23` | `getuai-2.0.md:19-42` | prototype with no metric loop | `content.skill6`; `q14.m4` |
| q10.cog5 | Content | brand voice as forcing function | tone/register before send | `getuai-email-2.0.md:91-118` | `gmi-prototype.md:37-54` | free-form prompt as brand | `content.skill1`; `q15.fm6` |
| q11.cog1 | Ads | LTV/CAC discipline | spend decision | `lawyer_marketing.md:291-304`, `getu_ads_v2.md:1048-1064` | `attribution_v2.md:117-119` | spend without identity | `ads.skill7`/`ads.skill8`; `q15.fm5` |
| q11.cog2 | Ads | pacing logic | budget/targeting change | `getu_ads_v2.md:1131-1149` | `getuai-ads.md:24-28` | assuming credentials | `ads.skill5`; `q15.fm4` |
| q11.cog3 | Ads | creative fatigue curves | RSA refresh | `getu_ads_v2.md:630-704`, `getu_ads_v2.md:1066-1086` | `getuai-ads-data.md:216-250` | aggregate rows hide ad fatigue | `ads.skill4`; `q15.fm1` |
| q11.cog4 | Ads | attribution paradox | better measurement adds fragility | `attribution_v2.md:13-23` | `attribution_v2.md:151-186` | SDK once and done | `ads.skill8`; `q15.fm5` |
| q11.cog5 | Ads | kill-vs-scale criteria | read -> write action | `lawyer_marketing.md:248-269` | `growth-engine-legacy.md:83-88` | engines own writes | `q13.f7`; `q15.fm6` |
| q12.cog1 | Social | platform-as-game-theory | community rules matter | `reddit-scount.md:108-181` | `openclaw-marketing.md:122-158` | universal adapter | `social.skill1`/`social.skill8`; `q15.fm6` |
| q12.cog2 | Social | algorithm preference modeling | search/feed/reply/video differs | `youtube-api-demo.md:48-54`, `openclaw-marketing.md:7392-7422` | `reddit-scount.md:141-181` | search-only engagement | `social.skill3`/`social.skill5` |
| q12.cog3 | Social | community fit before brand voice | reply context needed | `reddit-scount.md:108-139` | `openclaw-marketing.md:7392-7422` | raw X post before fit | `social.skill2`/`social.skill5`; `q15.fm6` |
| q12.cog4 | Social | viral mechanics | post/media affordance | `openclaw-marketing.md:7392-7422` | `youtube-api-demo.md:48-54` | video search as viral loop | `q14.m5` |
| q12.cog5 | Social | automation visibility cost | public/private automation | `openclaw-marketing.md:122-126`, `x-api-credit-monitor.md:7-17` | `openclaw-marketing.md:132-158` | always-on without visible controls | `q13.f5`/`q13.f7`; `q15.fm4`/`q15.fm6` |

Cognition synthesis: trigger discipline prevents model overreach. Shared infrastructure owns trust, schedules, observability, LLM routing, ledgers, credentials, approvals, and kill-switches; domain cognition owns ranking interpretation, tone, spend, and community context.

## Q13 - Shared Foundations

Decision rule: share tenant trust, credentials, schedules, ledgers, observability, LLM routing, approval, and governance because these create cross-domain safety and auditability. Isolate schemas, external APIs, ranking logic, tone/register, community rules, campaign mutations, and domain kill criteria because they encode domain semantics.

| row_id | foundation | shared contract | corpus evidence | domain-isolated boundary | hooks_to_q14_q15 |
|---|---|---|---|---|---|
| q13.f1 | identity/session | tenant/user/session context; no raw browser tokens in engines | `growth-engine-legacy.md:43-50`, `getuai-api.md:23-37`, `getuai-ui.md:35-60` | domain repos read scoped context only | `q14.m1`, `q14.m3`, `q14.m4`, `q15.fm1`, `q15.fm5` |
| q13.f2 | secrets/credentials | scoped leases, SDK/config lookup | `growth-engine-legacy.md:64-88`, `getuai-ads.md:21-28`, `x-api-credit-monitor.md:12-18`, `getuai-ads-sdk.md:146-161` | platform payload semantics stay in adapters | `q14.m1`, `q14.m2`, `q14.m4`, `q15.fm1`, `q15.fm4` |
| q13.f3 | data/artifacts/lake | sessions, growth artifacts, events/leads/scores, publishable records | `getuai-api.md:24-42`, `rankncompare.md:49-56`, `attribution_v2.md:13-16` | products, emails, campaigns, posts, ranks | `q14.m1`, `q14.m2`, `q14.m3`, `q14.m4`, `q15.fm3`, `q15.fm5`, `q15.fm8` |
| q13.f4 | schedules/queues | Core-owned schedules/poller or explicit monitor contract | `growth-engine-legacy.md:64-88`, `x-api-credit-monitor.md:82-93`, `attribution_v2.md:13-16` | job payload and cadence remain domain-owned | `q14.m1`, `q14.m5`, `q14.m6`, `q15.fm1`, `q15.fm4` |
| q13.f5 | observability | Sentry/Langfuse/run-event logs, request IDs, cost/rank/sentiment history | `growth-engine-legacy.md:64-70`, `LLMRush.md:19-23`, `x-api-credit-monitor.md:7-17` | domain metrics decide alert meaning | `q14.m1`, `q14.m2`, `q14.m4`, `q14.m5`, `q14.m6`, `q15.fm4`, `q15.fm7` |
| q13.f6 | LLM gateway | shared model/provider routing, prompt/cost controls, retrieval/citation guardrails | `getuai-seo.md:78-91`, `getuai-email-2.0.md:111-114`, `reddit-scount.md:233-239` | prompts, style guides, queries, critic rubrics | `q14.m3`, `q14.m6`, `q15.fm6`, `q15.fm7` |
| q13.f7 | human-in-loop console | review, approval, override, action ledger, kill-switch | `growth-engine-legacy.md:83-88`, `lawyer_marketing.md:248-269`, `getuai-email-2.0.md:111-118` | domain done/rejection reasons | `q14.m1`, `q14.m2`, `q14.m3`, `q14.m4`, `q14.m5`, `q14.m6`, `q15.fm1`, `q15.fm6` |
| q13.f8 | repo governance/template | AGENTS/CLAUDE rules, CI, version drift checks, no secret/run leakage | `optiminds-repo-template.md:9-63`, `optiminds-org-config.md:7-44`, `growth-engine.md:33-63` | product code remains in repos | `q14.m1`, `q14.m6`, `q15.fm2`, `q15.fm9` |

## Q14 - Build Sequence

| row_id | milestone | scope | dependencies | done_criteria | next_trigger | deferrals |
|---|---|---|---|---|---|---|
| q14.m1 | Day-1 | Core tenant/session/artifact/source/approval/schedule/run-event skeleton | `q13.f1`, `q13.f2`, `q13.f3`, `q13.f4`, `q13.f5`, `q13.f7`, `q13.f8` | target/session/artifact/action/schedule/run-event records persist; no run leakage | first durable tool | ads/social writes |
| q14.m2 | Week-1 | SEO/GEO read lane via `seo.skill6`-`seo.skill9` | `q13.f2`, `q13.f3`, `q13.f5`, `q13.f7`, Q1 traces | outputs stored, rank source declared, sitemap exists, publish requires approval | recurring/publish request | autopublish |
| q14.m3 | Week-2 | Content lane via `content.skill1`-`content.skill5` | `q13.f1`, `q13.f2`, `q13.f3`, `q13.f6`, `q13.f7`, Q2/Q6 | variables validate; drafts generated; review before send; citations retained | outbound metric need | rich media |
| q14.m4 | Week-4 | Ads read + attribution via `ads.skill7`/`ads.skill8`; no spend mutation | `q13.f1`, `q13.f2`, `q13.f3`, `q13.f5`, `q13.f7`, Q3 | reports + conversion events visible; read-only analyst; budget rec in action ledger | repeated budget recs | budget mutation/A-B |
| q14.m5 | Week-8 | controlled writes across domains | `q13.f2`, `q13.f3`, `q13.f4`, `q13.f5`, `q13.f7`, `q15.fm4`/`q15.fm6` | every write has ledger, envelope, monitor, approval, rollback/stop reason | stable weekly outcomes | full optimizer |
| q14.m6 | Month-3 | OODA orchestration + industry packs | `q13.f1`, `q13.f3`, `q13.f4`, `q13.f5`, `q13.f6`, `q13.f7`, `q13.f8`, all lanes | weekly observe-plan-approve-execute-review works; governance drift checked | tenant/industry scale | Temporal/marketplace/autonomous spend |

Evidence shape: thin prototype `getuai-2.0.md:19-42`, MVP route hardening `getuai-mvp.md:9-76`, production attribution refactor `attribution_v2.md:16-23`, vertical cases `lawyer_finder.md:11-16`, `cuilawgroup.md:10-27`, and backend-skeleton-first `growth-engine.md:8-12`.

## Q15 - Failure Modes

| row_id | failure_mode | domains | count | cause | early symptom | prophylactic | evidence_pair |
|---|---|---|---:|---|---|---|---|
| q15.fm1 | engines own platform facts | SEO/Ads/Social | 3 | scattered identity/creds/schedules | raw tokens/own cron | `q13.f1` identity, `q13.f2` leases, `q13.f4` schedules, `q13.f7` ledger | `growth-engine-legacy.md:43-50`, `growth-engine-legacy.md:83-88` |
| q15.fm2 | legacy scaffolding import | all | 4 | copying attempts | stale paths | greenfield contracts, `q13.f8` governance, `q9.cog3` specificity | `growth-engine.md:69-152` |
| q15.fm3 | docs without runtime | all | 4 | design outruns core | no `core/` tree | `q14.m1` with `q13.f3`, `q13.f4`, `q13.f5`, `q13.f8` | `growth-engine-legacy.md:16-22` |
| q15.fm4 | credential drift | SEO/Ads/Social | 3 | auth outside action layer | API/re-login errors | `q13.f2` leases + `q13.f5` monitors + `q13.f4` checks | `getuai-ads.md:24-28`, `x-api-credit-monitor.md:13-17` |
| q15.fm5 | attribution/session breakage | Ads/Content | 2 | cookie/user rotation | missing lead rows | `q13.f1` identity/session + `q13.f3` event model; `ads.skill8` tests | `attribution_v2.md:117-186` |
| q15.fm6 | writes without approval | SEO/Ads/Social | 3 | mixed read/write skills | agents mutate while analyzing | read-only diagnosis + `q13.f7` approval + `q13.f6` LLM guardrails | `lawyer_marketing.md:248-269`, `growth-engine-legacy.md:84` |
| q15.fm7 | static publisher as GEO evaluator | SEO/GEO | 1 | indexing confused with LLM visibility | sitemap but no LLM rank | LLMRush sensor with `q13.f5` observability and `q13.f6` gateway | `rankncompare.md:134-149`, `LLMRush.md:7-14` |
| q15.fm8 | prototype-local artifact store | Content/Social | 2 | local media only | no campaign/outcome link | Core artifact store via `q13.f3` | `gmi-prototype.md:14`, `gmi-prototype.md:50`, `getuai-api.md:24-40` |
| q15.fm9 | API prefix mismatch | shared | 2 | local/prod route drift | wrong backend path | `q13.f8` API_PREFIX/proxy governance | `getuai-mvp.md:9-76` |

Benchmark answers below are the direct machine-readable projection of this KB. Every citation array includes required `source-*` IDs plus load-bearing `repo.md:line-line` anchors.
