from analysis import analyze_company
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

    combined_context = (
        "Website context:\n"
        f"{website_context}\n\n"
        "External research:\n"
        f"{external_context}"
    )

    return analyze_company(research_context=combined_context)