from models import CompanyAnalysis
from compare import compare_companies


def _sample_company(name: str, score: int = None, signals: dict | None = None) -> CompanyAnalysis:
    return CompanyAnalysis(
        company=name,
        summary="Sample",
        industry="SaaS" if name == "A" else "Workflow",
        business_model="Subscription" if name == "A" else "Freemium",
        products=["P1"],
        customers=["C1"],
        competitors=[],
        risks=[],
        swot={"strengths": [], "weaknesses": [], "opportunities": [], "threats": []},
        signals=signals or {},
        acquisition_score=score or 0,
        recommendation="",
    )


def test_two_company_comparison():
    a = _sample_company("A", score=80, signals={"is_saas": True, "recurring_revenue": True})
    b = _sample_company("B", score=70, signals={"is_saas": False, "recurring_revenue": False})

    result = compare_companies([a, b])

    assert result.winner == "A"
    assert "acquisition_score" in result.metrics
    assert result.metrics["acquisition_score"]["A"] == 80


def test_three_company_comparison():
    a = _sample_company("A", score=60)
    b = _sample_company("B", score=75)
    c = _sample_company("C", score=50)

    result = compare_companies([a, b, c])

    assert result.rankings[0] == "B"
    assert len(result.companies) == 3


def test_missing_company_data_raises():
    try:
        compare_companies([_sample_company("A")])
        assert False, "Expected ValueError for fewer than two companies"
    except ValueError:
        pass


def test_preserves_existing_scores():
    a = _sample_company("A", score=88)
    b = _sample_company("B", score=72)

    result = compare_companies([a, b])
    assert result.metrics["acquisition_score"]["A"] == 88
    assert result.metrics["acquisition_score"]["B"] == 72


def test_does_not_generate_pdf_or_files(tmp_path):
    a = _sample_company("A", score=60)
    b = _sample_company("B", score=70)

    result = compare_companies([a, b])

    # Ensure no reports were created
    reports = list(tmp_path.glob("**/*.pdf"))
    assert reports == []
