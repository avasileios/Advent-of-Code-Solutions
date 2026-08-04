import os
import sys
import re
from fractions import Fraction


def parse_machine(line):
    """Parse a machine line: [light diagram] (buttons...) {joltage targets}."""
    target_match = re.search(r'\[([.#]+)\]', line)
    target_state = [1 if c == '#' else 0 for c in target_match.group(1)]

    buttons = []
    for b_str in re.findall(r'\(([\d,]+)\)', line):
        buttons.append([int(x) for x in b_str.split(',')])

    joltage_match = re.search(r'\{([\d,]+)\}', line)
    joltage_target = [int(x) for x in joltage_match.group(1).split(',')]

    return target_state, joltage_target, buttons


def solve_nonneg_min_sum(num_counters, buttons, target):
    """Part 2: solve A.x = b over the integers, x >= 0, minimizing sum(x).

    Gaussian elimination over the rationals gives each pivot variable as a
    linear expression of the free variables; enumerate the (few) free
    variables with branch-and-bound pruning.
    """
    num_vars = len(buttons)
    num_eqs = num_counters

    # augmented matrix with Fractions
    matrix = []
    for r in range(num_eqs):
        row = [Fraction(1, 1) if r in b else Fraction(0, 1) for b in buttons]
        row.append(Fraction(target[r], 1))
        matrix.append(row)

    # RREF over the rationals
    pivot_row = 0
    pivot_cols = []
    for c in range(num_vars):
        if pivot_row >= num_eqs:
            break
        swap_row = -1
        for r in range(pivot_row, num_eqs):
            if matrix[r][c] != 0:
                swap_row = r
                break
        if swap_row == -1:
            continue
        matrix[pivot_row], matrix[swap_row] = matrix[swap_row], matrix[pivot_row]
        pivot_val = matrix[pivot_row][c]
        for k in range(c, num_vars + 1):
            matrix[pivot_row][k] /= pivot_val
        for r in range(num_eqs):
            if r != pivot_row and matrix[r][c] != 0:
                factor = matrix[r][c]
                for k in range(c, num_vars + 1):
                    matrix[r][k] -= factor * matrix[pivot_row][k]
        pivot_cols.append(c)
        pivot_row += 1

    # consistency check
    for r in range(pivot_row, num_eqs):
        if matrix[r][num_vars] != 0:
            return float('inf')

    free_cols = [c for c in range(num_vars) if c not in pivot_cols]
    pivot_map = {col: r for r, col in enumerate(pivot_cols)}

    # each pivot x_p = const - sum(coeff_f * x_f)
    pivot_dependencies = []
    for p_col in pivot_cols:
        r = pivot_map[p_col]
        const_val = matrix[r][num_vars]
        coeffs = [(f_idx, matrix[r][f_col])
                  for f_idx, f_col in enumerate(free_cols)
                  if matrix[r][f_col] != 0]
        pivot_dependencies.append((const_val, coeffs))

    # a button never needs to be pressed more than the largest target
    search_limit = max(target) + 1
    num_free = len(free_cols)
    current_free = [Fraction(0, 1)] * num_free

    min_presses = float('inf')

    def evaluate(values):
        """Total presses for a full assignment of the free variables, or inf
        if any pivot variable is negative or non-integer."""
        total = sum(values)
        for const_val, coeffs in pivot_dependencies:
            val = const_val
            for f_i, c_val in coeffs:
                val -= c_val * values[f_i]
            if val < 0 or val.denominator != 1:
                return float('inf')
            total += int(val)
        return total

    # Seed the search with a few cheap assignments (small constant values)
    # so the branch-and-bound pruning is tight from the start.
    for seed_v in range(6):
        v = evaluate([seed_v] * num_free)
        if v < min_presses:
            min_presses = v
    if num_free:
        for seed_v in range(2, 7):
            v = evaluate([seed_v, 0] + [0] * (num_free - 2)
                         if num_free > 1 else [seed_v])
            if v < min_presses:
                min_presses = v

    def recursive(f_idx, current_sum):
        nonlocal min_presses
        if current_sum >= min_presses:
            return
        if f_idx == num_free:
            total = current_sum
            for const_val, coeffs in pivot_dependencies:
                val = const_val
                for f_i, c_val in coeffs:
                    val -= c_val * current_free[f_i]
                if val < 0 or val.denominator != 1:
                    return
                total += int(val)
                if total >= min_presses:
                    return
            min_presses = total
            return
        for val in range(search_limit):
            if current_sum + val >= min_presses:
                break
            current_free[f_idx] = Fraction(val, 1)
            recursive(f_idx + 1, current_sum + val)

    recursive(0, 0)
    return min_presses


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    total = 0
    for line in lines:
        _, joltage_target, buttons = parse_machine(line)
        total += solve_nonneg_min_sum(len(joltage_target), buttons,
                                      joltage_target)

    print(total)


if __name__ == "__main__":
    main()
