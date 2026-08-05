from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_company(company_url: str):

    response = client.search(
        query=f"{company_url} company business model competitors funding",
        search_depth="advanced",
        max_results=5,
    )

    context = ""

    for result in response["results"]:
        context += f"""
Title:
{result["title"]}

Content:
{result["content"]}

URL:
{result["url"]}

----------------------------
"""

    return context