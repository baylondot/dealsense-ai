from evidence import Evidence
from models import CompanyAnalysis, Portfolio
from news_intelligence import NewsItem
from portfolio import add_company, create_portfolio, remove_company, summarize_portfolio
from signals import InvestmentSignals


def _company(name: str, score: int, industry: str, business_model: str, *, risk_titles=None, news_items=None):
    return CompanyAnalysis(
        company=name,
        summary=f"{name} summary",
        industry=industry,
        business_model=business_model,
        products=["Product 1"],
        customers=["Customer A"],
        competitors=[],
        risks=[
            {"title": risk_title, "description": f"{risk_title} risk", "evidence": [{"source": "Website", "quote": f"{risk_title} risk evidence", "confidence": 80}]}
            for risk_title in (risk_titles or [])
        ],
        swot={"strengths": [], "weaknesses": [], "opportunities": [], "threats": []},
        signals=InvestmentSignals(
            is_saas=industry == "SaaS",
            is_b2b=business_model in {"Subscription", "B2B"},
            is_b2c=business_model == "B2C",
            recurring_revenue=True,
            ai_company=industry == "AI",
            enterprise_focus=True,
            subscription_model=business_model == "Subscription",
            global_presence=False,
            open_source=False,
            mobile_app=False,
            api_platform=True,
        ),
        acquisition_score=score,
        recommendation="Proceed with caution",
        evidence=[Evidence(source="Website", quote=f"Evidence for {name}", confidence=85)],
        news=news_items or [],
    )


def test_create_and_manage_portfolio():
    portfolio = create_portfolio("Acme Portfolio", "A portfolio of software companies")
    alpha = _company("Alpha", 82, "SaaS", "Subscription")
    beta = _company("Beta", 68, "AI", "B2B")

    portfolio = add_company(portfolio, alpha)
    portfolio = add_company(portfolio, beta)

    assert portfolio.name == "Acme Portfolio"
    assert len(portfolio.companies) == 2
    assert "Alpha" in portfolio.companies
    assert "Beta" in portfolio.companies

    portfolio = remove_company(portfolio, "Alpha")
    assert "Alpha" not in portfolio.companies
    assert len(portfolio.companies) == 1


def test_portfolio_metrics_and_risk_aggregation():
    alpha = _company("Alpha", 90, "SaaS", "Subscription", risk_titles=["Regulatory", "Competition"])
    beta = _company("Beta", 75, "AI", "B2B", risk_titles=["Regulatory"])
    gamma = _company("Gamma", 55, "SaaS", "B2C", risk_titles=[])

    portfolio = create_portfolio("Portfolio A")
    for company in [alpha, beta, gamma]:
        portfolio = add_company(portfolio, company)

    result = summarize_portfolio(portfolio, [alpha, beta, gamma])

    assert result.company_count == 3
    assert result.metrics["average_acquisition_score"] == 73
    assert result.metrics["highest_acquisition_score"] == 90
    assert result.metrics["lowest_acquisition_score"] == 55
    assert result.risk_summary["Regulatory"] == 2
    assert result.risk_summary["Competition"] == 1
    assert result.concentration["industry"]["SaaS"] == 2
    assert result.rankings[0] == "Alpha"


def test_portfolio_concentration_and_news_integration():
    alpha = _company("Alpha", 80, "SaaS", "Subscription", news_items=[NewsItem(title="Alpha raises funding", summary="Strong funding round", source="TechCrunch", url="https://example.com/alpha", confidence=80)])
    beta = _company("Beta", 70, "SaaS", "Subscription", news_items=[NewsItem(title="Beta launches product", summary="New launch", source="The Verge", url="https://example.com/beta", confidence=75)])
    gamma = _company("Gamma", 40, "Fintech", "B2C", news_items=[])

    portfolio = create_portfolio("Portfolio B")
    for company in [alpha, beta, gamma]:
        portfolio = add_company(portfolio, company)

    result = summarize_portfolio(portfolio, [alpha, beta, gamma])

    assert result.concentration["business_model"]["Subscription"] == 2
    assert result.concentration["signals"]["is_saas"] == 2
    assert len(result.news) == 2
    assert "Alpha raises funding" in [item.title for item in result.news]


def test_portfolio_reuses_company_comparison_and_evidence():
    alpha = _company("Alpha", 82, "SaaS", "Subscription", risk_titles=["Regulatory"])
    beta = _company("Beta", 74, "SaaS", "Subscription", risk_titles=["Competition"])

    portfolio = create_portfolio("Portfolio C")
    for company in [alpha, beta]:
        portfolio = add_company(portfolio, company)

    result = summarize_portfolio(portfolio, [alpha, beta])

    assert result.rankings == ["Alpha", "Beta"]
    assert result.evidence[0].source == "Website"
    assert result.evidence[0].quote.startswith("Evidence for")


def test_portfolio_does_not_generate_pdf_files():
    alpha = _company("Alpha", 76, "SaaS", "Subscription")
    beta = _company("Beta", 71, "AI", "B2B")

    portfolio = create_portfolio("Portfolio D")
    for company in [alpha, beta]:
        portfolio = add_company(portfolio, company)

    result = summarize_portfolio(portfolio, [alpha, beta])

    assert result.company_count == 2
    assert not hasattr(result, "pdf_path")
