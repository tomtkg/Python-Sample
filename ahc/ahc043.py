import sys

Pos = tuple[int, int]
COST_STATION = 5000
COST_RAIL = 100
OFFSETS = [
    (0, 0),
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
    (2, 0),
    (-2, 0),
    (0, 2),
    (0, -2),
]


def build_pos_to_idx(
    idx_to_pos: list[tuple[Pos, Pos]],
    N: int,
) -> dict[Pos, tuple[set[int], set[int]]]:
    pos_to_idx = {}
    for i, poss in enumerate(idx_to_pos):
        for j, (px, py) in enumerate(poss):
            for dx, dy in OFFSETS:
                p = (px + dx, py + dy)
                if not (0 <= p[0] < N and 0 <= p[1] < N):
                    continue

                if p not in pos_to_idx:
                    pos_to_idx[p] = (set(), set())
                pos_to_idx[p][j].add(i)

    return pos_to_idx


def build_candidate(
    pos_to_idx: dict[Pos, tuple[set[int], set[int]]], m: int
) -> set[Pos]:
    all_pos = set(pos_to_idx.keys())
    ext_pos = set()
    home_uncovered = set(range(m))
    work_uncovered = set(range(m))

    while home_uncovered or work_uncovered:
        score = 0
        pos = None
        home, work = set(), set()

        for p in all_pos:
            h, w = pos_to_idx[p]
            total_cover = len(h & home_uncovered) + len(w & work_uncovered)
            s = 100 * total_cover + len(h | w)

            if s > score:
                score = s
                pos = p
                home, work = h, w

        ext_pos.add(pos)
        all_pos.remove(pos)
        home_uncovered.difference_update(home)
        work_uncovered.difference_update(work)

    return ext_pos


def get_ids(stations: set[Pos], map: dict[Pos, set[int]]) -> set[int]:
    ids = set()
    for p in stations:
        if p in map:
            ids |= map[p]
    return ids


def is_between(p1: Pos, p2: Pos, p: Pos):
    return (min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0])) and (
        min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1])
    )


def next_position(flag: bool, p: Pos, target: Pos) -> Pos:
    r, c = p
    tr, tc = target
    if (flag and c != tc) or (not flag and r == tr):
        c += (tc > c) - (tc < c)  # cをtargetに近づける
    else:
        r += (tr > r) - (tr < r)  # rをtargetに近づける
    return r, c


def get_symbol(prev: Pos, curr: Pos, next: Pos) -> int:
    if prev[0] == next[0]:
        return 1  # RAIL_HORIZONTAL
    if prev[1] == next[1]:
        return 2  # RAIL_VERTICAL

    if prev[0] < curr[0] and curr[1] < next[1]:
        return 5  # RAIL_RIGHT_UP
    if prev[0] < curr[0] and curr[1] > next[1]:
        return 4  # RAIL_LEFT_UP
    if prev[0] > curr[0] and curr[1] < next[1]:
        return 6  # RAIL_RIGHT_DOWN
    if prev[0] > curr[0] and curr[1] > next[1]:
        return 3  # RAIL_LEFT_DOWN

    if prev[1] < curr[1] and curr[0] < next[0]:
        return 3  # RAIL_LEFT_DOWN
    if prev[1] < curr[1] and curr[0] > next[0]:
        return 4  # RAIL_LEFT_UP
    if prev[1] > curr[1] and curr[0] < next[0]:
        return 6  # RAIL_RIGHT_DOWN
    if prev[1] > curr[1] and curr[0] > next[0]:
        return 5  # RAIL_RIGHT_UP


def distance(a: Pos, b: Pos) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Solver:
    def __init__(
        self,
        N: int,
        M: int,
        K: int,
        T: int,
        idx_to_pos: list[tuple[Pos, Pos]],
        pos_to_idx: dict[Pos, tuple[set[int], set[int]]],
        candidate: set[Pos],
    ):
        self.N = N
        # self.M = M
        # self.K = K
        self.T = T
        self.idx_to_pos = idx_to_pos
        self.pos_to_idx = pos_to_idx
        self.candidate = candidate

        self.money = K
        self.income = 0
        self.actions = []

    def calc_income(self, stations: set[Pos]) -> int:
        home_ids = get_ids(stations, self.home_map)
        work_ids = get_ids(stations, self.work_map)
        return sum(distance(self.home[id], self.work[id]) for id in home_ids & work_ids)

    def build_rail(self, type: int, r: int, c: int) -> None:
        while self.money < COST_RAIL:
            self.build_nothing()
        self.money += self.income - COST_RAIL
        self.actions.append(f"{type} {r} {c}")

    def build_rails(self, path: list[Pos]) -> None:
        for p in range(1, len(path) - 1):
            symbol = get_symbol(path[p - 1], path[p], path[p + 1])
            self.build_rail(symbol, path[p][0], path[p][1])

    def build_station(self, r: int, c: int) -> None:
        self.stations.add((r, c))
        while self.money < COST_STATION:
            self.build_nothing()
        self.income = self.calc_income(self.stations)
        self.money += self.income - COST_STATION
        self.actions.append(f"{0} {r} {c}")

    def build_nothing(self) -> None:
        self.money += self.income
        self.actions.append("-1")

    def first_step(self) -> tuple[Pos, Pos]:
        max_d = (self.money - COST_STATION * 2) // COST_RAIL + 1
        score = 0
        st, st2 = None, None

        for p1, h_ids in self.home_map.items():
            for p2, w_ids in self.work_map.items():
                d = distance(p1, p2)
                if d < 5 or max_d < d:
                    continue

                pair_ids = h_ids & w_ids
                if p2 in self.home_map and p1 in self.work_map:
                    pair_ids |= self.home_map[p2] & self.work_map[p1]

                income = sum(distance(self.home[id], self.work[id]) for id in pair_ids)
                s = self.money - (9900 + 100 * d) + (800 - d) * income

                if s > score:
                    score = s
                    st, st2 = p1, p2

        return st, st2

    def solve(self) -> None:
        # 接続する人を見つける
        rail_count = (self.K - COST_STATION * 2) // COST_RAIL
        person_idx = 0
        while person_idx < self.M:
            if distance(self.home[person_idx], self.workplace[person_idx]) - 1 <= rail_count:
                break
            person_idx += 1
        assert person_idx != self.M

        # 駅の配置
        self.build_station(*self.home[person_idx])
        self.build_station(*self.workplace[person_idx])

        # 線路を配置して駅を接続する
        r0, c0 = self.home[person_idx]
        r1, c1 = self.workplace[person_idx]
        # r0 -> r1
        if r0 < r1:
            for r in range(r0 + 1, r1):
                self.build_rail(RAIL_VERTICAL, r, c0)
            if c0 < c1:
                self.build_rail(RAIL_RIGHT_UP, r1, c0)
            elif c0 > c1:
                self.build_rail(RAIL_LEFT_UP, r1, c0)
        elif r0 > r1:
            for r in range(r0 - 1, r1, -1):
                self.build_rail(RAIL_VERTICAL, r, c0)
            if c0 < c1:
                self.build_rail(RAIL_RIGHT_DOWN, r1, c0)
            elif c0 > c1:
                self.build_rail(RAIL_LEFT_DOWN, r1, c0)
        # c0 -> c1
        if c0 < c1:
            for c in range(c0 + 1, c1):
                self.build_rail(RAIL_HORIZONTAL, r1, c)
        elif c0 > c1:
            for c in range(c0 - 1, c1, -1):
                self.build_rail(RAIL_HORIZONTAL, r1, c)

        # あとは待機
        while len(self.actions) < self.T:
            self.build_nothing()


def main():
    N, M, K, T = map(int, input().split())

    data = [tuple(map(int, line.split())) for line in sys.stdin.read().splitlines()]
    home, work = zip(*[((r0, c0), (r1, c1)) for r0, c0, r1, c1 in data])

    solver = Solver(N, M, K, T, home, work)
    solver.solve()

    print("\n".join(map(str, solver.actions)))
    print(f"score={solver.money}", file=sys.stderr)


if __name__ == "__main__":
    main()
