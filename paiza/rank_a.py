def school_hiking():
    from itertools import combinations

    N, X = map(int, input().split())
    a = [int(input()) for _ in range(N)]

    for r in range(N):
        b = [X - sum(c) for c in combinations(a, N - r) if X >= sum(c)]
        if b:
            print(min(b))
            break


def janken():
    N, M = map(int, input().split())
    s = input()
    a = [s.count(x) for x in "GCP"]

    max_wins = 0
    for p in range(N):        # パーの数
        c = (M - p * 5) // 2  # チョキの数
        g = N - p - c         # グーの数
        if g >= 0 and p * 5 + c * 2 == M:
            max_wins = max(max_wins, sum(map(min, [p, g, c], a)))

    print(max_wins)


def h(n, a, b, c, move):  # ハノイの塔の再帰関数
    if n > 0:
        h(n - 1, a, c, b, move)
        move.append((a, b))  # 移動を記録
        h(n - 1, c, b, a, move)


def hanoi():
    n, t = map(int, input().split())
    move = []  # 移動記録用のリスト
    h(n, 0, 2, 1, move)

    poles = [list(range(n, 0, -1)), [], []]
    for a, b in move[:t]:  # 円盤をt回動かす
        poles[b].append(poles[a].pop())

    for x in poles:
        print(*x or "-")


def origami():
    v = []
    for _ in range(int(input())):
        v += [0] + [1 ^ i for i in v[::-1]]
    print(*v, sep="")


def book_sort():
    input()  # 不要な入力を捨てる
    x = [int(x) - 1 for x in input().split()]

    count = 0
    for i in range(len(x)):
        while x[i] != i:
            x[x[i]], x[i] = x[i], x[x[i]]
            count += 1
    print(count)
