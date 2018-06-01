import tkinter as tk
import maze

class MazeGui:
    """Main gui, contains the maze grid and the maze object. Allows to save,
    load and manipulate the mazes.

    Args:
        master: Parent tkinter object to write the child gui objects on.
    """
    def __init__(self, master):
        self.master = master
        self.line_width = 2
        self.tile_side = 50
        self.num_tiles = 15
        self.tiles = {}
        self.maze_dim = self.num_tiles * self.tile_side
        self.toggle_pos = None
        self.maze = maze.Maze(self.num_tiles)
        self.path = {}

        # Build empty maze
        self.build_grid()
        self.build_border()

        # Buttons frame
        self.btns_frame = tk.Frame(self.master)
        self.btns_frame.pack(padx=5, pady=5)

        # Buttons
        self.btn_dfs = tk.Button(self.btns_frame, text='Depth First Search', command=self.dfs)
        self.btn_clr_path = tk.Button(self.btns_frame, text='Clear Path', command=self.clear_path)
        self.btn_clr_path.pack(side=tk.BOTTOM)
        self.btn_dfs.pack(side=tk.BOTTOM)

        # Event bindings
        self.maze_grid.bind('<Button-1>', self.press_tile)
        self.maze_grid.bind('<B1-Motion>', self.update_toggle_pos)
        self.maze_grid.bind('<ButtonRelease-1>', self.clear_toggle_pos)

    def build_grid(self):
        """Draws the grid lines on the maze_grid canvas.
        """
        self.maze_grid = tk.Canvas(self.master, width=self.maze_dim, height=self.maze_dim,
                bg='white', highlightthickness=self.line_width, highlightbackground='black')
        self.maze_grid.pack(padx=5, pady=5)
        for px in range(self.tile_side+self.line_width, self.maze_dim, self.tile_side):
            self.maze_grid.create_line((px, 0), (px, self.maze_dim+self.line_width),
                    width=self.line_width, tag='grid_line')
            self.maze_grid.create_line((0, px), (self.maze_dim+self.line_width, px),
                    width=self.line_width, tag='grid_line')

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

    def tile_to_cords(self, tile_x, tile_y):
        """Calculates the coordinates of the left top and botton right edges of
        a tile on the canvas.

        Args:
            x: int, x position of the tile.
            y: int, y position of the tile.

        Returns:
            tuple, with the x1, y1, x2, y2 coordinates of the edges on the canvas.
        """
        x1 = (self.tile_side*tile_x) + self.line_width
        y1 = (self.tile_side*tile_y) + self.line_width
        x2 = (self.tile_side*tile_x) + self.tile_side + self.line_width
        y2 = (self.tile_side*tile_y) + self.tile_side + self.line_width
        return x1, y1, x2, y2

    def build_border(self):
        """Creates maze tile outer wall border.
        """
        exp_tile = self.tile_side + self.line_width
        last_tile = self.tile_side * (self.num_tiles-1) + self.line_width
        for px0 in range(self.line_width, self.maze_dim+1, self.tile_side):
            px1 = px0 + exp_tile
            if self.cords_to_tile(px0, 0) not in self.tiles:
                self.toggle_tile(*self.cords_to_tile(px0, 0))
            if self.cords_to_tile(px0, last_tile) not in self.tiles:
                self.toggle_tile(*self.cords_to_tile(px0, last_tile))
            if self.cords_to_tile(0, px0) not in self.tiles:
                self.toggle_tile(*self.cords_to_tile(0, px0))
            if self.cords_to_tile(last_tile, px0) not in self.tiles:
                self.toggle_tile(*self.cords_to_tile(last_tile, px0))
        self.maze_grid.tag_raise('grid_line')

    def toggle_tile(self, tile_x, tile_y):
        """Toggles the tile on the cursor position on the grid on or off.

        Args:
            tile_x: int, x coordinate of the tile on the grid.
            tile_y: int, y coordinate of the tile on the grid.
        """
        if (tile_x, tile_y) in self.tiles:
            self.maze_grid.delete(self.tiles[(tile_x, tile_y)])
            del self.tiles[(tile_x, tile_y)]
        else:
            x1, y1, x2, y2 = self.tile_to_cords(tile_x, tile_y)
            self.tiles[(tile_x, tile_y)] = self.maze_grid.create_rectangle(
                    x1, y1, x2, y2, fill='red', outline='')
        self.maze_grid.tag_raise('grid_line')
        self.maze.update_walls((tile_x, tile_y))

    def draw_path(self, path):
        for tile in path:
            tile_x, tile_y = tile
            x1, y1, x2, y2 = self.tile_to_cords(tile_x, tile_y)
            self.path[(tile_x, tile_y)] = self.maze_grid.create_rectangle(
                    x1, y1, x2, y2, fill='blue', outline='')
        self.maze_grid.tag_raise('grid_line')

    def clear_path(self):
        for tile in list(self.path):
            tile_x, tile_y = tile
            self.maze_grid.delete(self.path[(tile_x, tile_y)])
            del self.path[(tile_x, tile_y)]

    # Buttons methods
    def dfs(self, animate=False):
        self.clear_path()
        path = self.maze.dfs([], self.maze.start)
        if path:
            self.draw_path(path)

    # Bind methods
    def press_tile(self, event):
        """Calls the toggle_tile function if it the pressed tile is not on the edge.
        Bind of <Button1> event, or called by the update_toggle_pos function.

        Args:
            event: The event object of the bind
        """
        tile_x, tile_y = self.cords_to_tile(event.x, event.y)
        self.toggle_pos = (tile_x, tile_y)
        if 0 < tile_x < self.num_tiles-1 and 0 < tile_y < self.num_tiles-1:
            self.toggle_tile(tile_x, tile_y)

    def update_toggle_pos(self, event):
        """Updates the toggle_pos attribute and calls toggle_tile function if
        the coordinate changes while the mouse button1 is pressed. Bind of
        <B1-Motion> event.

        Args:
            event: The event object of the bind
        """
        tile_x, tile_y = self.cords_to_tile(event.x, event.y)
        if (tile_x, tile_y) != self.toggle_pos:
            self.toggle_pos = (tile_x, tile_y)
            self.press_tile(event)

    def clear_toggle_pos(self, event):
        """Clears the toggle_pos attribute setting it with the None value.
        Bind of <ButtonRelease-1> event.

        Args:
            event: The event object of the bind.
        """
        self.toggle_pos = None

if __name__ == '__main__':
    root = tk.Tk()
    MazeGui(root)
    root.mainloop()
