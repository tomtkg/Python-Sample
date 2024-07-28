def name_card():
    n, m = map(int, input().split())
    a, b = divmod(m - 1, 2 * n)
    print(2 * n * a + 2 * n - b)


def long_table():
    f = lambda: map(int, input().split())
    n, m = f()

    y = set()  # 客が居る座席の集合
    for _ in range(m):
        a, b = f()
        c = {(b + i) % n for i in range(a)}
        if not y & c:  # 集合yとcに重複がない
            y |= c  # yにcを追加（yとcの和集合でyを更新）

    print(len(y))


def word_chain():
    N, K, M = map(int, input().split())
    a = {input() for _ in range(K)}  # 単語集
    b = set()  # 発言集
    c = ""  # 直前の人の発言の最後の文字

    y = list(range(1, N + 1))  # 参加者リスト
    i = 0  # 手番
    for _ in range(M):
        x = input()
        if x not in a or (c and x[0] != c) or x in b or x[-1] == "z":
            y.pop(i)
            c = ""
        else:
            i += 1
            c = x[-1]

        b.add(x)
        if i >= len(y):
            i = 0

    print(len(y))
    print(*y, sep="\n")


def concentration():
    f = lambda: list(map(int, input().split()))
    H, W, N = f()
    a = [f() for _ in range(H)]
    f()  # 不要な入力を捨てる

    b = [0] * N  # 各プレイヤーの所持トランプ枚数
    i = 0  # 手番
    while sum(b) < H * W:
        s, t, r, u = f()
        if a[s - 1][t - 1] == a[r - 1][u - 1]:
            b[i] += 2
        else:
            i = (i + 1) % N

    print(*b, sep="\n")


def get_row(x: int) -> str:
    row = list(input())
    for _ in range(x):
        for i, c in enumerate(input()):
            if c == "#":
                row[i] = "#"
    return "".join(row)


def display_3d_printer():
    x, _, z = map(int, input().split())
    rows = [get_row(x) for _ in range(z)]
    print(*rows[::-1], sep="\n")
