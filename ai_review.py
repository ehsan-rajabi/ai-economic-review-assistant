
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
load_dotenv()
client =OpenAI(api_key=os.getenv("OPENAI_API_KEY"))




def review_assumptions(
    discount_rate,
    rate_wage_increase,
    rate_annuity_increase,
    productivity_rate,
    interst_rate,
    borrowing_rate,
):

    prompt = f"""
You are an actuarial expert specializing in Iranian pension funds.

Review ONLY these six economic assumptions:

Discount rate: {discount_rate}%
Wage increase rate: {rate_wage_increase}%
Annuity increase rate: {rate_annuity_increase}%
Productivity rate: {productivity_rate}%
Interest rate: {interst_rate}%
Borrowing rate: {borrowing_rate}%

Assess the assumptions using:
- Iranian historical and current economic conditions
- Plausible future Iranian economic trends
- Credibility and justification
- Internal consistency between the assumptions
- Suitability for pension actuarial valuation

Return a concise response.

The "review" should be ONE paragraph of approximately 150-200 words.

The "suggestions" should contain practical suggestions for improving
the assumptions, including better values or reasonable ranges where
appropriate.

The "overall_score" must be a number from 0 to 10.

Return ONLY valid JSON in exactly this structure:

{{
    "review": "One concise paragraph explaining the assessment.",
    "overall_score": 0,
    "suggestions": "Practical suggestions for improving the assumptions."
}}
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        reasoning={"effort": "low"},
        max_output_tokens=1000,
        input=prompt
    )

    result = json.loads(response.output_text)

    return {
        "review": result["review"],
        "score": result["overall_score"],
        "suggestions": result["suggestions"],
    }