import os
import sys
import re
from functools import lru_cache


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        data = f.read()

    # cost[type] = (ore, clay, obsidian)
    blueprints = []
    for line in data.strip().splitlines():
        nums = list(map(int, re.findall(r'\d+', line)))
        # blueprint id, ore cost, clay cost, obs ore, obs clay, geo ore, geo obs
        bp = {
            'ore': (nums[1], 0, 0),
            'clay': (nums[2], 0, 0),
            'obs': (nums[3], nums[4], 0),
            'geo': (nums[5], 0, nums[6]),
        }
        blueprints.append(bp)

    total = 0
    for bi, bp in enumerate(blueprints, 1):
        # upper bounds on robots
        max_ore = max(c[0] for c in bp.values())
        max_clay = max(c[1] for c in bp.values())
        max_obs = max(c[2] for c in bp.values())

        best = 0

        @lru_cache(maxsize=None)
        def dfs(minute, ore, clay, obs, geo, r_ore, r_clay, r_obs, r_geo):
            nonlocal best
            remaining = 24 - minute
            # upper bound: geode + r_geo*remaining + triangular(remaining)
            if geo + r_geo * remaining + remaining * (remaining - 1) // 2 <= best:
                return
            if minute == 24:
                best = max(best, geo)
                return
            # try building each robot
            for robot, (co, cc, cobs) in bp.items():
                if robot == 'ore' and r_ore >= max_ore:
                    continue
                if robot == 'clay' and r_clay >= max_clay:
                    continue
                if robot == 'obs' and r_obs >= max_obs:
                    continue
                if co <= ore and cc <= clay and cobs <= obs:
                    dfs(minute + 1,
                        ore + r_ore - co, clay + r_clay - cc, obs + r_obs - cobs,
                        geo + r_geo,
                        r_ore + (robot == 'ore'), r_clay + (robot == 'clay'),
                        r_obs + (robot == 'obs'), r_geo + (robot == 'geo'))
            # also do nothing
            dfs(minute + 1, ore + r_ore, clay + r_clay, obs + r_obs, geo + r_geo,
                r_ore, r_clay, r_obs, r_geo)

        dfs(0, 0, 0, 0, 0, 1, 0, 0, 0)
        total += bi * best

    print(total)


if __name__ == "__main__":
    main()
