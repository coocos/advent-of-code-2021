from copy import deepcopy
from pathlib import Path


Grid = list[list[str]]


def parse_input() -> Grid:
    return [
        list(line)
        for line in (Path(__file__).parent / "input.txt").read_text().splitlines()
    ]


def generate(grid: Grid) -> Grid:

    after_east = deepcopy(grid)

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            cell = grid[y][x]
            if cell != ">":
                continue
            nx = (x + 1) % len(grid[y])
            next_pos = grid[y][nx]
            if next_pos == ".":
                after_east[y][nx] = ">"
                after_east[y][x] = "."

    after_south = deepcopy(after_east)

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            cell = after_east[y][x]
            if cell != "v":
                continue
            ny = (y + 1) % len(grid)
            next_pos = after_east[ny][x]
            if next_pos == ".":
                after_south[ny][x] = "v"
                after_south[y][x] = "."

    return after_south


def solve() -> None:

    states: set[str] = set()
    grid = parse_input()
    step = 0

    while True:
        if (state := "\n".join("".join(row) for row in grid)) in states:
            break
        states.add(state)
        grid = generate(grid)
        step += 1

    # First part
    assert step == 400


if __name__ == "__main__":
    solve()
