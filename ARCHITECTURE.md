# DealSense AI - Architecture

## Current Architecture

DealSense AI is a modular Python backend with two current entry surfaces: Streamlit in `app.py` and FastAPI in `api/main.py`.

```text
Streamlit or POST /api/analyze
              |
        pipeline.run_pipeline
              |
   Jina website context + Tavily research
              |
   Tavily company-news collection (best effort)
              |
        analysis.analyze_company
              |
   OpenAI-compatible LLM -> JSON -> Pydantic
              |
   evidence normalization -> CompanyAnalysis
              |
   scoring.calculate_score / recommendation.get_recommendation
              |
   Streamlit response or API response
```

The pipeline catches failures from external research and news collection and continues with empty context/results. LLM or validation failures are not similarly hidden by the pipeline.

## Modules and Data Models

- `app.py`: Streamlit form, analysis display, evidence display for competitors/risks, memo display, and explicit PDF creation/download.
- `pipeline.py`: orchestration entry point. It derives a company name from the URL, gathers Jina context, Tavily research, and news, then calls analysis.
- `research.py`: Jina AI Reader website text retrieval.
- `scraper.py`: direct Requests/BeautifulSoup text extraction utility; not used by the current pipeline path.
- `tavily_search.py`: external company research context.
- `news_intelligence.py`: Tavily news collection, filtering, deduplication, dates, controlled event types, impact classification, confidence, and evidence.
- `analysis.py`: prompt construction, LLM call, JSON cleanup/parsing, `CompanyAnalysis` validation, and evidence normalization.
- `prompts.py`: system prompt source.
- `llm.py`: OpenAI client configuration using environment credentials and a Groq-compatible base URL.
- `models.py`: `CompanyAnalysis`, `SWOT`, `Competitor`, `Risk`, `CompanyComparisonResult`, `Portfolio`, and `PortfolioResult`.
- `signals.py`: boolean investment signals and signal evidence mapping.
- `evidence.py`: evidence model with source, quote, and 0-100 confidence.
- `scoring.py`: deterministic score from supported investment signals, product count, and risk count, bounded by constants.
- `recommendation.py`: score-to-recommendation mapping.
- `cache.py`: MD5-keyed local pickle storage.
- `compare.py`: comparison over existing analyses, with comparison-specific cache use, score ranking, signal matrix, differences, winner, and deterministic insights. It does not generate PDFs or files.
- `portfolio.py`: lightweight portfolio aggregation over supplied analyses; it reuses comparison, evidence, and news data.
- `report.py`: deterministic Markdown investment memo.
- `pdf_report.py`: ReportLab PDF generation from one `CompanyAnalysis`.

`CompanyAnalysis` contains company metadata, products, customers, competitors, risks, SWOT, signals, acquisition score, recommendation, evidence, and news.

## External Services

- Jina AI Reader is called by `research.py`.
- Tavily is called for external research and, independently, normalized company news.
- The OpenAI client in `llm.py` calls the configured Groq-compatible endpoint using `DEFAULT_MODEL`.
- ReportLab is local PDF generation, not a remote service.

Credentials and exact runtime availability depend on environment variables and installed dependencies. No database or hosted persistence service is verified.

## Caching

`cache.py` stores Python objects as pickle files in `cache/`. `compare.py` uses it for comparison results. `pipeline.py` accepts `refresh` but does not read or write the cache, so normal company analyses are not cached through the orchestration path.

## Evidence and News Flows

The LLM schema requests evidence for competitors, risks, and each signal. `analysis.py` normalizes missing evidence to conservative placeholder evidence. News items receive source, URL, date, event type, investment impact, confidence, and evidence. News is attached to the returned `CompanyAnalysis` by `pipeline.py`; it is available to API consumers and portfolio aggregation, but has no dedicated Streamlit display.

## Comparison and Portfolio Flows

Comparison accepts at least two existing `CompanyAnalysis` objects. It reuses existing scores where present, calculates missing scores, builds signal metrics and rankings, identifies field differences, and returns `CompanyComparisonResult`.

Portfolio models store company names rather than duplicate analyses. `summarize_portfolio` resolves those names against caller-supplied analyses, calculates score metrics, aggregates risk titles, counts industry/business-model/signal concentration, ranks companies, and reuses comparison/evidence/news data. Neither flow has a Streamlit or FastAPI route.

## Memo and PDF Flow

`report.generate_report` returns a Markdown investment memo from a `CompanyAnalysis`. The Streamlit app displays it after analysis. PDF output is created only when the user presses the explicit PDF button; `pdf_report.py` writes the requested report path and the app provides it as a download. Comparison and portfolio functions do not generate PDFs.

## API Layer

FastAPI currently provides:

- `GET /health`
- `POST /api/analyze`

`/api/analyze` validates `HttpUrl`, forwards the normalized URL and `refresh` flag to `run_pipeline`, returns `CompanyAnalysis`, and maps pipeline exceptions to HTTP 502. CORS defaults to local frontend development ports. Comparison, evidence, news, memo, PDF, and portfolio APIs are not currently implemented.

## Planned Architecture

```text
Planned frontend workspaces
              |
        FastAPI API layer
              |
        Existing Python backend
```

The planned frontend is a responsive premium SaaS interface with a roughly 6-8 section scrolling landing narrative, followed by focused analysis, comparison, evidence, news, portfolio, and report/memo workspaces. React/Next.js, Tailwind, Framer Motion, authentication, persistence, background work, and additional routes remain future work unless later verified in source.

## Future-Agent Safety Rules

Inspect implementation before adding anything. Never duplicate an existing component or intelligence engine. Reuse existing models, services, evidence, news, scoring, and caching where appropriate. Do not alter working backend logic merely for a UI. Keep frontend/backend concerns separated through APIs, avoid unintended side effects, create PDFs only on explicit request, and run tests after modifications.
