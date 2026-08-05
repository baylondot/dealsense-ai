from models import CompanyAnalysis


def generate_report(company: CompanyAnalysis) -> str:

    report = f"""
# Investment Memo

## Company

{company.company}

---

## Acquisition Score

{company.acquisition_score}/100

Recommendation:
{company.recommendation}

---

## Executive Summary

{company.summary}

---

## Industry

{company.industry}

---

## Business Model

{company.business_model}

---

## Products

"""

    for product in company.products:
        report += f"- {product}\n"

    report += "\n## Customers\n\n"

    for customer in company.customers:
        report += f"- {customer}\n"

    report += "\n## Competitors\n\n"

    for competitor in company.competitors:
        report += f"- {competitor.name}: {competitor.reason}\n"

    report += "\n## Risks\n\n"

    for risk in company.risks:
        report += f"- {risk}\n"

    report += "\n## SWOT\n\n"

    report += "### Strengths\n"

    for s in company.swot.strengths:
        report += f"- {s}\n"

    report += "\n### Weaknesses\n"

    for w in company.swot.weaknesses:
        report += f"- {w}\n"

    report += "\n### Opportunities\n"

    for o in company.swot.opportunities:
        report += f"- {o}\n"

    report += "\n### Threats\n"

    for t in company.swot.threats:
        report += f"- {t}\n"

    return report