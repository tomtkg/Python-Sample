from rank_d import *
from utils import check


def test_square(monkeypatch):
    check(monkeypatch, square, "4", "****")
    check(monkeypatch, square, "6", "******")


def test_email_address(monkeypatch):
    check(
        monkeypatch,
        email_address,
        "paiza\nexample.com",
        "paiza@example.com",
    )
    check(
        monkeypatch,
        email_address,
        "paiza.tarou2015\npaiza.jp",
        "paiza.tarou2015@paiza.jp",
    )


def test_addition(monkeypatch):
    check(monkeypatch, addition, "1 1", "2")
    check(monkeypatch, addition, "0 99", "99")


def test_min_num(monkeypatch):
    check(monkeypatch, min_num, "10\n12\n4\n8\n46", "4")
    check(monkeypatch, min_num, "1\n2\n3\n2\n1", "1")


def test_diff_str(monkeypatch):
    check(monkeypatch, diff_str, "paiza\npaiza", "OK")
    check(monkeypatch, diff_str, "paiza\naziap", "NG")
