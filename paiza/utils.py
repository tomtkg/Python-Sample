import io

def check(monkeypatch, func: None, input: str, output: str):
    stdin = io.StringIO(input)
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stdout", stdout)
        func()

    assert stdout.getvalue() == output + "\n"
