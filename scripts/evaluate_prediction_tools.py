#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import socket
import ssl
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from html import unescape
from pathlib import Path
from typing import Iterable
from urllib import error, request
from urllib.parse import urlparse


TARGET_SECTIONS = [
    "AI Agents",
    "APIs",
    "Aggregator",
    "Alerts",
    "Analytics Tools",
    "Dashboards",
    "Educational Resources",
]


SOCIAL_HOST_MARKERS = (
    "t.me",
    "telegram.me",
    "x.com",
    "twitter.com",
    "discord.com",
    "discord.gg",
)


MODULE_KEYWORDS = {
    "api": ["api", "sdk", "endpoint", "developer", "integration", "websocket", "rest"],
    "analytics": ["analytics", "trader", "wallet", "leaderboard", "pnl", "roi", "whale"],
    "alerts": ["alert", "notification", "telegram", "webhook", "watchlist"],
    "dashboard": ["dashboard", "terminal", "explorer", "visualization"],
    "aggregation": ["aggregate", "aggregator", "cross-market", "cross-venue", "comparison", "matching"],
    "arbitrage": ["arbitrage", "mispricing", "spread", "edge"],
    "ai": ["ai", "agent", "research", "sentiment", "model", "llm", "mcp"],
    "education": ["guide", "newsletter", "learn", "encyclopedia", "case studies", "podcast"],
    "execution": ["trade", "trading", "order", "execution", "paper trading", "copy trade"],
}


@dataclass
class CatalogItem:
    section: str
    name: str
    url: str
    description: str


@dataclass
class ProbeResult:
    section: str
    name: str
    url: str
    description: str
    final_url: str
    status: str
    response_ms: int
    title: str
    content_type: str
    platform_shape: str
    modules: list[str]
    notes: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate prediction market catalog entries.")
    parser.add_argument("--readme", required=True, help="Path to the Awesome catalog README")
    parser.add_argument("--output-json", required=True, help="Where to write the raw probe results JSON")
    parser.add_argument("--output-md", required=True, help="Where to write the markdown summary")
    parser.add_argument("--timeout", type=float, default=8.0, help="HTTP timeout seconds")
    parser.add_argument("--workers", type=int, default=12, help="Parallel workers")
    return parser.parse_args()


def extract_sections(readme: str, names: Iterable[str]) -> dict[str, str]:
    sections: dict[str, str] = {}
    for name in names:
        pattern = re.compile(rf"^##\s+.*{re.escape(name)}\s*$", re.MULTILINE)
        match = pattern.search(readme)
        if not match:
            continue
        start = match.end()
        next_heading = re.search(r"^##\s+", readme[start:], re.MULTILINE)
        body = readme[start : start + next_heading.start()] if next_heading else readme[start:]
        sections[name] = body
    return sections


def parse_catalog_items(readme_path: Path) -> list[CatalogItem]:
    readme = readme_path.read_text(encoding="utf-8")
    sections = extract_sections(readme, TARGET_SECTIONS)
    items: list[CatalogItem] = []
    line_pattern = re.compile(r"^- \[([^\]]+)\]\(([^)]+)\)\s+[—-]\s+(.*)$")

    for section in TARGET_SECTIONS:
        body = sections.get(section, "")
        for raw_line in body.splitlines():
            line = raw_line.strip()
            match = line_pattern.match(line)
            if not match:
                continue
            items.append(
                CatalogItem(
                    section=section,
                    name=match.group(1).strip(),
                    url=match.group(2).strip(),
                    description=match.group(3).strip(),
                )
            )
    return items


def infer_platform_shape(url: str, final_url: str, title: str, body: str, content_type: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    lowered = " ".join([url, final_url, title, body[:4000]]).lower()
    domain = urlparse(final_url or url).netloc.lower()

    if url == "#":
        return "placeholder", ["placeholder link"]
    if any(marker in domain or marker in url.lower() for marker in SOCIAL_HOST_MARKERS):
        return "social", ["social-only surface"]
    if "github.com" in domain:
        return "github_repo", ["open-source repo surface"]
    if "gitbook.io" in domain or "docs" in domain.split(".")[0] or "api" in domain.split(".")[0]:
        notes.append("docs-like domain")
    if "application/json" in content_type:
        return "api_endpoint", notes or ["raw API endpoint"]
    if "dashboard" in lowered or "terminal" in lowered:
        return "dashboard_app", notes
    if "api" in lowered and ("docs" in lowered or "developer" in lowered or "get started" in lowered):
        return "api_portal", notes
    if "pricing" in lowered or "login" in lowered or "sign in" in lowered or "get started" in lowered:
        return "web_app", notes
    if "guide" in lowered or "newsletter" in lowered or "podcast" in lowered or "case studies" in lowered:
        return "content_resource", notes
    return "website", notes


def infer_modules(item: CatalogItem, title: str, body: str) -> list[str]:
    lowered = " ".join([item.section, item.name, item.description, title, body[:6000]]).lower()
    modules = [name for name, keywords in MODULE_KEYWORDS.items() if any(keyword in lowered for keyword in keywords)]
    return sorted(set(modules))


def probe_item(item: CatalogItem, timeout: float, ssl_context: ssl.SSLContext) -> ProbeResult:
    started = time.perf_counter()
    if item.url == "#":
        return ProbeResult(
            section=item.section,
            name=item.name,
            url=item.url,
            description=item.description,
            final_url=item.url,
            status="placeholder",
            response_ms=0,
            title="",
            content_type="",
            platform_shape="placeholder",
            modules=infer_modules(item, "", ""),
            notes=["placeholder link"],
        )

    if any(marker in item.url.lower() for marker in SOCIAL_HOST_MARKERS):
        return ProbeResult(
            section=item.section,
            name=item.name,
            url=item.url,
            description=item.description,
            final_url=item.url,
            status="social",
            response_ms=0,
            title="",
            content_type="",
            platform_shape="social",
            modules=infer_modules(item, "", ""),
            notes=["social-only entry point"],
        )

    req = request.Request(item.url, headers={"User-Agent": "Mozilla/5.0 Codex evaluator"})
    try:
        with request.urlopen(req, timeout=timeout, context=ssl_context) as response:
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            final_url = response.geturl()
            content_type = response.headers.get("Content-Type", "")
            body = ""
            if any(text_type in content_type for text_type in ("text/html", "text/plain", "application/xhtml+xml")):
                raw = response.read(65536)
                body = raw.decode("utf-8", errors="ignore")
            title_match = re.search(r"<title[^>]*>(.*?)</title>", body, re.IGNORECASE | re.DOTALL)
            title = re.sub(r"\s+", " ", unescape(title_match.group(1))).strip() if title_match else ""
            shape, shape_notes = infer_platform_shape(item.url, final_url, title, body, content_type)
            modules = infer_modules(item, title, body)
            notes = list(shape_notes)
            if "docs" in body.lower():
                notes.append("mentions docs")
            if "github" in body.lower():
                notes.append("mentions github")
            if "api" in body.lower():
                notes.append("mentions api")
            return ProbeResult(
                section=item.section,
                name=item.name,
                url=item.url,
                description=item.description,
                final_url=final_url,
                status=str(getattr(response, "status", "ok")),
                response_ms=elapsed_ms,
                title=title[:160],
                content_type=content_type,
                platform_shape=shape,
                modules=modules,
                notes=sorted(set(notes)),
            )
    except error.HTTPError as exc:
        return ProbeResult(
            section=item.section,
            name=item.name,
            url=item.url,
            description=item.description,
            final_url=item.url,
            status=f"http_{exc.code}",
            response_ms=int((time.perf_counter() - started) * 1000),
            title="",
            content_type="",
            platform_shape="blocked",
            modules=infer_modules(item, "", ""),
            notes=[f"http error {exc.code}"],
        )
    except Exception as exc:  # noqa: BLE001
        return ProbeResult(
            section=item.section,
            name=item.name,
            url=item.url,
            description=item.description,
            final_url=item.url,
            status="error",
            response_ms=int((time.perf_counter() - started) * 1000),
            title="",
            content_type="",
            platform_shape="error",
            modules=infer_modules(item, "", ""),
            notes=[f"{type(exc).__name__}: {exc}"],
        )


def stability_label(status: str) -> str:
    if status == "200":
        return "reachable"
    if status in {"social", "placeholder"}:
        return "not-applicable"
    if status.startswith("http_") or status == "error":
        return "blocked-or-flaky"
    return "unknown"


def verdict_for_result(result: ProbeResult) -> str:
    if result.platform_shape in {"placeholder", "social"}:
        return "reject"
    if result.status in {"http_402", "http_403", "http_404", "http_429", "error"}:
        return "weak-surface"
    if result.platform_shape == "github_repo":
        return "needs-doc-review"
    if result.platform_shape in {"api_portal", "dashboard_app", "web_app"} and any(
        module in result.modules for module in ("api", "analytics", "alerts", "aggregation", "dashboard")
    ):
        return "deeper-review"
    if result.platform_shape == "content_resource":
        return "reference-only"
    return "triage"


def platform_label(result: ProbeResult) -> str:
    mapping = {
        "github_repo": "Open-source repo",
        "api_portal": "API portal",
        "api_endpoint": "API endpoint",
        "dashboard_app": "Dashboard app",
        "web_app": "Web app",
        "website": "Website",
        "content_resource": "Reference content",
        "social": "Social bot/feed",
        "placeholder": "Placeholder",
        "blocked": "Blocked surface",
        "error": "Probe error",
    }
    return mapping.get(result.platform_shape, result.platform_shape)


def stability_bucket(status: str) -> str:
    if status == "200":
        return "reachable"
    if status in {"social", "placeholder"}:
        return "n/a"
    if status in {"http_402", "http_403"}:
        return "gated"
    if status == "http_429":
        return "rate-limited"
    if status in {"http_404", "http_406", "http_521"}:
        return "broken"
    if status == "error":
        return "flaky"
    return "unknown"


def run_feel(result: ProbeResult) -> str:
    if result.platform_shape == "placeholder":
        return "not a real product link"
    if result.platform_shape == "social":
        return "social-only entry point"
    if result.platform_shape == "github_repo":
        return "repo/docs first, local run needed"
    if result.platform_shape == "content_resource":
        return "read-only reference"
    if result.status in {"http_402", "http_403"}:
        return "access wall before product depth"
    if result.status == "http_429":
        return "rate-limited during smoke test"
    if result.status in {"http_404", "http_406", "http_521"}:
        return "broken or unavailable in smoke test"
    if result.status == "error":
        return "transport or SSL failure in smoke test"
    if result.platform_shape == "api_portal":
        return "developer-first surface"
    if result.platform_shape == "dashboard_app":
        return "interactive anon dashboard"
    if result.platform_shape == "web_app":
        return "browseable but account-centric"
    return "marketing page with some live surface"


def summarize_function(text: str, limit: int = 110) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def write_markdown(results: list[ProbeResult], output_path: Path) -> None:
    by_section: dict[str, list[ProbeResult]] = defaultdict(list)
    for result in results:
        by_section[result.section].append(result)

    lines = [
        "# Catalog Evaluation Summary",
        "",
        "Automated first-pass probe across targeted `Awesome Prediction Market Tools` categories.",
        "",
        "## Section Summary",
        "",
        "| Section | Count | Reachable | Blocked/Flaky | Social/Placeholder |",
        "|---|---:|---:|---:|---:|",
    ]
    for section in TARGET_SECTIONS:
        section_results = by_section.get(section, [])
        reachable = sum(1 for result in section_results if stability_label(result.status) == "reachable")
        blocked = sum(1 for result in section_results if stability_label(result.status) == "blocked-or-flaky")
        socialish = sum(1 for result in section_results if result.platform_shape in {"social", "placeholder"})
        lines.append(f"| {section} | {len(section_results)} | {reachable} | {blocked} | {socialish} |")

    lines.extend(["", "## Results", ""])
    for section in TARGET_SECTIONS:
        lines.append(f"### {section}")
        lines.append("")
        lines.append("| Name | Function | Stability | Platform | Run Feel | Verdict |")
        lines.append("|---|---|---|---|---|---|")
        for result in sorted(by_section.get(section, []), key=lambda item: item.name.lower()):
            function = summarize_function(result.description)
            lines.append(
                f"| {result.name} | {function} | {stability_bucket(result.status)} | {platform_label(result)} | {run_feel(result)} | {verdict_for_result(result)} |"
            )
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    socket.setdefaulttimeout(args.timeout)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    items = parse_catalog_items(Path(args.readme))
    results: list[ProbeResult] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(probe_item, item, args.timeout, ssl_context) for item in items]
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda item: (item.section, item.name.lower()))
    summary = Counter(result.section for result in results)
    payload = {
        "generated_at": int(time.time()),
        "items": [
            asdict(result)
            | {
                "stability": stability_label(result.status),
                "stability_bucket": stability_bucket(result.status),
                "platform_label": platform_label(result),
                "run_feel": run_feel(result),
                "verdict": verdict_for_result(result),
            }
            for result in results
        ],
        "section_counts": dict(summary),
    }

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(results, Path(args.output_md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
