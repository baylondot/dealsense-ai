from pydantic import BaseModel, Field

from evidence import Evidence


class InvestmentSignals(BaseModel):
    is_saas: bool = False
    is_b2b: bool = False
    is_b2c: bool = False

    recurring_revenue: bool = False

    ai_company: bool = False

    enterprise_focus: bool = False

    marketplace: bool = False

    subscription_model: bool = False

    global_presence: bool = False

    open_source: bool = False

    mobile_app: bool = False

    api_platform: bool = False

    evidence: dict[str, list[Evidence]] = Field(default_factory=dict)