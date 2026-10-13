
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent import (
    get_total_revenue,
    get_top_product,
    get_sales_by_region,
)

# Load the Gemini API key
load_dotenv("gemini_test.env", override=True)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "Gemini API key not found. Check gemini_test.env."
    )

client = genai.Client(api_key=api_key)

# Connect Gemini to our existing Python functions
tools = [
    get_total_revenue,
    get_top_product,
    get_sales_by_region,
]


def ask_agent(question: str) -> str:
    """Answer sales questions using Gemini, with a Python fallback."""

    q = question.lower().strip()

    # Reliable local fallback if Gemini is unavailable
    def local_answer():
        if any(word in q for word in ["total revenue", "overall revenue", "total sales"]):
            return str(get_total_revenue())

        if any(word in q for word in ["top product", "highest revenue", "best-selling product", "best selling product"]):
            return str(get_top_product())

        if any(word in q for word in ["sales by region", "revenue by region", "region-wise", "region wise"]):
            return str(get_sales_by_region())

        return (
            "Gemini is temporarily unavailable. "
            "Try asking about total revenue, top product, or sales by region."
        )

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=(
                "You are a sales data analysis assistant. "
                "Use Python tools for sales figures. Do not invent numbers.\n"
                f"Question: {question}"
            ),
            config=types.GenerateContentConfig(tools=tools),
        )

        if response.text:
            return response.text

        return local_answer()

    except Exception as error:
        print(f"Gemini temporarily unavailable: {error}")
        return "Local Python result: " + local_answer()
        
if __name__ == "__main__":
    print("Enterprise AI Data Analysis Agent")
    print("Type 'exit' to stop.")

    while True:
        question = input("\nAsk a question: ").strip()

        if question.lower() == "exit":
            print("Agent stopped.")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            print("\nAgent:", ask_agent(question))
        except Exception as error:
            print(f"\nError: {error}")