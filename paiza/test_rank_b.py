from rank_b import (
    name_card,
    long_table,
    word_chain,
    concentration,
    display_3d_printer,
)
from utils import check


def test_name_card(monkeypatch):
    check(monkeypatch, name_card, "3 1", "6")
    check(monkeypatch, name_card, "3 6", "1")


def test_long_table(monkeypatch):
    check(monkeypatch, long_table, "6 3\n3 2\n1 6\n2 5", "4")
    check(monkeypatch, long_table, "12 6\n4 6\n4 8\n4 10\n4 12\n4 2\n4 4", "12")


def test_word_chain(monkeypatch):
    check(
        monkeypatch,
        word_chain,
        "3 6 7\na\naloha\napp\naz\npaiza\nwarp\napp\npaiza\na\naloha\naz\nwarp\npaiza",
        "1\n3",
    )
    check(
        monkeypatch,
        word_chain,
        "4 4 4\nabacus\nbanana\ncandy\nyankee\nbanana\ncandies\ncandies\nyankee",
        "2\n1\n4",
    )


def test_concentration(monkeypatch):
    check(
        monkeypatch,
        concentration,
        "2 3 2\n1 2 3\n2 1 3\n5\n1 1 2 1\n1 1 1 2\n1 1 2 2\n1 3 2 3\n1 2 2 1",
        "6\n0",
    )
    check(
        monkeypatch,
        concentration,
        "2 5 3\n5 8 8 6 3\n3 6 3 3 5\n8\n1 4 2 2\n1 3 2 1\n2 4 2 3\n1 3 1 5\n2 5 1 1\n2 1 1 2\n1 5 2 1\n1 2 1 3",
        "6\n2\n2",
    )


def test_display_3d_printer(monkeypatch):
    check(
        monkeypatch,
        display_3d_printer,
        "3 3 3\n###\n##.\n#..\n--\n##.\n##.\n...\n--\n##.\n##.\n...\n--",
        "##.\n##.\n###",
    )
