# Knowledge Base

Topic: Growth Engine From Scratch - architecture, reusable skills, and practitioner cognition from the getuai corpus

Iteration: 7 clause-level cross-model-evaluability patch

## Evidence Policy

Raw citations below omit common prefix `runs/growth-engine-from-scratch/sources/_raw/`; e.g. `getuai-seo.md:7-11` means `runs/growth-engine-from-scratch/sources/_raw/getuai-seo.md:7-11` (tier: file:line). Benchmark answers mirror required `[source-*]` IDs in `citations`.

## Evaluation Rubric Contract

| id | dimension | artifact-internal target |
|---|---|---|
| q1 | Architecture grounding | components, data flow, external dependencies, ranking signal source, content store, human-in-loop, kill-switch, convergence, disagreement, file:line |
| q2 | Architecture grounding | ideation, outline, draft, edit, publish, post-publish, LLM role, style injection, human review, load-bearing vs stylistic |
| q3 | Architecture grounding | campaign feed, bidding, reporting, attribution model, conversion event, budget pacing, anomaly detection, data model, platform boundary |
| q4 | Architecture grounding | listen, post, schedule, engage, monitor, adapter/abstraction, rate limit, credit accounting, moderation |
| q5 | Skill completeness | >=8 SEO/GEO rows, 8 columns, duplicate/canonical/deprecation/version |
| q6 | Skill completeness | >=8 Content rows, 8 columns, brittleness + mitigation for drift, hallucination, register, retrieval |
| q7 | Skill completeness | >=8 Ads rows, platform-bound vs platform-agnostic, abstraction, kill criteria |
| q8 | Skill completeness | >=8 Social rows, platform difference, parameterization, API-change failure |
| q9 | Cognition pairing | five SEO/GEO models with Decision, Trigger, Worked here, Failed here, anti-patterns |
| q10 | Cognition pairing | five content frames with worked/failed and Links to Q2/Q6 |
| q11 | Cognition pairing | five ads models with worked/failed, platform-change break, kill and scale criteria |
| q12 | Cognition pairing | five social models with worked/failed, per-platform evidence, automation visibility cost |
| q13 | Integration | >=6 shared foundations, contract, >=2 repo evidence points, share-vs-isolate rule |
| q14 | Integration | six milestone build-sequence with dependencies, done_criteria, next_trigger, deferrals, Q1-Q13 hooks |
| q15 | Integration | >=8 failure rows incl. >=3 growth-engine-legacy lessons, recurrence, cause, symptom, prophylactic, evidence_pair |

### Clause-Level Evaluation Anchors

| id | stable clause anchors | pass target | source vector |
|---|---|---|---|
| q1 | q1.r1 components/data-flow; q1.r2 deps/content/ranking; q1.r3 human/kill/disagreement | all anchors cited; trade-off named | source-seo-geo, source-shared-infra |
| q2 | q2.r1 six stages; q2.r2 LLM role; q2.r3 review/load-bearing/style | every stage has role + review/no-review | source-content-writing, source-shared-infra |
| q3 | q3.r1 closed loop; q3.r2 data/conversion; q3.r3 platform boundary | SDK vs shared business logic separated | source-ads, source-shared-infra |
| q4 | q4.r1 five surfaces; q4.r2 adapter vs abstraction; q4.r3 rate/credit/moderation | no invented clean abstraction | source-social, source-shared-infra |
| q5 | q5.s1 >=8 rows; q5.s2 8 cols; q5.s3 canonical/duplicate | incomplete rows do not count | source-seo-geo, source-skills-catalog |
| q6 | q6.s1 >=8 rows; q6.s2 brittleness; q6.s3 mitigation | drift/hallucination/register/retrieval visible | source-content-writing, source-skills-catalog |
| q7 | q7.s1 >=8 rows; q7.s2 platform boundary; q7.s3 kill/attribution | each row has boundary + kill signal | source-ads, source-skills-catalog |
| q8 | q8.s1 >=8 rows; q8.s2 parameterization; q8.s3 API failure | platform limits explicit | source-social, source-skills-catalog |
| q9 | q9.c1 topical authority; q9.c2 intent; q9.c3 E-E-A-T; q9.c4 GEO vs SEO; q9.c5 velocity | each has Decision, Trigger, Worked, Failed | source-seo-geo, source-cognitive-models, source-failure-modes |
| q10 | q10.c1 journey; q10.c2 portfolio; q10.c3 distribution; q10.c4 ROI; q10.c5 voice | each has worked/failed + Q2/Q6 hooks | source-content-writing, source-cognitive-models, source-failure-modes |
| q11 | q11.c1 LTV/CAC; q11.c2 pacing; q11.c3 fatigue; q11.c4 attribution paradox; q11.c5 kill-vs-scale | each names survival/break condition | source-ads, source-cognitive-models, source-failure-modes |
| q12 | q12.c1 platform game; q12.c2 algorithm; q12.c3 community; q12.c4 viral; q12.c5 visibility | each has per-platform worked/failed | source-social, source-cognitive-models, source-failure-modes |
| q13 | q13.i1 foundations; q13.i2 >=2 repos; q13.i3 decision rule | every row has contract + share/isolate | source-shared-infra, source-skills-catalog, source-platform-prototypes |
| q14 | q14.i1 six milestones; q14.i2 done/trigger; q14.i3 deferrals; q14.i4 Q hooks | table is the artifact | all 10 source-* IDs |
| q15 | q15.i1 failures; q15.i2 legacy; q15.i3 cause/symptom/prophylactic; q15.i4 evidence | rows hook to Q5-Q8/Q13 | source-failure-modes, source-cognitive-models, source-platform-prototypes |

## Q1 - SEO/GEO Architecture

Converged pattern: UI -> domain adapter/tools -> AI/recommendation service, with Core owning identity, sessions, credentials, ledgers, schedules, approvals, and kill-switches. `getuai-seo` provides UI/MCP/AI (`getuai-seo.md:7-11`, `:93-97`); `getuai-api` is session/data source of truth (`getuai-api.md:7-28`). Data flow: site/search/competitor/keyword/URL/clustering tools feed content and ranking sensors (`getuai-plugin.md:11-20`, `:117-126`); ranking signal is SEO metrics/keyword tracking in `getuai-seo` (`getuai-seo.md:101-106`) plus GEO rank/sentiment in LLMRush (`LLMRush.md:7-14`); content store/publisher is `rankncompare` JSON + sitemap/robots/metadata (`rankncompare.md:28`, `:53-56`, `:128-149`). External dependencies: search APIs, Google Ads keyword APIs, LLM providers, CMS/static publishing, app storage. Disagreement: product shell vs static publisher vs Core-owned facts (`growth-engine-legacy.md:43-50`). Recommendation: keep SEO tools isolated, but require human approval, override, and kill-switch ledgers before publish/recurring checks (`growth-engine-legacy.md:83-88`).

## Q2 - Content Writing Architecture

Pipeline: ideation -> outline -> draft -> edit -> publish -> post-publish. `getuai-email-2.0` gives Campaign CRUD, Recipients CSV, SMTP test, Batch create + AI generate + send (`getuai-email-2.0.md:70-73`) and the operator flow: prompt template/placeholders, SMTP test, import, batch, generation, review, send (`getuai-email-2.0.md:91-118`). LLM role: generator for drafts, critic/retriever for cited claims, orchestrator only for batch/recipient selection. Load-bearing: style guide injection through variables, recipient schema, mandatory SMTP test, human review before send, shared session/storage (`getuai-email-2.0.md:14`, `:91-99`, `:111-118`; `getuai-api.md:24-40`). Stylistic: exact UI/template/model. OpenClaw adds multi-modal image/text, summarizer, transcription primitives (`openclaw-marketing.md:153`, `:5104-5152`, `:6656-6716`).

## Q3 - Ads Architecture

Closed loop: campaign feed -> bidding/budget/targeting -> reporting -> attribution -> optimization. `getuai-ads` mirrors UI/MCP/AI and depends on Google Ads + DeepSeek credentials (`getuai-ads.md:7-11`, `:24-28`, `:66-100`). `getu_ads_v2` provides JSON stdin/file, `exec run`, `ResultEnvelope`, errors, and 38 operations over campaigns, ad groups, keywords, RSA, budgets, criteria, reporting, GAQL (`getu_ads_v2.md:9-67`, `:1010-1017`). `getuai-ads-data` is the platform-agnostic reporting lake for Google/Meta/TikTok and campaign/conversion fields (`getuai-ads-data.md:7`, `:15`, `:159-164`, `:216-250`). `attribution_v2` supplies browser SDK, Pub/Sub events, dashboard attribution, leads, scoring (`attribution_v2.md:13-16`). Boundary: platform SDKs/mutations stay platform-bound; ResultEnvelope, event schema, anomaly banners, pacing, kill/scale are shared. Human-in-loop uses read/write split from `lawyer_marketing` (`lawyer_marketing.md:248-269`).

## Q4 - Social Architecture

Surfaces: listen, post, schedule, engage, monitor. Listen: `reddit-scount` analyzes URL, audience, pain, competitors, subreddits, posts, comments (`reddit-scount.md:108-181`). YouTube is a search adapter with query/maxResults (`youtube-api-demo.md:7-20`, `:48-54`). X post/reply/search is OpenClaw `xurl` (`openclaw-marketing.md:7392-7422`, `:7502-7507`). Multi-platform abstraction is partial: OpenClaw Gateway/inbox/routing/sessions/tools/cron/webhooks + per-channel adapters (`openclaw-marketing.md:132-158`). Rate limit and credit accounting: X credit monitor reads balance/burn and alerts (`x-api-credit-monitor.md:7-17`, `:72-104`). Moderation insertion point: after generation and before public post/reply; DM pairing/allowlist blocks unknown senders (`openclaw-marketing.md:122-126`).

## Q5 - SEO/GEO Skill Catalog

| skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|
| seo-campaign-console | getuai-seo | `getuai-seo.md:93-106` | web UI + AI | campaign/account/files | recs/metrics | sessions/API | canonical shell; duplicate ads pattern |
| keyword-research-tracking | getuai-seo | `getuai-seo.md:101-102` | MCP/API | seed/site/locale | keywords/ranks | campaign store | overlaps plugin; canonical product row |
| content-optimization | getuai-seo | `getuai-seo.md:103` | AI rec | page + keyword | edits/recs | artifacts | prompt drift checks |
| backlink-analysis | getuai-seo | `getuai-seo.md:104` | MCP/API | domain/url | backlink report | campaign store | unique sample |
| competitor-analysis | getuai-seo/getuai-competitor-analysis | `getuai-seo.md:105`; `getuai-competitor-analysis.md:7-21` | MCP services | company/query | competitors/SERP | DB/files | duplicate; canonical plugin/MCP |
| site-structure-analyzer | getuai-plugin | `getuai-plugin.md:11-14` | FastAPI/Dify | URL/site | crawl/meta | logs | canonical crawler |
| google-search-analyzer | getuai-plugin | `getuai-plugin.md:16`, `:124` | FastAPI | query/domain | SERP insights | stateless/logs | Google Custom Search dependency |
| keyword-clustering | getuai-plugin | `getuai-plugin.md:20`, `:126` | FastAPI | keywords | clusters | stateless | retry API; canonical clustering |

Canonical: `getuai-plugin` for reusable tools, `getuai-seo` for product shell, `rankncompare` for static publisher; deprecate duplicates after Core skill registry.

## Q6 - Content Writing Skill Catalog

| skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|
| campaign-prompt-template | getuai-email-2.0 | `getuai-email-2.0.md:91-94` | UI form | name/vars | template | campaign DB | register drift via variables |
| personalized-email-draft | getuai-email-2.0 | `getuai-email-2.0.md:14`, `:111-114` | batch | recipient+prompt | draft | batch DB | hallucination via recipient grounding |
| recipient-import | getuai-email-2.0 | `getuai-email-2.0.md:70-73`, `:101-104` | API+CSV | CSV columns | recipients | MySQL | schema validation |
| smtp-test-and-send | getuai-email-2.0 | `getuai-email-2.0.md:96-99`, `:116-118` | UI/API | SMTP+batch | sent status | account DB | human review before send |
| cited-websearch-copy | reddit-scount | `reddit-scount.md:233-239` | service | query/context | cited answer | logs | retrieval grounding |
| multi-model-rank-summary | LLMRush | `LLMRush.md:7-14` | web/API | term/URL | rank/sentiment | history | evaluation rubric for GEO drift |
| image-text-composer | openclaw-marketing | `openclaw-marketing.md:153`, `:5104-5152` | skill CLI | prompt/images | asset/meta | files | asset/path persistence |
| summarizer-transcriber | openclaw-marketing | `openclaw-marketing.md:6656-6716` | CLI | URL/file | summary/transcript | file/log | provider fallback |

Brittleness controls: prompt template, voice and tone variables, multi-lingual/register review, retrieval grounding, evaluation rubric via rank/citation traces.

## Q7 - Ads Skill Catalog

| skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|
| google-ads-cli | getu_ads_v2 | `getu_ads_v2.md:9-67` | CLI stdin/file | op+JSON+config | ResultEnvelope | API effects | platform-bound Google; canonical shell |
| campaign-management | getu_ads_v2 | `getu_ads_v2.md:1010` | CLI op | campaign cfg/id | campaign result | Google Ads | kill on envelope/policy error |
| keyword-management | getu_ads_v2 | `getu_ads_v2.md:1012`, `:923-950` | CLI op | ad_group_ids/keywords | criteria | Google Ads | match type validation |
| rsa-creative-management | getu_ads_v2 | `getu_ads_v2.md:1013`, `:630-704` | CLI op | headlines/descriptions/url | RSA result | Google Ads | creative fatigue via ad report |
| budget-targeting | getu_ads_v2 | `getu_ads_v2.md:1014`, `:1131-1149` | CLI op | campaign/amount/geo/lang | budget/criteria | Google Ads | pacing guardrail |
| reporting-gaql | getu_ads_v2 | `getu_ads_v2.md:1048-1123` | CLI op | range/query | metrics/GAQL | report artifact | anomaly detection input |
| attribution-ingest | attribution_v2 | `attribution_v2.md:13-16` | SDK+FastAPI | UTM/events/users | events/leads | PubSub/tables | platform-agnostic conversion backbone |
| platform-credential-sdk | getuai-ads-sdk | `getuai-ads-sdk.md:7-12`, `:146-161` | Python SDK | user/token/platform | credentials | Redis/API | kill if unavailable |

A/B test orchestration remains campaign/ad variants plus reports. Platform-agnostic abstraction is envelope, event schema, metric schema, kill criteria.

## Q8 - Social Skill Catalog

| skill_name | originating_repo | path_reference | invocation_surface | input_schema | output_schema | state_persistence | maintenance_signals |
|---|---|---|---|---|---|---|---|
| reddit-opportunity-analysis | reddit-scount | `reddit-scount.md:108-139` | API | URL | keywords/pain/competitors | MySQL | Reddit-bound |
| reddit-discovery | reddit-scount | `reddit-scount.md:141-181` | API | keyword/competitor | posts/comments | MySQL/cache | topic selection/listening |
| youtube-search | youtube-api-demo | `youtube-api-demo.md:7-20`, `:48-54` | HTTP | query/maxResults | videos | stateless | quota/API change |
| x-credit-monitor | x-api-credit-monitor | `x-api-credit-monitor.md:7-17`, `:72-104` | launchd | session/thresholds | Lark alerts | logs/env | credit/re-login monitor |
| x-post-reply-search | openclaw-marketing | `openclaw-marketing.md:7392-7422`, `:7502-7507` | xurl CLI | text/post/query/media | post/reply/search | X effects | xurl/API break |
| multi-channel-inbox | openclaw-marketing | `openclaw-marketing.md:132-158` | Gateway | channel/account/session | routed message | gateway store | cross-platform adapters |
| slack-actions | openclaw-marketing | `openclaw-marketing.md:6314-6339` | tool | channel/message/content | send/edit/delete | Slack effects | per-platform semantics |
| channel-gating | openclaw-marketing | `openclaw-marketing.md:122-126` | config | dmPolicy/allowFrom | allow/deny | gateway config | moderation guardrail |

Parameterization: max length, media, mention semantics, hashtags, reply/thread ID, auth profile, sentiment/monitor target, quota/credit threshold.

## Q9 - SEO/GEO Cognition

1. Topical authority. Decision: entity/category pages before prompt volume. Trigger: stable crawlable demand. Worked here: `rankncompare` data/sitemap/robots/canonical/meta consistency (`rankncompare.md:128-187`, `:350`). Failed here: `getuai-2.0` lacks crawlable store (`getuai-2.0.md:19-42`).
2. Intent mapping. Decision: route search/competitor/keyword inputs before generation. Trigger: what-to-write ambiguity. Worked here: `getuai-plugin` separates site/search/competitor/keyword/URL/cluster tools (`getuai-plugin.md:11-20`, `:117-126`). Failed here: `rankncompare` publishes but does not discover intent (`rankncompare.md:53-56`, `:134-149`).
3. E-E-A-T. Decision: inject vertical evidence packs. Trigger: regulated/trust-sensitive claims. Worked here: `lawyer_marketing` legal intelligence (`lawyer_marketing.md:7-14`, `:291-317`). Failed here: `growth-engine` says industry difference must be packs (`growth-engine.md:8`, `:27`).
4. GEO vs SEO. Decision: split indexability from LLM-answer sensing. Trigger: metric becomes answer inclusion. Worked here: LLMRush multi-model rank/sentiment (`LLMRush.md:7-14`). Failed here: sitemap/robots cannot measure LLM inclusion (`rankncompare.md:134-149`; `LLMRush.md:7-14`).
5. Content velocity vs depth. Decision: scale cadence after evaluator exists. Trigger: generation outruns data. Worked here: `getuai-seo` ties keywords/content/backlinks/competitors/metrics (`getuai-seo.md:101-106`). Failed here: docs without Core runtime (`growth-engine-legacy.md:16-22`).

Anti-patterns: tool-first SEO without store; velocity without sensors; sitemap as GEO proof; generic advice without industry pack.

## Q10 - Content Writing Cognition

1. User journey. Decision: content is campaign-stage object. Trigger: recipients/channel/conversion. Worked: email campaign->review->send (`getuai-email-2.0.md:70-73`, `:91-118`). Failed: `gmi-prototype` asset without outcome loop (`gmi-prototype.md:7-14`, `:50-54`). Links to Q2 pipeline; Q6 templates/import/draft/send.
2. Portfolio theory. Decision: mix SEO/GEO, email, social, cited answers. Trigger: channel vs primitive choice. Worked: OpenClaw image/text/summarizer/transcriber (`openclaw-marketing.md:153`, `:5104-5152`, `:6656-6716`). Failed: email-only narrows portfolio (`getuai-email-2.0.md:70-73`, `:91-118`). Links Q2 shared review; Q6 composer/transcriber/rank.
3. Distribution over production. Decision: asset done only after publish/measure. Trigger: local files pile up. Worked: SMTP-tested review/send (`getuai-email-2.0.md:96-99`, `:111-118`). Failed: local videos only (`gmi-prototype.md:14`, `:50`). Links Q2 publish/post-publish; Q6 send/cited retrieval.
4. ROI window. Decision: near-term outbound, medium SEO, long GEO. Trigger: wrong horizon. Worked: LLMRush history/rank/sentiment/tokens (`LLMRush.md:7-23`). Failed: `getuai-2.0` lacks history/measurement (`getuai-2.0.md:19-42`). Links Q2 post-publish; Q6 rank/citation traces.
5. Brand voice. Decision: encode variables/retrieval/review. Trigger: many models/channels. Worked: placeholders + review (`getuai-email-2.0.md:91-99`, `:111-118`). Failed: free prompt no voice schema (`gmi-prototype.md:29-54`). Links Q2 style/review; Q6 template/draft/cited copy.

Anti-patterns: production over distribution; prompt-only voice; one-channel portfolio; wrong ROI window; no post-publish measure.

## Q11 - Ads Cognition

1. LTV/CAC. Decision: scale when cost and lead quality agree. Trigger: platform conversions without identity. Worked: legal benchmarks + cost/conversion reports (`lawyer_marketing.md:291-304`; `getu_ads_v2.md:1048-1064`). Failed: missing `setUserId`/session bridge (`attribution_v2.md:117-119`, `:151-155`).
2. Pacing. Decision: budget/targeting are gradual controls. Trigger: spend/CAC drift. Worked: budget/targeting ops (`getu_ads_v2.md:1014`, `:1131-1149`). Failed: credential drift blocks pacing (`getuai-ads.md:24-28`).
3. Creative fatigue. Decision: refresh RSA when ad-level metrics decay. Trigger: aggregate hides weak ads. Worked: RSA + ad reports (`getu_ads_v2.md:1013`, `:630-704`, `:1066-1086`). Failed: campaign-level data hides creative grain (`getuai-ads-data.md:216-250`).
4. Attribution paradox. Decision: source of truth and silent failure point. Trigger: healthy reports but missing leads/cookies. Worked: `attribution_v2` SDK/ingress/PubSub/dashboard/leads (`attribution_v2.md:13-23`). Failed: rows/user/session/cookie edges (`attribution_v2.md:117-119`, `:151-155`, `:184-186`).
5. Kill-vs-scale. Decision: freeze on envelope errors, attribution loss, CAC drift, policy failure; scale when reports+attribution agree. Trigger: write mutation. Worked: read/write split + ResultEnvelope (`lawyer_marketing.md:248-269`; `getu_ads_v2.md:9-67`). Failed: engines owning platform facts unsafe (`growth-engine-legacy.md:43-50`, `:83-88`).

Anti-patterns: scaling platform conversions alone; mutating before diagnosis; aggregate fatigue evidence; credential failures treated as model failures.

## Q12 - Social Cognition

1. Platform game theory. Decision: own grammar/quota/rules per platform. Trigger: workflow reused. Worked: Reddit audience/pain/subreddit model (`reddit-scount.md:108-181`). Failed: generic gateway needs adapters/allowlists/routing (`openclaw-marketing.md:122-158`, `:177-180`).
2. Algorithm preference. Decision: encode discovery/action primitive. Trigger: choose search/listen/post/reply. Worked: YouTube search vs X post/reply/search (`youtube-api-demo.md:7-20`, `:48-54`; `openclaw-marketing.md:7392-7422`, `:7502-7507`). Failed: YouTube search lacks schedule/reply/moderation/credit (`youtube-api-demo.md:7-20`, `:48-54`).
3. Community fit before brand voice. Decision: learn norms before tone. Trigger: entering community. Worked: Reddit audience/pain/competitors/subreddits (`reddit-scount.md:124-181`). Failed: `xurl` actions do not inspect norms (`openclaw-marketing.md:7392-7422`, `:7502-7507`).
4. Viral mechanics. Decision: expose reply/thread/media without calling it strategy. Trigger: reach loop. Worked: X post/reply/media/search (`openclaw-marketing.md:7392-7422`, `:7502-7507`). Failed: YouTube demo is discovery-only (`youtube-api-demo.md:7-20`, `:48-54`).
5. Automation visibility cost. Decision: moderation, allowlists, rate/credit monitor, approval before public automation. Trigger: agent-generated public content. Worked: allowlist + credit alerts (`openclaw-marketing.md:122-126`; `x-api-credit-monitor.md:7-17`, `:72-104`). Failed: direct X post/reply without moderation (`openclaw-marketing.md:7392-7422`, `:7502-7507`).

Anti-patterns: one tone everywhere; no rate/credit accounting; posting before listening; discovery API as engagement engine; automation control hidden in adapter.

## Q13 - Shared Foundations

| foundation | contract/interface | evidence | share vs isolate |
|---|---|---|---|
| identity/session | tenant/user/session, Core context | `growth-engine-legacy.md:43-50`; `getuai-api.md:23-37`; `attribution_v2.md:153-162` | shared continuity; identity never in engines |
| credentials/secrets | scoped leases, env sync, re-login monitor | `growth-engine-legacy.md:64-88`; `getuai-ads.md:21-28`; `x-api-credit-monitor.md:12-18` | shared trust; SDK calls isolated |
| data lake/artifacts | tenant/target/run/action/source keys | `getuai-api.md:24-42`; `rankncompare.md:49-56`; `attribution_v2.md:13-16`; `gmi-prototype.md:11-16` | shared retention; schemas isolated |
| schedules/queue | registry, cron/launchd adapters, retries | `growth-engine-legacy.md:64-88`; `x-api-credit-monitor.md:20`, `:82-93`; `attribution_v2.md:49-52` | shared lifecycle; cadence isolated |
| observability | run_event, request IDs, tracing, redaction | `growth-engine-legacy.md:64-70`, `:86`; `LLMRush.md:19-23`; `attribution_v2.md:107-119` | shared traces; dashboards isolated |
| LLM gateway | provider/model routing, prompt policy, token/cost | `getuai-seo.md:78-91`; `getuai-email-2.0.md:14`, `:111-114`; `openclaw-marketing.md:175-180`; `cuilawgroup.md:25-27` | shared cost/failover; prompts isolated |
| human console | approvals, overrides, kill-switch, ledger | `growth-engine-legacy.md:83-88`; `lawyer_marketing.md:248-269`; `getuai-email-2.0.md:115-118`; `openclaw-marketing.md:122-126` | shared audit; payload validation isolated |
| repo template | AGENTS/CLAUDE, skills, CI, version check | `optiminds-repo-template.md:9-30`, `:55-63`, `:156-177`; `lawyer_finder.md:71-86` | shared governance; product isolated |

Decision rule: share tenant trust, credentials, schedules, audit, observability, LLM routing, approval; isolate schema, external API, ranking logic, tone, kill criteria. Attribution events are shared (`attribution_v2.md:13-16`, `:153-162`); SEO/GEO rank interpretation stays isolated (`rankncompare.md:128-157`; `LLMRush.md:7-14`).

## Q14 - Build Sequence

| milestone | scope | dependencies | done_criteria | next_trigger | deferrals |
|---|---|---|---|---|---|
| Day-1 | Core tenant/session/artifact/source registry/repo-template/approval stub; delivers Q13 | none; `growth-engine` skeleton + template governance | growth_target persists; sessions/artifacts/approval/action records; no `runs/` leakage | first domain tool needs credentials/artifacts | defer ads/social writes until Q15 approval guard |
| Week-1 | SEO/GEO read-only: Q5 site/search/keyword/sitemap; Q1 separation | Day-1 Core + credentials/artifacts | outputs stored; rank source declared; content artifact; review point | recurring checks/publish requested | defer auto-publish until GEO/static guardrail |
| Week-2 | Content: Q6 template/import/draft/send + retrieval; Q2 flow | Core artifacts + Week-1 store + LLM gateway | variables validate; recipients import; draft; human review; SMTP test | outbound campaign/post-publish metric | defer rich media until artifact store fixed |
| Week-4 | Ads read-only + attribution: Q7 reports/attribution; Q11 CAC/pacing; no writes | credentials/campaign IDs/publish events | dashboard shows feed/report/conversions; session tests pass; read-only analyst | repeated budget recommendations | defer budget/A/B automation until boundary/attribution stable |
| Week-8 | Controlled writes behind approval: SEO/email/ads/social with ledger, channel-gating, credit monitor | prior evidence + human console + Q15 prophylactics | writes have approval, ledger, rollback/kill-switch, quota/session monitor | stable outcomes/repeated approvals | defer optimizer until platform tone/API isolated |
| Week-12 / Month-3 | OODA across SEO/GEO, Content, Ads, Social with industry packs and Q9-Q12 guardrails | all lanes + observability + vertical cases | one tenant runs weekly observe-plan-approve-execute-review | scale tenants/industries | defer Temporal-scale, marketplace, autonomous spend until monitors |

Corpus evolution: prototypes (`getuai-2.0.md:19-42`; `gmi-prototype.md:7-16`) -> MVP route/env (`getuai-mvp.md:9-76`) -> attribution parity refactor (`attribution_v2.md:16-23`) -> vertical public/admin/backend hardening (`lawyer_finder.md:11-16`, `:220-255`; `cuilawgroup.md:10-27`) -> growth-engine skeleton/schema/auth/engine slice (`growth-engine.md:8-12`).

## Q15 - Cross-Domain Failure Modes

| failure_mode | affected_domains | recurrence_count | structural_cause | early_symptom | prophylactic | evidence_pair |
|---|---|---:|---|---|---|---|
| Domain engines own platform facts | SEO, Ads, Social | 3 | scattered identity/credentials/schedules | raw tokens or own cron | Core owns facts/context/leases; Q13 identity/secrets | `growth-engine-legacy.md:43-50`, `:83-88` |
| Legacy scaffolding import | all | 4 | copying old attempt | stale paths/missing runtime | greenfield rewrite, references read-only | `growth-engine.md:69-100`, `:138-152` |
| Missing runtime core after docs | all | 4 | design without runtime | Core in docs only | Day-1 skeleton before domains | `growth-engine-legacy.md:16-22`, `growth-engine.md:11-12` |
| Platform API credential drift | SEO, Ads, Social | 3 | auth external to action layer | API errors/re-login alerts | central leases + monitors | `getuai-ads.md:24-28`, `x-api-credit-monitor.md:13-17`, `growth-engine-legacy.md:85` |
| Attribution/session breakage | Ads, Content | 2 | cookie/user rotation misunderstood | missing leads/cookies | SDK domain config + session tests | `attribution_v2.md:117-119`, `:153-155`, `:184-186` |
| Write operations without approval | SEO, Ads, Social | 3 | read/write mixed | agents mutate while analyzing | read-only analysis, hooks, ledger | `lawyer_marketing.md:248-269`, `growth-engine-legacy.md:84` |
| Static publisher as GEO evaluator | SEO/GEO | 1 | indexing confused with LLM visibility | sitemap but no LLM rank | add multi-model rank sensor | `rankncompare.md:134-149`, `LLMRush.md:7-14` |
| Prototype-local artifact store | Content, Social | 2 | media saved locally only | no campaign/outcome link | Core artifact store | `gmi-prototype.md:14`, `:50`, `getuai-api.md:24-40` |
| API prefix/proxy mismatch | shared infra | 2 | local/prod routes diverge | wrong backend path | API_PREFIX + proxy contract | `getuai-mvp.md:9-76` |

Pattern: shared Core for trust/ledgers, isolated platform adapters, human approval before writes, monitors for quota/session/attribution. Each prophylactic maps back to Q5-Q8 skills or Q13 foundations.
