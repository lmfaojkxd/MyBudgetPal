from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from frontend.app import BudgetApp
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