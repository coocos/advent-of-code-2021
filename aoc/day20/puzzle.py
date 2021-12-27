from __future__ import annotations
from pathlib import Path
from typing import Iterable, Literal
from dataclasses import dataclass


@dataclass(frozen=True)
class Pixel:

    x: int
    y: int

    def neighbours(self) -> Iterable[Pixel]:
        for y in range(-1, 2):
            for x in range(-1, 2):
                yield Pixel(self.x + x, self.y + y)


Pixels = dict[Pixel, Literal["#", "."]]


def parse_input() -> tuple[dict[int, bool], Pixels]:

    algorithm, image = (Path(__file__).parent / "input.txt").read_text().split("\n\n")

    pixels: dict[Pixel, Literal["#", "."]] = {}
    for y, row in enumerate(image.split("\n")):
        for x, cell in enumerate(row):
            assert cell == "#" or cell == "."
            pixels[(Pixel(x, y))] = cell

    return {i: v == "#" for i, v in enumerate(algorithm)}, pixels


def solve() -> None:

    algorithm, pixels = parse_input()

    pixels_at_step: list[int] = []

    for step in range(1, 51):

        next_gen: Pixels = {}
        min_x, *_, max_x = sorted([p.x for p in pixels])
        min_y, *_, max_y = sorted([p.y for p in pixels])
        for y in range(min_y - 1, max_y + 2):
            for x in range(min_x - 1, max_x + 2):
                pixel = Pixel(x, y)
                bits = 0
                for neighbour in pixel.neighbours():
                    if pixels.get(neighbour, "#" if step % 2 == 0 else ".") == "#":
                        bits |= 1
                    bits <<= 1
                bits >>= 1
                next_gen[pixel] = "#" if algorithm[bits] else "."
        pixels = next_gen
        pixels_at_step.append(len([pixel for pixel in pixels.values() if pixel == "#"]))

    # First part
    assert pixels_at_step[1] == 5437

    # Second part
    assert pixels_at_step[49] == 19340


if __name__ == "__main__":
    solve()
