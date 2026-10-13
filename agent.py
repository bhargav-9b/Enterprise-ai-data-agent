
import pandas as pd

# Load business data
df = pd.read_csv("sales.csv")

# Tool 1: Calculate total revenue
def get_total_revenue():
    revenue = df["quantity"] * df["unit_price"]
    return f"Total revenue: Rs. {revenue.sum():,.2f}"


# Tool 2: Find the product with highest revenue
def get_top_product():
    data = df.copy()
    data["revenue"] = data["quantity"] * data["unit_price"]

    result = data.groupby("product")["revenue"].sum()
    product = result.idxmax()
    amount = result.max()

    return f"Top product by revenue: {product} (Rs. {amount:,.2f})"


# Tool 3: Calculate revenue by region
def get_sales_by_region():
    data = df.copy()
    data["revenue"] = data["quantity"] * data["unit_price"]

    result = data.groupby("region")["revenue"].sum()
    return result.to_string()


# Simple planner: choose a tool based on the question

def run_agent(question):
    question = question.lower().strip()

    if not question:
        answer = "Please enter a question."

    elif "total revenue" in question or "total sales" in question:
        answer = get_total_revenue()

    elif "top product" in question or "highest revenue" in question:
        answer = get_top_product()

    elif "region" in question:
        answer = get_sales_by_region()

    else:
        answer = (
            "I cannot answer that question yet. Try asking about "
            "total revenue, top product, or sales by region."
        )

    print("\nAgent answer:")
    print(answer)
    return answer



# Interactive question loop
if __name__ == "__main__":
    print("Enterprise AI Data Analysis Agent")
    print("Type 'exit' to stop.")

    while True:
        question = input("\nAsk a business question: ")

        if question.lower().strip() == "exit":
            print("Agent stopped.")
            break

        run_agent(question)
