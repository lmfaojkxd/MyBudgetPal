# tests/test_main.py
from PyQt5.QtWidgets import QApplication
import sys
import pytest

def test_main_app_starts(monkeypatch):
    import main
    monkeypatch.setattr(sys, 'argv', ['main.py'])  # simulate CLI args
    assert callable(main.run_app)