from models import CompanyAnalysis


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
