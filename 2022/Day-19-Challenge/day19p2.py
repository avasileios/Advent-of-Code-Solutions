import os
import sys
import re
from functools import lru_cache


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        data = f.read()

    blueprints = []
    for line in data.strip().splitlines():
        nums = list(map(int, re.findall(r'\d+', line)))
        bp = {
            'ore': (nums[1], 0, 0),
            'clay': (nums[2], 0, 0),
            'obs': (nums[3], nums[4], 0),
            'geo': (nums[5], 0, nums[6]),
        }
        blueprints.append(bp)

    result = 1
    for bp in blueprints[:3]:
        max_ore = max(c[0] for c in bp.values())
        max_clay = max(c[1] for c in bp.values())
        max_obs = max(c[2] for c in bp.values())

        best = 0

        @lru_cache(maxsize=None)
        def dfs(minute, ore, clay, obs, geo, r_ore, r_clay, r_obs, r_geo):
            nonlocal best
            remaining = 32 - minute
            if geo + r_geo * remaining + remaining * (remaining - 1) // 2 <= best:
                return
            if minute == 32:
                best = max(best, geo)
                return
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
            dfs(minute + 1, ore + r_ore, clay + r_clay, obs + r_obs, geo + r_geo,
                r_ore, r_clay, r_obs, r_geo)

        dfs(0, 0, 0, 0, 0, 1, 0, 0, 0)
        result *= best

    print(result)


if __name__ == "__main__":
    main()
