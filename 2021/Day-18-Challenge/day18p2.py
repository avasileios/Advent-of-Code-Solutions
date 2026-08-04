import os
import sys
import json


def add_left(node, v):
    if isinstance(node, int):
        return node + v
    return [add_left(node[0], v), node[1]]


def add_right(node, v):
    if isinstance(node, int):
        return node + v
    return [node[0], add_right(node[1], v)]


def explode(node, depth=0):
    if isinstance(node, int):
        return False, 0, 0, node
    if depth == 4:
        return True, node[0], node[1], 0
    left, right = node
    changed, cl, cr, new_left = explode(left, depth + 1)
    if changed:
        if cr:
            right = add_left(right, cr)
        return True, cl, 0, [new_left, right]
    changed, cl, cr, new_right = explode(right, depth + 1)
    if changed:
        if cl:
            left = add_right(left, cl)
        return True, 0, cr, [left, new_right]
    return False, 0, 0, node


def split(node):
    if isinstance(node, int):
        if node >= 10:
            return True, [node // 2, (node + 1) // 2]
        return False, node
    changed, new_left = split(node[0])
    if changed:
        return True, [new_left, node[1]]
    changed, new_right = split(node[1])
    if changed:
        return True, [node[0], new_right]
    return False, node


def reduce(node):
    while True:
        changed, _, _, node = explode(node)
        if changed:
            continue
        changed, node = split(node)
        if not changed:
            break
    return node


def magnitude(node):
    if isinstance(node, int):
        return node
    return 3 * magnitude(node[0]) + 2 * magnitude(node[1])


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        numbers = [json.loads(line.strip()) for line in f if line.strip()]

    best = 0
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i == j:
                continue
            total = reduce([numbers[i], numbers[j]])
            best = max(best, magnitude(total))

    print(best)


if __name__ == "__main__":
    main()
