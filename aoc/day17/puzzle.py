import re
from typing import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Point:

    x: int
    y: int


@dataclass
class Probe:

    velocity: Point
    origin: Point = Point(0, 0)

    def apex(self) -> Point:

        if self.velocity.y < 0:
            return self.origin

        for pos, vel in self.shoot():
            if vel.y == 0:
                return pos

    def shoot(self) -> Iterable[tuple[Point, Point]]:

        pos = self.origin
        vel = self.velocity

        while True:
            yield pos, vel
            pos = Point(pos.x + vel.x, pos.y + vel.y)
            vel = Point(max(0, vel.x - 1), vel.y - 1)


def parse_input() -> Iterable[int]:

    bounds = re.search(
        r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)",
        (Path(__file__).parent / "input.txt").read_text(),
    ).groups()
    return [int(b) for b in bounds]


def successful_probes(x1: int, x2: int, y1: int, y2: int) -> list[Probe]:

    probes: list[Probe] = []

    for xv in range(x2 + 1):
        for yv in range(y1, abs(y1)):
            probe = Probe(Point(xv, yv))
            for pos, vel in probe.shoot():
                if x1 <= pos.x <= x2 and y1 <= pos.y <= y2:
                    probes.append(probe)
                    break
                if pos.y < y1 or pos.x > x2 or (vel.x == 0 and pos.x < x1):
                    break

    return probes


def solve() -> None:

    bounds = parse_input()
    probes = successful_probes(*bounds)

    # First part
    assert max(probe.apex().y for probe in probes) == 5151

    # Second part
    assert len(probes) == 968


if __name__ == "__main__":
    solve()
