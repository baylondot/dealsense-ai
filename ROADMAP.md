# DealSense AI - Roadmap

The repository is currently a v0.1-style backend foundation with a functional Streamlit interface and a minimal FastAPI surface. Status below reflects source code, not earlier plans.

## Completed

- Modular Python project structure and shared constants.
- LLM-driven structured company analysis with JSON parsing and Pydantic validation.
- Jina website research and Tavily external research in the active pipeline.
- Deterministic acquisition scoring and recommendation generation.
- Company metadata, products, customers, competitors, risks, SWOT, investment signals, and evidence models.
- News intelligence collection and normalization attached to pipeline results.
- Deterministic comparison over two or more existing company analyses.
- Lightweight portfolio creation, membership, aggregation, concentration counts, rankings, and reuse of existing intelligence.
- Investment memo generation.
- Explicit ReportLab PDF creation and Streamlit download workflow.
- Local pickle cache, currently used by comparison.
- Streamlit one-company analysis workflow.
- FastAPI `GET /health` and `POST /api/analyze` endpoints with URL validation, pipeline delegation, CORS, and error mapping.

## Integration / Stabilization

- Connect comparison and portfolio operations to an application workflow or API if those workflows are needed.
- Add dedicated Streamlit/API presentation for news and the full top-level evidence collection.
- Decide and implement the normal-analysis cache policy; the pipeline's `refresh` parameter currently has no effect.
- Decide whether the direct scraper utility should remain separate or be integrated; the active pipeline uses Jina Reader.
- Strengthen runtime and integration validation around external credentials, LLM output, research failures, and generated files.
- Confirm test-suite execution in the target environment. Existing tests cover API, evidence/memo/PDF, comparison, and portfolio behavior, but passing status is not inferred from their presence.
- Keep PDF/report generation explicitly user-triggered and prevent unintended filesystem side effects.

## Next

- Stabilize the existing backend contracts and API response behavior.
- Add only the API routes required to expose existing comparison, evidence, news, memo, report, or portfolio functionality.
- Establish persistence and history requirements before adding database-backed features.
- Improve analysis quality and evidence/source presentation based on verified test cases.
- Define a frontend/backend contract before building a new frontend.

## Future

- Planned frontend: a modern premium SaaS experience inspired by Linear/Vercel, with elegant typography, subtle gradients, smooth transitions, scroll-based reveal/fade animations, and responsive desktop/tablet/mobile behavior.
- Planned landing page: approximately 6-8 major narrative sections, transitioning into focused workspaces rather than making users operate inside a long scrolling page.
- Planned workspaces: analysis, comparison, evidence, news intelligence, portfolio, and report/memo presentation.
- Planned API evolution: expose existing backend functionality through FastAPI without duplicating backend intelligence.
- Authentication, user accounts, saved analyses, research history, database persistence, background jobs, usage analytics, team workspaces, billing, and deployment infrastructure.

## Frontend Plan / Not Implemented

The intended frontend is explicitly future work. No React, Next.js, JavaScript, TypeScript, Tailwind, or Framer Motion application is currently verified. The intended boundary is:

```text
Frontend -> FastAPI API -> Existing DealSense Python backend
```

The landing page should tell a scrolling product story, then hand users into focused workspaces for repeated diligence work. This plan must not be treated as an implemented interface.

## Engineering Rules

1. Inspect existing functionality before creating anything.
2. Never duplicate an existing component or intelligence engine.
3. Reuse existing models and services.
4. Do not modify working backend logic merely to accommodate a new UI.
5. Keep frontend and backend separated through APIs.
6. Avoid unintended side effects.
7. Generate PDFs/reports only when explicitly requested.
8. Reuse existing evidence and news functionality.
9. Test existing functionality after modifications.
