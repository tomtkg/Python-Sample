import numpy as np

def is_finish(m, a, b) -> bool:  # 終了条件を満たしているか
    f = lambda i: range(min(a[i], b[i]) + 1, max(a[i], b[i]))
    if a[0] == b[0]:  # 同じ行の場合
        return all(m[a[0], j] == '.' for j in f(1))
    if a[1] == b[1]:  # 同じ列の場合
        return all(m[i, a[1]] == '.' for i in f(0))
    return False

def highway():
    H, _ = map(int, input().split())
    m = np.array([list(input()) for _ in range(H)])  # マップ
    a = np.argwhere(m == "A")[0]  # "A"の位置
    b = np.argwhere(m == "B")[0]  # "B"の位置
    
    movable = set(map(tuple, np.argwhere(m != "#")))  # 訪問可能な位置の集合
    queue = [[a, 0]]  # BFSのキュー: [位置, 距離]
    
    while queue:  # Breadth-First Search
        a, dist = queue.pop(0)  # キューの先頭を取得

        if is_finish(m, a, b):  # 終了条件を満たしている
            print(dist)  # 距離を出力
            return

        for d in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4方向の確認
            pos = (a[0] + d[0], a[1] + d[1])  # 位置の更新
            if pos in movable:  # 訪問可能
                queue.append([pos, dist + 1])  # 現在位置と距離をキューに追加
                movable.remove(pos)  # 訪問済みとして削除

    print(-1)  # AからBを見つけることができない
