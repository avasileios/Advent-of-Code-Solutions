import os
import sys
import re


def get_edges(tile):
    """Return (top, right, bottom, left) edge strings of a tile."""
    top = tile[0]
    bottom = tile[-1]
    left = ''.join(r[0] for r in tile)
    right = ''.join(r[-1] for r in tile)
    return top, right, bottom, left


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        data = f.read()

    tiles = {}
    for block in data.split('\n\n'):
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        m = re.match(r'Tile (\d+):', lines[0])
        tid = int(m.group(1))
        tiles[tid] = lines[1:]

    # count how many edges of each tile match other tiles
    edge_owner = {}
    for tid, tile in tiles.items():
        for e in get_edges(tile):
            edge_owner.setdefault(e, []).append(tid)
            edge_owner.setdefault(e[::-1], []).append(tid)

    corners = []
    for tid, tile in tiles.items():
        # a corner has exactly two edges that match no other tile
        unmatched = 0
        for e in get_edges(tile):
            if all(other == tid for other in edge_owner[e]):
                unmatched += 1
        if unmatched == 2:
            corners.append(tid)

    result = 1
    for c in corners:
        result *= c
    print(result)


if __name__ == "__main__":
    main()
