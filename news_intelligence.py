from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

from pydantic import BaseModel, Field

from evidence import Evidence

try:
    from tavily import TavilyClient
except Exception:  # pragma: no cover - optional dependency safe guard
    TavilyClient = None


CONTROLLED_EVENT_TYPES = {
    "funding": {"funding", "raise", "raises", "round", "series", "financing", "capital", "debt"},
    "acquisition": {"acquisition", "acquired", "buyout", "takeover", "purchase"},
    "merger": {"merger", "merges", "combination", "combining"},
    "partnership": {"partnership", "partner", "collaborat", "alliance", "integration"},
    "product_launch": {"launch", "launched", "release", "releases", "introduces", "announcement", "debut"},
    "leadership": {"leadership", "ceo", "cfo", "cto", "executive", "appoint", "resign", "founder"},
    "expansion": {"expand", "expansion", "opens", "opening", "new facility", "new office", "entry into", "growth"},
    "layoffs": {"layoff", "layoffs", "restructur", "downsizing", "job cuts", "staff reduction"},
    "legal": {"lawsuit", "legal", "settlement", "court", "complaint", "sues", "claim"},
    "regulatory": {"regulatory", "regulation", "compliance", "sanction", "investigation", "approval", "fda", "sec", "probe"},
}

GENERIC_NEWS_PATTERNS = (
    "company overview",
    "about us",
    "what we do",
    "our mission",
    "careers",
    "job openings",
    "company profile",
    "press kit",
    "blog post",
    "employee spotlight",
    "industry overview",
    "market report",
    "analysis of",
    "how to",
)

POSITIVE_KEYWORDS = (
    "launch",
    "launched",
    "funding",
    "raise",
    "raises",
    "partnership",
    "acquired",
    "expansion",
    "new contract",
    "wins",
    "approval",
    "record revenue",
    "growth",
)
NEGATIVE_KEYWORDS = (
    "layoff",
    "layoffs",
    "restructur",
    "decline",
    "lawsuit",
    "regulatory probe",
    "investigation",
    "penalty",
    "sanction",
    "dismissal",
    "downgrade",
)


class NewsItem(BaseModel):
    title: str = ""
    summary: str = ""
    source: str = ""
    url: str = ""
    published_date: str | None = None
    event_type: str = "other"
    investment_impact: str = "unclear"
    confidence: int = Field(default=0, ge=0, le=100)
    evidence: list[Evidence] = Field(default_factory=list)


def _clean_text(value: Any, fallback: str = "") -> str:
    if value is None:
        return fallback
    text = str(value).strip()
    return text if text else fallback


def _slugify_source(value: str) -> str:
    cleaned = re.sub(r"https?://|www\.", "", value, flags=re.IGNORECASE)
    cleaned = cleaned.split("/")[0]
    cleaned = cleaned.replace(".", " ").strip()
    return cleaned.title() if cleaned else "Unknown source"


def _normalize_date(date_value: Any) -> str | None:
    if not date_value:
        return None

    date_text = str(date_value).strip()
    if not date_text:
        return None

    normalized = date_text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    except ValueError:
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%b %d, %Y", "%B %d, %Y"):
            try:
                parsed = datetime.strptime(date_text, fmt)
                return parsed.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
            except ValueError:
                continue
    return None


def _event_type_from_text(title: str, summary: str) -> str:
    text = f"{title} {summary}".lower()
    for event_type, keywords in CONTROLLED_EVENT_TYPES.items():
        for keyword in keywords:
            if keyword in text:
                return event_type
    return "other"


def _investment_impact_for(event_type: str, title: str, summary: str) -> str:
    text = f"{title} {summary}".lower()
    if any(keyword in text for keyword in NEGATIVE_KEYWORDS):
        return "negative"
    if any(keyword in text for keyword in POSITIVE_KEYWORDS):
        return "positive"
    if event_type in {"funding", "partnership", "product_launch", "expansion", "acquisition", "merger"}:
        return "neutral"
    return "unclear"


def _is_old_news(date_value: str | None) -> bool:
    if not date_value:
        return False

    try:
        parsed = datetime.fromisoformat(date_value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        cutoff = datetime.now(timezone.utc).replace(microsecond=0)
        return (cutoff - parsed.astimezone(timezone.utc)).days > 1095
    except ValueError:
        return False


def _is_irrelevant(result: dict[str, Any], company_name: str | None) -> bool:
    title = _clean_text(result.get("title", "")).lower()
    content = _clean_text(result.get("content") or result.get("snippet") or result.get("summary") or "").lower()
    url = _clean_text(result.get("url", "")).lower()

    text = f"{title} {content}"
    if not text.strip():
        return True

    if any(pattern in text for pattern in GENERIC_NEWS_PATTERNS):
        return True

    if company_name:
        company_name_lower = company_name.lower()
        if company_name_lower not in text and company_name_lower not in url:
            return True

    if not any(keyword in text for keyword in (
        "fund",
        "funding",
        "raise",
        "launch",
        "launched",
        "acquisition",
        "acquired",
        "merger",
        "partnership",
        "partner",
        "product",
        "expan",
        "leadership",
        "ceo",
        "layoff",
        "lawsuit",
        "regulatory",
        "investigation",
        "approval",
        "restructur",
        "award",
        "contract",
    )):
        return True

    return False


def _deduplicate_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for result in results:
        url = _clean_text(result.get("url") or result.get("link"))
        title = _clean_text(result.get("title"))
        date = _normalize_date(result.get("published_date") or result.get("date") or result.get("timestamp"))
        key = url or f"{title}|{date}"
        if not key:
            continue
        key = key.lower().strip()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(result)
    return deduped


def normalize_news_results(raw_results: list[dict[str, Any]], company_name: str | None = None) -> list[NewsItem]:
    deduped = _deduplicate_results(raw_results or [])
    news_items: list[NewsItem] = []

    for result in deduped:
        title = _clean_text(result.get("title"))
        summary = _clean_text(result.get("content") or result.get("snippet") or result.get("summary") or title)
        url = _clean_text(result.get("url") or result.get("link"))
        source = _clean_text(result.get("source") or result.get("publisher") or result.get("author"))
        published_date = _normalize_date(result.get("published_date") or result.get("date") or result.get("timestamp"))

        if not title or not url:
            continue
        if _is_irrelevant(result, company_name):
            continue
        if _is_old_news(published_date):
            continue

        event_type = _event_type_from_text(title, summary)
        investment_impact = _investment_impact_for(event_type, title, summary)
        confidence = 70
        if source:
            confidence += 10
        if published_date:
            confidence += 5
        if event_type != "other":
            confidence += 10
        confidence = max(0, min(100, confidence))

        evidence = [
            Evidence(
                source=source or _slugify_source(urlparse(url).netloc or "Other"),
                quote=f"{title}. {summary}".strip(),
                confidence=confidence,
            )
        ]

        news_items.append(
            NewsItem(
                title=title,
                summary=summary,
                source=source or _slugify_source(urlparse(url).netloc or "Other"),
                url=url,
                published_date=published_date,
                event_type=event_type,
                investment_impact=investment_impact,
                confidence=confidence,
                evidence=evidence,
            )
        )

    news_items.sort(key=lambda item: item.published_date or "", reverse=True)
    return news_items


def search_company_news(company_url: str, company_name: str | None = None, max_results: int = 5) -> list[NewsItem]:
    """Collect recent, company-specific news using the existing Tavily search infrastructure."""
    if TavilyClient is None:
        return []

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return []

    try:
        client = TavilyClient(api_key=api_key)
        company_label = company_name or ""
        query = (
            f'"{company_label}" {company_url} company news '
            "funding acquisition merger partnership product launch leadership layoffs legal regulatory"
        ).strip()
        response = client.search(query=query, search_depth="advanced", max_results=max_results)
    except Exception:
        return []

    results = response.get("results", []) if isinstance(response, dict) else []
    return normalize_news_results(results, company_name=(company_name or company_url))
