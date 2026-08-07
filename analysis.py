import json
import re

from llm import client
from models import CompanyAnalysis
from prompts import SYSTEM_PROMPT

from constants import DEFAULT_MODEL

def analyze_company(research_context: str) -> CompanyAnalysis:
    combined_context = research_context
    prompt = f"""
You are analysing a company for a Private Equity firm.

Below is the company's website content.

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
        "reason":""
    }}
],
  "risks": [],
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
    "api_platform":false
}},
  "acquisition_score": 0,
  "recommendation": ""
}}

Rules:

- Return ONLY JSON.
- No markdown.
- No explanations.
- No ```json.
- Products must be a list of STRINGS.
- Customers must be a list of STRINGS.
- Competitors must be a list of STRINGS.
- Risks must be a list of STRINGS.
- acquisition_score must be an integer between 0 and 100.
- If information isn't available, write "Not enough information."
- Each competitor must include a short reason explaining why it competes with the company.
- Determine the investment signals from the information.
- Every signal must be either true or false.
- Do not guess.
- If evidence doesn't exist,use false.
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

    return analysis