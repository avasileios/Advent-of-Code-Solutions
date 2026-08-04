import os
import sys


def path_to_root(obj, parent):
    path = []
    cur = obj
    while cur in parent:
        cur = parent[cur]
        path.append(cur)
    return path


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    parent = {}
    for line in lines:
        a, b = line.split(')')
        parent[b] = a

    you_path = path_to_root('YOU', parent)
    san_path = path_to_root('SAN', parent)
    you_set = set(you_path)

    # first common ancestor
    transfers = None
    for i, obj in enumerate(san_path):
        if obj in you_set:
            transfers = i + you_path.index(obj)
            break

    print(transfers)


if __name__ == "__main__":
    main()
