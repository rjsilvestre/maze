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
        self.maze_dim = self.num_tiles * self.tile_side + self.line_width
        self.toggle_pos = None
        self.maze_grid = tk.Canvas(self.master, width=self.maze_dim, height=self.maze_dim,
                bg='white')

        # Functions calls
        self.maze_grid.pack()
        self.build_grid()
        # self.build_empty_maze()

        # Event bindings
        self.maze_grid.bind('<Button-1>', self.toggle_tile)
        self.maze_grid.bind('<B1-Motion>', self.update_toggle_pos)
        self.maze_grid.bind('<ButtonRelease-1>', self.clear_toggle_pos)

    def build_grid(self):
        """Draws the grid lines on the maze_grid canvas.
        """
        self.maze_grid.delete('grid_line')
        for px in range(self.line_width, self.maze_dim+1, self.tile_side):
            self.maze_grid.create_line((px, 0), (px, self.maze_dim), width=self.line_width,
                    tag='grid_line')
            self.maze_grid.create_line((0, px), (self.maze_dim, px), width=self.line_width,
                    tag='grid_line')

    # TODO
    def build_empty_maze(self):
        sqr_size = self.tile_side + (2*self.line_width)
        for px0 in range(0, self.maze_dim+1, self.tile_side):
            px1 = px0 + sqr_size
            self.maze_grid.create_rectangle((px0, 0), (px1, sqr_size), fill='red', outline='')
            self.maze_grid.create_rectangle((0, px0), (sqr_size, px1), fill='red', outline='')
            self.maze_grid.tag_raise('grid_line')

    def toggle_tile(self, event):
        """Toggles the tile on the cursor position on the grid on or off.
        Bind of <Button1> event, or called by the update_toggle_pos function.

        Args:
            event: The event object of the bind
        """
        half_line_width = self.line_width / 2
        tile_x = event.x // (self.tile_side + (half_line_width/self.num_tiles))
        tile_y = event.y // (self.tile_side + (half_line_width/self.num_tiles))
        self.toggle_pos = (tile_x, tile_y)
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

    def update_toggle_pos(self, event):
        """Updates the toggle_pos attribute if the coordinate changes while the
        mouse button1 is pressed. Bind of <B1-Motion> event.

        Args:
            event: The event object of the bind
        """
        half_line_width = self.line_width / 2
        tile_x = event.x // (self.tile_side + (half_line_width/self.num_tiles))
        tile_y = event.y // (self.tile_side + (half_line_width/self.num_tiles))
        if (tile_x, tile_y) != self.toggle_pos:
            self.toggle_pos = (tile_x, tile_y)
            self.toggle_tile(event)

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
