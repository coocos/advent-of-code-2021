from pathlib import Path


def parse_input() -> list[int]:
    return [
        int(depth)
        for depth in (Path(__file__).parent / "input.txt").read_text().splitlines()
    ]


def count_increases(values: list[int], offset: int) -> int:
    return sum(
        int(second - first > 0) for first, second in zip(values, values[offset:])
    )


def solve() -> None:

    measurements = parse_input()

    # First part
    assert count_increases(measurements, offset=1) == 1374

    # Second part
    assert count_increases(measurements, offset=3) == 1418


if __name__ == "__main__":
    solve()
