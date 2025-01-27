import io
from rank_d import alley, casino, slums
from rank_c import room, park
from rank_b import downtown, hideout
from rank_a import highway
from rank_s import rooftop


# Rank D
def test_alley(monkeypatch):
    check(monkeypatch, alley, "3\n123\n813\n321", "813")
    check(monkeypatch, alley, "5\n10\n20\n50\n30\n40", "50")


def test_casino(monkeypatch):
    check(monkeypatch, casino, "1\n5\n2", "46")
    check(monkeypatch, casino, "8\n2\n80", "818")


def test_slums(monkeypatch):
    check(monkeypatch, slums, "1000", "600")
    check(monkeypatch, slums, "2100", "1150")


# Rank C
def test_room(monkeypatch):
    check(monkeypatch, room, "157", "120211")
    check(monkeypatch, room, "-100000", "211021211102")


def test_park(monkeypatch):
    check(monkeypatch, park, "5 0 0\n4 3\n2 2\n-2 4\n0 -3\n-3 -3", "2")
    check(monkeypatch, park, "5 0 0\n1000 1\n500 900\n800 -700\n0 -1000\n900 900", "4")


# Rank B
def test_downtown(monkeypatch):
    check(monkeypatch, downtown, "5\n.#.#.\n#####\n.#.#.\n##.##\n.###.", "3")
    check(monkeypatch, downtown, "5\n.....\n.....\n.....\n.....\n.....", "30")


def test_hideout(monkeypatch):
    check(
        monkeypatch,
        hideout,
        "5\n0 0 1 0 0\n0 1 1 1 0\n1 1 1 1 1\n0 1 0 1 0\n0 0 1 0 0",
        "Yes",
    )
    check(monkeypatch, hideout, "3\n0 0 0\n1 1 0\n0 0 1", "No")


# Rank A
def test_highway(monkeypatch):
    check(monkeypatch, highway, "3 5\nA....\n.#.#.\n....B", "2")
    check(monkeypatch, highway, "2 4\nA..B\n####", "0")


# Rank S
def test_rooftop(monkeypatch):
    check(monkeypatch, rooftop, "5 6 3\n3 2 2\n4 4 0\n5 5 1", "3")
    check(monkeypatch, rooftop, "3 3 1\n2 2 1", "0")


# Test Helpers
def check(monkeypatch, func: None, input: str, output: str):
    stdin = io.StringIO(input)
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stdout", stdout)
        func()

    assert stdout.getvalue() == output + "\n"
