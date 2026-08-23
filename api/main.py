import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

from models import CompanyAnalysis
from pipeline import run_pipeline


def _cors_origins() -> list[str]:
    configured_origins = os.getenv("DEALSENSE_CORS_ORIGINS")
    if configured_origins:
        return [origin.strip() for origin in configured_origins.split(",") if origin.strip()]
    return ["http://localhost:3000", "http://localhost:5173"]


class AnalyzeRequest(BaseModel):
    url: HttpUrl
    refresh: bool = False


app = FastAPI(title="DealSense AI API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze", response_model=CompanyAnalysis)
def analyze_company(request: AnalyzeRequest) -> CompanyAnalysis:
    try:
        return run_pipeline(str(request.url), refresh=request.refresh)
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail="Company analysis could not be completed.",
        ) from error