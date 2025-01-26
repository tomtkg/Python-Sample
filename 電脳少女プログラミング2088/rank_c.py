def room():
    n, a = int(input()), ""
    while n != 0:
        n, m = divmod(n, 3)
        a = str(m) + a
        if m == 2: n += 1
    print(a or 0)


def park():
    import numpy as np
    f = lambda: np.fromstring(input(), dtype=int, sep=" ")
    s = f()
    v = [np.linalg.norm(s[1:] - f()) for _ in range(s[0])]
    print(np.argmin(v) + 1)
