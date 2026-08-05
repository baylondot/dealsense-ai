from scraper import scrape_website
from research import get_company_context
from tavily_search import search_company


def collect_data(url: str) -> dict:
    """
    Collect all raw data required for analysis.
    """

    html = scrape_website(url)

    clean_text = get_company_context(url)

    external_research = search_company(url)

    return {
        "url": url,
        "html": html,
        "clean_text": clean_text,
        "external_research": external_research,
    }