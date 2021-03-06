import tkinter as tk
import maze

class MazeGui(tk.Frame):
    """Main gui, contains the maze grid and the maze object. Allows to save,
    load and manipulate the mazes.

    Args:
        master: Parent tkinter object to write the child gui objects on.
    """
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.line_width = 2
        self.tile_side = 50
        self.num_tiles = 15
        self.btn_width = 15
        self.maze_dim = self.num_tiles * self.tile_side
        self.toggle_pos = None
        self.animation = None
        self.tiles, self.path, self.visited = {}, {}, {}

        # Packs the main frame
        self.pack(padx=5, pady=5)

        # Creates a grid
        self.new_grid()

        # Buttons frames
        self.btns_frame = tk.Frame(self)
        self.btnsmz_frame = tk.LabelFrame(self.btns_frame, text='maze', padx=10,
                pady=10)
        self.btnspf_frame = tk.LabelFrame(self.btns_frame, text='pathfind', padx=10,
                pady=10)
        self.btns_frame.pack(side=tk.BOTTOM, fill='x', expand='yes')
        self.btnsmz_frame.pack(side=tk.LEFT, fill='x', expand='yes', padx=(0, 5),
                pady=(10, 0))
        self.btnspf_frame.pack(side=tk.LEFT, fill='x', expand='yes', padx=(5, 0),
                pady=(10, 0))

        # Buttons
        self.btnsmz_frame.grid_columnconfigure(0, weight=1)
        self.btnsmz_frame.grid_columnconfigure(1, weight=1)
        self.btnspf_frame.grid_columnconfigure(0, weight=1)
        self.btnspf_frame.grid_columnconfigure(1, weight=1)
        self.btn_dfs = tk.Button(self.btnspf_frame, text='Depth First Search',
                command=lambda: self.search_path(self.maze.dfs), width=self.btn_width)
        self.btn_dfs_anim = tk.Button(self.btnspf_frame, text='DFS Animated',
                command=lambda: self.search_path(self.maze.dfs, animate=True),
                width=self.btn_width)
        self.btn_bfs = tk.Button(self.btnspf_frame, text='Breadth First Search',
                command=lambda: self.search_path(self.maze.bfs), width=self.btn_width)
        self.btn_bfs_anim = tk.Button(self.btnspf_frame, text='BFS Animated',
                command=lambda: self.search_path(self.maze.bfs, animate=True),
                width=self.btn_width)
        self.btn_set_start = tk.Button(self.btnsmz_frame, text='Set Start',
                command=lambda: self.set_ends_bind('start'), width=self.btn_width)
        self.btn_set_goal = tk.Button(self.btnsmz_frame, text='Set Goal',
                command=lambda: self.set_ends_bind('goal'), width=self.btn_width)
        self.btn_clr_visited_path = tk.Button(self.btnsmz_frame, text='Clear Path',
                command=self.clear_visited_path, width=self.btn_width)
        self.btn_reset_grid = tk.Button(self.btnsmz_frame, text='Reset',
                command=self.new_grid, width=self.btn_width)
        self.btn_dfs.grid(row=0, column=0, sticky=tk.E)
        self.btn_dfs_anim.grid(row=0, column=1, sticky=tk.W)
        self.btn_bfs.grid(row=1, column=0, sticky=tk.E)
        self.btn_bfs_anim.grid(row=1, column=1, sticky=tk.W)
        self.btn_set_start.grid(row=2, column=0, sticky=tk.E)
        self.btn_set_goal.grid(row=2, column=1, sticky=tk.W)
        self.btn_clr_visited_path.grid(row=3, column=0, sticky=tk.E)
        self.btn_reset_grid.grid(row=3, column=1, sticky=tk.W)

    def set_binds(self):
        """Set the all the binds"""
        self.maze_grid.bind('<Button-1>', self.press_tile)
        self.maze_grid.bind('<B1-Motion>', self.update_toggle_pos)
        self.maze_grid.bind('<ButtonRelease-1>', self.clear_toggle_pos)

    def cancel_animation(func):
        def cancel(self, *args, **kargs):
            if self.animation:
                self.after_cancel(self.animation)
                self.animation = None
            func(self, *args, **kargs)
        return cancel

    def lock_animation(func):
        def lock(self, *args, **kargs):
            if not self.animation:
                func(self, *args, **kargs)
        return lock

    def cords_to_tile(self, x, y):
        """Calculates the position of a tile on the canvas grid from a x, y
        coordinates in pixels.

        Args:
            x: int, x coordinate in pixels.
            y: int, y coordinate in pixels.

        Returns:
            tuple, with the x, y position acording to the canvas grid.
        """
        half_line_width = self.line_width / 2
        tile_x = int(x // (self.tile_side + (half_line_width/self.num_tiles)))
        tile_y = int(y // (self.tile_side + (half_line_width/self.num_tiles)))
        return tile_x, tile_y

    def tile_to_cords(self, tile):
        """Calculates the coordinates of the left top and botton right edges of
        a tile on the canvas.

        Args:
            tile: tuple, with x, y ints as position of the tile

        Returns:
            tuple, with the x1, y1, x2, y2 coordinates of the edges on the canvas.
        """
        tile_x, tile_y = tile
        x1 = (self.tile_side*tile_x) + self.line_width
        y1 = (self.tile_side*tile_y) + self.line_width
        x2 = (self.tile_side*tile_x) + self.tile_side + self.line_width
        y2 = (self.tile_side*tile_y) + self.tile_side + self.line_width
        return x1, y1, x2, y2

    def toggle_tile(self, tile):
        """Toggles the tile on the cursor position on the grid on or off.

        Args:
            tile: tuple, with x, y ints as position of the tile
        """
        if tile in self.tiles:
            self.maze_grid.delete(self.tiles[tile])
            del self.tiles[tile]
        else:
            x1, y1, x2, y2 = self.tile_to_cords(tile)
            self.tiles[tile] = self.maze_grid.create_rectangle(x1, y1, x2, y2,
                    fill='red', outline='')
        self.maze_grid.tag_raise('grid_line')
        self.maze.update_walls(tile)

    def create_maze(self):
        """Calculates the default start and goal and creates a new maze object.
        """
        start = (1, 1)
        goal = (self.num_tiles-2, self.num_tiles-2)
        self.maze = maze.Maze(self.num_tiles, start, goal)

    def draw_grid(self):
        """Draws the grid lines on the maze_grid canvas."""
        self.maze_grid = tk.Canvas(self, width=self.maze_dim, height=self.maze_dim,
                bg='white', highlightthickness=self.line_width, highlightbackground='black')
        self.maze_grid.pack()
        for px in range(self.tile_side+self.line_width, self.maze_dim, self.tile_side):
            self.maze_grid.create_line((px, 0), (px, self.maze_dim+self.line_width),
                    width=self.line_width, tag='grid_line')
            self.maze_grid.create_line((0, px), (self.maze_dim+self.line_width, px),
                    width=self.line_width, tag='grid_line')

    def draw_border(self):
        """Creates maze tile outer wall border."""
        exp_tile = self.tile_side + self.line_width
        last_tile = self.tile_side * (self.num_tiles-1) + self.line_width
        for px0 in range(self.line_width, self.maze_dim+1, self.tile_side):
            px1 = px0 + exp_tile
            if self.cords_to_tile(px0, 0) not in self.tiles:
                self.toggle_tile(self.cords_to_tile(px0, 0))
            if self.cords_to_tile(px0, last_tile) not in self.tiles:
                self.toggle_tile(self.cords_to_tile(px0, last_tile))
            if self.cords_to_tile(0, px0) not in self.tiles:
                self.toggle_tile(self.cords_to_tile(0, px0))
            if self.cords_to_tile(last_tile, px0) not in self.tiles:
                self.toggle_tile(self.cords_to_tile(last_tile, px0))
        self.maze_grid.tag_raise('grid_line')

    def draw_ends(self, start=None, goal=None):
        """Draws the start and goal markers on the grid. Can draw both or only
        one.

        Args:
            start: tuple, the start position tile.
            goal: tuple, the goal position tile.
        """
        for end in ['start', 'goal']:
            tile = eval(end)
            if tile:
                x1, y1, x2, y2 = self.tile_to_cords(tile)
                x = (x1+x2) / 2
                y = (y1+y2) / 2
                setattr(self, end, self.maze_grid.create_text(x, y, text=end[0],
                    justify=tk.CENTER, font=("Helvetica", 18, "bold"), tag='end'))

    def draw_visited_path(self, path, visited=None):
        """Draws the visited tiles on the search and the final path. The visited
        is drawing is animated and is optional.

        Args:
            path: list, the list of the tiles of the final path.
            visited list, default=None the list of the visited tiles while searching
                for a path.
        """
        if visited:
            tile = visited.pop(0)
            x1, y1, x2, y2 = self.tile_to_cords(tile)
            self.visited[(tile)] = self.maze_grid.create_rectangle(x1, y1, x2, y2,
                    fill='green', outline='')
            self.maze_grid.tag_raise('grid_line')
            self.animation = self.after(100,
                    lambda: self.draw_visited_path(path, visited))
        else:
            self.animation = None
            for tile in path:
                x1, y1, x2, y2 = self.tile_to_cords(tile)
                self.path[(tile)] = self.maze_grid.create_rectangle(x1, y1, x2, y2,
                        fill='blue', outline='')
                self.maze_grid.tag_raise('grid_line')
        self.maze_grid.tag_raise('end')

    @cancel_animation
    def new_grid(self):
        """Creates a new grid. Destroys the previous grid canvas object if exists
        and resets all the relevant attributes.
        Builds the canvas using the instance attributes.
        """
        if hasattr(self, 'maze_grid'):
            self.maze_grid.destroy()
        self.tiles, self.path, self.visited = {}, {}, {}
        self.create_maze()
        self.draw_grid()
        self.draw_border()
        self.draw_ends(self.maze.start, self.maze.goal)
        self.set_binds()

    @cancel_animation
    def clear_visited_path(self):
        """Deletes the path and visisted tiles. Resets the dictionaries."""
        for tile in list(self.path):
            self.maze_grid.delete(self.path[tile])
        for tile in list(self.visited):
            self.maze_grid.delete(self.visited[tile])
        self.path, self.visited = {}, {}

    def search_path(self, search_func, animate=False):
        """Calls a search maze algorithm and draws the path to the goal and
        animates the search.

        Args:
            animate: bol, default=False. Animates the visited tiles during the
                search.
        """
        self.clear_visited_path()
        visited_path = search_func()
        if visited_path:
            path, visited = visited_path
            if animate:
                self.draw_visited_path(path, visited)
            else:
                self.draw_visited_path(path)

    def set_ends_bind(self, end):
        self.clear_visited_path()
        self.maze_grid.unbind('<Button-1>')
        self.maze_grid.unbind('<B1-Motion>')
        self.maze_grid.unbind('<ButtonRelease-1>')
        self.maze_grid.bind('<Button-1>', lambda event: self.set_end(event, end))

    # Bind methods
    @lock_animation
    def press_tile(self, event):
        """Calls the toggle_tile function if it the pressed tile is not on the
        edge or one of the ends of the path.
        Bind of <Button1> event, or called by the update_toggle_pos function.

        Args:
            event: The event object of the bind
        """
        tile = self.cords_to_tile(event.x, event.y)
        tile_x, tile_y = tile
        self.toggle_pos = tile
        if 0 < tile_x < self.num_tiles-1 and 0 < tile_y < self.num_tiles-1:
            if tile != self.maze.start and tile != self.maze.goal:
                self.toggle_tile(tile)

    @lock_animation
    def update_toggle_pos(self, event):
        """Updates the toggle_pos attribute and calls press_tile function if
        the coordinate changes while the mouse button1 is pressed. Bind of
        <B1-Motion> event.

        Args:
            event: The event object of the bind
        """
        tile_x, tile_y = self.cords_to_tile(event.x, event.y)
        if (tile_x, tile_y) != self.toggle_pos:
            self.toggle_pos = (tile_x, tile_y)
            self.press_tile(event)

    @lock_animation
    def clear_toggle_pos(self, event):
        """Clears the toggle_pos attribute setting it with the None value.
        Bind of <ButtonRelease-1> event.

        Args:
            event: The event object of the bind.
        """
        self.toggle_pos = None

    def set_end(self, event, end):
        new_end = self.cords_to_tile(event.x, event.y)
        new_end_x, new_end_y = new_end
        if ((new_end_x == 1 or new_end_x == self.num_tiles - 2) or
                (new_end_y == 1 or new_end_y == self.num_tiles - 2)):
            if (end == 'start' and new_end != self.maze.goal):
                self.maze_grid.delete(self.start)
                self.maze.start = new_end
                self.draw_ends(start=new_end)
            elif (end == 'goal' and new_end != self.maze.start):
                self.maze_grid.delete(self.goal)
                self.maze.goal = new_end
                self.draw_ends(goal=new_end)
            if new_end in self.tiles:
                self.toggle_tile(new_end)
        self.set_binds()

if __name__ == '__main__':
    root = tk.Tk()
    MazeGui(root)
    root.mainloop()
