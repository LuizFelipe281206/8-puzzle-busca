import heapq
from itertools import count
from typing import Callable, Optional

from puzzle.base_search import BaseSearch
from puzzle.result import SearchResult
from puzzle.state import GOAL_STATE, State


class AStar(BaseSearch):

    def __init__(self, heuristic: Optional[Callable[[State], int]] = None):
        self._custom_heuristic = heuristic

    def heuristic(self, state: State) -> int:
        if self._custom_heuristic is not None:
            return self._custom_heuristic(state)

        distance = 0
        for index, tile in enumerate(state.tiles):
            if tile:
                row, col = divmod(index, 3)
                goal_row, goal_col = divmod(GOAL_STATE.index(tile), 3)
                distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        tie_breaker = count()
        frontier = [(initial.cost + self.heuristic(initial), next(tie_breaker), initial)]
        best_cost = {initial: initial.cost}
        result = SearchResult(None, nodes_generated=1, max_frontier_size=1)

        while frontier:
            _, _, state = heapq.heappop(frontier)
            if state.cost != best_cost[state]:
                continue
            if state.is_goal:
                result.solution = state
                result.depth = state.cost - initial.cost
                return result

            result.nodes_expanded += 1
            for child in state.neighbors():
                if child in best_cost and child.cost >= best_cost[child]:
                    continue
                best_cost[child] = child.cost
                priority = child.cost + self.heuristic(child)
                heapq.heappush(frontier, (priority, next(tie_breaker), child))
                result.nodes_generated += 1
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
