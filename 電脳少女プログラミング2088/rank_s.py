def rooftop():
    import numpy as np
    from scipy.spatial import distance

    H, W, M = map(int, input().split())
    m = np.zeros([H, W], bool)  # マップ
    rc = np.array([[r, c] for r in range(H) for c in range(W)])

    f = lambda r, c, s: s >= distance.cdist(
        np.array([[r, c]]), rc, "cityblock"
    ).reshape(H, W)

    for _ in range(M):
        r, c, s = map(int, input().split())
        m[f(r - 1, c - 1, s)] = True  # r, c, sでマップを更新

    max_s = 0  # 他の縄張りとギリギリで重なる，最大のs
    for r, c in rc:  # マップを全探索
        for s in range(max_s, max(H, W)):  # s = max_sから探索
            if np.any(m & (f(r, c, s))):  # 他の縄張りと重なる
                max_s = max(max_s, s)  # max_sを更新
                break

    print(max_s - 1)  # 他の縄張りと重ならないsを出力
