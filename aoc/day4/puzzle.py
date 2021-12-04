from pathlib import Path
from collections import defaultdict


def parse_input() -> tuple[list[int], list[list[list[int]]]]:

    lines = (Path(__file__).parent / "input.txt").read_text().splitlines()
    numbers = [int(number) for number in lines[0].split(",")]

    boards = []
    for line in lines[1:]:
        if not line:
            boards.append([])
            continue
        boards[-1].append([int(value) for value in line.split()])
    return numbers, boards


def bingo(numbers: list[int], boards: list[list[list[int]]]) -> list[int]:

    columns_and_rows_for_value = defaultdict(list)

    for board, rows in enumerate(boards):
        values_for_column = defaultdict(set)
        values_for_row = defaultdict(set)
        for y, row in enumerate(rows):
            for x, value in enumerate(row):
                values_for_column[y].add(value)
                values_for_row[x].add(value)
                columns_and_rows_for_value[value] += [
                    (board, values_for_column[y]),
                    (board, values_for_row[x]),
                ]

    winners = set()
    scores = []

    for current, number in enumerate(numbers):
        for board, row_or_column in columns_and_rows_for_value[number]:
            if board in winners:
                continue

            row_or_column.remove(number)
            if not row_or_column:
                winners.add(board)
                score = sum(
                    value
                    for row in boards[board]
                    for value in row
                    if value not in numbers[: current + 1]
                )
                scores.append(number * score)

    return scores


def solve() -> None:

    numbers, boards = parse_input()
    scores = bingo(numbers, boards)

    # First part
    assert scores[0] == 51776

    # Second part
    assert scores[-1] == 16830


if __name__ == "__main__":
    solve()
