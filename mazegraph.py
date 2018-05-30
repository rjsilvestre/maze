class MazeGraph:
    def __init__(self, num_nodes):
        self._num_nodes = num_nodes

    def make_graph(self, walls):
        path = [(x, y) for x in range(self._num_nodes)
                for y in range(self._num_nodes) if (x, y) not in walls]
        self._graph = {(x, y): [] for x, y in path}
        for x, y in path:
            if (x+1, y) in path and (x+1, y) in self._graph:
                self._graph[(x, y)].append((x+1, y))
            if (x-1, y) in path and (x-1, y) in self._graph:
                self._graph[(x, y)].append((x-1, y))
            if (x, y+1) in path and (x, y+1) in self._graph:
                self._graph[(x, y)].append((x, y+1))
            if (x, y-1) in path and (x, y-1) in self._graph:
                self._graph[(x, y)].append((x, y-1))
