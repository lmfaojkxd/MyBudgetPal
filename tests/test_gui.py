# tests -> test_gui.py
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from frontend.app import BudgetApp
from unittest.mock import patch
import sys
import pytest
from PyQt5.QtWidgets import QApplication

@pytest.fixture
def app(qtbot):
    test_app = BudgetApp()
    qtbot.addWidget(test_app)
    return test_app

def test_income_button(app, qtbot):
    app.amount_entry.setText("500")
    app.category_entry.setText("Freelance")
    qtbot.mouseClick(app.income_btn, Qt.LeftButton)
    assert "₹ 500.00" in app.balance_label.text()
    
def test_expense_button(app, qtbot):
    app.amount_entry.setText("200")
    app.category_entry.setText("Groceries")
    qtbot.mouseClick(app.expense_btn, Qt.LeftButton)
    assert "₹ -200.00" in app.balance_label.text()

def test_blank_category_warning(app, qtbot):
    app.amount_entry.setText("100")
    app.category_entry.setText("   ")  # Blank category

    with patch.object(QMessageBox, 'warning') as mock_warning:
        qtbot.mouseClick(app.income_btn, Qt.LeftButton)
        mock_warning.assert_called_once_with(app, "Input Missing", "Please fill in both Amount and Category.")
        
def test_blank_amount_warning(app, qtbot):
    app.amount_entry.setText("")
    app.category_entry.setText("Groceries")

    with patch.object(QMessageBox, 'warning') as mock_warning:
        qtbot.mouseClick(app.expense_btn, Qt.LeftButton)
        mock_warning.assert_called_once_with(app, "Input Missing", "Please fill in both Amount and Category.")
    
def test_empty_savings_goal_warning(app, qtbot):
    app.goal_entry.setText("")
    with patch.object(QMessageBox, 'warning') as mock_warning:
        qtbot.mouseClick(app.set_goal_btn, Qt.LeftButton)
        mock_warning.assert_called_once()