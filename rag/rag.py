from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
CHROMA_PATH = BASE_DIR / "chroma_db"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = Chroma(
    collection_name="actuarial_documents",
    embedding_function=embeddings,
    persist_directory=str(CHROMA_PATH)
)


def retrieve_for_assumption(
    assumption_name,
    value,
    focus,
    k=3
):
    question = f"""
This is an actuarial valuation report for an Iranian pension fund.

Evaluate the following NEW actuarial economic assumption:

{assumption_name}: {value}%

Find evidence in the report specifically relevant to this
assumption.

Focus on:

1. The assumption used in the actuarial report.
2. The reason or methodology used to select it.
3. Historical averages or numerical evidence.
4. Economic or actuarial justification.
5. The effect of changing this assumption on actuarial liabilities.
6. Sensitivity analysis or scenario results involving this assumption.
7. Any statement explaining whether this assumption has a
   significant impact on actuarial results.

Specific focus:

{focus}

Prioritize numerical evidence and passages explaining
cause and effect.

Return the most relevant passages from the report.
"""

    results = vector_store.similarity_search(
        question,
        k=k
    )

    return results


def retrieve_rag_context(
    discount_rate,
    rate_wage_increase,
    rate_annuity_increase,
    productivity_rate,
    interest_rate,
    borrowing_rate,
):

    assumption_queries = [
        (
            "Discount rate",
            discount_rate,
            """
Find evidence about the discount rate, including its actuarial
impact, historical basis, expected return assumptions, and
sensitivity to changes in the discount rate.
"""
        ),
        (
            "Wage increase rate",
            rate_wage_increase,
            """
Find evidence about wage growth/increase assumptions, including
historical wage increases, future wage expectations, and the
effect of wage growth on actuarial liabilities.
"""
        ),
        (
            "Annuity increase rate",
            rate_annuity_increase,
            """
Find evidence about pension/annuity increases, including
historical pension increases, future pension expectations,
and the effect of pension increases on actuarial liabilities.
"""
        ),
        (
            "Productivity rate",
            productivity_rate,
            """
Find evidence about productivity assumptions, economic growth,
wage productivity, and how productivity affects actuarial
calculations or economic assumptions.
"""
        ),
        (
            "Interest rate",
            interest_rate,
            """
Find evidence about investment returns, interest rates,
investment income, fund assets, and the relationship between
investment returns and actuarial funding.
"""
        ),
        (
            "Borrowing rate",
            borrowing_rate,
            """
Find evidence about borrowing, borrowing costs, fund deficits,
future borrowing requirements, and the financial consequences
of borrowing assumptions.
"""
        ),
    ]

    all_results = []

    for assumption_name, value, focus in assumption_queries:

        results = retrieve_for_assumption(
            assumption_name,
            value,
            focus,
            k=3
        )

        all_results.extend(results)

    # Remove duplicate passages
    unique_results = []
    seen = set()

    for result in all_results:

        text = result.page_content.strip()

        if text not in seen:
            seen.add(text)
            unique_results.append(result)

    context_parts = []

    for result in unique_results:

        context_parts.append(
            result.page_content
        )

    context = "\n\n--- NEXT EVIDENCE ---\n\n".join(
        context_parts
    )
    sensitivity_table = """
TABLE 23 - Sensitivity test results (million Rial)

Base scenario: 70,108,351

Increase retirement age by 3 years: 72,293,056

Increase retirement service by 3 years: 74,231,472

Increase wage rate by 20%: 74,313,946

Increase pension rate by 20%: 89,855,703
"""

    context = context + "\n\n--- SENSITIVITY ANALYSIS ---\n\n" + sensitivity_table

    
    return context


if __name__ == "__main__":

    context = retrieve_rag_context(
        discount_rate=22,
        rate_wage_increase=20,
        rate_annuity_increase=20,
        productivity_rate=20,
        interest_rate=20,
        borrowing_rate=20,
    )

    print("\n--- RAG CONTEXT ---")
    print(context)

