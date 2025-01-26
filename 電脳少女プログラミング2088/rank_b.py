def downtown():
    import numpy as np
    n = int(input())
    m = np.array([list(input()) for _ in range(n)]) == '.'
    print(sum(np.sum(m[:-i, :-i] & m[:-i, i:] & m[i:, :-i] & m[i:, i:]) for i in range(1, n)))

def hideout():
    f = lambda x: x == x[::-1]
    tf = all(f(list(input())) for _ in range(int(input())))
    print("Yes" if tf else "No")
