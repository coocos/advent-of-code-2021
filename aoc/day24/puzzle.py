from functools import cache, reduce
from operator import mul
from pathlib import Path
from typing import Iterable
from collections import deque


Operation = list[str]


def parse_input() -> list[Operation]:
    operations: list[Operation] = []
    for line in (Path(__file__).parent / "input.txt").read_text().splitlines():
        if line:
            operations.append((line.split()))
    return operations


def alu(ops: list[Operation], inputs: deque[int]) -> dict[str, int]:

    variables = {
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0,
    }

    for op in ops:
        match op:
            case "inp", variable:
                variables[variable] = int(inputs.popleft())
            case "mul", a, b:
                if b in variables:
                    variables[a] *= variables[b]
                else:
                    variables[a] *= int(b)
            case "add", a, b:
                if b in variables:
                    variables[a] += variables[b]
                else:
                    variables[a] += int(b)
            case "div", a, b:
                if b in variables:
                    variables[a] = variables[a] // variables[b]
                else:
                    variables[a] = variables[a] // int(b)
            case "mod", a, b:
                if b in variables:
                    variables[a] = variables[a] % variables[b]
                else:
                    variables[a] = variables[a] % int(b)
            case "eql", a, b:
                if b in variables:
                    variables[a] = int(variables[a] == variables[b])
                else:
                    variables[a] = int(variables[a] == int(b))

    return variables


def valid_model(digit_range: Iterable[int]) -> int:

    # Hardcoded constants for this particular input
    xs = [11, 11, 15, -14, 10, 0, -6, 13, -3, 13, 15, -2, -9, -2]
    zs = [1, 1, 1, 26, 1, 26, 26, 1, 26, 1, 1, 26, 26, 26]
    ws = [6, 14, 13, 1, 6, 13, 6, 3, 8, 14, 4, 7, 15, 1]
    max_z = [reduce(mul, zs[i:]) for i in range(len(zs))]

    @cache
    def decompiled(number: int, offset: int, z: int):
        """Decompiled version of the 14 input programs"""
        if number == (z % 26 + xs[offset]):
            z = z // zs[offset]
        else:
            z = (z // zs[offset]) * 26 + number + ws[offset]
        return z

    def search(digits: list[int], z: int) -> int:

        if len(digits) == 14:
            if z == 0:
                return int("".join(str(d) for d in digits))
            return 0

        for digit in digit_range:
            next_z = decompiled(digit, len(digits), z)
            # If the next z value is larger than the product
            # of possible future divisions then z will never
            # reach zero and the recursion can be terminated
            # instantly
            if next_z > max_z[len(digits)]:
                continue
            if value := search(digits + [digit], next_z):
                return value
        return 0

    return search([], 0)


def solve() -> None:

    # The operations aren't really needed since the solution is
    # based on manually decompiling the input and then doing a DFS
    # using the decompiled program
    operations = parse_input()

    # First part
    assert valid_model(list(range(1, 10))) == 11211791111365

    # Second part
    assert valid_model(list(range(9, 0, -1))) == 51983999947999


if __name__ == "__main__":
    solve()
