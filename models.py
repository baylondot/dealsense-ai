from pydantic import BaseModel, Field

from evidence import Evidence
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