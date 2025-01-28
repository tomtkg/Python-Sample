import pytest


input1 = """
1
5
2
""".strip()

output1 = """
46
""".strip()

input2 = """
8
2
80
""".strip()

output2 = """
818
""".strip()


def main():
    # print(sum(i * int(input()) for i in [1, 5, 10]))
    a = int(input())
    b = int(input())
    c = int(input())
    d = a + 5 * b + 10 * c
    print(d)


# 以下は固定
def test_main(monkeypatch) -> None:
    check(monkeypatch, main, input1, output1)
    check(monkeypatch, main, input2, output2)


def check(monkeypatch, func: None, input: str, output: str) -> None:
    import io

    stdin = io.StringIO(input)
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stdout", stdout)
        func()

    assert stdout.getvalue() == output + "\n"


if __name__ == "__main__":
    pytest.main([__file__])
