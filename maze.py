class Maze:
    def __init__(self, num_nodes):
        self._num_nodes = num_nodes
        self._start = (1, 1)
        self._goal = (self._num_nodes-2, self._num_nodes-2)
        self._walls = set()

    @property
    def start(self):
        return self._start

    @property
    def goal(self):
        return self._goal

    def validate_tile(self, tile):
        if not isinstance(tile, tuple):
            raise TypeError('Tile is not a tuple.')
        x, y = tile
        if x not in range(self._num_nodes) or y not in range(self._num_nodes):
            raise ValueError('Tile coordinates are not valid.')

    def update_walls(self, tile):
        self.validate_tile(tile)
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
            if (x-1, y) in paths and (x-1, y) in self._graph:
                self._graph[(x, y)].append((x-1, y))
            if (x, y+1) in paths and (x, y+1) in self._graph:
                self._graph[(x, y)].append((x, y+1))
            if (x, y-1) in paths and (x, y-1) in self._graph:
                self._graph[(x, y)].append((x, y-1))

    def dfs(self, path, next_node):
        self.make_graph()
        # Concatenate instead of appending to not mutate path
        path = path + [next_node]
        if next_node == self._goal:
            return path
        for node in self._graph[next_node]:
            if node not in path:
                final_path = self.dfs(path, node)
                if final_path:
                    return final_path
