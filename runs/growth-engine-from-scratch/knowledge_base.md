# Knowledge Base

Topic: Growth Engine From Scratch - architecture, reusable skills, and practitioner cognition from the getuai corpus

Iteration: 15 citation-discipline repair with Q1/Q4 disagreement gains

## Evidence Policy

Direct citations use `repo.md:line-line` from `runs/growth-engine-from-scratch/sources/_raw/`. Source IDs are mirrored in top-level benchmark citation arrays. Benchmark answers must carry explicit file:line anchors, not source IDs alone.

## Stable Artifact ID Contract

Stable row IDs are part of the evaluation contract. Q1-Q4 traces use `q1.trace*` through `q4.trace*`; skill rows use `seo.skill*`, `content.skill*`, `ads.skill*`, and `social.skill*`; cognition rows use `q9.cog*` through `q12.cog*`; Q13 foundations use `q13.f*`; Q14 milestones use `q14.m*`; Q15 failure modes use `q15.fm*`. For Q1-Q4, every trace row reads as input -> component -> state -> output and terminates in direct file:line evidence.

## Q1 - SEO/GEO Architecture

Converged architecture: UI/product shell -> SEO/GEO adapters -> AI/recommendation layer -> Core-owned identity, credentials, artifacts, schedules, approvals, ledgers, and kill-switch. Evidence: `getuai-seo.md:7-11`, `getuai-seo.md:52-83`, `getuai-seo.md:93-97`, `getuai-api.md:7-28`, `growth-engine-legacy.md:43-50`, `growth-engine-legacy.md:83-88`. Repos disagree on packaging: `getuai-seo` runs three live components, UI/MCP/AI; `rankncompare` is a static publisher/content store; `growth-engine-legacy` takes the Browser -> Core-only counter-position where engines never own platform facts (`growth-engine-legacy.md:45-49`).

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

Trace lock: SEO/GEO is a reviewable chain, not a single service. Crawl/search inputs feed ranking sensors; ranking signals feed content store/generator/publisher; evaluator feedback feeds recommendations; any write crosses Core approval and kill-switch. External dependencies are search APIs, Google Ads/Custom Search credentials, LLM providers, CMS/static publishing, and Core credential leases. Failure handling lives at adapter retry/logging, artifact replay, and Core stop state.

| order | component | input | state | output | citation |
|---:|---|---|---|---|---|
| 1 | crawler/search adapter | URL, site, query, domain | crawl/meta/link/SERP | discovery artifact | `getuai-plugin.md:11-20` |
| 2 | ranking signal source | term, company, campaign | keyword/rank metrics | SEO ranking signal | `getuai-seo.md:101-106` |
| 3 | GEO evaluator sensor | term, URL, model set | rank/sentiment/history | LLM visibility signal | `LLMRush.md:7-14` |
| 4 | content store | category/product JSON | products/categories/metadata | publishable corpus | `rankncompare.md:128-149` |
| 5 | publisher | stored routes/pages | sitemap.xml/robots.txt | crawler-facing surface | `rankncompare.md:53-56` |
| 6 | human-in-loop Core control | publish or optimization request | action ledger/approval state | approved, overridden, or killed action | `growth-engine-legacy.md:83-88` |

Disagreement is architectural: `getuai-seo` converges on UI/MCP/AI product runtime (`getuai-seo.md:52-83`), `rankncompare` keeps a static publisher/content store, and `growth-engine-legacy` rejects engines owning platform facts (`growth-engine-legacy.md:45-49`). The recommendation is domain-owned crawl/evaluate/publish logic with shared Core identity, credentials, artifacts, approvals, schedules, ledgers, and kill-switch.

## Q2 - Content Writing Architecture

Architecture: campaign/entity facts -> ideation -> outline -> draft -> edit/review -> publish -> post-publish learning. `getuai-email-2.0` provides the concrete path: campaign CRUD, recipient import, SMTP CRUD/test, batch create, AI generate, review, send (`getuai-email-2.0.md:70-73`, `getuai-email-2.0.md:91-118`). Load-bearing choices are prompt/style variables, recipient schema, SMTP validation, human review, and shared API artifact/session storage (`getuai-api.md:24-40`). Stylistic choices are table UI, template file format, and frontend stack.

| step | input -> component -> state -> output trace |
|---|---|
| q2.trace1 | campaign fields/style variables -> prompt-template form -> prompt state -> ideation/outline contract (`getuai-email-2.0.md:91-94`) |
| q2.trace2 | CSV recipient fields -> import service -> recipient records -> personalization input (`getuai-email-2.0.md:101-104`) |
| q2.trace3 | batch + prompt + recipient -> LLM generator -> generated email rows -> draft output (`getuai-email-2.0.md:111-114`) |
| q2.trace4 | generated emails -> human review -> approved content state -> sendable batch (`getuai-email-2.0.md:111-118`) |
| q2.trace5 | SMTP account + approved batch -> SMTP test/send -> sent/failed status -> publish outcome (`getuai-email-2.0.md:96-99`) |
| q2.trace6 | image/text/company artifacts -> API store -> session-scoped content -> post-publish input (`getuai-api.md:24-40`) |
| q2.trace7 | factual question -> retrieval-grounded copy -> cited answer -> hallucination guard (`reddit-scount.md:233-239`) |

## Q3 - Ads Architecture

Architecture: campaign feed -> bidding/budget/targeting -> reporting -> attribution -> optimization. `getuai-ads` shows the UI/MCP/AI product and credential dependencies (`getuai-ads.md:7-11`, `getuai-ads.md:24-28`). `getu_ads_v2` is the platform-bound Google Ads adapter: stdin/file JSON, `exec run`, compact ResultEnvelope, and 38 operations (`getu_ads_v2.md:9-67`, `getu_ads_v2.md:1010-1017`). Platform-agnostic logic is ResultEnvelope, reporting lake, attribution events, anomaly/pacing checks, approval ledger, and kill criteria. `getuai-ads-data` supplies cross-platform campaign/conversion tables (`getuai-ads-data.md:216-250`); `attribution_v2` supplies SDK -> ingress/consumer -> Pub/Sub -> events/leads/scores (`attribution_v2.md:13-16`).

| step | input -> component -> state -> output trace |
|---|---|
| q3.trace1 | credentials + brief -> Ads UI/MCP/AI -> campaign feed/recs -> operator workbench (`getuai-ads.md:7-11`) |
| q3.trace2 | operation JSON -> google-ads-cli exec -> ResultEnvelope -> agent-readable output (`getu_ads_v2.md:9-67`) |
| q3.trace3 | campaign/adgroup/keyword/RSA/budget payload -> 38 ops -> platform campaign tree -> mutation/list result (`getu_ads_v2.md:1010-1017`) |
| q3.trace4 | date range/GAQL -> reports -> campaign/ad/search-term metrics -> optimization input (`getu_ads_v2.md:1048-1123`) |
| q3.trace5 | SDK event + UTM + user/session -> attribution ingress/consumer -> event-table state -> conversion/lead score (`attribution_v2.md:13-16`) |
| q3.trace6 | Google/Meta/TikTok report rows -> ads data platform -> campaign/conversion model -> trend/anomaly candidate (`getuai-ads-data.md:216-250`) |
| q3.trace7 | budget/targeting rec -> read/write approval boundary -> blocked or approved action -> action log (`lawyer_marketing.md:248-269`) |
| q3.trace8 | unsafe write/lost attribution/envelope error -> Core kill-switch -> freeze/pause/reduce -> audited stop (`growth-engine-legacy.md:83-88`) |
| q3.trace9 | normalized rows -> platform-agnostic analyst -> anomaly/pacing state -> kill-vs-scale recommendation (`getuai-ads-data.md:216-250`) |

Trace lock: Ads has two boundaries. Platform SDK mutations stay Google-bound; reports, attribution, anomalies, pacing, ledgers, and kill criteria are shared business logic. First safe version reads and recommends; writes require human approval.

## Q4 - Social Architecture

Architecture: listen, post, schedule, engage, monitor as platform adapters behind Gateway-style control, not a fake universal adapter. Reddit handles listen/topic selection (`reddit-scount.md:108-181`), YouTube handles search monitoring (`youtube-api-demo.md:48-54`), X handles post/reply/search (`openclaw-marketing.md:7392-7422`), OpenClaw Gateway routes multi-channel engagement (`openclaw-marketing.md:132-158`), and x-api-credit-monitor handles schedule, rate limit, credit accounting, and re-login alerts (`x-api-credit-monitor.md:7-17`, `x-api-credit-monitor.md:72-104`). Moderation enters before automation (`openclaw-marketing.md:122-126`). Policy breakers keep the abstraction honest: `dmPolicy='pairing'`, explicit `allowFrom`, mention gating, reply tags, and per-channel chunking (`openclaw-marketing.md:124-126`, `openclaw-marketing.md:158`).

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

Schema note: the artifact keeps the required 8 contract columns and adds `row_id` plus domain for scoring. IDs are canonical.

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

Margin audit: Q5 has 9 rows, Q6 has 8, Q7 has 9, Q8 has 8. Protected rows are `seo.skill9`, `content.skill8`, `ads.skill6`, and `social.skill8`.

## Q9-Q12 Cognition Evidence Table

Every model has trigger, worked-here evidence, failed-here evidence, anti-pattern, and hook. Unsupported cognition claims are intentionally excluded.

| row_id | domain | model_name | trigger | worked_here | failed_here | anti_pattern | hook_to_skill_or_failure_mode |
|---|---|---|---|---|---|---|---|
| q9.cog1 | SEO/GEO | topical authority | Category/product corpus needs searchable depth | `rankncompare.md:128-187` | `getuai-2.0.md:19-42` | Thin AI-Studio prototype treated as SEO corpus | Q1 content store + `seo.skill9`; `q15.fm8` |
| q9.cog2 | SEO/GEO | intent mapping | Search term, competitor, or URL must become target map | `getuai-plugin.md:11-20` | `rankncompare.md:53-56` | Sitemap generation used as intent research | Q1 crawler/search; `seo.skill7`/`seo.skill8` |
| q9.cog3 | SEO/GEO | E-E-A-T / vertical expertise | YMYL/legal claims require vertical authority | `lawyer_marketing.md:291-317` | `growth-engine.md:7-30` | Generic industry labels | `q13.f8`; `q14.m6`; `q15.fm2` |
| q9.cog4 | SEO/GEO | GEO vs SEO pivot | Visibility shifts to LLM answer ranking/sentiment | `LLMRush.md:7-14` | `rankncompare.md:134-149` | Treating sitemap/robots as GEO evaluator | Q1 GEO evaluator; `content.skill6`; `q15.fm7` |
| q9.cog5 | SEO/GEO | content velocity vs depth | Frequent recs compete with durable reviewed assets | `getuai-seo.md:101-106` | `growth-engine-legacy.md:16-22` | Docs-heavy runtime with no executable Core tree | `q1.trace8`; `q14.m2`/`q14.m5`; `q15.fm3` |
| q10.cog1 | Content | user journey mapping | Recipient/audience state drives draft and send | `getuai-email-2.0.md:70-118` | `gmi-prototype.md:7-54` | Local generation detached from outcome state | Q2 pipeline; `content.skill1`; `q15.fm8` |
| q10.cog2 | Content | content portfolio theory | Growth surface needs multiple media/content types | `openclaw-marketing.md:5104-5152`, `openclaw-marketing.md:6656-6716` | `getuai-email-2.0.md:70-73` | Email batch treated as whole content system | `content.skill7`/`content.skill8`; `q14.m3` deferral |
| q10.cog3 | Content | distribution over production | Draft value needs review/send/publish path | `getuai-email-2.0.md:111-118` | `gmi-prototype.md:50` | Content lands in local folders | Q2 review/send; `content.skill4`; `q15.fm6` |
| q10.cog4 | Content | ROI time window | Content must produce ranking/sentiment/outbound outcomes | `LLMRush.md:7-23` | `getuai-2.0.md:19-42` | Prototype UI with no metric loop | Q2 post-publish learning; `content.skill6`; `q14.m4` |
| q10.cog5 | Content | brand voice as forcing function | Tone/register constrained before send | `getuai-email-2.0.md:91-118` | `gmi-prototype.md:37-54` | Free-form prompt as brand system | `content.skill1` + review; `q15.fm6` |
| q11.cog1 | Ads | LTV/CAC discipline | Spend decision needs metrics and business value | `lawyer_marketing.md:291-304`, `getu_ads_v2.md:1048-1064` | `attribution_v2.md:117-119` | Spend optimized while identity missing | Q3 reporting/attribution; `ads.skill7`/`ads.skill8`; `q15.fm5` |
| q11.cog2 | Ads | pacing logic | Budget/geo/language targeting changes | `getu_ads_v2.md:1131-1149` | `getuai-ads.md:24-28` | Credentialed mutations assumed available | Q3 budget pacing; `ads.skill5`; `q15.fm4` |
| q11.cog3 | Ads | creative fatigue curves | RSA/ad creative needs performance refresh | `getu_ads_v2.md:630-704`, `getu_ads_v2.md:1066-1086` | `getuai-ads-data.md:216-250` | Aggregate rows replace ad-level diagnosis | Q3 anomaly input; `ads.skill4`; `q15.fm1` |
| q11.cog4 | Ads | attribution paradox | Better measurement raises session fragility | `attribution_v2.md:13-23` | `attribution_v2.md:151-186` | SDK install treated as solved attribution | Q3 attribution; `ads.skill8`; `q15.fm5` |
| q11.cog5 | Ads | kill-vs-scale criteria | Recommendation crosses into spend/write action | `lawyer_marketing.md:248-269` | `growth-engine-legacy.md:83-88` | Engines own writes or restart after stop | Q3 approval/kill-switch; `ads.skill2`/`ads.skill5`; `q15.fm6` |
| q12.cog1 | Social | platform-as-game-theory | Engagement depends on native community rules | `reddit-scount.md:108-181` | `openclaw-marketing.md:122-158` | Universal social adapter bypasses policy | Q4 Reddit/Gateway; `social.skill1`/`social.skill8`; `q15.fm6` |
| q12.cog2 | Social | algorithm preference modeling | Distribution is search/feed/reply/video result | `youtube-api-demo.md:48-54`, `openclaw-marketing.md:7392-7422` | `reddit-scount.md:141-181` | Search monitor treated as engagement engine | Q4 adapters; `social.skill3`/`social.skill5` |
| q12.cog3 | Social | community fit before brand voice | Reply voice needs topic/community context | `reddit-scount.md:108-139` | `openclaw-marketing.md:7392-7422` | Raw post before community-fit analysis | Q4 listen before post; `social.skill2`/`social.skill5`; `q15.fm6` |
| q12.cog4 | Social | viral mechanics | Post/reply/media affordances require monitor loop | `openclaw-marketing.md:7392-7422` | `youtube-api-demo.md:48-54` | Video search result treated as viral loop | Q4 post/monitor split; `q14.m5` |
| q12.cog5 | Social | automation visibility cost | Automation touches public/private channels | `openclaw-marketing.md:122-126`, `x-api-credit-monitor.md:7-17` | `openclaw-marketing.md:132-158` | Always-on assistant without visible guards | `social.skill8`/`social.skill4`; `q15.fm4`, `q15.fm6` |

Cognition synthesis: trigger discipline routes ranking, tone, spend, and community interpretation to domain-owned skills until the action crosses shared trust, credential, schedule, approval, ledger, or kill-switch contracts.

## Q13 - Shared Foundations

Decision rule: share tenant trust, credentials, schedules, ledgers, observability, LLM routing, approval, and governance when the component crosses tenant, money, secret, queue, audit, or operator-control boundaries. Keep domain-isolated when it encodes ranking logic, creative/tone judgment, platform API semantics, industry facts, content schema, or channel-specific kill criteria.

| row_id | foundation | shared_contract | corpus_evidence | domain_isolated_boundary | hooks_to_q14_q15 |
|---|---|---|---|---|---|
| q13.f1 | identity/session | Core validates tenant/user/session, issues request context, and keeps browser-facing auth out of engines. Version policy: token/context schema migrates in Core, not per engine. | `growth-engine-legacy.md:43-50`; `getuai-api.md:23-37`; `getuai-ui.md:18-32` | Domain repos may keep audience, campaign, or channel state, but not raw Logto/session ownership. | `q14.m1`, `q14.m3`, `q14.m4`; prevents `q15.fm1`, `q15.fm5` |
| q13.f2 | credentials/secrets | Credentials are stored centrally and leased/scoped to adapters; secrets never become prompt or artifact payload. Version policy: provider credential schema is additive and audited. | `growth-engine-legacy.md:64-88`; `getuai-ads.md:21-28`; `getuai-ads-sdk.md:7-12`; `x-api-credit-monitor.md:12-18` | Platform-specific OAuth/API SDK code stays in adapters. | `q14.m1`, `q14.m2`, `q14.m4`, `q14.m5`; prevents `q15.fm1`, `q15.fm4`, `q15.fm6` |
| q13.f3 | data/artifacts | Shared artifact ledger stores run inputs, generated assets, reports, citations, and replay pointers. Version policy: stable artifact IDs plus append-only metadata migrations. | `getuai-api.md:24-42`; `rankncompare.md:49-56`; `attribution_v2.md:13-16`; `gmi-prototype.md:14-50` | Domain schemas decide what rank report, draft, ad report, or social post means. | `q14.m1`, `q14.m2`, `q14.m3`, `q14.m4`; prevents `q15.fm3`, `q15.fm8`, `q15.fm9` |
| q13.f4 | schedules/queues | Core registers schedules, queues, retries, and terminal-stop semantics; engines expose idempotent units of work. Version policy: queue payloads get stable operation names and result envelopes. | `growth-engine-legacy.md:64-88`; `x-api-credit-monitor.md:72-104`; `openfang.md:39-70` | Domain cadence and trigger interpretation remain domain-owned. | `q14.m1`, `q14.m5`, `q14.m6`; prevents `q15.fm1`, `q15.fm3`, `q15.fm4` |
| q13.f5 | observability | Shared run events, request IDs, cost/usage, trace logs, and redaction policy. Version policy: observability fields are additive and PII-redacted before persistence. | `growth-engine-legacy.md:64-70`; `LLMRush.md:19-23`; `x-api-credit-monitor.md:7-17`; `attribution_v2.md:13-23` | Domain dashboards can define metrics, but trace/cost/event emission uses shared shape. | `q14.m1`, `q14.m4`, `q14.m6`; prevents `q15.fm3`, `q15.fm4`, `q15.fm5` |
| q13.f6 | LLM gateway | Shared model routing, prompt/cost guardrails, provider fallback, and response-envelope discipline. Version policy: gateway aliases and model contracts update with README/CLI/provider factory together. | `getuai-seo.md:78-91`; `getuai-email-2.0.md:111-114`; `LLMRush.md:7-14`; `reddit-scount.md:233-239` | Prompt templates, tone, ranking interpretation, and retrieval corpus stay domain-specific. | `q14.m2`, `q14.m3`, `q14.m6`; prevents `q15.fm7`, `q15.fm8` |
| q13.f7 | human-in-loop console | Shared review, approval, override, kill-switch, and action ledger for writes. Version policy: read/write permissions and terminal stop reasons are explicit. | `growth-engine-legacy.md:83-88`; `lawyer_marketing.md:248-269`; `openclaw-marketing.md:122-126` | Domain UIs can propose actions, but approvals and stop states are Core-owned. | `q14.m1`, `q14.m5`, `q14.m6`; prevents `q15.fm1`, `q15.fm3`, `q15.fm6` |
| q13.f8 | repo-template governance | Shared AGENTS/CLAUDE rules, skill installation, CI gates, and version drift checks. Version policy: template version is tracked and re-apply is idempotent. | `optiminds-repo-template.md:9-63`; `optiminds-org-config.md:7-47`; `lawyer_finder.md:18-72` | Product/domain business logic and vertical facts stay in consumer repos. | `q14.m1`, `q14.m6`; prevents `q15.fm2`, `q15.fm3`, `q15.fm9` |

Q13 synthesis: the shared layer is the narrow set of contracts whose breakage corrupts multiple domains: tenant trust, credentials, artifacts, schedules, observability, model routing, approvals, and governance.

## Q14 - Build Sequence

| row_id | milestone | scope | dependencies | done_criteria | next_trigger | deferrals |
|---|---|---|---|---|---|---|
| q14.m1 | Day-1 | Core tenant/session/artifact/source/approval skeleton for Q13 foundations and `q15.fm1`/`q15.fm3` prevention | `q13.f1`, `q13.f2`, `q13.f3`, `q13.f4`, `q13.f5`, `q13.f7`, `q13.f8` | target/session/artifact/action records persist; no run leakage; terminal stop reason explicit | first durable tool | ads/social writes; rich media; autonomous schedules beyond smoke |
| q14.m2 | Week-1 | SEO/GEO read lane: Q1 crawl/search/keyword/sitemap via `seo.skill6`-`seo.skill9` | `q13.f2`, `q13.f3`, `q13.f5`, `q13.f6`, `q13.f7` | outputs stored; rank source declared; sitemap exists; evaluator boundary named | recurring/publish request | autopublish; GEO treated as sitemap output |
| q14.m3 | Week-2 | Content lane: Q2 templates/import/draft/SMTP/retrieval via `content.skill1`-`content.skill5` | `q13.f1`, `q13.f2`, `q13.f3`, `q13.f6`, `q13.f7` plus SEO store | variables validate; drafts generated; citations or recipient grounding present; review before send | outbound metric need | rich media; multilingual variants; fully automated send |
| q14.m4 | Week-4 | Ads read + attribution via `ads.skill7`/`ads.skill8`; no spend mutation | `q13.f1`, `q13.f2`, `q13.f3`, `q13.f5` plus campaign IDs | reports + conversion events visible; read-only analyst emits kill-vs-scale recs | repeated budget recs | budget mutation; A/B tests; autonomous bidding |
| q14.m5 | Week-8 | Controlled writes across domains using Q3/Q4 approval and moderation guardrails | `q13.f2`, `q13.f3`, `q13.f4`, `q13.f5`, `q13.f7`; read evidence from `q14.m2`-`q14.m4` | every write has ledger, envelope, quota/credit monitor, and rollback or pause path | stable weekly outcomes | full optimizer; cross-platform rewrite marketplace |
| q14.m6 | Month-3 | OODA orchestration + industry packs, especially `q9.cog3` vertical expertise | `q13.f1`, `q13.f3`, `q13.f4`, `q13.f5`, `q13.f6`, `q13.f7`, `q13.f8`; all lanes | weekly observe-plan-approve-execute-review works; vertical pack has evidence and kill criteria | tenant/industry scale | Temporal marketplace; autonomous spend; generic industry labels |

Evidence shape: thin prototype `getuai-2.0.md:19-42`, MVP route hardening `getuai-mvp.md:9-76`, production refactor `attribution_v2.md:16-23`, vertical cases `lawyer_finder.md:11-16`, `cuilawgroup.md:10-27`, backend-skeleton-first `growth-engine.md:8-12`. Deferrals are failure-informed: no autopublish before `q14.m2`, no budget mutation or A/B before `q14.m4`, and no autonomous spend before `q14.m6`.

## Q15 - Failure Modes

| row_id | failure_mode | domains | count | cause | early symptom | prophylactic | evidence_pair |
|---|---|---|---:|---|---|---|---|
| q15.fm1 | engines own platform facts | SEO/Ads/Social | 3 | scattered identity/creds/schedules | raw tokens/own cron | `q13.f1`, `q13.f2`, `q13.f4`, `q13.f7`: Core facts/context leases and action ledger | `growth-engine-legacy.md:43-50`, `growth-engine-legacy.md:83-88` |
| q15.fm2 | legacy scaffolding import | all | 4 | copying attempts | stale paths | `q13.f8` plus `q9.cog3`: greenfield contracts and vertical specificity | `growth-engine.md:69-152` |
| q15.fm3 | docs without runtime | all | 4 | design outruns core | no `core/` tree | `q13.f3`, `q13.f4`, `q13.f5`, `q13.f7`, `q13.f8` and Day-1 skeleton `q14.m1` | `growth-engine-legacy.md:16-22` |
| q15.fm4 | credential drift | SEO/Ads/Social | 3 | auth outside action layer | API/re-login errors | `q13.f2`, `q13.f4`, `q13.f5`: leases, schedules, monitors; `social.skill4` | `getuai-ads.md:24-28`, `x-api-credit-monitor.md:13-17` |
| q15.fm5 | attribution/session breakage | Ads/Content | 2 | cookie/user rotation | missing lead rows | `q13.f1`, `q13.f3`, `q13.f5`: SDK domain/session tests and artifact traces; `ads.skill8` | `attribution_v2.md:117-186` |
| q15.fm6 | writes without approval | SEO/Ads/Social | 3 | mixed read/write skills | agents mutate while analyzing | `q13.f2`, `q13.f3`, `q13.f7`: read-only diagnosis + ledger; `q11.cog5`, `q12.cog1`, `q12.cog5` guard public actions | `lawyer_marketing.md:248-269`, `growth-engine-legacy.md:84` |
| q15.fm7 | static publisher as GEO evaluator | SEO/GEO | 1 | indexing confused with LLM visibility | sitemap but no LLM rank | `q13.f3`, `q13.f5`, `q13.f6`: LLMRush sensor and evaluator artifacts; `content.skill6` | `rankncompare.md:134-149`, `LLMRush.md:7-14` |
| q15.fm8 | prototype-local artifact store | Content/Social | 2 | local media only | no campaign/outcome link | `q13.f3`, `q13.f6`, `q13.f7`: Core artifact store, gateway routing, review ledger | `gmi-prototype.md:14`, `gmi-prototype.md:50`, `getuai-api.md:24-40` |
| q15.fm9 | API prefix mismatch | shared | 2 | local/prod route drift | wrong backend path | `q13.f3`, `q13.f5`, `q13.f8`: API_PREFIX/proxy contract, observability, template governance | `getuai-mvp.md:9-76` |

ID lock: `q15.fm1`-`q15.fm9` are canonical. Every prophylactic should cite the relevant `q13.f*` foundation plus the cognition row that prevents misapplication.

## Benchmark Answers

Machine-readable benchmark answers are emitted in the top-level `benchmark_answers` JSON array. Q1/Q3 carry component trace locks; Q2/Q4 retain trace tables; Q5-Q8 retain 34 skill rows; Q9-Q12 retain cognition evidence pairs; Q13 carries `q13.f1`-`q13.f8`; Q14 carries `q14.m1`-`q14.m6`; Q15 carries `q15.fm1`-`q15.fm9`. The benchmark arrays below restore direct file:line anchors on every answer.
