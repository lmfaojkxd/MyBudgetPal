# frontend.py

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtCore import QDate, QSize
from PyQt5.QtGui import QIcon, QPixmap
from datetime import datetime  
import sys
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QHeaderView
)
from .style import APP_STYLE
from backend import BudgetManager

class BudgetApp(QWidget):
    def __init__(self, demo_mode=False):
        super().__init__()
        self.manager = BudgetManager()
        self.goal_achieved_popup_shown = False
        self.init_ui()
        if demo_mode:
            self.load_demo_data()

    def init_ui(self):
        self.setWindowTitle("MyBudgetPal – Personal Budget Tracker")
        self.setGeometry(100, 100, 800, 650)
        icon_size = QSize(24, 24)

        # Balance Label
        self.balance_text = QLabel("Current Balance:")
        self.balance_text.setStyleSheet("font-size: 16px;")
        self.balance_label = QLabel("₹ 0.00")
        self.balance_label.setObjectName("balance_label")

        balance_layout = QHBoxLayout()
        balance_layout.addWidget(self.balance_text)
        balance_layout.addWidget(self.balance_label)
        balance_layout.addStretch()

        # Savings Goal
        self.goal_label = QLabel("Savings Goal (₹):")
        self.goal_entry = QLineEdit()
        self.set_goal_btn = QPushButton()
        self.set_goal_btn.setIcon(QIcon("assets/goal.png"))
        self.set_goal_btn.setIconSize(icon_size)
        self.set_goal_btn.setToolTip("Set Goal")
        self.set_goal_btn.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.set_goal_btn.clicked.connect(self.set_goal)

        self.goal_status = QLabel("No goal set.")
        self.goal_status.setObjectName("goal_status")

        goal_layout = QHBoxLayout()
        goal_layout.addWidget(self.goal_label)
        goal_layout.addWidget(self.goal_entry)
        goal_layout.addWidget(self.set_goal_btn)
        goal_layout.addSpacing(20)
        goal_layout.addWidget(self.goal_status)
        goal_layout.addStretch()

        # Input Fields
        self.date_label = QLabel("Date:")
        self.date_entry = QDateEdit()
        self.date_entry.setCalendarPopup(True)
        self.date_entry.setDate(QDate.currentDate())

        self.amount_label = QLabel("Amount (₹):")
        self.amount_entry = QLineEdit()

        self.category_label = QLabel("Category:")
        self.category_entry = QLineEdit()

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.date_label)
        input_layout.addWidget(self.date_entry)
        input_layout.addWidget(self.amount_label)
        input_layout.addWidget(self.amount_entry)
        input_layout.addWidget(self.category_label)
        input_layout.addWidget(self.category_entry)

        # Buttons
        self.income_btn = QPushButton("Add Income")
        self.income_btn.clicked.connect(lambda: self.add_transaction("Income"))

        self.expense_btn = QPushButton("Add Expense")
        self.expense_btn.clicked.connect(lambda: self.add_transaction("Expense"))

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.income_btn)
        btn_layout.addWidget(self.expense_btn)
        btn_layout.addStretch()

        # Table
        self.tree = QTableWidget()
        self.tree.setColumnCount(4)
        self.tree.setHorizontalHeaderLabels(["Type", "Amount", "Category", "Date"])
        self.tree.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tree.setEditTriggers(QTableWidget.NoEditTriggers)

        # Export & Chart Buttons (Icon only)
        self.export_btn = QPushButton()
        self.export_btn.setIcon(QIcon("assets/export.png"))
        self.export_btn.setIconSize(icon_size)
        self.export_btn.setToolTip("Export to CSV")
        self.export_btn.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.export_btn.clicked.connect(self.export_csv)

        self.chart_btn = QPushButton()
        self.chart_btn.setIcon(QIcon("assets/chart.png"))
        self.chart_btn.setIconSize(icon_size)
        self.chart_btn.setToolTip("View Chart")
        self.chart_btn.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        self.chart_btn.clicked.connect(self.show_chart)

        export_layout = QHBoxLayout()
        export_layout.addStretch()
        export_layout.addWidget(self.export_btn)
        export_layout.addWidget(self.chart_btn)
        export_layout.addStretch()

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(balance_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(goal_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(input_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(btn_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.tree)
        main_layout.addSpacing(20)
        main_layout.addLayout(export_layout)

        self.setLayout(main_layout)

        # StyleSheet
        self.setStyleSheet(APP_STYLE)

    def load_demo_data(self):
        try:
            with open("assets/demo_data.csv", "r") as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    type_, amount, category, date_str = row
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    self.manager.add_transaction(type_, float(amount), category, date)
            self.update_ui()
        except Exception as e:
            QMessageBox.critical(self, "Demo Mode Error", f"Failed to load demo data:\n{e}")
    
    def add_transaction(self, type_):
        date = self.date_entry.date().toPyDate()
        amount_str = self.amount_entry.text().strip()
        category = self.category_entry.text().strip()

        if not amount_str or not category:
            QMessageBox.warning(self, "Input Missing", "Please fill in both Amount and Category.")
            return

        try:
            amount = float(amount_str)
            self.manager.add_transaction(type_, amount, category, date)
            self.update_ui()
            self.amount_entry.clear()
            self.category_entry.clear()
        except ValueError as e:
            QMessageBox.critical(self, "Invalid Input", f"Error: {e}")

    def update_ui(self):
        balance = self.manager.get_balance()
        self.balance_label.setText(f"₹ {balance:.2f}")

        self.tree.setRowCount(0)
        for t in self.manager.get_transactions():
            row_position = self.tree.rowCount()
            self.tree.insertRow(row_position)
            self.tree.setItem(row_position, 0, QTableWidgetItem(t[0]))
            self.tree.setItem(row_position, 1, QTableWidgetItem(str(t[1])))
            self.tree.setItem(row_position, 2, QTableWidgetItem(t[2]))
            self.tree.setItem(row_position, 3, QTableWidgetItem(t[3]))

        goal = self.manager.get_savings_goal()
        if goal > 0:
            if self.manager.is_goal_met():
                self.goal_status.setText(f"🎉 Goal of ₹ {goal:.2f} achieved!")
                self.goal_status.setStyleSheet("font-size: 13px; color: #00e676; font-weight: bold;")
                if not self.goal_achieved_popup_shown:
                    self.show_goal_achieved_popup()
                    self.goal_achieved_popup_shown = True
            else:
                remaining = goal - self.manager.get_balance()
                self.goal_status.setText(f"Savings Goal: ₹ {goal:.2f} | Remaining: ₹ {remaining:.2f}")
                self.goal_status.setStyleSheet("font-size: 13px; color: #ffb300;")
        else:
            self.goal_status.setText("No goal set.")
            self.goal_status.setStyleSheet("font-size: 13px; color: #bdbdbd;")

    def show_goal_achieved_popup(self):
        popup = QMessageBox(self)
        popup.setWindowTitle("Goal Achieved 🎯")
        popup.setText("Congratulations! You reached your savings goal!")
        pixmap = QPixmap("assets/savings_achieved.png").scaledToWidth(100)
        popup.setIconPixmap(pixmap)
        popup.exec_()

    def set_goal(self):
        goal_str = self.goal_entry.text().strip()
        if not goal_str:
            QMessageBox.warning(self, "Input Missing", "Please enter a savings goal.")
            return
        try:
            goal = float(goal_str)
            self.manager.set_savings_goal(goal)
            self.goal_achieved_popup_shown = False
            self.update_ui()
            self.goal_entry.clear()
        except ValueError as e:
            QMessageBox.critical(self, "Invalid Input", f"Error: {e}")

    def export_csv(self):
        if not self.manager.get_transactions():
            QMessageBox.warning(self, "Empty", "No data to export.")
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)", options=options)
        if file_path:
            try:
                with open(file_path, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Type", "Amount", "Category", "Date"])
                    writer.writerows(self.manager.get_transactions())
                QMessageBox.information(self, "Exported", f"Data saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")

    def show_chart(self):
        summary = self.manager.get_monthly_summary()

        if not summary:
            QMessageBox.warning(self, "No Data", "No transaction data available to show chart.")
            return

        months = list(summary.keys())
        incomes = [summary[m]['Income'] for m in months]
        expenses = [summary[m]['Expense'] for m in months]

        fig, ax = plt.subplots()
        bar_width = 0.35
        index = range(len(months))

        ax.bar(index, incomes, bar_width, label='Income', color='#4caf50')
        ax.bar([i + bar_width for i in index], expenses, bar_width, label='Expense', color='#f44336')

        ax.set_xlabel('Month')
        ax.set_ylabel('Amount (₹)')
        ax.set_title('Monthly Income vs Expenses')
        ax.set_xticks([i + bar_width / 2 for i in index])
        ax.set_xticklabels(months)
        ax.legend()

        plt.tight_layout()
        plt.show()
