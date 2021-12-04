from pathlib import Path
from collections import defaultdict


def parse_input() -> list[int]:
    lines = (Path(__file__).parent / "input.txt").read_text().splitlines()

    numbers = [int(number) for number in lines[0].split(",")]

    boards = []
    rows = []
    for line in lines[1:]:
        if not line:
            if rows:
                boards.append(rows)
            rows = []
            continue
        rows.append([int(number) for number in line.split()])

    boards.append(rows)

    index = defaultdict(list)
    for board_id, board in enumerate(boards):
        rows = [set() for _ in range(len(board))]
        cols = [set() for _ in range(len(board))]
        for y in range(len(board)):
            for x in range(len(board)):
                number = board[y][x]
                rows[y].add(number)
                cols[x].add(number)
                index[number].append((board_id, rows[y]))
                index[number].append((board_id, cols[x]))

    scores = []
    winners = set()
    for i, number in enumerate(numbers):
        if number in index:
            for board_id, row_col in index[number]:
                if board_id not in winners:
                    row_col.remove(number)
                    if not row_col:
                        unmarked_sum = 0
                        for row in boards[board_id]:
                            for value in row:
                                if value not in numbers[: i + 1]:
                                    unmarked_sum += value
                        scores.append(number * unmarked_sum)
                        winners.add(board_id)
    return scores


def solve() -> None:

    scores = parse_input()

    assert scores[0] == 51776
    assert scores[-1] == 16830


if __name__ == "__main__":
    solve()
