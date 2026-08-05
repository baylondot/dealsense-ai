from pydantic import BaseModel
from signals import InvestmentSignals

class SWOT(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    opportunities: list[str]
    threats: list[str]

class Competitor(BaseModel):
    name: str
    reason: str

class CompanyAnalysis(BaseModel):
    company: str
    summary: str
    industry: str
    business_model: str

    # Keep products simple for now.
    # We'll upgrade them to Product objects later once
    # we enforce structured output from the LLM.
    products: list[str]

    customers: list[str]
    competitors: list[Competitor]
    risks: list[str]

    swot: SWOT

    signals: InvestmentSignals
    acquisition_score: int
    recommendation: str