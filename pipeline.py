from urllib.parse import urlparse

from analysis import analyze_company
from news_intelligence import search_company_news
from research import get_company_context
from tavily_search import search_company


def run_pipeline(url: str, refresh: bool = False):
    """
    Main orchestration function.

    This is the single entry point for the entire
    due diligence workflow.

    Future stages:
    - Cache
    - Parallel research
    - Multi-agent execution
    - Logging
    - Metrics
    """

    website_context = get_company_context(url) or ""

    try:
        external_context = search_company(url)
    except Exception:
        external_context = ""

    company_name = urlparse(url).netloc.replace("www.", "").split(":")[0]
    try:
        news_items = search_company_news(url, company_name=company_name, max_results=5)
    except Exception:
        news_items = []

    combined_context = (
        "Website context:\n"
        f"{website_context}\n\n"
        "External research:\n"
        f"{external_context}"
    )

    analysis = analyze_company(research_context=combined_context)
    analysis.news = news_items
    return analysis