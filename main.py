# main.py
from frontend.app import BudgetApp
from PyQt5.QtWidgets import QApplication
import sys

def run_app():
    app = QApplication(sys.argv)
    demo_mode = "--demo" in sys.argv
    window = BudgetApp(demo_mode=demo_mode)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()