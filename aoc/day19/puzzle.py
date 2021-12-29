from __future__ import annotations
from pathlib import Path
from itertools import combinations
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Vector:

    x: int
    y: int
    z: int

    def __add__(self, v: Vector) -> Vector:
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v: Vector) -> Vector:
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)

    def manhattan(self, v: Vector) -> int:
        difference = self - v
        return abs(difference.x) + abs(difference.y) + abs(difference.z)

    def mag(self) -> int:
        return self.x ** 2 + self.y ** 2 + self.z ** 2


@dataclass(frozen=True)
class Matrix:

    top: Vector
    mid: Vector
    bot: Vector

    def __mul__(self, vec: Vector) -> Vector:
        return Vector(
            self.top.x * vec.x + self.top.y * vec.y + self.top.z * vec.z,
            self.mid.x * vec.x + self.mid.y * vec.y + self.mid.z * vec.z,
            self.bot.x * vec.x + self.bot.y * vec.y + self.bot.z * vec.z,
        )


@dataclass
class Scanner:

    id: int
    beacons: set[Vector] = field(default_factory=set)
    position: Vector = Vector(0, 0, 0)

    def distances(self) -> list[set[int]]:
        distances = []
        for beacon in self.beacons:
            distances.append({(beacon - b).mag() for b in self.beacons})
        return distances

    def overlaps(self, other: Scanner) -> bool:
        s1_distances = self.distances()
        s2_distances = other.distances()
        for d1 in s1_distances:
            for d2 in s2_distances:
                if len(d1 & d2) >= 12:
                    return True
        return False


def parse_input() -> list[Scanner]:

    scanners: list[Scanner] = []

    for line in (Path(__file__).parent / "input.txt").read_text().splitlines():
        if not line:
            continue
        if line.startswith("---"):
            scanners.append(Scanner(len(scanners)))
        else:
            beacon = Vector(*[int(v) for v in line.split(",")])
            scanners[-1].beacons.add(beacon)

    return scanners


directions = [
    Matrix(Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)),
    Matrix(Vector(0, 1, 0), Vector(-1, 0, 0), Vector(0, 0, 1)),
    Matrix(Vector(-1, 0, 0), Vector(0, -1, 0), Vector(0, 0, 1)),
    Matrix(Vector(0, -1, 0), Vector(1, 0, 0), Vector(0, 0, 1)),
    Matrix(Vector(1, 0, 0), Vector(0, 0, -1), Vector(0, 1, 0)),
    Matrix(Vector(1, 0, 0), Vector(0, 0, 1), Vector(0, -1, 0)),
]
rotations = [
    Matrix(Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1)),
    Matrix(Vector(0, 0, -1), Vector(0, 1, 0), Vector(1, 0, 0)),
    Matrix(Vector(-1, 0, 0), Vector(0, 1, 0), Vector(0, 0, -1)),
    Matrix(Vector(0, 0, 1), Vector(0, 1, 0), Vector(-1, 0, 0)),
]


def align(origin: Scanner, scanner: Scanner) -> Scanner | None:

    if not origin.overlaps(scanner):
        return

    for orient in directions:
        for rotate in rotations:

            beacons = {rotate * (orient * beacon) for beacon in scanner.beacons}

            distances = {
                "x": defaultdict(int),
                "y": defaultdict(int),
                "z": defaultdict(int),
            }
            for b1 in beacons:
                for b2 in origin.beacons:
                    for axis in "xyz":
                        distances[axis][getattr(b1, axis) - getattr(b2, axis)] += 1
            offsets = []
            for axis, dists in distances.items():
                for dist, beacon_pairs in dists.items():
                    if beacon_pairs >= 12:
                        offsets.append(dist)
            if len(offsets) == 3:
                offset = Vector(*offsets)
                return Scanner(
                    scanner.id,
                    {b - offset for b in beacons},
                    offset,
                )


def align_scanners(scanners: dict[int, Scanner]) -> dict[int, Scanner]:

    aligned: dict[int, Scanner] = {0: scanners[0]}
    unaligned: dict[int, Scanner] = {
        scanner.id: scanner
        for scanner in scanners.values()
        if scanner.id not in aligned
    }
    explored: set[int] = set()

    while unaligned:
        found: list[Scanner] = []
        for origin in aligned.values():
            if origin.id in explored:
                continue
            explored.add(origin.id)
            for candidate in unaligned.values():
                if scanner := align(origin, candidate):
                    found.append(scanner)
        for scanner in found:
            if scanner.id in unaligned:
                del unaligned[scanner.id]
                aligned[scanner.id] = scanner

    return aligned


def solve() -> None:

    scanners = {scanner.id: scanner for scanner in parse_input()}

    aligned_scanners = align_scanners(scanners)

    # First part
    beacons: set[Vector] = set()
    for scanner in aligned_scanners.values():
        beacons.update(scanner.beacons)
    assert len(beacons) == 442

    # Second part
    span = max(
        s1.position.manhattan(s2.position)
        for s1, s2 in combinations(list(aligned_scanners.values()), 2)
    )
    assert span == 11079


if __name__ == "__main__":
    solve()
