import json
import re

from evidence import Evidence
from llm import client
from models import CompanyAnalysis, Competitor, Risk
from prompts import SYSTEM_PROMPT

from constants import DEFAULT_MODEL


SIGNAL_NAMES = [
    "is_saas",
    "is_b2b",
    "is_b2c",
    "recurring_revenue",
    "ai_company",
    "enterprise_focus",
    "marketplace",
    "subscription_model",
    "global_presence",
    "open_source",
    "mobile_app",
    "api_platform",
]


def _ensure_evidence(item, default_quote: str = "No direct evidence identified in the collected research."):
    if isinstance(item, list):
        if not item:
            return [Evidence(source="Other", quote=default_quote, confidence=20)]
        return item

    if not item:
        return [Evidence(source="Other", quote=default_quote, confidence=20)]

    return item


def _normalize_analysis(analysis: CompanyAnalysis) -> CompanyAnalysis:
    normalized_competitors = []
    for competitor in analysis.competitors:
        if isinstance(competitor, str):
            normalized_competitors.append(
                Competitor(
                    name=competitor,
                    reason="Not enough information.",
                    evidence=[Evidence(source="Other", quote="No direct evidence identified in the collected research.", confidence=20)],
                )
            )
        else:
            competitor.evidence = _ensure_evidence(competitor.evidence)
            normalized_competitors.append(competitor)
    analysis.competitors = normalized_competitors

    normalized_risks = []
    for risk in analysis.risks:
        if isinstance(risk, str):
            normalized_risks.append(
                Risk(
                    title=risk,
                    description=risk,
                    evidence=[Evidence(source="Other", quote="No direct evidence identified in the collected research.", confidence=20)],
                )
            )
        else:
            risk.evidence = _ensure_evidence(risk.evidence)
            normalized_risks.append(risk)
    analysis.risks = normalized_risks

    evidence_map = analysis.signals.evidence or {}
    for signal_name in SIGNAL_NAMES:
        evidence_map.setdefault(signal_name, [Evidence(source="Other", quote="No direct evidence identified in the collected research.", confidence=20)])
    analysis.signals.evidence = evidence_map

    return analysis


def analyze_company(research_context: str) -> CompanyAnalysis:
    combined_context = research_context or "Not enough information."
    prompt = f"""
You are analysing a company for a Private Equity firm.

Below is the company's website content and external research.

=========================
{combined_context}
=========================

Return ONLY valid JSON.

Schema:

{{
  "company": "",
  "summary": "",
  "industry": "",
  "business_model": "",
  "products": [],
  "customers": [],
  "competitors":[
    {{
      "name":"",
      "reason":"",
      "evidence":[{{"source":"Website","quote":"","confidence":0}}]
    }}
  ],
  "risks":[
    {{
      "title":"",
      "description":"",
      "evidence":[{{"source":"Website","quote":"","confidence":0}}]
    }}
  ],
  "swot": {{
      "strengths": [],
      "weaknesses": [],
      "opportunities": [],
      "threats": []
  }},
  "signals":{{
    "is_saas":false,
    "is_b2b":false,
    "is_b2c":false,
    "recurring_revenue":false,
    "ai_company":false,
    "enterprise_focus":false,
    "marketplace":false,
    "subscription_model":false,
    "global_presence":false,
    "open_source":false,
    "mobile_app":false,
    "api_platform":false,
    "evidence":{{
      "is_saas":[{{"source":"Website","quote":"","confidence":0}}],
      "is_b2b":[{{"source":"Website","quote":"","confidence":0}}],
      "is_b2c":[{{"source":"Website","quote":"","confidence":0}}],
      "recurring_revenue":[{{"source":"Website","quote":"","confidence":0}}],
      "ai_company":[{{"source":"Website","quote":"","confidence":0}}],
      "enterprise_focus":[{{"source":"Website","quote":"","confidence":0}}],
      "marketplace":[{{"source":"Website","quote":"","confidence":0}}],
      "subscription_model":[{{"source":"Website","quote":"","confidence":0}}],
      "global_presence":[{{"source":"Website","quote":"","confidence":0}}],
      "open_source":[{{"source":"Website","quote":"","confidence":0}}],
      "mobile_app":[{{"source":"Website","quote":"","confidence":0}}],
      "api_platform":[{{"source":"Website","quote":"","confidence":0}}]
    }}
  }},
  "acquisition_score": 0,
  "recommendation": ""
}}

Rules:

- Return ONLY JSON.
- No markdown.
- No explanations.
- No ```json.
- Products, customers, strengths, weaknesses, opportunities, and threats must be arrays of strings.
- acquisition_score must be an integer between 0 and 100.
- If information isn't available, write "Not enough information."
- Each competitor must include a short reason and at least one evidence item.
- Each risk must include a title, description, and at least one evidence item.
- Each investment signal must be either true or false AND must have an evidence list in `signals.evidence`.
- Determine the investment signals from the information.
- Do not guess.
- If evidence doesn't exist, use a conservative estimate with source "Other" and confidence 20-40.
"""

    response = client.chat.completions.create(

        model=DEFAULT_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown fences if model still returns them
    content = re.sub(r"^```json\s*", "", content, flags=re.IGNORECASE)
    content = re.sub(r"^```\s*", "", content)
    content = re.sub(r"\s*```$", "", content)

    # Extract only JSON
    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1:
        raise Exception(
            "The model did not return valid JSON.\n\n"
            f"Raw response:\n{content}"
        )

    content = content[start:end + 1]

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise Exception(
            f"JSON Parsing Failed\n\n{e}\n\nRaw Response:\n{content}"
        )

    analysis = CompanyAnalysis(**data)
    return _normalize_analysis(analysis)