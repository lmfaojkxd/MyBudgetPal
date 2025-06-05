# style.py

APP_STYLE = """
    QWidget {
        background-color: #1C1C1E;
        color: white;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 14px;
    }

    QLabel {
        color: #D1D1D6;
    }

    QLineEdit, QComboBox, QDateEdit {
        background-color: #2C2C2E;
        color: white;
        border: 1px solid #3A3A3C;
        border-radius: 8px;
        padding: 6px 10px;
    }

    QPushButton {
        background-color: #0A84FF;
        color: white;
        padding: 8px 12px;
        border: none;
        border-radius: 10px;
    }

    QPushButton:hover {
        background-color: #409CFF;
    }

    QTableWidget {
        background-color: #2C2C2E;
        border: 1px solid #3A3A3C;
        color: white;
        gridline-color: #48484A;
    }

    QHeaderView::section {
        background-color: #2C2C2E;
        color: #D1D1D6;
        border: none;
        font-weight: 600;
        padding: 6px;
    }
"""