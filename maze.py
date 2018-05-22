import tkinter as tk

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
        self.maze_grid = tk.Canvas(self.master, width=self.maze_dim, height=self.maze_dim,
                bg='white', highlightthickness=self.line_width, highlightbackground='black')

        # Functions calls
        self.maze_grid.pack()
        self.build_grid()
        self.build_border()

        # Event bindings
        self.maze_grid.bind('<Button-1>', self.press_tile)
        self.maze_grid.bind('<B1-Motion>', self.update_toggle_pos)
        self.maze_grid.bind('<ButtonRelease-1>', self.clear_toggle_pos)

    def build_grid(self):
        """Draws the grid lines on the maze_grid canvas.
        """
        self.maze_grid.delete('grid_line')
        for px in range(self.tile_side+self.line_width, self.maze_dim, self.tile_side):
            self.maze_grid.create_line((px, 0), (px, self.maze_dim+self.line_width),
                    width=self.line_width, tag='grid_line')
            self.maze_grid.create_line((0, px), (self.maze_dim+self.line_width, px),
                    width=self.line_width, tag='grid_line')

    def pos_to_cords(self, x, y):
        """Calculates the cordinates of a tile on the canvas grid from a x, y
        absolute position in pixels.

        Args:
            x: int, absolute x position in pixels.
            y: int, aboslute y position in pixels.

        Returns:
            tuple, with the x, y coordinates acording to the canvas grid.
        """
        half_line_width = self.line_width / 2
        tile_x = int(x // (self.tile_side + (half_line_width/self.num_tiles)))
        tile_y = int(y // (self.tile_side + (half_line_width/self.num_tiles)))
        return tile_x, tile_y

    def build_border(self):
        exp_tile = self.tile_side + self.line_width
        last_tile = self.tile_side * (self.num_tiles-1) + self.line_width
        for px0 in range(self.line_width, self.maze_dim+1, self.tile_side):
            px1 = px0 + exp_tile
            if self.pos_to_cords(px0, 0) not in self.tiles:
                self.toggle_tile(*self.pos_to_cords(px0, 0))
            if self.pos_to_cords(px0, last_tile) not in self.tiles:
                self.toggle_tile(*self.pos_to_cords(px0, last_tile))
            if self.pos_to_cords(0, px0) not in self.tiles:
                self.toggle_tile(*self.pos_to_cords(0, px0))
            if self.pos_to_cords(last_tile, px0) not in self.tiles:
                self.toggle_tile(*self.pos_to_cords(last_tile, px0))
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
            x = (self.tile_side*tile_x) + self.line_width
            y = (self.tile_side*tile_y) + self.line_width
            x2 = (self.tile_side*tile_x) + self.tile_side + self.line_width
            y2 = (self.tile_side*tile_y) + self.tile_side + self.line_width
            self.tiles[(tile_x, tile_y)] = self.maze_grid.create_rectangle(
                    x, y, x2, y2, fill='red', outline='')
            self.maze_grid.tag_raise('grid_line')

    def press_tile(self, event):
        """Calls the toggle_tile function if it the pressed tile is not on the edge.
        Bind of <Button1> event, or called by the update_toggle_pos function.

        Args:
            event: The event object of the bind
        """
        tile_x, tile_y = self.pos_to_cords(event.x, event.y)
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
        tile_x, tile_y = self.pos_to_cords(event.x, event.y)
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

root = tk.Tk()
MazeGui(root)
root.mainloop()
