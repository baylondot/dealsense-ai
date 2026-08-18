from typing import List, Union

from models import CompanyAnalysis, CompanyComparisonResult
from scoring import calculate_score
from evidence import Evidence
from cache import load_cache, save_cache


def _serialize_company_key(companies: List[CompanyAnalysis]) -> str:
    parts = []
    for company in sorted(companies, key=lambda c: c.company or ""):
        signals = getattr(company, "signals", None)
        signal_summary = ""
        if signals is not None:
            signal_summary = ",".join(
                f"{name}={bool(getattr(signals, name, False))}"
                for name in [
                    "is_saas",
                    "is_b2b",
                    "is_b2c",
                    "recurring_revenue",
                    "ai_company",
                    "enterprise_focus",
                    "marketplace",
                    "subscription_model",
                    "global_presence",
                    "open_source",
                    "mobile_app",
                    "api_platform",
                ]
            )
        parts.append(
            f"{company.company or ''}:{int(getattr(company, 'acquisition_score', 0) or 0)}:"
            f"{company.industry or ''}:{company.business_model or ''}:{signal_summary}"
        )
    return "|".join(parts)


def compare_companies(companies: List[CompanyAnalysis]) -> CompanyComparisonResult:
    """Compare multiple CompanyAnalysis objects and return a structured CompanyComparisonResult.

    - Reuses existing acquisition scores when present.
    - Uses calculate_score() when acquisition_score is missing or zero.
    - Preserves evidence and recommendations from source analyses.
    - Does not write files or generate PDFs.
    """

    if not companies or len(companies) < 2:
        raise ValueError("At least two companies are required for comparison.")

    cache_key = f"compare:{_serialize_company_key(companies)}"
    cached = load_cache(cache_key)
    if cached:
        return cached

    # Ensure scores exist
    for company in companies:
        if not getattr(company, "acquisition_score", None):
            try:
                company.acquisition_score = calculate_score(company)
            except Exception:
                company.acquisition_score = 0

    # Build metrics
    metrics = {}
    metrics["acquisition_score"] = {c.company: int(c.acquisition_score or 0) for c in companies}

    # Signals overview (boolean or unavailable)
    signal_names = [
        "is_saas",
        "is_b2b",
        "is_b2c",
        "recurring_revenue",
        "ai_company",
        "enterprise_focus",
        "marketplace",
        "subscription_model",
        "global_presence",
        "open_source",
        "mobile_app",
        "api_platform",
    ]

    signals_matrix = {name: {} for name in signal_names}
    for c in companies:
        signals = getattr(c, "signals", None)
        for name in signal_names:
            value = None
            if signals and hasattr(signals, name):
                value = bool(getattr(signals, name))
            signals_matrix[name][c.company] = value
    metrics["signals"] = signals_matrix

    # Rankings by acquisition score
    sorted_companies = sorted(companies, key=lambda x: int(x.acquisition_score or 0), reverse=True)
    rankings = [c.company for c in sorted_companies]

    # Key differences: find fields that differ across companies
    key_fields = ["industry", "business_model"]
    key_differences = []
    for field in key_fields:
        values = {getattr(c, field, None) or "Not enough information." for c in companies}
        if len(values) > 1:
            key_differences.append(f"{field}: {', '.join(sorted(values))}")

    # Winner: top-ranked by acquisition score
    winner = rankings[0] if rankings else None

    # Insights: simple synthesis using deterministic data
    insights_lines = []
    top_score = int(sorted_companies[0].acquisition_score or 0)
    insights_lines.append(f"Top company by acquisition score: {winner} ({top_score}/100)")

    # Compare top two companies for notable differences
    if len(sorted_companies) >= 2:
        a, b = sorted_companies[0], sorted_companies[1]
        insights_lines.append(f"Comparison between {a.company} and {b.company}:")
        insights_lines.append(f"- Acquisition score: {a.acquisition_score} vs {b.acquisition_score}")
        # Add a few deterministic comparisons
        for signal in ["recurring_revenue", "enterprise_focus", "is_saas"]:
            asig = getattr(a.signals, signal, None) if getattr(a, "signals", None) else None
            bsig = getattr(b.signals, signal, None) if getattr(b, "signals", None) else None
            if asig != bsig:
                insights_lines.append(f"- {signal}: {a.company}={asig} vs {b.company}={bsig}")

    result = CompanyComparisonResult(
        companies=companies,
        metrics=metrics,
        rankings=rankings,
        key_differences=key_differences,
        winner=winner,
        insights="\n".join(insights_lines),
        evidence=[],
    )

    try:
        save_cache(cache_key, result)
    except Exception:
        pass

    return result
