from pathlib import Path


def parse_input() -> list[list[str]]:
    return [
        list(line)
        for line in (Path(__file__).parent / "input.txt").read_text().splitlines()
    ]


def solve() -> None:

    lines = parse_input()

    bracket_pairs = {"{": "}", "(": ")", "<": ">", "[": "]"}
    syntax_points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    autocomplete_points = {")": 1, "]": 2, "}": 3, ">": 4}

    syntax_scores = []
    autocomplete_scores = []

    for line in lines:
        stack = []
        for bracket in line:
            if bracket in bracket_pairs:
                stack.append(bracket)
            elif bracket_pairs[stack.pop()] != bracket:
                syntax_scores.append(syntax_points[bracket])
                break
        else:
            line_score = 0
            for bracket in reversed(stack):
                line_score = (
                    line_score * 5 + autocomplete_points[bracket_pairs[bracket]]
                )
            autocomplete_scores.append(line_score)

    # First part
    assert sum(syntax_scores) == 311895

    # Second part
    assert sorted(autocomplete_scores)[len(autocomplete_scores) // 2] == 2904180541


if __name__ == "__main__":
    solve()
