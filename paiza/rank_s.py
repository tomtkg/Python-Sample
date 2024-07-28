def group_popularity():
    import numpy as np

    N, M, Q = map(int, input().split())
    N += 1  # 入力が1～Nのため

    m = np.zeros((N, N), dtype=int)
    for _ in range(M):
        a, b, f = map(int, input().split())
        m[a][b] = m[b][a] = f

    g = np.zeros(N, dtype=bool)
    for _ in range(Q):
        q = input().split()
        g[int(q[1])] = q[0] == "+"
        print(np.max(m[g][:, ~g], initial=0))


def search_island():
    from scipy.ndimage import label

    f = lambda: list(map(int, input().split()))
    m = [f() for _ in range(f()[1])]
    print(label(m)[1])


def mod7():
    from itertools import combinations

    a = [int(input()) for _ in range(int(input()))]
    print(sum(not sum(x) % 7 for x in combinations(a, 3)))


def word_collection():
    from collections import defaultdict

    N, M = map(int, input().split())

    d = defaultdict(int)
    for _ in range(N):
        k, v = input().split()
        d[k] += int(v)

    for _ in range(M):
        q = input()
        print(sum(v * k.startswith(q) for k, v in d.items()))


def continuous_winning():
    from collections import Counter

    N, X = map(int, input().split())
    A = [int(input()) for _ in range(N)]

    # b：(現在の連勝数, X連勝後に敗北) とその数
    b = Counter({(0, False): 1})

    for a in A:  # 各ステージの処理
        c = Counter()
        for (w, t), n in b.items():
            if w + a <= X:
                # 全勝しても連勝数がX以下の場合
                c[(w + a, t)] += n  # 全勝パターン
                c[(0, t)] += n * a  # 途中敗北
            else:
                # 全勝すると連勝数がXを超える場合
                c[(0, True)] += n  # X連勝後に敗北
                c[(0, t)] += n * (X - w)  # X連勝以下で敗北
                # n * (w + a - X) パターン # 連勝数がX以上

        b = c  # 状態を更新

    print(sum(n for (w, t), n in b.items() if w == X or t) % 10**9)
