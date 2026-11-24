from puzzle.base_search import BaseSearch
from puzzle.result import SearchResult
from puzzle.state import State

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [(initial, 0)]
        shallowest = {}
        result = SearchResult(None, nodes_generated=1, max_frontier_size=1)

        while frontier:
            state, depth = frontier.pop()
            if state in shallowest and depth >= shallowest[state]:
                continue
            shallowest[state] = depth

            if state.is_goal:
                result.solution = state
                result.depth = depth
                return result
            if depth >= self.depth_limit:
                continue

            result.nodes_expanded += 1
            child_depth = depth + 1

            for child in reversed(state.neighbors()):
                if child not in shallowest or child_depth < shallowest[child]:
                    frontier.append((child, child_depth))
                    result.nodes_generated += 1
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
