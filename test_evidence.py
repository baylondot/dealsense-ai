from pathlib import Path

from models import CompanyAnalysis
from news_intelligence import NewsItem, normalize_news_results
from report import generate_report


def test_evidence_fields_are_supported():
    analysis = CompanyAnalysis(
        company="Acme",
        summary="Acme is a B2B SaaS company.",
        industry="SaaS",
        business_model="Subscription",
        products=["Platform"],
        customers=["Enterprise customers"],
        competitors=[
            {
                "name": "Competitor One",
                "reason": "Competes in the same workflow category.",
                "evidence": [
                    {
                        "source": "Website",
                        "quote": "We help teams automate workflows.",
                        "confidence": 87,
                    }
                ],
            }
        ],
        risks=[
            {
                "title": "Customer concentration",
                "description": "The company relies on a few large customers.",
                "evidence": [
                    {
                        "source": "Tavily",
                        "quote": "The company lists three customers that account for most revenue.",
                        "confidence": 91,
                    }
                ],
            }
        ],
        swot={
            "strengths": ["Strong product"],
            "weaknesses": ["Limited brand"],
            "opportunities": ["Expansion"],
            "threats": ["Competition"],
        },
        signals={
            "is_saas": True,
            "is_b2b": True,
            "is_b2c": False,
            "recurring_revenue": True,
            "ai_company": False,
            "enterprise_focus": True,
            "marketplace": False,
            "subscription_model": True,
            "global_presence": False,
            "open_source": False,
            "mobile_app": False,
            "api_platform": True,
            "evidence": {
                "is_saas": [
                    {
                        "source": "Website",
                        "quote": "Subscription pricing for enterprise customers.",
                        "confidence": 88,
                    }
                ]
            },
        },
        acquisition_score=72,
        recommendation="Worth further due diligence.",
    )

    assert analysis.competitors[0].evidence[0].source == "Website"
    assert analysis.risks[0].evidence[0].confidence == 91
    assert analysis.signals.evidence["is_saas"][0].source == "Website"


def test_investment_memo_has_required_sections():
    analysis = CompanyAnalysis(
        company="Acme",
        summary="Acme operates a subscription software platform for enterprise teams.",
        industry="SaaS",
        business_model="Subscription-based workflow platform",
        products=["Workflow platform"],
        customers=["Enterprise customers"],
        competitors=[
            {
                "name": "Competitor One",
                "reason": "Competes in the same flow automation category.",
                "evidence": [
                    {
                        "source": "Website",
                        "quote": "We help teams automate workflows.",
                        "confidence": 87,
                    }
                ],
            }
        ],
        risks=[
            {
                "title": "Customer concentration",
                "description": "Revenue depends on a small number of enterprise accounts.",
                "evidence": [
                    {
                        "source": "Tavily",
                        "quote": "The company lists three customers that account for most revenue.",
                        "confidence": 94,
                    }
                ],
            }
        ],
        swot={
            "strengths": ["Strong product-market fit"],
            "weaknesses": ["Limited brand recognition"],
            "opportunities": ["Expansion into adjacent workflows"],
            "threats": ["Competitive pricing pressure"],
        },
        signals={
            "is_saas": True,
            "is_b2b": True,
            "is_b2c": False,
            "recurring_revenue": True,
            "ai_company": False,
            "enterprise_focus": True,
            "marketplace": False,
            "subscription_model": True,
            "global_presence": False,
            "open_source": False,
            "mobile_app": False,
            "api_platform": True,
            "evidence": {
                "is_saas": [
                    {
                        "source": "Website",
                        "quote": "Subscription pricing for enterprise customers.",
                        "confidence": 89,
                    }
                ]
            },
        },
        acquisition_score=74,
        recommendation="Worth further due diligence.",
    )

    memo = generate_report(analysis)
    for section in [
        "## Executive Summary",
        "## Investment Thesis",
        "## Business Model",
        "## Risks",
        "## Opportunities",
        "## SWOT",
        "## Acquisition Score",
        "## Recommendation",
    ]:
        assert section in memo


def test_generate_pdf_report_creates_a_file_from_company_analysis(tmp_path):
    from pdf_report import generate_pdf_report

    analysis = CompanyAnalysis(
        company="Acme",
        summary="Acme operates a subscription software platform for enterprise teams.",
        industry="SaaS",
        business_model="Subscription-based workflow platform",
        products=["Workflow platform", "API suite"],
        customers=["Enterprise customers", "Mid-market accounts"],
        competitors=[
            {
                "name": "Competitor One",
                "reason": "Competes in the same workflow category.",
                "evidence": [{"source": "Website", "quote": "We automate workflows.", "confidence": 85}],
            }
        ],
        risks=[
            {
                "title": "Customer concentration",
                "description": "Revenue depends on a small number of enterprise accounts.",
                "evidence": [{"source": "Tavily", "quote": "Top three customers drive most revenue.", "confidence": 90}],
            }
        ],
        swot={
            "strengths": ["Strong product-market fit"],
            "weaknesses": ["Limited brand recognition"],
            "opportunities": ["Expansion into adjacent workflows"],
            "threats": ["Competitive pricing pressure"],
        },
        signals={
            "is_saas": True,
            "is_b2b": True,
            "is_b2c": False,
            "recurring_revenue": True,
            "ai_company": False,
            "enterprise_focus": True,
            "marketplace": False,
            "subscription_model": True,
            "global_presence": False,
            "open_source": False,
            "mobile_app": False,
            "api_platform": True,
            "evidence": {"is_saas": [{"source": "Website", "quote": "Subscription pricing for enterprise customers.", "confidence": 88}]},
        },
        acquisition_score=74,
        recommendation="Worth further due diligence.",
    )

    output_path = tmp_path / "acme_report.pdf"
    generated_path = generate_pdf_report(analysis, str(output_path))

    assert generated_path == str(output_path)
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_app_requires_an_explicit_pdf_generation_button():
    app_source = Path("app.py").read_text(encoding="utf-8")

    assert 'if st.button("📄 Create PDF Report"' in app_source
    create_button_index = app_source.index('if st.button("📄 Create PDF Report"')
    pdf_call_index = app_source.index('generate_pdf_report(')

    assert create_button_index < pdf_call_index


def test_news_intelligence_filters_irrelevant_or_duplicate_results():
    raw_results = [
        {
            "title": "Acme Launches New AI Platform",
            "content": "Acme today announced the launch of its new AI platform for enterprise teams, expanding its product offering.",
            "url": "https://example.com/acme-launches-ai-platform",
            "published_date": "2026-08-01T12:00:00Z",
            "source": "Reuters",
        },
        {
            "title": "Acme Launches New AI Platform",
            "content": "Duplicate article with same launch information.",
            "url": "https://example.com/acme-launches-ai-platform",
            "published_date": "2026-08-01T12:00:00Z",
            "source": "Reuters",
        },
        {
            "title": "Acme Company Overview",
            "content": "Acme is a technology company that helps customers with software solutions.",
            "url": "https://example.com/acme-overview",
            "published_date": "2025-01-05T05:00:00Z",
            "source": "Crunchbase",
        },
        {
            "title": "Acme has a team lunch in Seattle",
            "content": "The company held a lunch event for employees.",
            "url": "https://example.com/acme-lunch",
            "published_date": "2026-08-02T00:00:00Z",
            "source": "Local Blog",
        },
    ]

    news = normalize_news_results(raw_results, company_name="Acme")

    assert len(news) == 1
    assert news[0].title == "Acme Launches New AI Platform"
    assert news[0].event_type == "product_launch"
    assert news[0].source == "Reuters"
    assert news[0].url == "https://example.com/acme-launches-ai-platform"
    assert news[0].published_date == "2026-08-01T12:00:00Z"
    assert news[0].investment_impact in {"positive", "neutral", "unclear"}


def test_company_analysis_accepts_news_items():
    analysis = CompanyAnalysis(
        company="Acme",
        summary="Acme is a growing software company.",
        industry="SaaS",
        business_model="Subscription",
        products=["Platform"],
        customers=["Customers"],
        competitors=[],
        risks=[],
        swot={"strengths": ["Strong product"], "weaknesses": [], "opportunities": [], "threats": []},
        signals={
            "is_saas": True,
            "is_b2b": True,
            "is_b2c": False,
            "recurring_revenue": True,
            "ai_company": True,
            "enterprise_focus": True,
            "marketplace": False,
            "subscription_model": True,
            "global_presence": False,
            "open_source": False,
            "mobile_app": False,
            "api_platform": True,
            "evidence": {
                "is_saas": [{"source": "Website", "quote": "Subscription product", "confidence": 80}],
                "is_b2b": [{"source": "Website", "quote": "Enterprise customers", "confidence": 82}],
                "is_b2c": [{"source": "Website", "quote": "Not consumer-facing", "confidence": 60}],
                "recurring_revenue": [{"source": "Website", "quote": "Subscription pricing", "confidence": 85}],
                "ai_company": [{"source": "Website", "quote": "AI features", "confidence": 74}],
                "enterprise_focus": [{"source": "Website", "quote": "Enterprise customers", "confidence": 80}],
                "marketplace": [{"source": "Website", "quote": "No marketplace", "confidence": 70}],
                "subscription_model": [{"source": "Website", "quote": "Subscription pricing", "confidence": 85}],
                "global_presence": [{"source": "Website", "quote": "No global claim", "confidence": 50}],
                "open_source": [{"source": "Website", "quote": "Proprietary product", "confidence": 65}],
                "mobile_app": [{"source": "Website", "quote": "No mobile app", "confidence": 60}],
                "api_platform": [{"source": "Website", "quote": "API integration", "confidence": 75}],
            },
        },
        acquisition_score=75,
        recommendation="Worth pursuing.",
        news=[
            NewsItem(
                title="Acme Launches New AI Platform",
                summary="Acme introduced a new AI platform.",
                source="Reuters",
                url="https://example.com/acme-launches-ai-platform",
                published_date="2026-08-01T12:00:00Z",
                event_type="product_launch",
                investment_impact="positive",
                confidence=88,
                evidence=[{"source": "Reuters", "quote": "Acme launched a new AI platform.", "confidence": 88}],
            )
        ],
    )

    assert analysis.news[0].event_type == "product_launch"
    assert analysis.news[0].evidence[0].source == "Reuters"
