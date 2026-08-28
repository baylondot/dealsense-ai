# DealSense AI - Project Context

## Product

DealSense AI is a Python due-diligence application for Private Equity, Venture Capital, M&A, investment banking, and acquisition users. A user supplies a company URL and receives structured company intelligence, investment signals, risks, SWOT analysis, an acquisition score, a recommendation, evidence, and recent news when available.

The repository is the source of truth. This document describes verified current behavior and separates it from future product direction.

## Current Capabilities

### Completed

- Company analysis through `analysis.py`, using structured JSON from an OpenAI-compatible client configured for a Groq-compatible endpoint and the model in `constants.py`.
- Website context collection through Jina AI Reader in `research.py` and external company research through Tavily in `tavily_search.py`.
- Pydantic models for company analysis, SWOT, competitors, risks, signals, evidence, news, comparison results, and portfolio results.
- Deterministic acquisition scoring in `scoring.py` and recommendation mapping in `recommendation.py`.
- Evidence normalization and confidence-bearing evidence objects in `evidence.py` and the analysis models.
- News collection and normalization in `news_intelligence.py`, including filtering, deduplication, event classification, investment impact, and evidence.
- Deterministic comparison of two or more existing `CompanyAnalysis` objects in `compare.py`.
- In-memory portfolio creation, membership management, metric aggregation, risk aggregation, concentration counts, ranking, and reuse of comparison/evidence/news data in `portfolio.py`.
- Investment memo text generation in `report.py`.
- Explicit PDF generation and download from the Streamlit application through `pdf_report.py`. PDF generation is not automatic.
- File-backed pickle caching in `cache.py`; currently used by comparison, not by the ordinary company-analysis pipeline.
- FastAPI `GET /health` and `POST /api/analyze` endpoints.

### Partially Implemented / Integration Required

- `pipeline.py` collects Jina context, Tavily research, and news, then calls analysis and attaches news. Its `refresh` argument is accepted but currently has no effect.
- Evidence and news are present in returned models and backend output. Streamlit shows evidence for competitors and risks, but has no dedicated news view or complete top-level evidence view.
- Comparison and portfolio are callable backend modules only. They are not connected to Streamlit or the API.
- Streamlit supports one-company analysis, memo display, and explicit PDF creation, but remains a basic temporary interface.
- `scraper.py` provides direct BeautifulSoup scraping but is not used by the current pipeline, which uses Jina Reader.
- Caching exists but is not a complete cache strategy for normal analysis runs.

### Planned

- A production frontend and dedicated analysis, comparison, evidence, news, portfolio, and report workspaces.
- Additional API endpoints exposing existing backend functionality.
- Authentication, persistence/database support, background jobs, history, analytics, and commercial SaaS features.

## Technical Stack Verified in Repository

- Python, Streamlit, FastAPI, and Pydantic
- OpenAI Python client configured with a Groq-compatible base URL
- Jina AI Reader via HTTP requests
- Tavily Search
- Requests and BeautifulSoup
- ReportLab for PDF output
- Local pickle files under `cache/`

No React, Next.js, JavaScript, TypeScript, database, Redis, Docker, or deployment configuration is currently verified in the repository.

## Current Interfaces

The current user interface is Streamlit. The API currently exposes only:

- `GET /health`
- `POST /api/analyze`, accepting a URL and optional `refresh`, returning `CompanyAnalysis`

The API has configurable CORS origins and defaults to local ports 3000 and 5173. No comparison, evidence, news, memo, report, or portfolio endpoint is currently implemented.

## Frontend Plan / Future

The intended frontend is a modern premium SaaS experience inspired by Linear and Vercel: responsive, typographically polished, with subtle gradients, smooth transitions, and scroll-based reveal/fade motion. The planned landing page has approximately 6-8 narrative sections, then transitions into focused workspaces for analysis, comparison, evidence, news, portfolio, and report/memo presentation across desktop, tablet, and mobile.

This frontend does not currently exist. The intended separation is:

```text
Frontend -> FastAPI API -> Existing DealSense Python backend
```

The API should expose existing functionality rather than duplicate intelligence engines.

## Architectural Principles for Future Agents

1. Inspect existing functionality before creating anything.
2. Never duplicate an existing component, model, service, or intelligence engine.
3. Reuse existing models and external services.
4. Do not modify working backend logic merely to accommodate a new UI.
5. Keep frontend and backend separated through APIs.
6. Avoid unintended side effects.
7. Generate PDFs/reports only when explicitly requested.
8. Reuse existing evidence and news functionality rather than duplicating it.
9. Test existing functionality after modifications.

## Known Limitations

- Research and LLM calls depend on external services and environment credentials.
- Normal analysis is not cached by the current pipeline, and `refresh` is not operational.
- Portfolio data is lightweight and in memory; no persistence layer is verified.
- Comparison and portfolio operations require existing `CompanyAnalysis` objects and have no application/API workflow.
- The production frontend, authentication, user accounts, history, and deployment system are not implemented.
