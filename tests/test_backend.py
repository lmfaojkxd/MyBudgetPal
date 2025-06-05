import unittest
from backend import BudgetManager
from datetime import datetime

class TestBudgetManager(unittest.TestCase):

    def setUp(self):
        self.manager = BudgetManager()

    # Equivalence class: valid income
    def test_add_valid_income_transaction(self):
        self.manager.add_transaction("Income", 1000, "Salary", datetime.today())
        self.assertEqual(len(self.manager.get_transactions()), 1)
        self.assertEqual(self.manager.get_balance(), 1000.0)

    # Invalid (negative amount)
    def test_add_transaction_with_negative_amount(self):
        with self.assertRaises(ValueError):
            self.manager.add_transaction("Income", -500, "Salary", datetime.today())

    # Invalid (empty category)
    def test_add_transaction_with_empty_category(self):
        with self.assertRaises(ValueError):
            self.manager.add_transaction("Expense", 100, "   ", datetime.today())

    # Boundary: 0 amount
    def test_zero_amount_transaction(self):
        with self.assertRaises(ValueError):
            self.manager.add_transaction("Income", 0, "Gift", datetime.today())

    def test_add_expense_transaction(self):
        self.manager.add_transaction("Expense", 200, "Groceries", datetime.today())
        self.assertEqual(self.manager.get_balance(), -200)

    def test_savings_goal_positive(self):
        self.manager.set_savings_goal(500)
        self.assertEqual(self.manager.get_savings_goal(), 500)

    def test_savings_goal_negative(self):
        with self.assertRaises(ValueError):
            self.manager.set_savings_goal(-100)

    def test_goal_achievement(self):
        self.manager.set_savings_goal(500)
        self.manager.add_transaction("Income", 600, "Freelance", datetime.today())
        self.assertTrue(self.manager.is_goal_met())

    def test_monthly_summary(self):
        date = datetime(2024, 6, 5)
        self.manager.add_transaction("Income", 1000, "Job", date)
        self.manager.add_transaction("Expense", 300, "Rent", date)
        summary = self.manager.get_monthly_summary()
        self.assertEqual(summary["Jun 2024"]["Income"], 1000)
        self.assertEqual(summary["Jun 2024"]["Expense"], 300)

if __name__ == "__main__":
    unittest.main()