from __future__ import annotations
from collections import deque, defaultdict
from heapq import heappush, heappop
from dataclasses import dataclass
from typing import Literal, Iterable, Deque
from pathlib import Path


@dataclass(frozen=True, order=True)
class Point:

    x: int
    y: int

    def neighbours(self) -> Iterable[Point]:
        for x, y in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            yield Point(self.x + x, self.y + y)


@dataclass(frozen=True, order=True)
class Pod:

    type: Literal["A", "B", "C", "D"]
    pos: Point

    def cost(self) -> int:
        if self.type == "A":
            return 1
        elif self.type == "B":
            return 10
        elif self.type == "C":
            return 100
        else:
            return 1000


rooms_small = {
    "A": [Point(3, 2), Point(3, 3)],
    "B": [Point(5, 2), Point(5, 3)],
    "C": [Point(7, 2), Point(7, 3)],
    "D": [Point(9, 2), Point(9, 3)],
}

rooms_large = {
    "A": rooms_small["A"] + [Point(3, 4), Point(3, 5)],
    "B": rooms_small["B"] + [Point(5, 4), Point(5, 5)],
    "C": rooms_small["C"] + [Point(7, 4), Point(7, 5)],
    "D": rooms_small["D"] + [Point(9, 4), Point(9, 5)],
}

room_points = set()
for points in rooms_large.values():
    for point in points:
        room_points.add(point)

hallway = [
    Point(1, 1),
    Point(2, 1),
    Point(4, 1),
    Point(6, 1),
    Point(8, 1),
    Point(10, 1),
    Point(11, 1),
]


@dataclass(frozen=True, order=True)
class State:

    pods: frozenset[Pod]
    burrow: frozenset[Point]

    def is_valid(self) -> bool:
        for pod in self.pods:
            if pod.pos not in self.rooms[pod.type]:
                return False
        return True

    @property
    def rooms(self) -> dict[str, list[Point]]:
        return rooms_small if len(self.pods) == 8 else rooms_large

    def possible_points(self, pod: Pod) -> dict[Point, int]:
        occupied = {other.pos for other in self.pods if other != pod}
        queue: Deque[tuple[int, Point]] = deque([(0, pod.pos)])
        visited = {pod.pos: 0}

        while queue:
            cost, pos = queue.popleft()
            for neighbour in pos.neighbours():
                if (
                    neighbour in self.burrow
                    and neighbour not in occupied
                    and neighbour not in visited
                ):
                    queue.append((cost + pod.cost(), neighbour))
                    visited[neighbour] = cost + pod.cost()
        return visited

    def moves(self, pod: Pod) -> Iterable[tuple[int, Point]]:

        # Pod is within the correct room
        if pod.pos in self.rooms[pod.type]:
            # Already at the bottom, do not move
            if pod.pos == self.rooms[pod.type][-1]:
                return
            # Room is already full with correct pods
            pods_in_room = []
            for other in self.pods:
                if other.pos in self.rooms[pod.type] and other.type == pod.type:
                    pods_in_room.append(other)
            if len(pods_in_room) == len(self.rooms[pod.type]):
                return
            # Move within the room
            possible_points = self.possible_points(pod)
            for point in self.rooms[pod.type]:
                if point != pod.pos and point in possible_points:
                    yield possible_points[point], point
            # Move to the hallway
            for point in hallway:
                if point in possible_points:
                    yield possible_points[point], point
        # Pod is within some other room
        elif pod.pos in room_points:
            possible_points = self.possible_points(pod)
            for point in hallway:
                if point in possible_points:
                    yield possible_points[point], point
        # Pod is in the hallway
        else:
            # Target room contains pod from other color - do not move into it
            for other in self.pods:
                if other.pos in self.rooms[pod.type] and other.type != pod.type:
                    return
            possible_points = self.possible_points(pod)
            for point in self.rooms[pod.type]:
                if point in possible_points:
                    yield possible_points[point], point


def parse_input(input_file: str) -> State:

    pods: set[Pod] = set()
    burrow: set[Point] = set()

    for y, row in enumerate(
        (Path(__file__).parent / input_file).read_text().splitlines()
    ):
        for x, cell in enumerate(row):
            point = Point(x, y)
            if cell in "ABCD":
                pods.add(Pod(cell, point))
                burrow.add(point)
            elif cell == ".":
                burrow.add(point)

    return State(frozenset(pods), frozenset(burrow))


def least_energy(initial_state: State) -> int:

    heap: list[tuple[int, State]] = []
    heappush(heap, (0, initial_state))
    costs = defaultdict(lambda: 1_000_000)

    while heap:

        cost, state = heappop(heap)
        if state.is_valid():
            return cost

        if costs[state.pods] <= cost:
            continue
        costs[state.pods] = cost

        for pod in state.pods:
            for move_cost, point in state.moves(pod):
                pods = frozenset(
                    [Pod(pod.type, point)] + [p for p in state.pods if p != pod]
                )
                next_state = State(pods, state.burrow)
                if costs[next_state.pods] > cost + move_cost:
                    heappush(heap, (cost + move_cost, next_state))

    return -1


def solve() -> None:

    # First part
    state = parse_input("input_1.txt")
    assert least_energy(state) == 12240

    # Second part
    state = parse_input("input_2.txt")
    assert least_energy(state) == 44618


if __name__ == "__main__":
    solve()
