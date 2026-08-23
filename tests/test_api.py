from fastapi.testclient import TestClient

from api.main import app
from evidence import Evidence
from models import CompanyAnalysis
from signals import InvestmentSignals


client = TestClient(app)


def _sample_analysis() -> CompanyAnalysis:
    return CompanyAnalysis(
        company="Example",
        summary="A sample company.",
        signals=InvestmentSignals(),
        evidence=[Evidence(source="Website", quote="Example", confidence=80)],
    )


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_delegates_to_pipeline(monkeypatch) -> None:
    calls = []

    def fake_run_pipeline(url: str, refresh: bool = False) -> CompanyAnalysis:
        calls.append((url, refresh))
        return _sample_analysis()

    monkeypatch.setattr("api.main.run_pipeline", fake_run_pipeline)

    response = client.post(
        "/api/analyze",
        json={"url": "https://example.com", "refresh": True},
    )

    assert response.status_code == 200
    assert calls == [("https://example.com/", True)]
    assert response.json()["company"] == "Example"
    assert response.json()["signals"]["is_saas"] is False


def test_analyze_rejects_invalid_url() -> None:
    response = client.post("/api/analyze", json={"url": "not-a-url"})

    assert response.status_code == 422


def test_analyze_hides_pipeline_errors(monkeypatch) -> None:
    def failing_run_pipeline(url: str, refresh: bool = False) -> CompanyAnalysis:
        raise RuntimeError("secret backend details")

    monkeypatch.setattr("api.main.run_pipeline", failing_run_pipeline)

    response = client.post("/api/analyze", json={"url": "https://example.com"})

    assert response.status_code == 502
    assert response.json() == {"detail": "Company analysis could not be completed."}
    assert "secret backend details" not in response.text


def test_analyze_cors_for_local_frontend() -> None:
    response = client.options(
        "/api/analyze",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"