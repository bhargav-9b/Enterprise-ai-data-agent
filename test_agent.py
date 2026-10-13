
import unittest

from agent import (
    get_total_revenue,
    get_top_product,
    get_sales_by_region,
)


class TestDataAnalysisAgent(unittest.TestCase):

    def test_total_revenue(self):
        result = get_total_revenue()
        self.assertIn("232,500.00", result)

    def test_top_product(self):
        result = get_top_product()
        self.assertIn("Laptop", result)
        self.assertIn("150,000.00", result)

    def test_sales_by_region(self):
        result = get_sales_by_region()
        self.assertIn("South", result)
        self.assertIn("111500", result)

    
    def test_unknown_question_handling(self):
        from agent import run_agent

        result = run_agent("What is the weather today?")
        self.assertIn("cannot answer", result)

    def test_empty_question(self):
        from agent import run_agent

        result = run_agent("   ")
        self.assertEqual(result, "Please enter a question.")



if __name__ == "__main__":
    unittest.main()
