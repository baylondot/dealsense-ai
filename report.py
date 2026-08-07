from models import CompanyAnalysis


def _safe_text(value: str | None) -> str:
    return value.strip() if value and value.strip() else "Not enough information."


def _normalize_risk(risk) -> str:
    if hasattr(risk, "title"):
        if risk.title and risk.description:
            return f"- {risk.title}: {risk.description}"
        if risk.title:
            return f"- {risk.title}"
        if risk.description:
            return f"- {risk.description}"
    if isinstance(risk, str):
        return f"- {risk}"
    return f"- {str(risk)}"


def _normalize_list(items: list[str]) -> str:
    if not items:
        return "- Not enough information."
    return "\n".join(f"- {item}" for item in items)


def _render_evidence(items: list) -> str:
    if not items:
        return "- No direct evidence available."
    lines = []
    for evidence in items:
        source = getattr(evidence, "source", "Other")
        confidence = getattr(evidence, "confidence", 0)
        quote = getattr(evidence, "quote", "")
        lines.append(f"- Source: {source} | Confidence: {confidence}/100\n  Quote: \"{quote}\"")
    return "\n".join(lines)


def generate_investment_memo(company: CompanyAnalysis) -> str:
    signals = company.signals
    thesis_parts = [
        f"{company.company or 'The company'} operates in the {company.industry or 'target'} market",
    ]

    if company.business_model:
        thesis_parts.append(f"with a {company.business_model.lower()} model")

    if getattr(signals, "subscription_model", False):
        thesis_parts.append("subscription-based monetization")
    if getattr(signals, "is_saas", False):
        thesis_parts.append("SaaS revenue characteristics")
    if getattr(signals, "enterprise_focus", False):
        thesis_parts.append("enterprise customer concentration")

    thesis_text = ", ".join(thesis_parts).rstrip(", ") + "."

    risks_text = "\n".join(
        _normalize_risk(risk) for risk in company.risks
    ) if company.risks else "- Not enough information."

    opportunities_text = _normalize_list(company.swot.opportunities)
    if not company.swot.opportunities and company.products:
        opportunities_text = "\n".join(f"- Expand {product.lower()} adoption" for product in company.products)

    report = f"""
# Investment Memo

## Company

{_safe_text(company.company)}

---

## Executive Summary

{_safe_text(company.summary)}

---

## Investment Thesis

{thesis_text}

The company appears to offer a {company.business_model or 'commercial product'} with {company.acquisition_score or 0}/100 acquisition appeal based on current research. The analysis indicates a mix of strengths and execution risk, with the investment case most credible when supported by validated customer and market evidence.

---

## Business Model

{_safe_text(company.business_model)}

---

## Risks

{risks_text}

---

## Opportunities

{opportunities_text}

---

## SWOT

### Strengths
{_normalize_list(company.swot.strengths)}

### Weaknesses
{_normalize_list(company.swot.weaknesses)}

### Opportunities
{_normalize_list(company.swot.opportunities)}

### Threats
{_normalize_list(company.swot.threats)}

---

## Acquisition Score

{company.acquisition_score}/100

---

## Recommendation

{_safe_text(company.recommendation)}
"""

    return report.strip() + "\n"


def generate_report(company: CompanyAnalysis) -> str:
    return generate_investment_memo(company)