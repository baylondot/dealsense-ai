from models import CompanyAnalysis
from constants import MAX_SCORE, MIN_SCORE

def calculate_score(company: CompanyAnalysis) -> int:
    score = 50

    signals = company.signals
    score = 50

    if signals.is_saas:
        score += 10

    if signals.subscription_model:
        score += 10

    if signals.ai_company:
        score += 6

    if signals.enterprise_focus:
        score += 7

    if signals.recurring_revenue:
        score += 8

    if signals.global_presence:
        score += 5

    if signals.api_platform:
        score += 4

    if signals.marketplace:
        score += 3

    if len(company.products) >= 5:
        score += 5

    if len(company.risks) >= 5:
        score -= 8


    return max(MIN_SCORE, min(score, MAX_SCORE))