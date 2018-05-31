class Maze:
    def __init__(self, num_nodes):
        self._num_nodes = num_nodes
        self._start = (1, 1)
        self._goal = (self._num_nodes-2, self._num_nodes-2)
        self._walls = set()

    def update_walls(self, tile):
        if not isinstance(tile, tuple):
            raise TypeError('Tile is not a tuple.')
        x, y = tile
        if x not in range(self._num_nodes) or y not in range(self._num_nodes):
            raise ValueError('Tile coordinates are not valid.')
        if tile in self._walls:
            self._walls.remove(tile)
        else:
            self._walls.add(tile)

    def make_graph(self):
        path = [(x, y) for x in range(self._num_nodes)
                for y in range(self._num_nodes) if (x, y) not in self._walls]
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
