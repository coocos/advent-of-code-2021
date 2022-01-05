from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Cuboid:

    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]
    on: bool = True

    @property
    def volume(self) -> int:
        return (
            (abs(self.x[0] - self.x[1]) + 1)
            * (abs(self.y[0] - self.y[1]) + 1)
            * (abs(self.z[0] - self.z[1]) + 1)
        )

    def tiny(self) -> bool:
        coords = [*self.x, *self.y, *self.z]
        return all(-50 <= coord <= 50 for coord in coords)

    def intersects(self, cuboid: Cuboid) -> bool:
        for axis in ["x", "y", "z"]:
            a1, a2 = getattr(self, axis)
            b1, b2 = getattr(cuboid, axis)
            if a2 < b1:
                return False
            if a1 > b2:
                return False
        return True

    def split(self, other: Cuboid) -> list[Cuboid]:
        x1, x2, x3, x4 = sorted([*self.x, *other.x])
        y1, y2, y3, y4 = sorted([*self.y, *other.y])
        z1, z2, z3, z4 = sorted([*self.z, *other.z])
        candidates: list[Cuboid] = []
        for xs, xe in [(x1, x2 - 1), (x2, x3), (x3 + 1, x4)]:
            for ys, ye in [(y1, y2 - 1), (y2, y3), (y3 + 1, y4)]:
                for zs, ze in [(z1, z2 - 1), (z2, z3), (z3 + 1, z4)]:
                    candidate = Cuboid((xs, xe), (ys, ye), (zs, ze), True)
                    if self.intersects(candidate) and not other.intersects(candidate):
                        candidates.append(candidate)
        return candidates


def parse_input() -> list[Cuboid]:
    cuboids: list[Cuboid] = []
    pattern = r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)"
    for line in (Path(__file__).parent / "input.txt").read_text().splitlines():
        on, x1, x2, y1, y2, z1, z2 = re.search(pattern, line).groups()
        cuboids.append(
            Cuboid(
                (int(x1), int(x2)), (int(y1), int(y2)), (int(z1), int(z2)), on == "on"
            )
        )
    return cuboids


def split_cuboids(cuboids: list[Cuboid]) -> list[Cuboid]:
    previous = [cuboids[0]]
    for cuboid in cuboids[1:]:
        next = []
        for existing_cuboid in previous:
            if existing_cuboid.intersects(cuboid):
                for mini_cuboid in existing_cuboid.split(cuboid):
                    next.append(mini_cuboid)
            else:
                next.append(existing_cuboid)
        if cuboid.on:
            next.append(cuboid)
        previous = next
    return previous


def solve() -> None:

    cuboids = parse_input()

    # First part
    assert (
        sum(cuboid.volume for cuboid in split_cuboids([c for c in cuboids if c.tiny()]))
        == 615869
    )

    # Second part
    assert sum(cuboid.volume for cuboid in split_cuboids(cuboids)) == 1323862415207825


if __name__ == "__main__":
    solve()
