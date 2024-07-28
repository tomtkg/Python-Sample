from rank_s import (
    group_popularity,
    search_island,
    mod7,
    word_collection,
    continuous_winning,
)
from utils import check


def test_group_popularity(monkeypatch):
    check(
        monkeypatch,
        group_popularity,
        "3 2 3\n1 2 1\n1 3 3\n+ 1\n+ 2\n- 1",
        "3\n3\n1",
    )
    check(
        monkeypatch,
        group_popularity,
        "5 4 4\n2 5 9\n2 4 0\n1 5 6\n1 4 6\n+ 1\n- 1\n+ 1\n+ 5",
        "6\n0\n6\n9",
    )


def test_search_island(monkeypatch):
    check(
        monkeypatch,
        search_island,
        "4 5\n0 1 1 0\n1 0 1 0\n1 0 0 0\n0 0 1 1\n0 1 1 1",
        "3",
    )
    check(
        monkeypatch,
        search_island,
        "6 6\n1 1 1 1 1 1\n1 0 1 0 0 0\n1 0 1 0 1 1\n0 1 0 0 0 1\n1 0 1 1 1 1\n0 1 0 0 0 0",
        "5",
    )


def test_mod7(monkeypatch):
    check(monkeypatch, mod7, "3\n10\n4\n14", "1")
    check(monkeypatch, mod7, "10\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10", "17")


def test_word_collection(monkeypatch):
    check(
        monkeypatch,
        word_collection,
        "6 5\nbcac 3\nabcd 14\nabccjg 92\nbcaddgie 2\nabcd 6\ncb 200\nb\na\nabcd\ngagioheo\ncb",
        "5\n112\n20\n0\n200",
    )
    check(
        monkeypatch,
        word_collection,
        "5 3\npaiza 16\npizza 1\npaizaio 4\npaizapoh 2\npizzaio 8\npaiza\npizza\np",
        "22\n9\n31",
    )


def test_continuous_winning(monkeypatch):
    check(monkeypatch, continuous_winning, "3 4\n3\n2\n3", "7")
    check(monkeypatch, continuous_winning, "5 1\n1\n1\n1\n1\n1", "12")
