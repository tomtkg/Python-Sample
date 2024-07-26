def leftover():
    m, p, q = map(int, input().split())
    print(m * (100 - p) * (100 - q) / 1e4)


def fizz_buzz():
    for i in range(1, int(input()) + 1):
        print(
            "Fizz Buzz" if i % 15 == 0
            else "Fizz" if i % 3 == 0
            else "Buzz" if i % 5 == 0
            else i
        )


def mikan():
    N, M = map(int, input().split())
    for _ in range(M):
        print(max(N, round(int(input()) / N) * N))


def umpire():
    for _ in range(int(input()) - 1):
        print(input() + "!")
    print("fourball!" if input() == "ball" else "out!")


def lottery():
    b = input()
    for _ in range(int(input())):
        v = input()
        print(
            "first" if b == v  # 1等：当選番号と一致する番号
            else "adjacent" if abs(int(b) - int(v)) == 1  # 前後賞：当選番号±1の番号
            else "second" if b[-4:] == v[-4:]  # 2等：当選番号と下4桁が一致する番号
            else "third" if b[-3:] == v[-3:]   # 3等：当選番号と下3桁が一致する番号
            else "blank"
        )
