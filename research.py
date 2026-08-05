import requests


def get_company_context(url: str) -> str:
    """
    Fetches a clean text version of a website using Jina AI Reader.
    """

    jina_url = f"https://r.jina.ai/http://{url.replace('https://', '').replace('http://', '')}"

    try:
        response = requests.get(jina_url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception:
        return ""