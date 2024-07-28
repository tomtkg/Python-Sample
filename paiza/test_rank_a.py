from rank_a import (
    school_hiking,
    janken,
    hanoi,
    origami,
    book_sort,
)
from utils import check


def test_school_hiking(monkeypatch):
    check(monkeypatch, school_hiking, "3 300\n150\n120\n130", "20")
    check(monkeypatch, school_hiking, "4 1000\n200\n20\n500\n60", "220")


def test_janken(monkeypatch):
    check(monkeypatch, janken, "4 7\nCGPC", "4")
    check(monkeypatch, janken, "5 10\nGPCPC", "3")


def test_hanoi(monkeypatch):
    check(monkeypatch, hanoi, "3 4", "-\n2 1\n3")
    check(monkeypatch, hanoi, "4 6", "4 1\n3 2\n-")


def test_origami(monkeypatch):
    check(monkeypatch, origami, "1", "0")
    check(monkeypatch, origami, "2", "001")
    check(monkeypatch, origami, "3", "0010011")
    check(monkeypatch, origami, "4", "001001100011011")


def test_book_sort(monkeypatch):
    check(monkeypatch, book_sort, "5\n5 4 3 2 1", "2")
    check(monkeypatch, book_sort, "10\n8 7 9 1 5 6 2 10 4 3", "6")
