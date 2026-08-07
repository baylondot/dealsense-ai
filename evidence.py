from pydantic import BaseModel, Field


class Evidence(BaseModel):
    source: str = "Other"
    quote: str = ""
    confidence: int = Field(default=0, ge=0, le=100)

    def __str__(self) -> str:
        return f"{self.source} ({self.confidence}/100): {self.quote}"