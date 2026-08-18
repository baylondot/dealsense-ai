from __future__ import annotations

from collections import Counter
from typing import Iterable

from compare import compare_companies
from models import CompanyAnalysis, Portfolio, PortfolioResult


def create_portfolio(name: str, description: str = "") -> Portfolio:
    """Create a portfolio with the project's lightweight in-memory model."""
    return Portfolio(id=f"portfolio-{abs(hash(name))}", name=name, description=description, companies=[])


def add_company(portfolio: Portfolio, company: CompanyAnalysis) -> Portfolio:
    """Add an existing CompanyAnalysis to the portfolio if it is not already present."""
    if not company or not company.company:
        raise ValueError("A valid company analysis is required.")

    if not portfolio:
        raise ValueError("Portfolio is required.")

    company_name = company.company.strip()
    if not company_name:
        raise ValueError("Company name is required.")

    if company_name in portfolio.companies:
        return portfolio

    portfolio.companies.append(company_name)
    return portfolio


def remove_company(portfolio: Portfolio, company_name: str) -> Portfolio:
    """Remove a company by name from a portfolio."""
    if not portfolio:
        raise ValueError("Portfolio is required.")

    portfolio.companies = [name for name in portfolio.companies if name != company_name]
    return portfolio


def _portfolio_companies(portfolio: Portfolio, companies: Iterable[CompanyAnalysis] | None = None) -> list[CompanyAnalysis]:
    if companies is None:
        return []

    by_name = {company.company: company for company in companies if getattr(company, "company", None)}
    ordered = []
    for name in portfolio.companies:
        company = by_name.get(name)
        if company is not None:
            ordered.append(company)
    return ordered


def _normalize_metric_value(value: int | float | None) -> int:
    if value is None:
        return 0
    return int(value)


def summarize_portfolio(portfolio: Portfolio, companies: Iterable[CompanyAnalysis] | None = None) -> PortfolioResult:
    """Aggregate existing company results into a deterministic portfolio summary."""
    if not portfolio:
        raise ValueError("Portfolio is required.")

    company_list = _portfolio_companies(portfolio, companies)

    if not company_list:
        raise ValueError("Portfolio is empty.")

    scores = [_normalize_metric_value(getattr(company, "acquisition_score", 0)) for company in company_list]
    average_score = sum(scores) // len(scores) if scores else 0

    metrics = {
        "average_acquisition_score": average_score,
        "highest_acquisition_score": max(scores) if scores else 0,
        "lowest_acquisition_score": min(scores) if scores else 0,
        "company_count": len(company_list),
    }

    risk_summary: dict[str, int] = {}
    for company in company_list:
        for risk in getattr(company, "risks", []) or []:
            title = getattr(risk, "title", None) or str(risk)
            risk_summary[title] = risk_summary.get(title, 0) + 1

    portfolio_companies = [company.company for company in company_list]
    concentration: dict[str, dict[str, int]] = {"industry": {}, "business_model": {}, "signals": {}}

    industry_counts = Counter(company.industry for company in company_list if getattr(company, "industry", None))
    concentration["industry"] = dict(sorted(industry_counts.items()))

    model_counts = Counter(company.business_model for company in company_list if getattr(company, "business_model", None))
    concentration["business_model"] = dict(sorted(model_counts.items()))

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
    signal_counts: dict[str, int] = {}
    for signal_name in signal_names:
        count = sum(1 for company in company_list if getattr(getattr(company, "signals", None), signal_name, False))
        if count:
            signal_counts[signal_name] = count
    concentration["signals"] = signal_counts

    rankings = [company.company for company in sorted(company_list, key=lambda company: _normalize_metric_value(getattr(company, "acquisition_score", 0)), reverse=True)]
    comparison = compare_companies(company_list)

    evidence = []
    for company in company_list:
        evidence.extend(getattr(company, "evidence", []) or [])

    news = []
    for company in company_list:
        news.extend(getattr(company, "news", []) or [])

    if comparison and getattr(comparison, "insights", None):
        insight_lines = [comparison.insights]
    else:
        insight_lines = [f"Portfolio contains {len(company_list)} companies."]
    insight_lines.append(f"Highest scoring company: {rankings[0] if rankings else 'N/A'}")

    return PortfolioResult(
        portfolio_name=portfolio.name,
        company_count=len(company_list),
        companies=portfolio_companies,
        metrics=metrics,
        risk_summary=risk_summary,
        concentration=concentration,
        rankings=rankings,
        insights="\n".join(insight_lines),
        evidence=evidence,
        news=news,
    )
