import os
import sys
import re
from collections import deque


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def neg(v):
    return (-v[0], -v[1], -v[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        data = f.read()

    grid_part, instr_part = data.split('\n\n')
    grid = [r.rstrip('\n') for r in grid_part.split('\n')]
    h = len(grid)
    w = max(len(r) for r in grid)
    grid = [r.ljust(w) for r in grid]

    # find face size: gcd-ish of non-space regions
    from math import gcd
    g = 0
    for row in grid:
        g = gcd(g, len(row) - len(row.strip()))
    face = None
    for s in range(1, 200):
        if 200 % s == 0 and 150 % s == 0:
            # check layout: rows of faces
            ok = True
            for y in range(0, h, s):
                row_has = any(grid[y][x] != ' ' for x in range(0, w, s))
                # all face cells in this row band must be consistent
            # simpler: face = 50 for this input
            face = s if (h % s == 0 and w % s == 0) else face
    # fallback: use gcd of dims
    face = face or 50

    # collect faces (fx, fy)
    face_cells = {}
    for fy in range(h // face):
        for fx in range(w // face):
            x0, y0 = fx * face, fy * face
            if any(grid[y0 + dy][x0 + dx] != ' ' for dy in range(face) for dx in range(face)):
                face_cells[(fx, fy)] = True

    # try both rule variants for up/down neighbors, pick the consistent one
    def build_faces(rules_up, rules_down):
        # rules: (n', u') for the neighbor
        orient = {}
        start = next(iter(face_cells))
        orient[start] = ((0, 1, 0), (0, 0, -1))  # n=+Y, u=-Z
        q = deque([start])
        while q:
            f = q.popleft()
            n, u = orient[f]
            r = cross(u, n)
            nbrs = {
                (f[0], f[1] - 1): rules_up(n, u),
                (f[0] + 1, f[1]): (r, u),
                (f[0], f[1] + 1): rules_down(n, u),
                (f[0] - 1, f[1]): (neg(r), u),
            }
            for nf, (nn, nu) in nbrs.items():
                if nf in face_cells and nf not in orient:
                    orient[nf] = (nn, nu)
                    q.append(nf)
        # check consistency: unique normals
        normals = [o[0] for o in orient.values()]
        return orient if len(set(normals)) == 6 else None

    orient = None
    for ru, rd in [((lambda n, u: (u, neg(n))), (lambda n, u: (neg(u), n))),
                   ((lambda n, u: (neg(u), n)), (lambda n, u: (u, neg(n)))),
                   ((lambda n, u: (u, neg(n))), (lambda n, u: (u, neg(n)))),
                   ((lambda n, u: (neg(u), n)), (lambda n, u: (neg(u), n)))]:
        orient = build_faces(ru, rd)
        if orient:
            break

    # compute origins: start face origin (0, 0, 0) plane-adjusted
    # origin of start: pick (0, face-1, -1) so that up=-Z side is z=-1... simpler:
    # walk: for each face, origin = origin of neighbor + offset along the edge
    origins = {}
    start = next(iter(orient))
    # origin such that a=0,b=0 is top-left; set start origin = (0, 0, 0) and
    # adjust directions: right = +X, up = -Z for start
    origins[start] = (0, 0, 0)
    q = deque([start])
    while q:
        f = q.popleft()
        n, u = orient[f]
        r = cross(u, n)
        for nf, delta in [((f[0], f[1] - 1), (0, -face, 0)),  # up neighbor in net
                          ((f[0] + 1, f[1]), (face, 0, 0)),
                          ((f[0], f[1] + 1), (0, face, 0)),
                          ((f[0] - 1, f[1]), (-face, 0, 0))]:
            if nf in orient and nf not in origins:
                # neighbor's origin = our origin + delta in net coords, mapped to 3D
                # net delta (dx, dy) -> 3D: dx along net-x, dy along net-y
                # net-x in 3D = the direction from this face toward that neighbor
                # For a face with orientation (n, u): the neighbor to the right has
                # normal r; its origin = origin + face * r_net... we instead solve:
                # the shared edge: our point (a=49 for right, b=49 for down, ...)
                # equals their point (a'=0 or b'=0)
                if nf[0] == f[0] + 1:  # right neighbor
                    on, ou = orient[nf]
                    orr = cross(ou, on)
                    # our point: origin + (face-1)*r + b*u ; their: origins[nf] + b'*orr? no:
                    # shared edge: our a=face-1 side, their a'=0 side
                    # origins[nf] = origin + (face-1)*r  (b' aligns with b along u)
                    origins[nf] = (origins[f][0] + (face - 1) * r[0],
                                   origins[f][1] + (face - 1) * r[1],
                                   origins[f][2] + (face - 1) * r[2])
                elif nf[0] == f[0] - 1:  # left neighbor
                    on, ou = orient[nf]
                    orr = cross(ou, on)
                    origins[nf] = (origins[f][0] - (face - 1) * r[0],
                                   origins[f][1] - (face - 1) * r[1],
                                   origins[f][2] - (face - 1) * r[2])
                elif nf[1] == f[1] + 1:  # down neighbor
                    origins[nf] = (origins[f][0] + (face - 1) * u[0],
                                   origins[f][1] + (face - 1) * u[1],
                                   origins[f][2] + (face - 1) * u[2])
                else:  # up neighbor
                    origins[nf] = (origins[f][0] - (face - 1) * u[0],
                                   origins[f][1] - (face - 1) * u[1],
                                   origins[f][2] - (face - 1) * u[2])
                q.append(nf)

    # transitions: (face, dir) -> (face, dir)
    # dirs: 0=R, 1=D, 2=L, 3=U (net directions)
    trans = {}
    for f, (n, u) in orient.items():
        r = cross(u, n)
        gvec = [r, neg(u), neg(r), u]  # net dirs: R(+x), D(+y net-> -u?), L, U
        # net y-axis is "down" -> 3D -u; net x-axis -> r
        for d, gd in enumerate(gvec):
            # target face: normal == gd
            for g, (gn, gu) in orient.items():
                if gn == gd:
                    trans[(f, d)] = g
                    break

    # walking: position in net coords (x, y) + face (fx, fy)
    # find start
    start_y = 0
    start_x = grid[0].index('.')
    fx, fy = start_x // face, start_y // face
    x, y = start_x % face, start_y % face
    d = 0  # 0=R, 1=D, 2=L, 3=U

    def step():
        nonlocal x, y, fx, fy, d
        # local direction in face coords: R: (1,0), D: (0,1), L: (-1,0), U: (0,-1)
        dirs_local = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        dxl, dyl = dirs_local[d]
        nx, ny = x + dxl, y + dyl
        nfx, nfy, nd = fx, fy, d
        if not (0 <= nx < face and 0 <= ny < face):
            # cross edge: find new face and new local pos/dir
            n, u = orient[(fx, fy)]
            r = cross(u, n)
            gd = [r, neg(u), neg(r), u][d]
            g = trans[((fx, fy), d)]
            gn, gu = orient[g]
            gr = cross(gu, gn)
            # 3D position of the point we exit from (on the edge)
            a, b = x, y
            P = (origins[(fx, fy)][0] + a * r[0] + b * u[0],
                 origins[(fx, fy)][1] + a * r[1] + b * u[1],
                 origins[(fx, fy)][2] + a * r[2] + b * u[2])
            og = origins[g]
            a2 = dot((P[0] - og[0], P[1] - og[1], P[2] - og[2]), gr)
            b2 = dot((P[0] - og[0], P[1] - og[1], P[2] - og[2]), gu)
            a2 = round(a2)
            b2 = round(b2)
            # clamp to edge (may be -1 or face due to rounding)
            a2 = max(0, min(face - 1, a2))
            b2 = max(0, min(face - 1, b2))
            # new direction: away from the entry edge
            if a2 == 0 and b2 != 0:
                nd = 0  # R
            elif a2 == face - 1:
                nd = 2  # L
            elif b2 == 0:
                nd = 1  # D
            else:
                nd = 3  # U
            nfx, nfy = g
            nx, ny = a2, b2
        # check wall
        if grid[nfy * face + ny][nfx * face + nx] == '#':
            return False
        x, y, fx, fy, d = nx, ny, nfx, nfy, nd
        return True

    instrs = re.findall(r'\d+|[LR]', instr_part)
    for ins in instrs:
        if ins == 'L':
            d = (d - 1) % 4
        elif ins == 'R':
            d = (d + 1) % 4
        else:
            for _ in range(int(ins)):
                if not step():
                    break

    # final position: face origin in net coords + local
    col = fx * face + x + 1
    row = fy * face + y + 1
    print(1000 * row + 4 * col + d)


if __name__ == "__main__":
    main()
