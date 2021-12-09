import operator
from collections import deque
from functools import reduce
from pathlib import Path
from typing import Iterable

Point = tuple[int, int]
Grid = list[list[int]]


def parse_input() -> Grid:
    return [
        list(int(col) for col in row)
        for row in (Path(__file__).parent / "input.txt").read_text().splitlines()
    ]


def adjacents(point: Point, grid: Grid) -> Iterable[Point]:
    for xd, yd in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        nx = point[0] + xd
        ny = point[1] + yd
        if not 0 <= nx < len(grid[point[1]]):
            continue
        if not 0 <= ny < len(grid):
            continue
        yield (nx, ny)


def basin_size(point: Point, grid: Grid) -> int:

    points = deque([point])
    seen = set()
    while points:
        for x, y in adjacents(points.popleft(), grid):
            if grid[y][x] != 9 and (x, y) not in seen:
                points.append((x, y))
                seen.add((x, y))
    return len(seen)


def find_low_points(grid: Grid) -> list[Point]:

    low_points = []
    for y in range(len((grid))):
        for x in range(len(grid[y])):
            adjacent_heights = [grid[ay][ax] for ax, ay in adjacents((x, y), grid)]
            if all(grid[y][x] < adj for adj in adjacent_heights):
                low_points.append((x, y))
    return low_points


def solve() -> None:

    grid = parse_input()

    # First part
    low_points = find_low_points(grid)
    assert sum(grid[y][x] + 1 for x, y in low_points) == 496

    # Second part
    top_basins = sorted(basin_size(point, grid) for point in low_points)[-3:]
    assert reduce(operator.mul, top_basins) == 902880


if __name__ == "__main__":
    solve()
