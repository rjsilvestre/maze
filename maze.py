class Maze:
    """Square maze object with. Creates a graph of the possible paths from the maze
    walls. Calculates a path to the goal using different pathfinding algorithms.

    Args:
        num_nodes: int, number of nodes per side.
        start: tuple, with two ints, the position on the grid.
        goal: tuple, with two ints, the position on the grid.
    """
    def __init__(self, num_nodes, start, goal):
        self._num_nodes = num_nodes
        self._walls = set()
        self.start = start
        self.goal = goal

    def validate_tile(func):
        """Validates if the argument is a valid maze tile.

        Raises:
            TypeError: If the argument is not a tuple.
            ValueError: If ane of the elements is not in a valid range.
        """
        def validation(self, tile):
            if not isinstance(tile, tuple):
                raise TypeError('Tile is not a tuple.')
            x, y = tile
            if x not in range(self._num_nodes) or y not in range(self._num_nodes):
                raise ValueError('Tile coordinates are not valid.')
            return func(self, tile)
        return validation

    @property
    def start(self):
        return self._start

    @start.setter
    @validate_tile
    def start(self, tile):
        self._start = tile

    @property
    def goal(self):
        return self._goal

    @goal.setter
    @validate_tile
    def goal(self, tile):
        self._goal = tile

    @validate_tile
    def update_walls(self, tile):
        if tile in self._walls:
            self._walls.remove(tile)
        else:
            self._walls.add(tile)

    def make_graph(self):
        paths = [(x, y) for x in range(self._num_nodes)
                for y in range(self._num_nodes) if (x, y) not in self._walls]
        self._graph = {(x, y): [] for x, y in paths}
        for x, y in paths:
            if (x+1, y) in paths and (x+1, y) in self._graph:
                self._graph[(x, y)].append((x+1, y))
            if (x, y+1) in paths and (x, y+1) in self._graph:
                self._graph[(x, y)].append((x, y+1))
            if (x-1, y) in paths and (x-1, y) in self._graph:
                self._graph[(x, y)].append((x-1, y))
            if (x, y-1) in paths and (x, y-1) in self._graph:
                self._graph[(x, y)].append((x, y-1))

    def dfs(self, next_node=None, path=[], visited=None):
        self.make_graph()
        if not next_node:
            next_node = self._start    # self._start cannot be used as default value
        if not visited:
            visited = []               # Empty list as default value will be used on repeated calls
        path = path + [next_node]      # Concatenate instead of appending to not mutate path
        visited.append(next_node)
        if next_node == self._goal:
            return path, visited
        for node in self._graph[next_node]:
            if node not in visited:
                visited_path = self.dfs(node, path, visited)
                if visited_path:
                    return visited_path

    def bfs(self):
        self.make_graph()
        paths = [[self._start]]
        visited = [self._start]
        while paths:
            cur_path = paths.pop(0)
            cur_node = cur_path[-1]
            for next_node in self._graph[cur_node]:
                if next_node not in visited:
                    visited.append(next_node)
                    new_path = cur_path + [next_node]
                    paths.append(new_path)
                if next_node == self._goal:
                    return new_path, visited
