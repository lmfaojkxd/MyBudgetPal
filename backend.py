# backend.py

from collections import defaultdict
from datetime import datetime

class BudgetManager:
    def __init__(self):
        self.transactions = []
        self.balance = 0.0
        self.savings_goal = 0.0

    def add_transaction(self, type_, amount, category, date):
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if not category.strip():
            raise ValueError("Category cannot be empty.")

        if type_ == 'Expense':
            amount = -amount

        self.balance += amount
        self.transactions.append((type_, abs(amount), category.strip(), date.strftime("%Y-%m-%d")))


    def get_balance(self):
        return self.balance

    def get_transactions(self):
        return self.transactions

    def export_to_csv(self, file_path):
        import csv
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "Amount", "Category"])
            writer.writerows(self.transactions)

    def set_savings_goal(self, amount):
        if amount < 0:
            raise ValueError("Savings goal must be non-negative.")
        self.savings_goal = amount

    def get_savings_goal(self):
        return self.savings_goal

    def is_goal_met(self):
        return self.balance >= self.savings_goal
    
    def get_monthly_summary(self):
        summary = defaultdict(lambda: {'Income': 0, 'Expense': 0})
        for entry in self.transactions:
            type_, amount, category, date_str = entry
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                month = date.strftime("%b %Y")
            except Exception:
                month = "Unknown"

            summary[month][type_] += amount
        return summary


