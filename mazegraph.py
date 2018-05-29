class MazeGraph:
    def __init__(self, maze_dim):
        self._maze_dim = maze_dim

    def make_graph(self, walls):
        path = [(x, y) for x in range(self._maze_dim)
                for y in range(self._maze_dim) if (x, y) not in walls]
        self._graph = {(x, y): [] for x in range(self._maze_dim)
                for y in range(self._maze_dim)}
        for tile in path:
            x, y = tile
            if (x+1, y) in path and (x+1, y) in self._graph:
                self._graph[tile].append((x+1, y))
            if (x-1, y) in path and (x-1, y) in self._graph:
                self._graph[tile].append((x-1, y))
            if (x, y+1) in path and (x, y+1) in self._graph:
                self._graph[tile].append((x, y+1))
            if (x, y-1) in path and (x, y-1) in self._graph:
                self._graph[tile].append((x, y-1))
