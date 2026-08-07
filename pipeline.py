from analysis import analyze_company


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

    result = analyze_company(
        url=url,
        refresh=refresh
    )

    return result