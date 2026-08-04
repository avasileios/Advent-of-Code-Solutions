import os
import sys
import re


def get_edges(tile):
    top = tile[0]
    bottom = tile[-1]
    left = ''.join(r[0] for r in tile)
    right = ''.join(r[-1] for r in tile)
    return top, right, bottom, left


def transforms(tile):
    """All 8 orientations of a tile (rotations + flips)."""
    outs = []
    cur = tile
    for _ in range(2):
        for _ in range(4):
            outs.append([r[:] for r in cur])
            cur = [''.join(cur[h][w] for h in range(len(cur) - 1, -1, -1))
                   for w in range(len(cur[0]))]
        cur = cur[::-1]
    return outs


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
        tiles[int(m.group(1))] = lines[1:]

    orients = {tid: transforms(t) for tid, t in tiles.items()}

    # assemble with BFS from an arbitrary tile.  Edges are matched WITHOUT
    # reversal: every flip is already among the 8 orientations, so the
    # matching orientation is unique.
    placed = {}  # (x, y) -> (tid, oi)
    used = set()
    tid0 = next(iter(tiles))
    placed[(0, 0)] = (tid0, 0)
    used.add(tid0)

    queue = [(0, 0)]
    while queue:
        x, y = queue.pop()
        for nx, ny in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
            if (nx, ny) in placed:
                continue
            # needed edges (top, right, bottom, left) from the neighbors
            need = [None, None, None, None]
            if (nx, ny - 1) in placed:
                ptid, poi = placed[(nx, ny - 1)]
                need[0] = get_edges(orients[ptid][poi])[2]  # their bottom
            if (nx + 1, ny) in placed:
                ptid, poi = placed[(nx + 1, ny)]
                need[1] = get_edges(orients[ptid][poi])[3]  # their left
            if (nx, ny + 1) in placed:
                ptid, poi = placed[(nx, ny + 1)]
                need[2] = get_edges(orients[ptid][poi])[0]  # their top
            if (nx - 1, ny) in placed:
                ptid, poi = placed[(nx - 1, ny)]
                need[3] = get_edges(orients[ptid][poi])[1]  # their right
            found = None
            for tid, ol in orients.items():
                if tid in used:
                    continue
                for oi, orient in enumerate(ol):
                    t, r, b, l = get_edges(orient)
                    if ((need[0] is None or need[0] == t) and
                            (need[1] is None or need[1] == r) and
                            (need[2] is None or need[2] == b) and
                            (need[3] is None or need[3] == l)):
                        found = (tid, oi)
                        break
                if found:
                    break
            if found is None:
                continue
            placed[(nx, ny)] = found
            used.add(found[0])
            queue.append((nx, ny))

    if len(placed) != len(tiles):
        print('assembly incomplete:', len(placed))
        return

    # build the image without borders
    xs = [p[0] for p in placed]
    ys = [p[1] for p in placed]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    size = len(orients[tid0][0]) - 2
    image = []
    for y in range(y0, y1 + 1):
        for row in range(size):
            line = ''
            for x in range(x0, x1 + 1):
                tid, oi = placed[(x, y)]
                tile = orients[tid][oi]
                line += tile[row + 1][1:-1]
            image.append(line)

    # search for sea monsters in every orientation of the image
    monster = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   ',
    ]
    mh = len(monster)
    mw = len(monster[0])
    monster_cells = set()
    for my in range(mh):
        for mx in range(mw):
            if monster[my][mx] == '#':
                monster_cells.add((mx, my))

    best = 0
    for img in transforms(image):
        h = len(img)
        w = len(img[0])
        found = 0
        for y in range(h - mh + 1):
            for x in range(w - mw + 1):
                if all(img[y + my][x + mx] == '#'
                       for mx, my in monster_cells):
                    found += 1
        best = max(best, found)

    total_hash = sum(row.count('#') for row in image)
    print(total_hash - best * len(monster_cells))


if __name__ == "__main__":
    main()
