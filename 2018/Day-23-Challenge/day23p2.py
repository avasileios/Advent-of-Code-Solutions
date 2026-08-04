import re
import os
import heapq

def solve_part2():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    nanobots = []
    pattern = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")

    if not os.path.exists(file_path):
        return "Error: input.txt not found."

    with open(file_path, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                x, y, z, r = map(int, match.groups())
                nanobots.append((x, y, z, r))

    # Define a bounding box large enough to contain all nanobot spheres
    min_coord = min(min(b[0]-b[3], b[1]-b[3], b[2]-b[3]) for b in nanobots)
    max_coord = max(max(b[0]+b[3], b[1]+b[3], b[2]+b[3]) for b in nanobots)

    # Use a power-of-2 size for the search cube to make subdivision clean
    size = 1
    while size < max_coord - min_coord:
        size *= 2

    # Priority Queue stores: (-potential_count, cube_size, dist_to_origin, x, y, z)
    # We use negative count because heapq is a min-heap, and we want the MAX count.
    pq = [(-len(nanobots), size, 0, min_coord, min_coord, min_coord)]

    while pq:
        count, s, dist, x, y, z = heapq.heappop(pq)
        
        # If size is 1, we have narrowed it down to a single point
        if s == 1:
            return dist

        new_size = s // 2
        # Generate 8 sub-cubes
        for dx in [0, new_size]:
            for dy in [0, new_size]:
                for dz in [0, new_size]:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    
                    # Calculate how many bots could reach any point in this sub-cube
                    reachable_count = 0
                    for bx, by, bz, br in nanobots:
                        # Manhattan distance from the bot to the nearest point on the cube
                        d = 0
                        if bx < nx: d += nx - bx
                        elif bx > nx + new_size - 1: d += bx - (nx + new_size - 1)
                        
                        if by < ny: d += ny - by
                        elif by > ny + new_size - 1: d += by - (ny + new_size - 1)
                        
                        if bz < nz: d += nz - bz
                        elif bz > nz + new_size - 1: d += bz - (nz + new_size - 1)
                        
                        if d <= br:
                            reachable_count += 1
                    
                    if reachable_count > 0:
                        new_dist = abs(nx) + abs(ny) + abs(nz)
                        heapq.heappush(pq, (-reachable_count, new_size, new_dist, nx, ny, nz))

if __name__ == "__main__":
    result = solve_part2()
    print(f"Shortest Manhattan distance to best coordinate: {result}")