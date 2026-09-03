# DealSense AI — Frontend

This is the independent frontend model for DealSense AI.

## Current architecture

Frontend → FastAPI → existing Python backend

The verified backend currently exposes:

- `GET /health`
- `POST /api/analyze`

The other workspaces are intentionally UI-ready and use isolated mock data until their corresponding APIs exist.

## Run

```bash
npm install
copy .env.example .env.local
npm run dev
```

Then open `http://localhost:3000`.

For live analysis, set:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_USE_MOCK=false
```

The frontend calls:

```text
POST /api/analyze
{
  "url": "https://example.com",
  "refresh": false
}
```

It expects the existing `CompanyAnalysis` JSON response.

## Important

- No Python code is imported by the frontend.
- No provider API keys belong in the frontend.
- Mock data is isolated in `lib/mock.ts`.
- API access is isolated in `lib/api.ts`.
- PDF/report generation is never triggered by analysis.
- Comparison, evidence, news, reports and portfolio screens do not claim to be live until their APIs are actually exposed.

This project intentionally does not include `node_modules`.
