from __future__ import annotations
import itertools
from concurrent.futures import ProcessPoolExecutor
from math import floor, ceil
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Regular:

    value: int

    def debug(self) -> str:
        return str(self.value)

    def magnitude(self) -> int:
        return self.value


@dataclass
class Pair:

    left: Regular | Pair
    right: Regular | Pair
    should_explode: bool = False

    def magnitude(self) -> int:
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def debug(self) -> str:
        return f"[{self.left.debug()},{self.right.debug()}]"


def parse_input() -> list[str]:
    return (Path(__file__).parent / "input.txt").read_text().splitlines()


def tree(number: list[int] | int) -> Pair | Regular:

    if isinstance(number, int):
        return Regular(number)

    return Pair(tree(number[0]), tree(number[1]))


def explode(node: Pair | Regular) -> bool:

    # FIXME: Using nonlocals is nasty
    leaves: list[Regular | None] = []
    exploded_once = False

    def dfs(node: Pair | Regular, depth: int = 0) -> Pair | None:

        if isinstance(node, Regular):
            leaves.append(node)
            return

        if depth == 4 and isinstance(node, Pair):
            nonlocal exploded_once
            if not exploded_once:
                node.should_explode = True
                exploded_once = True
                leaves.append(None)
            else:
                dfs(node.left)
                dfs(node.right)
            return node

        left = dfs(node.left, depth + 1)

        if isinstance(left, Pair) and left.should_explode:
            left.should_explode = False
            node.left = Regular(0)

        right = dfs(node.right, depth + 1)

        if isinstance(right, Pair) and right.should_explode:
            right.should_explode = False
            node.right = Regular(0)

        return left or right

    exploded_node = dfs(node)
    if not exploded_node:
        return False

    previous = leaves.index(None) - 1
    next = leaves.index(None) + 1
    if previous >= 0:
        leaves[previous].value += exploded_node.left.value
    if next < len(leaves):
        leaves[next].value += exploded_node.right.value

    return True


def split(node: Pair | Regular) -> bool:

    # FIXME: Using a nonlocal is nasty
    split_once = False

    def dfs(node: Pair | Regular) -> bool:

        nonlocal split_once

        if isinstance(node, Regular):
            return node.value >= 10

        if dfs(node.left):
            if not split_once:
                value = node.left.value / 2
                node.left = Pair(Regular(floor(value)), Regular(ceil(value)))
                split_once = True
        elif dfs(node.right):
            if not split_once:
                value = node.right.value / 2
                node.right = Pair(Regular(floor(value)), Regular(ceil(value)))
                split_once = True

        return False

    dfs(node)
    return split_once


def final_sum(numbers: list[str]) -> int:

    first = numbers[0]
    for second in numbers[1:]:
        pair = Pair(tree(eval(first)), tree(eval(second)))
        while True:
            pair = tree(eval(pair.debug()))
            if explode(pair):
                continue
            if split(pair):
                continue
            break
        first = pair.debug()
    return tree(eval(first)).magnitude()


def reduce(numbers: tuple[str, str]) -> int:

    first, second = numbers
    pair = Pair(tree(eval(first)), tree(eval(second)))
    while True:
        pair = tree(eval(pair.debug()))
        if explode(pair):
            continue
        if split(pair):
            continue
        break
    return pair.magnitude()


def max_magnitude(numbers: list[str]) -> int:

    magnitudes = []
    with ProcessPoolExecutor() as pool:
        for mag in pool.map(reduce, itertools.permutations(numbers, 2)):
            magnitudes.append(mag)
    return max(magnitudes)


def solve() -> None:

    numbers = parse_input()

    # First part
    assert final_sum(numbers) == 4137

    # Second part
    assert max_magnitude(numbers) == 4573


if __name__ == "__main__":
    solve()
