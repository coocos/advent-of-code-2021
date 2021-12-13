import re
from typing import Literal
from pathlib import Path
from textwrap import dedent


Fold = tuple[Literal["x", "y"], int]
Point = tuple[int, int]


def parse_input() -> tuple[set[Point], list[Fold]]:

    lines = (Path(__file__).parent / "input.txt").read_text().splitlines()

    points: set[Point] = set()
    for i, line in enumerate(lines):
        if not line:
            break
        x, y = line.split(",")
        points.add((int(x), int(y)))

    folds: list[Fold] = []
    for fold in lines[i + 1 :]:
        match = re.search(r"fold along ([xy])=(\d+)", fold)
        assert match
        axis, value = match.groups()
        assert axis == "x" or axis == "y"
        folds.append((axis, int(value)))

    return points, folds


def draw(points: set[Point]) -> str:

    width = max(x for x, _ in points)
    height = max(y for _, y in points)

    paper: list[list[str]] = []
    for y in range(height + 1):
        row = []
        for x in range(width + 1):
            row.append("#" if (x, y) in points else ".")
        paper.append(row)
    return "\n".join("".join(row) for row in paper)


def fold(points: set[Point], folds: list[Fold]) -> set[Point]:

    if not folds:
        return points

    folded: set[Point] = set()
    axis, length = folds[0]

    for x, y in points:
        if axis == "x":
            folded.add((x, y) if x < length else ((2 * length - x, y)))
        else:
            folded.add((x, y) if y < length else (x, 2 * length - y))

    return fold(folded, folds[1:])


def solve() -> None:

    points, folds = parse_input()

    # First part
    assert len(fold(points, folds[:1])) == 765

    # Second part
    letters = draw(fold(points, folds))
    assert (
        letters
        == dedent(
            """
            ###..####.#..#.####.#....###...##..#..#
            #..#....#.#.#.....#.#....#..#.#..#.#..#
            #..#...#..##.....#..#....#..#.#....####
            ###...#...#.#...#...#....###..#.##.#..#
            #.#..#....#.#..#....#....#....#..#.#..#
            #..#.####.#..#.####.####.#.....###.#..#
            """
        ).strip()
    )


if __name__ == "__main__":
    solve()
