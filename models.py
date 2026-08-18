from datetime import datetime, timezone

from pydantic import BaseModel, Field

from evidence import Evidence
from news_intelligence import NewsItem
from signals import InvestmentSignals


class SWOT(BaseModel):
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    opportunities: list[str] = Field(default_factory=list)
    threats: list[str] = Field(default_factory=list)


class Competitor(BaseModel):
    name: str = ""
    reason: str = ""
    evidence: list[Evidence] = Field(default_factory=list)


class Risk(BaseModel):
    title: str = ""
    description: str = ""
    evidence: list[Evidence] = Field(default_factory=list)

    def __str__(self) -> str:
        if self.description:
            return self.description
        return self.title


class CompanyAnalysis(BaseModel):
    company: str = ""
    summary: str = ""
    industry: str = ""
    business_model: str = ""

    products: list[str] = Field(default_factory=list)
    customers: list[str] = Field(default_factory=list)
    competitors: list[Competitor | str] = Field(default_factory=list)
    risks: list[Risk | str] = Field(default_factory=list)

    swot: SWOT = Field(default_factory=SWOT)

    signals: InvestmentSignals
    acquisition_score: int = 0
    recommendation: str = ""
    evidence: list[Evidence] = Field(default_factory=list)
    news: list[NewsItem] = Field(default_factory=list)


class CompanyComparisonResult(BaseModel):
    companies: list[CompanyAnalysis] = Field(default_factory=list)
    metrics: dict = Field(default_factory=dict)
    rankings: list[str] = Field(default_factory=list)
    key_differences: list[str] = Field(default_factory=list)
    winner: str | None = None
    insights: str = ""
    evidence: list[Evidence] = Field(default_factory=list)


class Portfolio(BaseModel):
    id: str = ""
    name: str = ""
    description: str = ""
    companies: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PortfolioResult(BaseModel):
    portfolio_name: str = ""
    company_count: int = 0
    companies: list[str] = Field(default_factory=list)
    metrics: dict = Field(default_factory=dict)
    risk_summary: dict[str, int] = Field(default_factory=dict)
    concentration: dict = Field(default_factory=dict)
    rankings: list[str] = Field(default_factory=list)
    insights: str = ""
    evidence: list[Evidence] = Field(default_factory=list)
    news: list[NewsItem] = Field(default_factory=list)