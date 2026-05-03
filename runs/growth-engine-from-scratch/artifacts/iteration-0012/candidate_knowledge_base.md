# Knowledge Base

Topic: Growth Engine From Scratch - architecture, skills, cognition from getuai corpus
Iteration: 15 direct architecture-disagreement evidence patched

## Evidence And Stable IDs
Direct citations are `repo.md:line-line` from `runs/growth-engine-from-scratch/sources/_raw/`. Stable IDs: `q1.trace*`-`q4.trace*`, `seo.skill*`, `content.skill*`, `ads.skill*`, `social.skill*`, `q9.cog*`-`q12.cog*`, `q13.f1`-`q13.f8`, `q14.m1`-`q14.m6`, `q15.fm1`-`q15.fm9`.

## Q1 - SEO/GEO Architecture
Converged design: crawler/search adapters -> ranking sensors -> content store/generator -> publisher/evaluator -> Core approval, ledger, credentials, schedules, kill-switch. Packaging disagreement is direct: `getuai-seo.md:7-11` declares UI/MCP/AI layers and `getuai-seo.md:52-97` says three components run separately; `rankncompare.md:128-149` is a static product/category content store; `growth-engine-legacy.md:45-49` requires Browser -> Core only and Core ownership of identity, tenancy, credentials, runs, artifacts, actions, schedules, observability.

| step | trace |
|---|---|
| q1.trace1 | URL/site -> site-structure analyzer -> crawl/meta/link artifact (`getuai-plugin.md:11-14`) |
| q1.trace2 | query/domain -> search/competitor/keyword tools -> SERP/intent state (`getuai-plugin.md:16-20`) |
| q1.trace3 | term/company -> SEO keyword/rank metrics -> ranking signal (`getuai-seo.md:101-106`) |
| q1.trace4 | term/company -> LLMRush model rank/sentiment -> GEO signal (`LLMRush.md:7-14`) |
| q1.trace5 | category/product JSON -> content store -> publishable corpus (`rankncompare.md:128-149`) |
| q1.trace6 | stored routes -> sitemap/robots publisher -> crawler surface (`rankncompare.md:53-56`) |
| q1.trace7 | publish/check request -> Core approval/ledger/kill-switch -> audit trail (`growth-engine-legacy.md:83-88`) |
| q1.trace8 | page+keyword gap -> optimization generator -> human review candidate (`getuai-seo.md:103-106`) |

## Q2 - Content Writing Architecture
Pipeline: campaign/entity facts -> ideation/outline through prompt variables -> recipient import -> LLM draft -> human edit/review -> SMTP/publish -> post-publish metric learning. Load-bearing choices: style-guide injection, recipient schema, SMTP test, review gate, artifact/session store (`getuai-email-2.0.md:70-118`, `getuai-api.md:24-40`). Stylistic choices: table UI, frontend stack, file format.

| step | trace |
|---|---|
| q2.trace1 | prompt variables -> reusable ideation/outline contract (`getuai-email-2.0.md:91-94`) |
| q2.trace2 | CSV fields -> recipient records -> personalization input (`getuai-email-2.0.md:101-104`) |
| q2.trace3 | batch+prompt+recipient -> LLM -> drafts (`getuai-email-2.0.md:111-114`) |
| q2.trace4 | drafts -> human review -> sendable batch (`getuai-email-2.0.md:111-118`) |
| q2.trace5 | SMTP+batch -> test/send -> sent/failed status (`getuai-email-2.0.md:96-99`) |
| q2.trace6 | image/text/company artifacts -> API store -> replay state (`getuai-api.md:24-40`) |
| q2.trace7 | factual query -> retrieval-grounded cited copy (`reddit-scount.md:233-239`) |

## Q3 - Ads Architecture
Closed loop: campaign feed -> bidding/budget candidates -> reporting -> attribution -> anomaly/pacing -> approved optimization. Platform-bound: Google Ads operations, credentials, mutations (`getu_ads_v2.md:9-67`, `getu_ads_v2.md:1010-1017`). Platform-agnostic: ResultEnvelope, reporting lake, attribution event model, anomaly detection, pacing, approval ledger, kill criteria (`getuai-ads-data.md:216-250`, `attribution_v2.md:13-16`, `lawyer_marketing.md:248-269`).

| step | trace |
|---|---|
| q3.trace1 | credentials+brief -> Ads UI/MCP/AI workbench (`getuai-ads.md:7-11`) |
| q3.trace2 | op JSON stdin/file -> Google Ads CLI -> ResultEnvelope (`getu_ads_v2.md:9-67`) |
| q3.trace3 | campaign/adgroup/keyword/RSA/budget -> 38 ops -> mutation/list (`getu_ads_v2.md:1010-1017`) |
| q3.trace4 | date/GAQL -> reports -> optimization signal (`getu_ads_v2.md:1048-1123`) |
| q3.trace5 | SDK+UTM+session -> ingress/consumer -> conversion/lead score (`attribution_v2.md:13-16`) |
| q3.trace6 | Google/Meta/TikTok rows -> data platform -> anomaly/trend candidate (`getuai-ads-data.md:216-250`) |
| q3.trace7 | budget rec -> read/write approval -> action log (`lawyer_marketing.md:248-269`) |
| q3.trace8 | unsafe write/lost attribution -> Core kill-switch (`growth-engine-legacy.md:83-88`) |

## Q4 - Social Architecture
Decompose into listen, post, schedule, engage, monitor behind a Gateway control plane plus per-platform adapters. Reddit listen/discovery (`reddit-scount.md:108-181`), YouTube monitor (`youtube-api-demo.md:48-54`), X post/reply/search (`openclaw-marketing.md:7392-7422`), Gateway inbox/routing (`openclaw-marketing.md:132-158`), credit/rate monitor (`x-api-credit-monitor.md:7-17`, `x-api-credit-monitor.md:72-104`), moderation gate (`openclaw-marketing.md:122-126`). Reject a universal social adapter: Discord attempts flat `message` but still requires `channel: discord` plus per-channel action gates (`openclaw-marketing.md:2638-2646`); Slack remains a separate configured tool with `channelId`/`messageId` (`openclaw-marketing.md:6310-6330`); DM policy/allowFrom is channel-specific (`openclaw-marketing.md:122-126`).

| step | trace |
|---|---|
| q4.trace1 | company URL -> Reddit analysis -> keywords/pain/subreddits (`reddit-scount.md:108-139`) |
| q4.trace2 | analysis+index -> Reddit discovery -> posts/comments (`reddit-scount.md:141-181`) |
| q4.trace3 | query+maxResults -> YouTube adapter -> monitor candidates (`youtube-api-demo.md:48-54`) |
| q4.trace4 | text/post_id/query/media -> X side effect (`openclaw-marketing.md:7392-7422`) |
| q4.trace5 | channel message -> Gateway route; not universal due Discord gates (`openclaw-marketing.md:132-158`, `openclaw-marketing.md:2638-2646`) |
| q4.trace6 | schedule+Chrome session+threshold -> heartbeat/alert quota output (`x-api-credit-monitor.md:72-104`) |
| q4.trace7 | generated reply -> DM/channel gate -> moderated automation (`openclaw-marketing.md:122-126`, `openclaw-marketing.md:6310-6330`) |

## Q5-Q8 Skill Catalog
| row_id | domain | skill | repo/path | invocation | input -> output | state | maintenance |
|---|---|---|---|---|---|---|---|
| seo.skill1 | SEO | seo-campaign-console | `getuai-seo.md:93-106` | web+AI | campaign/files -> recs/metrics | session/API | duplicate ads console |
| seo.skill2 | SEO | keyword-research-tracking | `getuai-seo.md:101-102` | MCP/API | seed/site -> keywords/ranks | campaign | plugin overlap |
| seo.skill3 | SEO | content-optimization | `getuai-seo.md:103` | AI rec | page+keyword -> edits | artifact | prompt drift |
| seo.skill4 | SEO | backlink-analysis | `getuai-seo.md:104` | MCP/API | domain -> backlinks | campaign | unique sample |
| seo.skill5 | SEO | competitor-analysis | `getuai-competitor-analysis.md:7-21` | MCP | company/query -> competitors | DB/files | plugin canonical |
| seo.skill6 | SEO | site-structure-analyzer | `getuai-plugin.md:11-14` | FastAPI | URL -> crawl/meta/links | logs | fetch retries |
| seo.skill7 | SEO | google-search-analyzer | `getuai-plugin.md:16` | FastAPI | query -> SERP insights | logs | Google dep |
| seo.skill8 | SEO | keyword-clustering | `getuai-plugin.md:20` | FastAPI | keywords -> clusters | stateless | model retry |
| seo.skill9 | SEO | sitemap-robots-generator | `rankncompare.md:53-56`, `rankncompare.md:134-149` | build/route | product/category -> sitemap/robots | JSON/static | rebuild on schema |
| content.skill1 | Content | campaign-prompt-template | `getuai-email-2.0.md:91-94` | UI | placeholders -> prompt | campaign DB | register drift |
| content.skill2 | Content | personalized-email-draft | `getuai-email-2.0.md:111-114` | batch | recipient+prompt -> draft | batch DB | recipient grounding |
| content.skill3 | Content | recipient-import | `getuai-email-2.0.md:101-104` | API/CSV | CSV -> recipients | MySQL | schema validate |
| content.skill4 | Content | smtp-test-and-send | `getuai-email-2.0.md:96-99`, `getuai-email-2.0.md:116-118` | UI/API | SMTP+batch -> send status | SMTP DB | review gate |
| content.skill5 | Content | cited-websearch-copy | `reddit-scount.md:233-239` | service | query -> cited answer | logs | hallucination guard |
| content.skill6 | Content | multi-model-rank-summary | `LLMRush.md:7-14` | web/API | term/URL -> rank/sentiment | history | GEO drift |
| content.skill7 | Content | image-text-composer | `openclaw-marketing.md:5104-5152` | CLI | prompt+images -> asset | files | path mapping |
| content.skill8 | Content | summarizer-transcriber | `openclaw-marketing.md:6656-6716` | CLI | URL/file -> summary | files/logs | provider fallback |
| ads.skill1 | Ads | google-ads-cli | `getu_ads_v2.md:9-67` | CLI stdin/file | op JSON -> envelope | API effects | Google-bound |
| ads.skill2 | Ads | campaign-management | `getu_ads_v2.md:1010` | CLI | campaign -> create/list/update | Google Ads | policy kill |
| ads.skill3 | Ads | keyword-management | `getu_ads_v2.md:1012`, `getu_ads_v2.md:923-950` | CLI | ad_group+keywords -> criteria | Google Ads | match validate |
| ads.skill4 | Ads | rsa-creative-management | `getu_ads_v2.md:1013`, `getu_ads_v2.md:630-704` | CLI | creative/url -> RSA | Google Ads | fatigue reports |
| ads.skill5 | Ads | budget-targeting | `getu_ads_v2.md:1014`, `getu_ads_v2.md:1131-1149` | CLI | campaign/geo/lang -> budget/criteria | Google Ads | pacing guard |
| ads.skill6 | Ads | composite-campaign-build | `getu_ads_v2.md:630-704` | CLI | campaign tree -> full structure | Google Ads | retry via envelope |
| ads.skill7 | Ads | reporting-gaql | `getu_ads_v2.md:1048-1123` | CLI | date/query -> metrics | report | agnostic envelope |
| ads.skill8 | Ads | attribution-ingest | `attribution_v2.md:13-16` | SDK+API | UTM/events -> events/leads/scores | tables/PubSub | conversion backbone |
| ads.skill9 | Ads | platform-credential-sdk | `getuai-ads-sdk.md:7-12`, `getuai-ads-sdk.md:146-161` | SDK | user/token/platform -> credentials | Redis/API | kill if unavailable |
| social.skill1 | Social | reddit-opportunity-analysis | `reddit-scount.md:108-139` | API | URL -> keywords/pain | MySQL | Reddit-bound |
| social.skill2 | Social | reddit-discovery | `reddit-scount.md:141-181` | API | analysis+index -> posts/comments | MySQL/cache | topic selection |
| social.skill3 | Social | youtube-search | `youtube-api-demo.md:48-54` | HTTP | query/max -> videos | stateless | quota/API risk |
| social.skill4 | Social | x-credit-monitor | `x-api-credit-monitor.md:7-17`, `x-api-credit-monitor.md:72-104` | launchd | session/threshold -> Lark alert | logs/env | re-login monitor |
| social.skill5 | Social | x-post-reply-search | `openclaw-marketing.md:7392-7422` | CLI | text/id/query/media -> post/reply/search | X effects | API break risk |
| social.skill6 | Social | multi-channel-inbox | `openclaw-marketing.md:132-158` | Gateway | channel/session -> routed msg | gateway store | adapter abstraction |
| social.skill7 | Social | slack-actions | `openclaw-marketing.md:6314-6339` | tool | channel/message -> reaction/send/edit | Slack effects | per-platform semantics |
| social.skill8 | Social | channel-gating | `openclaw-marketing.md:122-126` | config | dmPolicy/allowFrom -> allow/deny | config | moderation guard |

## Q9-Q12 Cognition
| row_id | model | worked | failed | anti-pattern/hook |
|---|---|---|---|---|
| q9.cog1 | topical authority | `rankncompare.md:128-187` | `getuai-2.0.md:19-42` | thin prototype as corpus; `q15.fm8` |
| q9.cog2 | intent mapping | `getuai-plugin.md:11-20` | `rankncompare.md:53-56` | sitemap as discovery |
| q9.cog3 | E-E-A-T vertical expertise | `lawyer_marketing.md:291-317` | `growth-engine.md:7-13`, `growth-engine.md:23-30` | generic industry labels; `q13.f8` |
| q9.cog4 | GEO vs SEO pivot | `LLMRush.md:7-14` | `rankncompare.md:134-149` | sitemap as GEO evaluator |
| q9.cog5 | content velocity vs depth | `getuai-seo.md:101-106` | `growth-engine-legacy.md:16-22` | docs without runtime |
| q10.cog1 | user journey mapping | `getuai-email-2.0.md:70-118` | `gmi-prototype.md:7-54` | no campaign/outcome link |
| q10.cog2 | content portfolio | `openclaw-marketing.md:5104-5152`, `openclaw-marketing.md:6656-6716` | `getuai-email-2.0.md:70-73` | email-only system |
| q10.cog3 | distribution over production | `getuai-email-2.0.md:111-118` | `gmi-prototype.md:50` | local files without ledger |
| q10.cog4 | ROI window | `LLMRush.md:7-23` | `getuai-2.0.md:19-42` | no metric loop |
| q10.cog5 | brand voice forcing function | `getuai-email-2.0.md:91-118` | `gmi-prototype.md:37-54` | free prompt as brand system |
| q11.cog1 | LTV/CAC | `lawyer_marketing.md:291-304`, `getu_ads_v2.md:1048-1064` | `attribution_v2.md:117-119` | spend without identity/session |
| q11.cog2 | pacing | `getu_ads_v2.md:1131-1149` | `getuai-ads.md:24-28` | mutations assume credentials |
| q11.cog3 | creative fatigue | `getu_ads_v2.md:630-704`, `getu_ads_v2.md:1066-1086` | `getuai-ads-data.md:216-250` | aggregate rows hide ad-level issue |
| q11.cog4 | attribution paradox | `attribution_v2.md:13-23` | `attribution_v2.md:151-186` | SDK install considered done |
| q11.cog5 | kill-vs-scale | `lawyer_marketing.md:248-269` | `growth-engine-legacy.md:83-88` | engine-owned writes |
| q12.cog1 | platform game theory | `reddit-scount.md:108-181` | `openclaw-marketing.md:122-126`, `openclaw-marketing.md:2638-2646`, `openclaw-marketing.md:6310-6330` | universal social adapter |
| q12.cog2 | algorithm preference | `youtube-api-demo.md:48-54`, `openclaw-marketing.md:7392-7422` | `reddit-scount.md:141-181` | search monitor as engagement |
| q12.cog3 | community fit before voice | `reddit-scount.md:108-139` | `openclaw-marketing.md:7392-7422` | raw X posting before fit |
| q12.cog4 | viral mechanics | `openclaw-marketing.md:7392-7422` | `youtube-api-demo.md:48-54` | video search as viral loop |
| q12.cog5 | automation visibility cost | `openclaw-marketing.md:122-126`, `x-api-credit-monitor.md:7-17` | `openclaw-marketing.md:132-158` | always-on assistant without quota/moderation |

## Q13 - Shared Foundations
Decision rule: share components crossing tenant, money, secret, queue, audit, operator-control, or version-governance boundaries; isolate ranking logic, tone/creative judgment, platform API semantics, vertical facts, content schema, and channel-specific kill criteria.

| row_id | foundation | shared_contract | corpus_evidence | domain_isolated_boundary | hooks_to_q14_q15 |
|---|---|---|---|---|---|
| q13.f1 | identity/session | Core validates tenant/user/session; token/context schema migrates in Core | `growth-engine-legacy.md:45-49`; `getuai-api.md:23-37`; `getuai-ui.md:11-20`; `getuai-ui.md:139-161` | audience/campaign/channel state only | `q14.m1`,`q14.m3`,`q14.m4`; prevents `q15.fm1`,`q15.fm5` |
| q13.f2 | credentials/secrets | central storage, scoped leases, audited additive schema | `growth-engine-legacy.md:64-88`; `getuai-ads.md:21-28`; `getuai-ads-sdk.md:7-12`; `x-api-credit-monitor.md:12-18` | platform SDK/OAuth adapters | `q14.m1`,`q14.m2`,`q14.m4`,`q14.m5`; prevents `q15.fm1`,`q15.fm4`,`q15.fm6` |
| q13.f3 | data/artifacts | artifact ledger for inputs/assets/reports/citations/replay | `getuai-api.md:24-42`; `rankncompare.md:49-56`; `attribution_v2.md:13-16`; `gmi-prototype.md:14-50` | rank/draft/ad/social schemas | `q14.m1`-`q14.m4`; prevents `q15.fm3`,`q15.fm8`,`q15.fm9` |
| q13.f4 | schedules/queues | registered schedules, retries, terminal stops, stable operation names | `growth-engine-legacy.md:64-88`; `x-api-credit-monitor.md:72-104`; `openfang.md:44-78` | domain cadence interpretation | `q14.m1`,`q14.m5`,`q14.m6`; prevents `q15.fm1`,`q15.fm3`,`q15.fm4` |
| q13.f5 | observability | run events, request IDs, cost/usage, trace logs, redaction | `growth-engine-legacy.md:64-70`; `LLMRush.md:19-23`; `x-api-credit-monitor.md:7-17`; `attribution_v2.md:13-23` | metric dashboards | `q14.m1`,`q14.m4`,`q14.m6`; prevents `q15.fm3`-`q15.fm5` |
| q13.f6 | LLM gateway | model routing, prompt/cost guardrails, fallback, envelopes | `getuai-seo.md:78-91`; `getuai-email-2.0.md:111-114`; `LLMRush.md:7-14`; `reddit-scount.md:233-239` | prompt templates and corpora | `q14.m2`,`q14.m3`,`q14.m6`; prevents `q15.fm7`,`q15.fm8` |
| q13.f7 | human-in-loop console | review, approval, override, action gates, kill-switch, ledger | `growth-engine-legacy.md:83-88`; `lawyer_marketing.md:248-269`; `openclaw-marketing.md:122-126`; `openclaw-marketing.md:2638-2646` | domain UIs propose only | `q14.m1`,`q14.m5`,`q14.m6`; prevents `q15.fm1`,`q15.fm3`,`q15.fm6` |
| q13.f8 | repo-template governance | AGENTS/CLAUDE, skills, CI gates, version drift, idempotent apply | `optiminds-repo-template.md:9-63`; `optiminds-org-config.md:9-53`; `lawyer_finder.md:69-115` | product logic and vertical facts | `q14.m1`,`q14.m6`; prevents `q15.fm2`,`q15.fm3`,`q15.fm9` |

## Q14 - Build Sequence
| row_id | milestone | scope | dependencies | done_criteria | next_trigger | deferrals |
|---|---|---|---|---|---|---|
| q14.m1 | Day-1 | Core tenant/session/artifact/source/approval skeleton | `q13.f1`,`q13.f2`,`q13.f3`,`q13.f4`,`q13.f5`,`q13.f7`,`q13.f8` | target/session/artifact/action persist; no run leakage; terminal stop explicit | first durable tool | ads/social writes; rich media; autonomous schedules |
| q14.m2 | Week-1 | SEO/GEO read lane via `seo.skill6`-`seo.skill9` | `q13.f2`,`q13.f3`,`q13.f5`,`q13.f6`,`q13.f7` | outputs stored; rank source declared; sitemap exists; evaluator boundary named | recurring/publish request | autopublish; GEO as sitemap |
| q14.m3 | Week-2 | Content lane via `content.skill1`-`content.skill5` | `q13.f1`,`q13.f2`,`q13.f3`,`q13.f6`,`q13.f7` | variables validate; drafts generated; grounding/citations; review before send | outbound metric need | rich media; multilingual; automated send |
| q14.m4 | Week-4 | Ads read + attribution via `ads.skill7`,`ads.skill8` | `q13.f1`,`q13.f2`,`q13.f3`,`q13.f5` | reports + conversion events visible; read-only kill-vs-scale recs | repeated budget recs | budget mutation; A/B; autonomous bidding |
| q14.m5 | Week-8 | controlled writes with approval/moderation | `q13.f2`,`q13.f3`,`q13.f4`,`q13.f5`,`q13.f7`; evidence from m2-m4 | every write has ledger, envelope, quota monitor, rollback/pause | stable weekly outcomes | full optimizer; rewrite marketplace |
| q14.m6 | Month-3 | OODA orchestration + industry packs | `q13.f1`,`q13.f3`,`q13.f4`,`q13.f5`,`q13.f6`,`q13.f7`,`q13.f8`; all lanes | weekly observe-plan-approve-execute-review; vertical pack evidence+kill criteria | tenant/industry scale | Temporal marketplace; autonomous spend; generic industry labels |
Evidence: prototype-to-MVP route hardening and backend skeleton (`getuai-2.0.md:19-42`, `getuai-mvp.md:9-76`, `attribution_v2.md:16-23`, `lawyer_finder.md:11-16`, `cuilawgroup.md:10-27`, `growth-engine.md:8-12`).

## Q15 - Failure Modes
| row_id | failure_mode | domains | count | cause | early symptom | prophylactic | evidence_pair |
|---|---|---|---:|---|---|---|---|
| q15.fm1 | engines own platform facts | SEO/Ads/Social | 3 | scattered identity/creds/schedules | raw tokens/own cron | `q13.f1`,`q13.f2`,`q13.f4`,`q13.f7` | `growth-engine-legacy.md:43-50`, `growth-engine-legacy.md:83-88` |
| q15.fm2 | legacy scaffolding import | all | 4 | copying attempts | stale paths | `q13.f8` + `q9.cog3` | `growth-engine.md:69-152` |
| q15.fm3 | docs without runtime | all | 4 | design outruns core | no `core/` tree | `q13.f3`,`q13.f4`,`q13.f5`,`q13.f7`,`q13.f8`; `q14.m1` | `growth-engine-legacy.md:16-22` |
| q15.fm4 | credential drift | SEO/Ads/Social | 3 | auth outside action layer | API/re-login errors | `q13.f2`,`q13.f4`,`q13.f5`; `social.skill4` | `getuai-ads.md:24-28`, `x-api-credit-monitor.md:13-17` |
| q15.fm5 | attribution/session breakage | Ads/Content | 2 | cookie/user rotation | missing lead rows | `q13.f1`,`q13.f3`,`q13.f5`; `ads.skill8` | `attribution_v2.md:117-186` |
| q15.fm6 | writes without approval | SEO/Ads/Social | 3 | mixed read/write skills | agents mutate while analyzing | `q13.f2`,`q13.f3`,`q13.f7`; `q11.cog5`,`q12.cog1`,`q12.cog5` | `lawyer_marketing.md:248-269`, `growth-engine-legacy.md:84` |
| q15.fm7 | static publisher as GEO evaluator | SEO/GEO | 1 | indexing confused with LLM visibility | sitemap but no LLM rank | `q13.f3`,`q13.f5`,`q13.f6`; `content.skill6` | `rankncompare.md:134-149`, `LLMRush.md:7-14` |
| q15.fm8 | prototype-local artifact store | Content/Social | 2 | local media only | no campaign/outcome link | `q13.f3`,`q13.f6`,`q13.f7` | `gmi-prototype.md:14`, `gmi-prototype.md:50`, `getuai-api.md:24-40` |
| q15.fm9 | API prefix mismatch | shared | 2 | local/prod route drift | wrong backend path | `q13.f3`,`q13.f5`,`q13.f8` | `getuai-mvp.md:9-76` |
