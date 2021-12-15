from math import sqrt
from heapq import heappop, heappush
from typing import Iterable
from pathlib import Path


Point = tuple[int, int]
Grid = dict[Point, int]


def parse_input() -> Grid:

    grid: Grid = {}
    for y, row in enumerate(
        (Path(__file__).parent / "input.txt").read_text().splitlines()
    ):
        for x, col in enumerate(row):
            grid[(x, y)] = int(col)
    return grid


def neighbours(point: Point, grid: Grid) -> Iterable[Point]:

    for x, y in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        neighbour = (x + point[0], y + point[1])
        if neighbour in grid:
            yield neighbour


def lowest_risk(grid: Grid) -> int:

    risks = {point: float("inf") for point in grid}
    risks[(0, 0)] = 0
    queue = [(0, (0, 0))]

    while queue:

        risk, point = heappop(queue)
        if risks[point] < risk:
            continue

        for neighbour in neighbours(point, grid):
            neighbour_risk = grid[neighbour]
            cumulative_risk = risk + neighbour_risk
            if cumulative_risk < risks[neighbour]:
                risks[neighbour] = cumulative_risk
                heappush(queue, (cumulative_risk, neighbour))

    return risks[(max(x for x, _ in grid), max(y for _, y in grid))]


def tiled_grid(grid: Grid) -> Grid:

    size = int(sqrt(len(grid)))
    tiled = {}
    for (x, y), risk in grid.items():
        for tile_y in range(5):
            for tile_x in range(5):
                scaled_point = (size * tile_x + x, size * tile_y + y)
                tiled[scaled_point] = (
                    scaled_risk
                    if (scaled_risk := risk + tile_x + tile_y) <= 9
                    else scaled_risk - 9
                )
    return tiled


def solve() -> None:

    grid = parse_input()

    # First part
    assert lowest_risk(grid) == 403

    # Second part
    assert lowest_risk(tiled_grid(grid)) == 2840


if __name__ == "__main__":
    solve()
