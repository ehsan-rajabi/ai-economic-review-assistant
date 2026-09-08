import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from rag.rag import retrieve_rag_context

load_dotenv()

class AssumptionReview(BaseModel):
    review: str = Field(
        description="A concise 150-200 word actuarial review."
    )

    overall_score: float = Field(
        description="Overall score from 0 to 10.",
        ge=0,
        le=10
    )

    suggestions: str = Field(
        description="Practical suggestions for improving the assumptions."
    )

    comparison: str = Field(
        description=(
            "Explain whether the new assumptions are better, worse, "
            "or similar to the previous assumptions and why. "
            "If there are no previous assumptions, state that this "
            "is the first assessment and there is nothing to compare."
        )
    )

model = ChatOpenAI(
model="gpt-5.6-luna",
reasoning_effort="low",
api_key=os.getenv("OPENAI_API_KEY")
)

structured_model = model.with_structured_output(AssumptionReview)

prompt = ChatPromptTemplate.from_messages([
("system", """
You are an actuarial expert specializing in Iranian pension funds.

Your task is to review the NEW economic assumptions.

NEW ASSUMPTIONS:

Discount rate: {discount_rate}%
Wage increase rate: {rate_wage_increase}%
Annuity increase rate: {rate_annuity_increase}%
Productivity rate: {productivity_rate}%
Interest rate: {interest_rate}%
Borrowing rate: {borrowing_rate}%

PREVIOUS ASSESSMENT:

{previous_information}

REFERENCE INFORMATION FROM THE ACTUARIAL REPORT:

{rag_context}

Use the reference information from the actuarial report
as evidence when it is relevant to the review.

Do not assume that information in the reference material
is automatically correct for the NEW assessment. Evaluate
it together with the NEW assumptions and current economic
conditions.

If the reference information does not contain relevant
information for a particular issue, do not invent information
from the report.

Assess the NEW assumptions using:

* Iranian historical and current economic conditions
* Plausible future Iranian economic trends
* Credibility and justification
* Internal consistency between the assumptions
* Suitability for pension actuarial valuation
* Relevant evidence from the actuarial report
* Relevant sensitivity analysis from the actuarial report

Pay particular attention to numerical evidence in the report.

Use sensitivity analysis when it is relevant to explain
how changes in assumptions affect actuarial liabilities.

If previous assumptions are provided, compare the NEW assumptions
with the PREVIOUS assumptions and previous score.

Explain whether the NEW assumptions are better, worse, or similar
to the previous assumptions and explain the actuarial/economic
reasons.

If this is the FIRST assessment and no previous assumptions exist,
do not attempt a comparison. State clearly that this is the first
assessment.

The review should be approximately 150-200 words.
""")
])

chain = prompt | structured_model

previous_assumptions = None
previous_score = None

def review_assumptions(
    discount_rate,
    rate_wage_increase,
    rate_annuity_increase,
    productivity_rate,
    interst_rate,
    borrowing_rate,
):

    global previous_assumptions, previous_score

    if previous_assumptions is None:
        previous_information = """
There are no previous assumptions.
This is the first assessment.
There is no previous score.
"""
    else:
        previous_information = f"""
Previous assumptions:

Discount rate: {previous_assumptions["discount_rate"]}%
Wage increase rate: {previous_assumptions["rate_wage_increase"]}%
Annuity increase rate: {previous_assumptions["rate_annuity_increase"]}%
Productivity rate: {previous_assumptions["productivity_rate"]}%
Interest rate: {previous_assumptions["interest_rate"]}%
Borrowing rate: {previous_assumptions["borrowing_rate"]}

Previous overall score: {previous_score}
"""

    rag_context = retrieve_rag_context(
        discount_rate=discount_rate,
        rate_wage_increase=rate_wage_increase,
        rate_annuity_increase=rate_annuity_increase,
        productivity_rate=productivity_rate,
        interest_rate=interst_rate,
        borrowing_rate=borrowing_rate,
    )

    result = chain.invoke({
        "previous_information": previous_information,
        "rag_context": rag_context,
        "discount_rate": discount_rate,
        "rate_wage_increase": rate_wage_increase,
        "rate_annuity_increase": rate_annuity_increase,
        "productivity_rate": productivity_rate,
        "interest_rate": interst_rate,
        "borrowing_rate": borrowing_rate,
    })

    # Save the current assessment for the NEXT request
    previous_assumptions = {
        "discount_rate": discount_rate,
        "rate_wage_increase": rate_wage_increase,
        "rate_annuity_increase": rate_annuity_increase,
        "productivity_rate": productivity_rate,
        "interest_rate": interst_rate,
        "borrowing_rate": borrowing_rate,
    }

    previous_score = result.overall_score

    return {
        "review": result.review,
        "score": result.overall_score,
        "suggestions": result.suggestions,
        "comparison": result.comparison,
    }