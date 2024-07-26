from rank_c import leftover, fizz_buzz, mikan, umpire, lottery
from utils import check


def test_leftover(monkeypatch):
    check(monkeypatch, leftover, "1 80 40", "0.12")
    check(monkeypatch, leftover, "10 31 52", "3.312")


def test_fizz_buzz(monkeypatch):
    check(monkeypatch, fizz_buzz, "5", "1\n2\nFizz\n4\nBuzz")
    check(
        monkeypatch,
        fizz_buzz,
        "20",
        "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n"
        "11\nFizz\n13\n14\nFizz Buzz\n16\n17\nFizz\n19\nBuzz",
    )


def test_mikan(monkeypatch):
    check(monkeypatch, mikan, "10 3\n24\n35\n3", "20\n40\n10")
    check(monkeypatch, mikan, "50 3\n40\n90\n10", "50\n100\n50")


def test_umpire(monkeypatch):
    check(
        monkeypatch,
        umpire,
        "5\nball\nstrike\nball\nstrike\nstrike",
        "ball!\nstrike!\nball!\nstrike!\nout!",
    )
    check(
        monkeypatch,
        umpire,
        "6\nball\nstrike\nball\nball\nstrike\nball",
        "ball!\nstrike!\nball!\nball!\nstrike!\nfourball!",
    )


def test_lottery(monkeypatch):
    check(
        monkeypatch,
        lottery,
        "142358\n3\n195283\n167358\n142359",
        "blank\nthird\nadjacent",
    )
