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
        return {
            "A": 1,
            "B": 10,
            "C": 100,
            "D": 1000,
        }[self.type]


@dataclass(frozen=True, order=True)
class State:

    pods: list[Pod]
    burrow: set[Point]
    previous: State | None = None
    cost: int = 0

    def pod_hash(self) -> tuple[Pod, ...]:
        return tuple(sorted(self.pods))

    @property
    def rooms(self) -> dict[Literal["A", "B", "C", "D"], list[Point]]:
        return {
            "A": [Point(3, 2), Point(3, 3)],
            "B": [Point(5, 2), Point(5, 3)],
            "C": [Point(7, 2), Point(7, 3)],
            "D": [Point(9, 2), Point(9, 3)],
        }

    @property
    def hallway(self) -> list[Point]:
        return [
            Point(1, 1),
            Point(2, 1),
            Point(4, 1),
            Point(6, 1),
            Point(8, 1),
            Point(10, 1),
            Point(11, 1),
        ]

    def is_valid(self) -> bool:
        for pod in self.pods:
            if pod.pos not in self.rooms[pod.type]:
                return False
        return True

    def can_move_to(self, pod: Pod, dest: Point) -> int:
        visited: set[Point] = set()
        other_pods = {other.pos for other in self.pods if other != pod}

        queue: Deque[tuple[int, Point]] = deque([(0, pod.pos)])
        while queue:
            cost, pos = queue.popleft()
            if pos == dest:
                return cost
            visited.add(pos)
            for neighbour in pos.neighbours():
                if (
                    neighbour in self.burrow
                    and neighbour not in other_pods
                    and neighbour not in visited
                ):
                    queue.append((cost + pod.cost(), neighbour))
        return -1

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
            for point in self.rooms[pod.type]:
                if point != pod.pos:
                    if (cost := self.can_move_to(pod, point)) != -1:
                        yield cost, point
            # Move to the hallway
            for point in self.hallway:
                if (cost := self.can_move_to(pod, point)) != -1:
                    yield cost, point
        # Pod is within some other room
        elif (
            pod.pos
            in self.rooms["A"] + self.rooms["B"] + self.rooms["C"] + self.rooms["D"]
        ):
            for point in self.hallway:
                if (cost := self.can_move_to(pod, point)) != -1:
                    yield cost, point
        # Pod is in the hallway
        else:
            # Room contains pod from other color - do not move into it
            for other in self.pods:
                if other.pos in self.rooms[pod.type] and other.type != pod.type:
                    return
            for point in self.rooms[pod.type]:
                if (cost := self.can_move_to(pod, point)) != -1:
                    yield cost, point


def parse_input() -> State:

    pods: list[Pod] = []
    burrow: set[Point] = set()

    for y, row in enumerate(
        (Path(__file__).parent / "input.txt").read_text().splitlines()
    ):
        for x, cell in enumerate(row):
            point = Point(x, y)
            if cell in "ABCD":
                pods.append(Pod(cell, point))
                burrow.add(point)
            elif cell == ".":
                burrow.add(point)

    return State(pods, burrow)


def draw(state: State) -> None:

    grid: list[list[str]] = []
    for y in range(5):
        grid.append([])
        for x in range(13):
            for pod in state.pods:
                if pod.pos == Point(x, y):
                    grid[-1].append(pod.type)
                    break
            else:
                if Point(x, y) in state.burrow:
                    grid[-1].append(".")
                else:
                    grid[-1].append(" ")
    print("\n".join("".join(row) for row in grid))


def bfs(genesis: State) -> int:

    heap: list[tuple[int, State]] = []
    heappush(heap, (genesis.cost, genesis))
    costs = defaultdict(lambda: 1_000_000)

    while heap:

        cost, state = heappop(heap)
        if state.is_valid():
            return cost

        if costs[state.pod_hash()] <= cost:
            continue
        costs[state.pod_hash()] = cost

        if state.is_valid():
            print(state.cost)
            return state.cost

        for pod in state.pods:
            for cost, point in state.moves(pod):
                pods = [Pod(pod.type, point)] + [p for p in state.pods if p != pod]
                next_state = State(pods, state.burrow, state, state.cost + cost)
                if costs[next_state.pod_hash()] > next_state.cost:
                    heappush(heap, (next_state.cost, next_state))
    return -1


def solve() -> None:

    state = parse_input()
    draw(state)

    # First part
    assert bfs(state) == 12240


if __name__ == "__main__":
    solve()
