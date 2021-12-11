from collections import deque
from typing import Iterable, Deque
from pathlib import Path

Grid = list[list[int]]
Point = tuple[int, int]


def parse_input() -> Grid:

    return [
        [int(col) for col in row]
        for row in (Path(__file__).parent / "input.txt").read_text().splitlines()
    ]


def neighbours(point: Point, grid: Grid) -> Iterable[Point]:

    for x, y in [
        (0, -1),
        (1, -1),
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
    ]:
        nx = point[0] + x
        ny = point[1] + y
        if not 0 <= nx < len(grid):
            continue
        if not 0 <= ny < len(grid):
            continue
        yield (nx, ny)


def solve() -> None:

    grid = parse_input()
    flashes = 0
    flashes_at_step: list[int] = []

    while True:

        will_flash: Deque[Point] = deque()

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                grid[y][x] += 1
                if grid[y][x] > 9:
                    will_flash.append((x, y))

        flashed: set[Point] = set()
        while will_flash:
            x, y = will_flash.popleft()
            if (x, y) in flashed:
                continue
            flashed.add((x, y))
            for nx, ny in neighbours((x, y), grid):
                grid[ny][nx] += 1
                if grid[ny][nx] > 9 and (nx, ny) not in flashed:
                    will_flash.append((nx, ny))
        flashes += len(flashed)
        flashes_at_step.append(flashes)

        if len(flashed) == len(grid) ** 2:
            break

        for y in range(len(grid)):
            for x in range(len(grid)):
                if grid[y][x] > 9:
                    grid[y][x] = 0

    # First part
    assert flashes_at_step[100] == 1739

    # Second part
    assert len(flashes_at_step) == 324


if __name__ == "__main__":
    solve()
