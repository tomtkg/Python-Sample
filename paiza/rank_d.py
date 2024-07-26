def square():
    print("*" * int(input()))


def email_address():
    print(input() + "@" + input())


def addition():
    print(sum(int(x) for x in input().split()))


def min_num():
    print(min(int(input()) for _ in range(5)))


def diff_str():
    print("OK" if input() == input() else "NG")
