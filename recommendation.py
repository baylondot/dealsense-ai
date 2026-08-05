def get_recommendation(score: int):

    if score >= 85:
        return "★★★★★ Strong Acquisition Target"

    if score >= 70:
        return "★★★★ Worth Further Due Diligence"

    if score >= 55:
        return "★★★ Monitor"

    if score >= 40:
        return "★★ Weak Opportunity"

    return "★ Avoid"