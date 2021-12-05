import re
from dataclasses import dataclass
from typing import Iterator
from pathlib import Path


@dataclass(frozen=True)
class Vector:

    x: int
    y: int


@dataclass(frozen=True)
class Line:

    start: Vector
    end: Vector

    def is_diagonal(self) -> bool:
        return self.start.x != self.end.x and self.start.y != self.end.y

    def __iter__(self) -> Iterator[Vector]:
        """Yields all points on the line"""

        xd = self.end.x - self.start.x
        yd = self.end.y - self.start.y
        unit = Vector(xd // abs(xd) if xd != 0 else 0, yd // abs(yd) if yd != 0 else 0)

        current = self.start
        while current != Vector(self.end.x + unit.x, self.end.y + unit.y):
            yield current
            current = Vector(current.x + unit.x, current.y + unit.y)


def parse_input() -> list[Line]:

    lines: list[Line] = []
    pattern = r"(\d+),(\d+) -> (\d+),(\d+)"

    for line in (Path(__file__).parent / "input.txt").read_text().splitlines():
        groups = re.match(pattern, line).groups()
        start = Vector(int(groups[0]), int(groups[1]))
        end = Vector(int(groups[2]), int(groups[3]))
        lines.append(Line(start, end))

    return lines


def intersections(lines: list[Line]) -> set[Vector]:

    points: set[Vector] = set()
    intersections: set[Vector] = set()

    for line in lines:
        for point in line:
            if point in points:
                intersections.add(point)
            else:
                points.add(point)

    return intersections


def solve() -> None:

    lines = parse_input()

    # First part
    assert (
        len(intersections([line for line in lines if not line.is_diagonal()])) == 4826
    )

    # Second part
    assert len(intersections(lines)) == 16793


if __name__ == "__main__":
    solve()
