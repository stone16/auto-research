# Knowledge Base

Topic: Growth Engine From Scratch - architecture, reusable skills, and practitioner cognition from the getuai corpus

Iteration: 14 structured Q13 foundation rows merged without Q1-Q4 trace regression

## Stable Artifact ID Contract
Q1-Q4 architecture trace rows use `q1.trace*` through `q4.trace*`; Q13 shared foundations use `q13.f1` through `q13.f8`; Q5-Q8 skill rows use `seo.skill*`, `content.skill*`, `ads.skill*`, and `social.skill*`; Q9-Q12 cognition rows use `q9.cog*` through `q12.cog*`; Q14 milestones use `q14.m1` through `q14.m6`; Q15 failure modes use `q15.fm1` through `q15.fm9`.

## Architecture Trace Contract
For Q1-Q4, every trace row is read as input -> component -> state -> output and terminates in direct file:line evidence. Shared Core is cited only where the step crosses trust, approval, credential, schedule, ledger, observability, LLM routing, or kill-switch boundaries.

## Q1 - SEO/GEO Architecture
Converged pattern: crawler/search adapter -> ranking signal source -> GEO evaluator -> content store -> generator -> publisher -> Core human-in-loop approval and kill-switch. `getuai-seo` packages UI/MCP/AI, `rankncompare` packages static publisher/content store, and `growth-engine-legacy` makes Core own platform facts.

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

## Q2 - Content Writing Architecture
Architecture: campaign/entity facts -> ideation -> outline -> draft -> edit/review -> publish -> post-publish learning. Load-bearing choices are prompt/style variables, recipient schema, SMTP test, human review, retrieval grounding, and shared artifact/session storage.

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
Architecture: campaign feed -> bidding/budget/targeting -> reporting -> attribution -> optimization. Platform SDKs and mutations stay platform-bound; ResultEnvelope, reporting lake, attribution events, anomaly/pacing checks, approval ledger, and kill criteria are platform-agnostic.

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
| q3.trace9 | normalized rows -> platform-agnostic analyst -> anomaly/pacing state -> kill-vs-scale recommendation (`getuai-ads-data.md:216-250`) |

## Q4 - Social Architecture
Architecture: listen, post, schedule, engage, monitor as platform adapters behind Gateway-style routing, not a fake universal adapter.

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
Protected artifact: 34 skill rows remain stable: SEO `seo.skill1`-`seo.skill9`, Content `content.skill1`-`content.skill8`, Ads `ads.skill1`-`ads.skill9`, and Social `social.skill1`-`social.skill8`. Each row preserves skill_name, originating_repo, path_reference, invocation_surface, input_schema, output_schema, state_persistence, and maintenance_signals. Canonical evidence anchors include `getuai-seo.md:93-106`, `getuai-plugin.md:11-20`, `rankncompare.md:53-56`, `getuai-email-2.0.md:91-118`, `reddit-scount.md:233-239`, `getu_ads_v2.md:9-67`, `getu_ads_v2.md:1010-1017`, `attribution_v2.md:13-16`, `x-api-credit-monitor.md:72-104`, and `openclaw-marketing.md:122-158`.

## Q9-Q12 Cognition Evidence Table
Protected cognition rows remain stable: SEO/GEO `q9.cog1`-`q9.cog5`, Content `q10.cog1`-`q10.cog5`, Ads `q11.cog1`-`q11.cog5`, and Social `q12.cog1`-`q12.cog5`. Every row keeps trigger, worked_here, failed_here, anti_pattern, and hook fields. Worked/failed anchors include `rankncompare.md:128-187` vs `getuai-2.0.md:19-42`, `getuai-plugin.md:11-20` vs `rankncompare.md:53-56`, `lawyer_marketing.md:291-317` vs `growth-engine.md:7-30`, `LLMRush.md:7-14` vs `rankncompare.md:134-149`, `getuai-email-2.0.md:70-118` vs `gmi-prototype.md:7-54`, `getu_ads_v2.md:1131-1149` vs `getuai-ads.md:24-28`, and `reddit-scount.md:108-181` vs `openclaw-marketing.md:122-158`.

## Q13 - Shared Foundations
Decision rule: share tenant trust, credentials, schedules, ledgers, observability, LLM routing, approval, and governance because these create cross-domain auditability and safety. Isolate schemas, external APIs, ranking logic, tone/register, community rules, campaign mutations, and domain kill criteria because those encode domain semantics.

| row_id | foundation | shared contract | corpus evidence | domain-isolated boundary | hooks_to_q14_q15 |
|---|---|---|---|---|---|
| q13.f1 | identity/session | tenant/user/session context; Core signs or constructs RequestContext | `growth-engine-legacy.md:43-50`, `getuai-api.md:23-37`, `getuai-ui.md:35-60` | domain repos read scoped context, not auth truth | `q14.m1`, `q14.m3`, `q14.m4`, `q15.fm1`, `q15.fm5` |
| q13.f2 | secrets/credentials | scoped leases, SDK/config lookup, no raw durable engine secrets | `growth-engine-legacy.md:64-88`, `getuai-ads.md:21-28`, `x-api-credit-monitor.md:12-18`, `getuai-ads-sdk.md:146-161` | platform payload semantics stay adapter-local | `q14.m1`, `q14.m2`, `q14.m4`, `q15.fm1`, `q15.fm4` |
| q13.f3 | data/artifacts/lake | session artifacts, growth artifacts, events/leads/scores, publishable records | `getuai-api.md:24-42`, `rankncompare.md:49-56`, `attribution_v2.md:13-16` | products, emails, campaigns, posts, ranks schemas | `q14.m1`, `q14.m2`, `q14.m3`, `q14.m4`, `q15.fm3`, `q15.fm5`, `q15.fm8` |
| q13.f4 | schedules/queues | Core-owned schedules/poller or explicit monitor contract | `growth-engine-legacy.md:64-88`, `x-api-credit-monitor.md:82-93`, `attribution_v2.md:13-16` | payload and cadence remain domain-owned | `q14.m5`, `q14.m6`, `q15.fm1`, `q15.fm4` |
| q13.f5 | observability | Sentry/Langfuse/run-event logs, request IDs, cost/rank/sentiment history | `growth-engine-legacy.md:64-70`, `LLMRush.md:19-23`, `x-api-credit-monitor.md:7-17` | domain metrics decide alert meaning | `q14.m2`, `q14.m4`, `q14.m5`, `q14.m6`, `q15.fm4`, `q15.fm7` |
| q13.f6 | LLM gateway | model routing, prompt/cost controls, retrieval/citation guardrails | `getuai-seo.md:78-91`, `getuai-email-2.0.md:111-114`, `reddit-scount.md:233-239` | prompts, style, rank queries, critic rubrics | `q14.m3`, `q14.m6`, `q15.fm6`, `q15.fm7` |
| q13.f7 | human-in-loop console | review, approval, override, action ledger, kill-switch for writes | `growth-engine-legacy.md:83-88`, `lawyer_marketing.md:248-269`, `getuai-email-2.0.md:111-118` | domain rejection reasons stay lane-local | `q14.m1`, `q14.m2`, `q14.m3`, `q14.m4`, `q14.m5`, `q14.m6`, `q15.fm1`, `q15.fm6` |
| q13.f8 | repo governance/template | AGENTS/CLAUDE rules, CI, version drift, PR conventions, no run leakage | `optiminds-repo-template.md:9-63`, `optiminds-org-config.md:7-44`, `growth-engine.md:33-63` | product/business code remains in consuming repos | `q14.m1`, `q14.m6`, `q15.fm2`, `q15.fm9` |

## Q14 - Build Sequence
| row_id | milestone | scope | dependencies | done_criteria | next_trigger | deferrals |
|---|---|---|---|---|---|---|
| q14.m1 | Day-1 | Core tenant/session/artifact/source/approval skeleton | `q13.f1`, `q13.f2`, `q13.f3`, `q13.f7`, `q13.f8` | target/session/artifact/action records persist; no run leakage | first durable tool | ads/social writes |
| q14.m2 | Week-1 | SEO/GEO read lane via `seo.skill6`-`seo.skill9` | `q13.f2`, `q13.f3`, `q13.f5`, `q13.f7`, `q1.trace1`-`q1.trace8` | outputs stored, rank source declared, sitemap exists, approval before publish | recurring/publish request | autopublish |
| q14.m3 | Week-2 | Content templates/import/draft/SMTP/retrieval | `q13.f1`, `q13.f2`, `q13.f3`, `q13.f6`, `q13.f7`, Q2/Q6 rows | variables validate; drafts generated; review before send | outbound metric need | rich media |
| q14.m4 | Week-4 | Ads read + attribution; no spend mutation | `q13.f1`, `q13.f2`, `q13.f3`, `q13.f5`, `q13.f7`, Q3 rows | reports and conversion events visible; recommendation logged before write | repeated budget recs | budget mutation/A-B |
| q14.m5 | Week-8 | Controlled writes with approval/moderation guardrails | `q13.f2`, `q13.f3`, `q13.f4`, `q13.f5`, `q13.f7`, `q15.fm4`, `q15.fm6` | every write has ledger, envelope, monitor, approval, rollback/stop reason | stable weekly outcomes | full optimizer |
| q14.m6 | Month-3 | OODA orchestration + industry packs | `q13.f1`, `q13.f3`, `q13.f4`, `q13.f5`, `q13.f6`, `q13.f7`, `q13.f8`, all lanes | weekly observe-plan-approve-execute-review works | tenant/industry scale | Temporal/marketplace/autonomous spend |

Evidence shape: prototype `getuai-2.0.md:19-42`, MVP route hardening `getuai-mvp.md:9-76`, production refactor `attribution_v2.md:16-23`, vertical cases `lawyer_finder.md:11-16`, `cuilawgroup.md:10-27`, backend skeleton `growth-engine.md:8-12`.

## Q15 - Failure Modes
| row_id | failure_mode | domains | count | cause | early symptom | prophylactic | evidence_pair |
|---|---|---|---:|---|---|---|---|
| q15.fm1 | engines own platform facts | SEO/Ads/Social | 3 | scattered identity/creds/schedules | raw tokens/own cron | `q13.f1`, `q13.f2`, `q13.f4`, `q13.f7` | `growth-engine-legacy.md:43-50`, `growth-engine-legacy.md:83-88` |
| q15.fm2 | legacy scaffolding import | all | 4 | copying old attempt | stale paths | `q13.f8` governance + `q9.cog3` vertical specificity | `growth-engine.md:69-152` |
| q15.fm3 | docs without runtime | all | 4 | design outruns core | no `core/` tree | `q14.m1` with `q13.f3` and `q13.f8` | `growth-engine-legacy.md:16-22` |
| q15.fm4 | credential drift | SEO/Ads/Social | 3 | auth outside action layer | API/re-login errors | `q13.f2` leases + `q13.f5` monitors + `q13.f4` checks | `getuai-ads.md:24-28`, `x-api-credit-monitor.md:13-17` |
| q15.fm5 | attribution/session breakage | Ads/Content | 2 | cookie/user rotation | missing lead rows | `q13.f1`, `q13.f3`, SDK domain/session tests | `attribution_v2.md:117-186` |
| q15.fm6 | writes without approval | SEO/Ads/Social | 3 | mixed read/write skills | agents mutate while analyzing | `q13.f7` ledger/approval + `q13.f6` guardrails | `lawyer_marketing.md:248-269`, `growth-engine-legacy.md:84` |
| q15.fm7 | static publisher as GEO evaluator | SEO/GEO | 1 | indexing confused with LLM visibility | sitemap but no LLM rank | LLMRush sensor with `q13.f5` and `q13.f6` | `rankncompare.md:134-149`, `LLMRush.md:7-14` |
| q15.fm8 | prototype-local artifact store | Content/Social | 2 | local media only | no campaign/outcome link | Core artifact store via `q13.f3` | `gmi-prototype.md:14`, `gmi-prototype.md:50`, `getuai-api.md:24-40` |
| q15.fm9 | API prefix mismatch | shared | 2 | local/prod route drift | wrong backend path | `q13.f8` API_PREFIX/proxy contract | `getuai-mvp.md:9-76` |
