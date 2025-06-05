# main.py
import sys
from PyQt5.QtWidgets import QApplication
from frontend.app import BudgetApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo_mode = "--demo" in sys.argv
    window = BudgetApp(demo_mode=demo_mode)
    window.show()
    sys.exit(app.exec_())