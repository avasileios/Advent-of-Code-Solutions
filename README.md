# 🎄 Advent of Code Solutions

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Years](https://img.shields.io/badge/Years-2015%E2%80%932025-0f0f23?style=for-the-badge)
![Stars](https://img.shields.io/badge/Stars-%E2%98%85%20%E2%98%85-ffff66?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-009900?style=for-the-badge)

> **My complete [Advent of Code](https://adventofcode.com) journey — every year, every day, every star.** 🐍✨

A collection of solutions to the [Advent of Code](https://adventofcode.com) programming puzzles, spanning **11 years** of daily coding challenges. Each solution is written in **Python**, with a consistent structure, runnable test harnesses, and verified results.

---

## 📅 Years

| Year | Days | Solvers | Runner | Status |
|------|:----:|:-------:|:------:|:------:|
| [2015](https://adventofcode.com/2015) | 25 | 49 | ✅ | ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ |
| [2016](https://adventofcode.com/2016) | 25 | 49 | ✅ | ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ |
| [2017](https://adventofcode.com/2017) | 25 | 49 | ✅ | ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ |
| [2018](https://adventofcode.com/2018) | 25 | 49 | ✅ | ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ |
| [2019](https://adventofcode.com/2019) | 25 | 49 | ✅ | ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ |
| [2020](https://adventofcode.com/2020) | 25 | 49 | ✅ | ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ |
| [2021](https://adventofcode.com/2021) | 25 | 49 | ✅ | ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ |
| [2022](https://adventofcode.com/2022) | 25 | 49 | ✅ | ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ |
| [2023](https://adventofcode.com/2023) | 25 | 49 | ✅ | ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ |
| [2024](https://adventofcode.com/2024) | 25 | 49 | ✅ | ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ |
| [2025](https://adventofcode.com/2025) | 12 | 24 | ✅ | ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ |

**Total: 262 days · 514 solvers · all years complete** 🏆

---

## 📁 Repository Structure

Every year follows the exact same layout:

```
Advent-of-Code-Solutions/
├── 2015/                        # Year folder
│   ├── Day-01-Challenge/        # One folder per day
│   │   ├── day1p1.py            #   Part 1 solution
│   │   ├── day1p2.py            #   Part 2 solution
│   │   └── input.txt            #   Puzzle input
│   ├── Day-02-Challenge/
│   │   ├── day2p1.py
│   │   ├── day2p2.py
│   │   └── input.txt
│   ├── ...
│   ├── Day-25-Challenge-Final/  # Day 25 has a special "Final" folder
│   │   ├── day25Final.py        #   Single script for both parts
│   │   └── input.txt
│   ├── run_all_advent.py        # Runs all 49 solvers in this year
│   ├── fix_advent_paths.py      # Path-fixing helper for the runner
│   └── advent_results_*.txt     # Latest run results
├── 2016/
├── ...
└── 2025/
```

Each `dayNp1.py` / `dayNp2.py` script:
- 🧩 Solves one puzzle part
- 📥 Reads its input from `input.txt` in the same folder
- 🖨️ Prints the answer when run

---

## 🚀 Usage

### Run a single solution

```bash
python3 2023/Day-01-Challenge/day1p1.py
# or pass an explicit input file
python3 2023/Day-01-Challenge/day1p1.py /path/to/input.txt
```

### Run a whole year (all 49 solvers)

```bash
cd 2023
python3 run_all_advent.py
```

The runner executes every solver in the year, times them, and saves a full report to `advent_results_<timestamp>.txt`.

### Run everything

```bash
for year in 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025; do
  cd "$year" && python3 run_all_advent.py && cd ..
done
```

---

## 🛠️ Requirements

- **Python 3.8+** (standard library only — no third-party dependencies 🎉)

---

## 📜 Notes

- All solutions are original work, written for learning and fun.
- Puzzle inputs are unique per user — the `input.txt` files here are my own.
- Results files (`advent_results_*.txt`) contain the latest verified output of every solver.
- Special shout-out to the [Advent of Code](https://adventofcode.com) team for creating the best holiday coding tradition. 🎅

---

<p align="center">
  <sub>Made with 💚 and a lot of ☕ · Merry Christmas, and happy coding!</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Day%2025%20Complete-%E2%98%85%E2%98%85-ffff66?style=flat-square" alt="Day 25 complete"/>
</p>
