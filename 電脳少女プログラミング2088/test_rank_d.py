from rank_d import alley, casino, slums
from utils import check


def test_alley(monkeypatch):
    check(monkeypatch, alley, "3\n123\n813\n321", "813")
    check(monkeypatch, alley, "5\n10\n20\n50\n30\n40", "50")


def test_casino(monkeypatch):
    check(monkeypatch, casino, "1\n5\n2", "paiza@example.com", "46")
    check(monkeypatch, casino, "8\n2\n80", "818")


def test_slums(monkeypatch):
    check(monkeypatch, slums, "1000", "600")
    check(monkeypatch, slums, "2100", "1150")
