from pydantic import BaseModel


class InvestmentSignals(BaseModel):
    is_saas: bool
    is_b2b: bool
    is_b2c: bool

    recurring_revenue: bool

    ai_company: bool

    enterprise_focus: bool

    marketplace: bool

    subscription_model: bool

    global_presence: bool

    open_source: bool

    mobile_app: bool

    api_platform: bool