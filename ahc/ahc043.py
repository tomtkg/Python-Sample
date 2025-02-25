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


def get_ids(
    pos_to_idx: dict[Pos, tuple[set[int], set[int]]], poss: list[Pos]
) -> tuple[set[int], set[int]]:
    set1, set2 = set(), set()
    for pos in poss:
        if pos in pos_to_idx:
            idx1, idx2 = pos_to_idx[pos]
            set1.update(idx1)
            set2.update(idx2)

    return set1, set2


def is_between(p1: Pos, p2: Pos, p: Pos):
    return (min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0])) and (
        min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1])
    )


def next_pos(flag: bool, p: Pos, target: Pos) -> Pos:
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
    ):
        self.N = N
        # self.M = M
        # self.K = K
        self.T = T
        self.idx_to_pos = idx_to_pos
        self.pos_to_idx = pos_to_idx

        self.money = K
        self.income = 0
        self.actions = []
        self.rails = set()
        self.stations = set()  # 建設済みの駅
        self.stations2 = set()  # 建設済みの駅 + 線路上の駅候補

    def calc_income(self, stations: set[Pos] = {()}) -> int:
        stations |= self.stations
        home_ids, work_ids = get_ids(self.pos_to_idx, stations)
        return sum(distance(*self.idx_to_pos[idx]) for idx in home_ids & work_ids)

    def build_rail(self, type: int, r: int, c: int) -> None:
        while self.money < COST_RAIL:
            self.build_nothing()
        self.money += self.income - COST_RAIL
        self.actions.append(f"{type} {r} {c}")

    def build_rails(self, path: list[Pos]) -> None:
        self.rails.update(path)
        for i in range(1, len(path) - 1):
            symbol = get_symbol(path[i - 1], path[i], path[i + 1])
            self.build_rail(symbol, path[i][0], path[i][1])

    def build_station(self, p: Pos) -> None:
        if p in self.stations:
            return
        while self.money < COST_STATION:
            self.build_nothing()

        self.stations.add(p)
        self.income = self.calc_income()
        self.money += self.income - COST_STATION
        self.actions.append(f"{0} {p[0]} {p[1]}")

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

    def find_2stations(self, candidate: set[Pos]) -> tuple[list[Pos], set[Pos]]:
        max_d = (self.money - COST_STATION * 2) // COST_RAIL + 1
        score = 0
        stations = []

        list_candidate, n = list(candidate), len(candidate)

        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = list_candidate[i], list_candidate[j]

                d = distance(p1, p2)
                if d > max_d:
                    continue

                h_ids1, w_ids1 = self.pos_to_idx[p1]
                h_ids2, w_ids2 = self.pos_to_idx[p2]
                pair_ids = h_ids1 & w_ids2 | h_ids2 & w_ids1

                income = sum(distance(*self.idx_to_pos[idx]) for idx in pair_ids)
                s = self.money - (9900 + 100 * d) + (800 - d) * income

                if s > score:
                    score = s
                    stations = [p1, p2]

        candidate.difference_update(stations)

        return stations, candidate

    def find_next(
        self, stations: list[Pos], candidate: set[Pos]
    ) -> tuple[list[Pos], set[Pos]]:
        h_ids, w_ids = get_ids(self.pos_to_idx, stations)
        h_ids, w_ids = h_ids - w_ids, w_ids - h_ids

        score = 0
        income = 0
        station = None

        for p in candidate:
            home_ids, work_ids = self.pos_to_idx[p]
            pair2 = (h_ids | home_ids) & (w_ids | work_ids)

            sumd = sum(distance(*self.idx_to_pos[idx]) for idx in pair2)
            s = 1000 * len(pair2) + 10 * sumd + len(home_ids) + len(work_ids)

            if s > score:
                score = s
                income = sumd
                station = p

        if income > 0:
            stations.append(station)
        candidate.remove(station)

        return stations, candidate

    def get_built(self, built: list[Pos], stations: list[Pos]) -> list[Pos]:
        for p in stations:
            if p in self.rails:
                continue
            for i in range(1, len(built)):
                if is_between(built[i - 1], built[i], p):
                    built = built[:i] + [p] + built[i:]
                    break

        return built

    def build_path(self, stations: list[Pos]) -> list[Pos]:
        path = [stations[0]]
        segment2 = []

        for goal in stations[1:]:
            segment, flag = [path[-1]], False

            while segment[-1] != goal:
                current = segment[-1]

                if current in self.rails:
                    if current in self.stations2:
                        path.extend(segment[1:])
                        return path

                    detour = self.detour(path + segment, goal)
                    if detour is not None:
                        segment.pop()
                        segment.extend(detour)
                        
                        if detour[-1] == goal:
                            break
                        else:
                            path.extend(segment[1:])
                            return path

                    if flag:
                        path.extend(min(segment, segment2, key=len)[1:])
                        return path
                    else:
                        segment2 = segment[:]
                        segment, flag = [path[-1]],  True
                        continue

                segment.append(next_pos(flag, current, goal))

            path.extend(segment[1:])

        return path

    def detour(self, out: list[Pos], goal: Pos) -> list[Pos] | None:
        x, y = out[-2]
        for dx, dy in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            p = (x + dx, y + dy)
            if p in out or not (0 <= p[0] < self.N and 0 <= p[1] < self.N):
                continue

            path, flag = [p], False

            while True:
                current = path[-1]
                if current == goal:
                    return path

                if current in self.rails or current in out:
                    if current in self.stations2:
                        return path
                    if flag:
                        break

                    path, flag = [p], True
                    continue

                path.append(next_pos(flag, current, goal))

        return None

    def calc_score(self, path: list[Pos]) -> tuple[int, int]:
        s = self.money - COST_STATION
        t = self.T - len(self.actions)
        income = self.income
        score = self.money + t * income

        if path[-1] not in self.stations and path[0] not in self.rails:
            t2 = max(1, -s // income + 1)
            s += t2 * income - COST_STATION
            t -= t2
            income = self.calc_income({path[-1]})

        s -= COST_RAIL * max(0, len(path) - 2)
        t2 = max(len(path) - 2, -s // income + 1)
        s += t2 * income + (t - t2) * self.calc_income({path[-1], path[0]})

        return score, s

    def solve(self, candidate: set[Pos]):
        # 建設候補駅を見つける
        stations, candidate = self.find_2stations(candidate)
        while len(candidate) > 0:
            stations, candidate = self.find_next(stations, candidate)

        # 駅と線路を建設
        self.first_build(stations)
        leftovers = []
        for i in range(2, len(stations)):
            ok = self.second_build(i, stations)
            if not ok:
                leftovers.append(stations[i])
        for i in range(len(leftovers)):
            _ = self.second_build(i, leftovers)

        # あとは待機
        num_stop = len(self.actions)
        for i in range(num_stop, self.T):
            self.build_nothing()

        return num_stop


def main():
    N, M, K, T = map(int, input().split())

    data = [tuple(map(int, line.split())) for line in sys.stdin.read().splitlines()]
    idx_to_pos = [*[((r0, c0), (r1, c1)) for r0, c0, r1, c1 in data]]
    pos_to_idx = build_pos_to_idx(idx_to_pos, N)

    candidate = build_candidate(pos_to_idx, M)

    solver = Solver(N, M, K, T, idx_to_pos, pos_to_idx)
    stop = solver.solve(candidate)

    print("\n".join(map(str, solver.actions)))
    print(
        f"score, {solver.money}, stations, {len(solver.stations)}, stop, {stop}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    sys.stdin = open("ahc/ahc043.txt")
    main()
