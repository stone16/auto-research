# Repo: getu_ads_v2

## README.md
```markdown
# getu_ads_v2
getu ads v2

```

## skills/google-ads-cli/SKILL.md
```markdown
---
name: google-ads-cli
description: >
  Google Ads Search Campaign CLI for automated campaign management via shell commands.
  Provides 38 operations covering campaigns, ad groups, keywords, RSA ads, budgets, criteria,
  composite creation, reporting, and GAQL query building/validation/execution.
  Use when an agent needs to create/update/list/remove Google Ads resources, run performance
  reports, build full campaign structures end-to-end, discover API fields/resources,
  programmatically construct GAQL queries, or validate and execute arbitrary GAQL.
  Triggers on: google ads, create campaign, manage ads, ad group, keyword management,
  RSA ad, budget update, campaign report, search terms, GAQL query, GAQL build, GAQL validate,
  field discovery, resource discovery, composite create, google ads cli, exec run operation.
---

# Google Ads CLI

A standalone CLI for managing Google Ads Search campaigns. Designed for agent automation
via a unified `exec run` interface that accepts JSON payloads and returns structured JSON.

## Invocation

```bash
echo '<json_payload>' | python -m google_ads_cli exec run \
  --operation <operation_name> --stdin --compact \
  -c <path_to>/config.yaml
```

Or with a file:

```bash
python -m google_ads_cli exec run \
  --operation <operation_name> -f payload.json --compact \
  -c <path_to>/config.yaml
```

### Key Flags

| Flag | Description |
|------|-------------|
| `--operation` | Operation identifier (e.g. `search.campaign.create`) |
| `--stdin` | Read JSON payload from stdin |
| `-f, --file` | Read payload from JSON/YAML file |
| `-c, --config` | Path to config.yaml with credentials |
| `--compact` | Single-line JSON output (recommended for agents) |
| `--format` | Output format: `json` (default) or `yaml` |
| `-o, --output` | Write output to file instead of stdout |

### Response Format

All operations return a `ResultEnvelope`:

```json
{
  "success": true,
  "command": "exec search.campaign.list",
  "result": { ... },
  "elapsed_ms": 2239.9
}
```

On failure: `success: false`, `errors: [...]`, exit code `1`.

### Error Discovery

Pass an unknown operation to list all available operations:

```bash
echo '{}' | python -m google_ads_cli exec run --operation help --stdin --compact -c config.yaml
```

## Available Operations (38)

| Scenario | Ops | Detail | Key operations |
|----------|-----|--------|----------------|
| Campaign Management | 6 | [campaign.md](references/campaign.md) | `search.campaign.create`, `list`, `find`, `update`, `update_bidding`, `copy` |
| Ad Group Management | 5 | [ad_group.md](references/ad_group.md) | `search.ad_group.create`, `list`, `find`, `update_status`, `remove` |
| Keyword Management | 3 | [keyword.md](references/keyword.md) | `search.keyword.add`, `list`, `remove` |
| Ad / RSA Creative | 7 | [ad.md](references/ad.md) | `search.ad.create_rsa`, `get_rsa`, `update_rsa`, `update_status`, `list`, `remove`, `copy_rsa` |
| Targeting & Budget | 5 | [targeting.md](references/targeting.md) | `search.budget.update`, `search.criteria.add`, `list`, `remove`, `add_negatives` |
| Composite Build | 2 | [composite.md](references/composite.md) | `search.composite.create_full`, `create_groups` |
| Reporting | 4 | [report.md](references/report.md) | `report.campaign`, `ad`, `search_terms`, `gaql` |
| GAQL Builder | 6 | [gaql.md](references/gaql.md) | `gaql.resources`, `fields`, `field`, `build`, `validate`, `run` |

Click the **Detail** link for payload schemas and examples of each operation.
For a quick decision guide, see [references/operations.md](references/operations.md).

## Quick Examples

### List enabled campaigns

```bash
echo '{"campaign_type":"SEARCH","status_filter":"ENABLED"}' | \
  python -m google_ads_cli exec run --operation search.campaign.list --stdin --compact -c config.yaml
```

### Create a full campaign structure in one shot

```bash
python -m google_ads_cli exec run \
  --operation search.composite.create_full -f full_campaign.json --compact -c config.yaml
```

### Get campaign performance report

```bash
echo '{"date_range":"LAST_7_DAYS"}' | \
  python -m google_ads_cli exec run --operation report.campaign --stdin --compact -c config.yaml
```

### Run custom GAQL query

```bash
echo '{"query":"SELECT campaign.id, campaign.name FROM campaign WHERE campaign.status = '\''ENABLED'\'' LIMIT 10"}' | \
  python -m google_ads_cli exec run --operation report.gaql --stdin --compact -c config.yaml
```

### Build and execute GAQL programmatically

```bash
echo '{"resource":"campaign","fields":["campaign.id","campaign.name","metrics.clicks"],"conditions":["campaign.status = '\''ENABLED'\''"],"order_by":"metrics.clicks DESC","limit":10,"date_range":"LAST_30_DAYS"}' | \
  python -m google_ads_cli exec run --operation gaql.build --stdin --compact -c config.yaml
```

### Discover available fields for a resource

```bash
echo '{"resource":"campaign"}' | \
  python -m google_ads_cli exec run --operation gaql.fields --stdin --compact -c config.yaml
```

### Validate GAQL before executing

```bash
echo '{"query":"SELECT campaign.id, campaign.name FROM campaign"}' | \
  python -m google_ads_cli exec run --operation gaql.validate --stdin --compact -c config.yaml
```

## Configuration

The CLI reads credentials from a YAML config file:

```yaml
google_ads:
  client_id: "YOUR_CLIENT_ID.apps.googleusercontent.com"
  client_secret: "YOUR_CLIENT_SECRET"
  refresh_token: "YOUR_REFRESH_TOKEN"
  developer_token: "YOUR_DEVELOPER_TOKEN"
  customer_id: "1234567890"
  # login_customer_id: "0987654321"  # MCC account (optional)
  # api_version: "v23"               # defaults to v23
```

Credentials can also be overridden via CLI flags: `--customer_id`, `--login_customer_id`, `--developer_token`.

## Workflow Patterns

### Pattern 1: Incremental Build

1. `search.campaign.create` - Create campaign
2. `search.ad_group.create` - Add ad groups (can include keywords inline)
3. `search.ad.create_rsa` - Add RSA ads
4. `search.criteria.add` - Add location/language targeting
5. `search.criteria.add_negatives` - Add campaign negative keywords

### Pattern 2: One-Shot Full Build (Recommended)

Use `search.composite.create_full` with a single payload containing campaign config,
ad groups (with keywords), and ads. Handles all steps automatically with partial
failure tolerance.

### Pattern 3: Expand Existing Campaign

Use `search.composite.create_groups` to add new ad groups + ads to an existing campaign.

### Pattern 4: Monitor and Optimize

1. `report.campaign` - Check campaign-level metrics
2. `report.ad` - Check ad-level performance
3. `report.search_terms` - Discover search terms
4. `search.keyword.add` - Add winning search terms as keywords
5. `search.criteria.add_negatives` - Negate irrelevant terms
6. `search.campaign.update_bidding` - Adjust bidding strategy

### Pattern 5: GAQL Discovery and Execution

1. `gaql.resources` - List all available GAQL resources
2. `gaql.fields` - Discover selectable/filterable fields for a resource
3. `gaql.field` - Inspect a single field's metadata (type, compatibility)
4. `gaql.build` - Programmatically construct a GAQL query with static validation
5. `gaql.validate` - Validate query (static rules + API dry-run) before execution
6. `gaql.run` - Execute GAQL and get flattened results

This pattern is ideal for agents that need to dynamically construct queries based on
user intent rather than using predefined report operations.

```

## skills/google-ads-cli/references/ad.md
```markdown
# Ad / RSA Operations (7)

## search.ad.create_rsa

Create Responsive Search Ads.

```json
{
  "campaign_id": "23219624121",
  "ads": [
    {
      "ad_group_id": "189105408658",
      "ad_name": "Brand RSA v1",
      "headlines": [
        "Buy Running Shoes",
        "Free Shipping Today",
        "Top Rated Athletic Gear"
      ],
      "descriptions": [
        "Shop our collection of premium running shoes. Free returns.",
        "Discover top-rated footwear for every activity."
      ],
      "final_url": "https://www.example.com/shoes",
      "path1": "shoes",
      "path2": "running"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ads | array | yes | 1-50 RSA items |
| ads[].ad_group_id | string | yes | Target ad group ID |
| ads[].ad_name | string | yes | Ad name (1-100 chars) |
| ads[].headlines | string[] | yes | 3-15 headlines (each max 30 chars) |
| ads[].descriptions | string[] | yes | 2-4 descriptions (each max 90 chars) |
| ads[].final_url | string | yes | Landing page URL (max 255) |
| ads[].path1 | string | no | Display URL path 1 (max 25 chars) |
| ads[].path2 | string | no | Display URL path 2 (max 25 chars) |

## search.ad.get_rsa

Get RSA details by ad IDs.

```json
{
  "campaign_id": "23219624121",
  "ad_ids": ["741457938700", "741457938701"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_ids | string[] | yes | 1-50 ad IDs |

## search.ad.update_rsa

Update RSA content (headlines, descriptions, URLs, paths).

```json
{
  "campaign_id": "23219624121",
  "updates": [
    {
      "ad_id": "741457938700",
      "headlines": ["New Headline 1", "New Headline 2", "New Headline 3"],
      "descriptions": ["Updated description one.", "Updated description two."],
      "final_url": "https://www.example.com/new-landing",
      "path1": "new",
      "path2": "page"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| updates | array | yes | 1-50 update items |
| updates[].ad_id | string | yes | Ad ID |
| updates[].headlines | string[] | no | 3-15 new headlines (replaces all) |
| updates[].descriptions | string[] | no | 2-4 new descriptions (replaces all) |
| updates[].final_url | string | no | New landing URL |
| updates[].path1 | string | no | New path1 |
| updates[].path2 | string | no | New path2 |

## search.ad.update_status

Change ad status.

```json
{
  "ad_group_ad_ids": ["189105408658~741457938700"],
  "status": "PAUSED"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ad_group_ad_ids | string[] | yes | 1-100 IDs in `ad_group_id~ad_id` format |
| status | enum | yes | `ENABLED` or `PAUSED` |

## search.ad.list

List ads in a campaign.

```json
{
  "campaign_id": "23219624121",
  "ad_group_id": "189105408658",
  "status_filter": "ENABLED"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_group_id | string | no | Filter by ad group |
| status_filter | string | no | `ENABLED`, `PAUSED`, or null |

## search.ad.remove

Remove ads.

```json
{
  "ad_group_ad_ids": ["189105408658~741457938700"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ad_group_ad_ids | string[] | yes | 1-100 IDs in `ad_group_id~ad_id` format |

## search.ad.copy_rsa

Copy RSA ads to a different ad group. Fetches source ad content automatically.

```json
{
  "source_campaign_id": "23219624121",
  "source_ad_ids": ["741457938700"],
  "target_ad_group_id": "189105408698",
  "target_campaign_id": "23219624121"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| source_campaign_id | string | yes | Source campaign ID |
| source_ad_ids | string[] | yes | 1-50 source ad IDs |
| target_ad_group_id | string | yes | Destination ad group |
| target_campaign_id | string | yes | Destination campaign |

```

## skills/google-ads-cli/references/ad_group.md
```markdown
# Ad Group Operations (5)

## search.ad_group.create

Create ad groups in a campaign. Can include keywords inline.

```json
{
  "campaign_id": "23219624121",
  "ad_groups": [
    {
      "ad_group_name": "Brand Terms",
      "target_cpa": 5.0,
      "keywords": [
        { "text": "buy shoes online", "match_type": ["EXACT", "PHRASE"] }
      ],
      "negative_keywords": [
        { "text": "free", "match_type": ["BROAD"] }
      ]
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_groups | array | yes | 1-100 ad groups |
| ad_groups[].ad_group_name | string | yes | Name (1-100 chars) |
| ad_groups[].target_cpa | float | no | Target CPA (0.01-100) |
| ad_groups[].keywords | array | no | Keywords (max 100). See keyword format below |
| ad_groups[].negative_keywords | array | no | Negative keywords (max 100) |

**Keyword format**: `{ "text": "keyword text", "match_type": ["EXACT", "PHRASE", "BROAD"] }`
Each keyword can have multiple match types; a separate criterion is created for each.

## search.ad_group.list

List ad groups in a campaign.

```json
{
  "campaign_id": "23219624121",
  "status_filter": "ENABLED"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| status_filter | string | no | `ENABLED`, `PAUSED`, or null (all) |

## search.ad_group.find

Find ad groups by name.

```json
{
  "campaign_id": "23219624121",
  "ad_group_names": ["Brand Terms", "Generic SEO"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_group_names | string[] | yes | 1-50 ad group names |

## search.ad_group.update_status

Change ad group status.

```json
{
  "campaign_id": "23219624121",
  "ad_group_ids": ["189105408658", "189105408698"],
  "status": "PAUSED"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_group_ids | string[] | yes | 1-100 ad group IDs |
| status | enum | yes | `ENABLED` or `PAUSED` |

## search.ad_group.remove

Remove ad groups.

```json
{
  "campaign_id": "23219624121",
  "ad_group_ids": ["189105408658"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_group_ids | string[] | yes | 1-100 ad group IDs |

```

## skills/google-ads-cli/references/campaign.md
```markdown
# Campaign Operations (6)

## search.campaign.create

Create a new Search campaign with budget.

```json
{
  "campaign_name": "My Campaign",
  "budget_amount": 10.0,
  "status": "PAUSED",
  "start_days_from_now": 0,
  "end_days_from_now": 30,
  "bidding_strategy": "MAXIMIZE_CONVERSIONS",
  "maximize_conversions": { "target_cpa": 5.0 }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_name | string | yes | 1-255 chars |
| budget_amount | float | no | Daily budget (default 1.0, range 0.01-100000) |
| status | enum | no | `ENABLED` or `PAUSED` (default) |
| start_days_from_now | int | no | Start date offset (default 0, range 0-365) |
| end_days_from_now | int | no | End date offset (range 10-3650, null = indefinite) |
| bidding_strategy | enum | no | See bidding strategies below (default `MAXIMIZE_CONVERSIONS`) |
| maximize_conversions | object | no | `{ "target_cpa": float }` (0.1-100) |
| maximize_conversion_value | object | conditional | `{ "target_roas": float }` (0.1-1000). Required when strategy is `MAXIMIZE_CONVERSION_VALUE` |
| target_impression_share | object | conditional | Required when strategy is `TARGET_IMPRESSION_SHARE` |
| target_spend | object | conditional | `{ "cpc_bid_ceiling": float }` (0.1-1000). Required when strategy is `TARGET_SPEND` |

**Bidding strategies**: `MAXIMIZE_CONVERSIONS`, `MAXIMIZE_CONVERSION_VALUE`, `TARGET_IMPRESSION_SHARE`, `TARGET_SPEND`

**target_impression_share object**:
```json
{
  "location": "ABSOLUTE_TOP_OF_PAGE",
  "location_fraction": 0.9,
  "cpc_bid_ceiling": 2.0
}
```
Location options: `ANYWHERE_ON_PAGE`, `TOP_OF_PAGE`, `ABSOLUTE_TOP_OF_PAGE`

## search.campaign.list

List campaigns by type and status.

```json
{
  "campaign_type": "SEARCH",
  "status_filter": "ENABLED"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_type | string | no | `SEARCH` (default), `DISPLAY`, `DEMAND_GEN`, `APP` |
| status_filter | string | no | `ENABLED`, `PAUSED`, or null (all) |

## search.campaign.find

Find campaigns by IDs or names.

```json
{
  "campaign_ids_or_names": ["23219624121", "My Campaign Name"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_ids_or_names | string[] | yes | 1-50 campaign IDs or names |

## search.campaign.update

Update campaign name, status, or end date.

```json
{
  "campaigns": [
    {
      "campaign_id": "23219624121",
      "campaign_name": "New Name",
      "status": "PAUSED",
      "end_days_from_now": 60
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaigns | array | yes | 1-20 update items |
| campaigns[].campaign_id | string | yes | Campaign ID |
| campaigns[].campaign_name | string | no | New name (max 255) |
| campaigns[].status | enum | no | `ENABLED` or `PAUSED` |
| campaigns[].end_days_from_now | int | no | New end date (1-3650 days) |

## search.campaign.update_bidding

Change bidding strategy for campaigns.

```json
{
  "campaigns": [
    {
      "campaign_id": "23219624121",
      "bidding_strategy": "TARGET_SPEND",
      "target_spend": { "cpc_bid_ceiling": 1.5 }
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaigns | array | yes | 1-20 bidding update items |
| campaigns[].campaign_id | string | yes | Campaign ID |
| campaigns[].bidding_strategy | enum | yes | New bidding strategy |
| campaigns[].maximize_conversions | object | no | Strategy-specific params |
| campaigns[].maximize_conversion_value | object | no | Strategy-specific params |
| campaigns[].target_impression_share | object | no | Strategy-specific params |
| campaigns[].target_spend | object | no | Strategy-specific params |

## search.campaign.copy

Copy a campaign (optionally with ad groups).

```json
{
  "source_campaign_id": "23219624121",
  "copy_with_groups": false,
  "campaigns": [
    { "campaign_name": "Copy of Campaign", "budget_amount": 10.0 }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| source_campaign_id | string | yes | Source campaign ID |
| copy_with_groups | bool | no | Copy ad groups too (default false) |
| campaigns | array | yes | 1-20 target campaigns |
| campaigns[].campaign_name | string | yes | New campaign name (max 255) |
| campaigns[].budget_amount | float | no | Override budget (default: source budget) |

```

## skills/google-ads-cli/references/composite.md
```markdown
# Composite Operations (2)

One-shot creation of full campaign structures. Recommended for building new campaigns from scratch.

## search.composite.create_full

Create a complete campaign structure in one shot: campaign + targeting + ad groups (with keywords) + RSA ads.

```json
{
  "campaign": {
    "campaign_name": "Full Campaign Test",
    "budget_amount": 10.0,
    "status": "PAUSED",
    "bidding_strategy": "MAXIMIZE_CONVERSIONS",
    "locations": ["2840"],
    "languages": ["1000"],
    "negative_keywords": [
      { "text": "free", "match_type": "BROAD" }
    ]
  },
  "ad_groups": [
    {
      "ad_group_name": "Brand Terms",
      "keywords": [
        { "text": "brand shoes", "match_type": ["EXACT", "PHRASE"] }
      ]
    },
    {
      "ad_group_name": "Generic Terms",
      "keywords": [
        { "text": "running shoes", "match_type": ["BROAD"] }
      ]
    }
  ],
  "ads": [
    {
      "ad_group_name": "Brand Terms",
      "ad_name": "Brand RSA",
      "headlines": ["Buy Brand Shoes", "Official Store", "Free Shipping"],
      "descriptions": ["Shop the official brand store.", "Premium quality guaranteed."],
      "final_url": "https://www.example.com/brand"
    },
    {
      "ad_group_name": "Generic Terms",
      "ad_name": "Generic RSA",
      "headlines": ["Best Running Shoes", "Top Rated Footwear", "Shop Now"],
      "descriptions": ["Find your perfect pair today.", "Free returns on all orders."],
      "final_url": "https://www.example.com/running"
    }
  ]
}
```

**Campaign config fields**: Same as `search.campaign.create` (see [campaign.md](campaign.md)) plus:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| locations | string[] | no | Geo target constant IDs |
| languages | string[] | no | Language constant IDs |
| negative_keywords | array | no | Campaign-level negatives `[{text, match_type}]` |

**Ad groups**: Same as `search.ad_group.create` items (name, target_cpa, keywords, negative_keywords).

**Ads**: Reference ad groups by `ad_group_name` (must match an entry in `ad_groups`).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ad_group_name | string | yes | Must match an ad_group in the ad_groups array |
| ad_name | string | yes | Ad name (1-100 chars) |
| headlines | string[] | yes | 3-15 headlines (each max 30 chars) |
| descriptions | string[] | yes | 2-4 descriptions (each max 90 chars) |
| final_url | string | yes | Landing page URL |
| path1 | string | no | Display URL path 1 |
| path2 | string | no | Display URL path 2 |

The operation is fault-tolerant: if ad creation fails (e.g. policy violation), the campaign and ad groups are still preserved.

## search.composite.create_groups

Add ad groups + ads to an existing campaign.

```json
{
  "campaign_id": "23219624121",
  "ad_groups": [
    {
      "ad_group_name": "New Group",
      "keywords": [
        { "text": "new keyword", "match_type": ["EXACT"] }
      ]
    }
  ],
  "ads": [
    {
      "ad_group_name": "New Group",
      "ad_name": "New RSA",
      "headlines": ["Headline 1", "Headline 2", "Headline 3"],
      "descriptions": ["Description one.", "Description two."],
      "final_url": "https://www.example.com/new"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Existing campaign ID |
| ad_groups | array | yes | 1-100 ad group configs |
| ads | array | yes | 1-100 ad configs (reference ad_group_name) |

```

## skills/google-ads-cli/references/gaql.md
```markdown
# GAQL Operations (6)

Field/resource discovery, programmatic query building, validation, and enhanced execution.
Adapted from the [google-ads-api-developer-assistant](https://github.com/googleads/google-ads-api-developer-assistant) design patterns.

## gaql.resources

List all available GAQL resources (tables).

```json
{}
```

No payload fields required.

**Response example**:
```json
{
  "total": 120,
  "resources": [
    { "name": "ad_group", "category": "RESOURCE", "data_type": "MESSAGE" },
    { "name": "campaign", "category": "RESOURCE", "data_type": "MESSAGE" }
  ]
}
```

## gaql.fields

Discover all selectable fields for a resource.

```json
{
  "resource": "campaign"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| resource | string | yes | Resource name (e.g. `campaign`, `ad_group`, `ad_group_ad`) |

**Response**: Returns each field with `name`, `category`, `data_type`, `selectable`, `filterable`, `sortable`, `is_repeated`, `selectable_with`, `metrics`, `segments`, `attribute_resources`.

## gaql.field

Get detailed metadata for a single field.

```json
{
  "field_name": "metrics.clicks"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| field_name | string | yes | Full field name (e.g. `metrics.clicks`, `campaign.status`) |

**Response**: Detailed field info including `data_type`, `selectable`, `filterable`, `sortable`, `selectable_with` (list of compatible resources/segments), `enum_values` (for ENUM types).

## gaql.build

Programmatically construct a GAQL query from parameters. Runs static validation rules automatically.

```json
{
  "resource": "campaign",
  "fields": ["campaign.id", "campaign.name", "metrics.clicks", "metrics.impressions"],
  "conditions": ["campaign.status = 'ENABLED'"],
  "order_by": "metrics.clicks DESC",
  "limit": 10,
  "date_range": "LAST_30_DAYS"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| resource | string | yes | GAQL resource name |
| fields | string[] | yes | Fields to SELECT (min 1) |
| conditions | string[] | no | WHERE conditions |
| order_by | string | no | ORDER BY clause (e.g. `metrics.clicks DESC`) |
| limit | int | no | LIMIT rows (1-10000) |
| date_range | string | no | Date range: `LAST_30_DAYS`, `YESTERDAY`, etc., or custom `YYYY-MM-DD,YYYY-MM-DD` |

**Response**:
```json
{
  "query": "SELECT campaign.id, campaign.name, metrics.clicks, metrics.impressions FROM campaign WHERE campaign.status = 'ENABLED' AND segments.date DURING LAST_30_DAYS ORDER BY metrics.clicks DESC LIMIT 10",
  "validation": {
    "valid": true,
    "error_count": 0,
    "warning_count": 0,
    "issues": []
  }
}
```

**Static validation rules**:
- GAQL `OR` operator is forbidden (use `IN(...)` instead)
- Date segments in SELECT require `DURING` or `BETWEEN` in WHERE
- `ORDER BY` fields should appear in SELECT
- `click_view` resource requires single-day date filter (TODAY, YESTERDAY, or same-day BETWEEN)
- `change_status` resource requires `BETWEEN` on `last_change_date_time` + LIMIT

## gaql.validate

Validate a GAQL query without executing it. Runs static rules first, then API dry-run (`validateOnly=true`).

```json
{
  "query": "SELECT campaign.id, campaign.name FROM campaign WHERE campaign.status = 'ENABLED'"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | yes | GAQL query to validate (min 10 chars) |

**Response**:
```json
{
  "query": "SELECT campaign.id, campaign.name FROM campaign WHERE campaign.status = 'ENABLED'",
  "static_validation": {
    "valid": true,
    "error_count": 0,
    "warning_count": 0,
    "issues": []
  },
  "dry_run": {
    "executed": true,
    "valid": true,
    "error": null
  },
  "valid": true
}
```

If static validation fails, dry-run is skipped. If dry-run fails, `dry_run.error` contains the API error message.

## gaql.run

Execute a GAQL query and return results. Supports flattening nested JSON to dot-notation keys.

```json
{
  "query": "SELECT campaign.id, campaign.name, campaign.status, metrics.clicks FROM campaign WHERE campaign.status != 'REMOVED' LIMIT 5",
  "flatten": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | yes | GAQL query to execute (min 10 chars) |
| flatten | bool | no | Flatten nested response (default `true`) |

**Response (flatten=true)**:
```json
{
  "query": "SELECT campaign.id, campaign.name ...",
  "total": 5,
  "rows": [
    {
      "campaign.resourceName": "customers/123/campaigns/456",
      "campaign.id": "456",
      "campaign.name": "My Campaign",
      "campaign.status": "ENABLED",
      "metrics.clicks": "142"
    }
  ]
}
```

**Response (flatten=false)**: Returns raw nested API response structure.

**Difference from `report.gaql`**: `gaql.run` provides `flatten` option for cleaner output and includes the original query in the response. `report.gaql` returns raw API results for backward compatibility.

```

## skills/google-ads-cli/references/keyword.md
```markdown
# Keyword Operations (3)

## search.keyword.add

Add keywords and/or negative keywords to an ad group.

```json
{
  "campaign_id": "23219624121",
  "ad_group_id": "189105408658",
  "keywords": [
    { "text": "running shoes", "match_type": ["EXACT", "PHRASE"] },
    { "text": "athletic footwear", "match_type": ["BROAD"] }
  ],
  "negative_keywords": [
    { "text": "cheap", "match_type": ["BROAD"] }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_group_id | string | yes | Ad group ID |
| keywords | array | no | Positive keywords (max 100) |
| negative_keywords | array | no | Negative keywords (max 100) |

At least one of `keywords` or `negative_keywords` must be provided.

## search.keyword.list

List keywords in ad groups.

```json
{
  "ad_group_ids": ["189105408658", "189105408698"],
  "status": "ENABLED"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ad_group_ids | string[] | yes | 1-20 ad group IDs |
| status | string | no | `ENABLED` (default) or `PAUSED` |

## search.keyword.remove

Remove keywords by criterion ID.

```json
{
  "campaign_id": "23219624121",
  "ad_group_id": "189105408658",
  "criterion_ids": ["123456789", "987654321"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| ad_group_id | string | yes | Ad group ID |
| criterion_ids | string[] | yes | Criterion IDs to remove |

```

## skills/google-ads-cli/references/operations.md
```markdown
# Operations Reference

38 operations organized by usage scenario. Each operation is invoked via:

```bash
echo '<payload>' | python -m google_ads_cli exec run --operation <name> --stdin --compact -c config.yaml
```

All operations return a `ResultEnvelope`:

```json
{ "success": true, "command": "exec <operation>", "result": { ... }, "elapsed_ms": 1234.5 }
```

On failure: `success: false`, `errors: [...]`, exit code `1`.

---

## Operations by Scenario

| Scenario | File | Operations | When to use |
|----------|------|------------|-------------|
| Campaign Management | [campaign.md](campaign.md) | `search.campaign.create`, `list`, `find`, `update`, `update_bidding`, `copy` (6) | Create, list, find, update, or copy campaigns |
| Ad Group Management | [ad_group.md](ad_group.md) | `search.ad_group.create`, `list`, `find`, `update_status`, `remove` (5) | Manage ad groups within a campaign |
| Keyword Management | [keyword.md](keyword.md) | `search.keyword.add`, `list`, `remove` (3) | Add, list, or remove keywords in ad groups |
| Ad / RSA Creative | [ad.md](ad.md) | `search.ad.create_rsa`, `get_rsa`, `update_rsa`, `update_status`, `list`, `remove`, `copy_rsa` (7) | Create, edit, or manage Responsive Search Ads |
| Targeting & Budget | [targeting.md](targeting.md) | `search.budget.update`, `search.criteria.add`, `list`, `remove`, `add_negatives` (5) | Set budgets, location/language targeting, campaign negatives |
| Composite Build | [composite.md](composite.md) | `search.composite.create_full`, `create_groups` (2) | Build full campaign structures in one shot |
| Reporting | [report.md](report.md) | `report.campaign`, `ad`, `search_terms`, `gaql` (4) | Run predefined performance reports or raw GAQL |
| GAQL Builder | [gaql.md](gaql.md) | `gaql.resources`, `fields`, `field`, `build`, `validate`, `run` (6) | Discover fields, build/validate/execute GAQL queries |

---

## Quick Decision Guide

**"I need to create a new campaign from scratch"**
→ Use `search.composite.create_full` ([composite.md](composite.md)) for one-shot setup

**"I need to check performance"**
→ Use `report.campaign` or `report.ad` ([report.md](report.md))

**"I need a custom data query"**
→ Use `gaql.build` + `gaql.run` ([gaql.md](gaql.md))

**"I need to know what fields/resources exist"**
→ Use `gaql.resources` or `gaql.fields` ([gaql.md](gaql.md))

**"I need to adjust an existing campaign"**
→ See [campaign.md](campaign.md) for updates, [targeting.md](targeting.md) for budget/criteria

```

## skills/google-ads-cli/references/report.md
```markdown
# Report Operations (4)

Predefined performance reports and raw GAQL execution. For dynamic query building, see [gaql.md](gaql.md).

## report.campaign

Campaign performance report.

```json
{
  "date_range": "LAST_7_DAYS",
  "campaign_ids": ["23219624121"],
  "status_filter": "ENABLED"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| date_range | string | no | Default `LAST_30_DAYS`. Options: `TODAY`, `YESTERDAY`, `LAST_7_DAYS`, `LAST_30_DAYS`, `THIS_MONTH`, `LAST_MONTH`, or custom `YYYY-MM-DD,YYYY-MM-DD` |
| campaign_ids | string[] | no | Filter by campaigns |
| status_filter | string | no | `ENABLED`, `PAUSED` |

Returns: impressions, clicks, cost, conversions, ctr, avg_cpc, cost_per_conversion per campaign per date.

## report.ad

Ad-level performance report.

```json
{
  "campaign_id": "23219624121",
  "ad_group_id": "189105408658",
  "date_range": "LAST_30_DAYS",
  "limit": 50
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | no | Filter by campaign |
| ad_group_id | string | no | Filter by ad group |
| date_range | string | no | Default `LAST_30_DAYS` |
| limit | int | no | Max rows (1-500, default 50) |

## report.search_terms

Search terms performance report.

```json
{
  "campaign_id": "23219624121",
  "date_range": "LAST_30_DAYS",
  "limit": 100
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | no | Filter by campaign |
| ad_group_id | string | no | Filter by ad group |
| date_range | string | no | Default `LAST_30_DAYS` |
| limit | int | no | Max rows (1-500, default 100) |

Returns: search_term, keyword_text, keyword_match_type, impressions, clicks, cost, conversions, ctr, avg_cpc, cost_per_conversion.

## report.gaql

Run a custom GAQL query. Returns raw API results.

```json
{
  "query": "SELECT campaign.id, campaign.name, metrics.impressions FROM campaign WHERE campaign.status = 'ENABLED' AND segments.date DURING LAST_7_DAYS ORDER BY metrics.impressions DESC LIMIT 10"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | yes | GAQL query (min 10 chars) |

Returns raw API results without parsing. For flattened results and validation, use `gaql.run` instead (see [gaql.md](gaql.md)).

**GAQL reference**: [Google Ads Query Language grammar](https://developers.google.com/google-ads/api/docs/query/grammar)

```

## skills/google-ads-cli/references/targeting.md
```markdown
# Targeting & Budget Operations (5)

Budget updates, location/language targeting, and campaign-level negative keywords.

## search.budget.update

Update daily budget for campaigns.

```json
{
  "budget_updates": [
    { "campaign_id": "23219624121", "amount": 15.0 }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| budget_updates | array | yes | 1-100 budget updates |
| budget_updates[].campaign_id | string | yes | Campaign ID |
| budget_updates[].amount | float | yes | New daily budget (0.01-100000) |

## search.criteria.add

Add location and/or language targeting to a campaign.

```json
{
  "campaign_id": "23219624121",
  "location_ids": ["2840", "2124"],
  "language_ids": ["1000", "1001"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| location_ids | string[] | no | Geo target constant IDs (e.g. 2840 = US, 2124 = CA) |
| language_ids | string[] | no | Language constant IDs (e.g. 1000 = English, 1001 = French) |

## search.criteria.list

List all criteria for campaigns.

```json
{
  "campaign_ids": ["23219624121"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_ids | string[] | yes | 1-20 campaign IDs |

## search.criteria.remove

Remove campaign criteria.

```json
{
  "campaign_id": "23219624121",
  "criterion_ids": ["12345", "67890"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| criterion_ids | string[] | yes | Criterion IDs to remove |

## search.criteria.add_negatives

Add campaign-level negative keywords.

```json
{
  "campaign_id": "23219624121",
  "negative_keywords": [
    { "text": "free download", "match_type": "BROAD" },
    { "text": "open source", "match_type": "PHRASE" }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| campaign_id | string | yes | Campaign ID |
| negative_keywords | array | yes | 1-1000 negative keywords |
| negative_keywords[].text | string | yes | Keyword text (1-80 chars) |
| negative_keywords[].match_type | string | no | `EXACT`, `PHRASE`, or `BROAD` (default) |

```
