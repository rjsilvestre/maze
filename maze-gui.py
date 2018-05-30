import tkinter as tk
import mazegraph as mg

class MazeGui:
    """Main gui, contains the maze grid and the maze object. Allows to save,
    load and manipulate the mazes.

    Args:
        master: Parent tkinter object to write the child gui objects on.
    """
    def __init__(self, master):
        self.master = master
        self._line_width = 2
        self._tile_side = 50
        self._num_tiles = 15
        self._tiles = {}
        self._maze_dim = self._num_tiles * self._tile_side
        self._toggle_pos = None
        self._maze = mg.MazeGraph(self._num_tiles)

        # Creates frame
        self.main_frame = tk.Frame(master=self.master, padx=5, pady=5)
        self.main_frame.pack()

        # Functions calls
        self.build_grid()
        self.build_border()

        # Event bindings
        self.maze_grid.bind('<Button-1>', self.press_tile)
        self.maze_grid.bind('<B1-Motion>', self.update_toggle_pos)
        self.maze_grid.bind('<ButtonRelease-1>', self.clear_toggle_pos)

    def build_grid(self):
        """Draws the grid lines on the maze_grid canvas.
        """
        self.maze_grid = tk.Canvas(self.main_frame, width=self._maze_dim, height=self._maze_dim,
                bg='white', highlightthickness=self._line_width, highlightbackground='black')
        self.maze_grid.pack()
        for px in range(self._tile_side+self._line_width, self._maze_dim, self._tile_side):
            self.maze_grid.create_line((px, 0), (px, self._maze_dim+self._line_width),
                    width=self._line_width, tag='grid_line')
            self.maze_grid.create_line((0, px), (self._maze_dim+self._line_width, px),
                    width=self._line_width, tag='grid_line')

    def pos_to_cords(self, x, y):
        """Calculates the cordinates of a tile on the canvas grid from a x, y
        absolute position in pixels.

        Args:
            x: int, absolute x position in pixels.
            y: int, aboslute y position in pixels.

        Returns:
            tuple, with the x, y coordinates acording to the canvas grid.
        """
        half_line_width = self._line_width / 2
        tile_x = int(x // (self._tile_side + (half_line_width/self._num_tiles)))
        tile_y = int(y // (self._tile_side + (half_line_width/self._num_tiles)))
        return tile_x, tile_y

    def build_border(self):
        """Creates maze tile outer wall border.
        """
        exp_tile = self._tile_side + self._line_width
        last_tile = self._tile_side * (self._num_tiles-1) + self._line_width
        for px0 in range(self._line_width, self._maze_dim+1, self._tile_side):
            px1 = px0 + exp_tile
            if self.pos_to_cords(px0, 0) not in self._tiles:
                self.toggle_tile(*self.pos_to_cords(px0, 0))
            if self.pos_to_cords(px0, last_tile) not in self._tiles:
                self.toggle_tile(*self.pos_to_cords(px0, last_tile))
            if self.pos_to_cords(0, px0) not in self._tiles:
                self.toggle_tile(*self.pos_to_cords(0, px0))
            if self.pos_to_cords(last_tile, px0) not in self._tiles:
                self.toggle_tile(*self.pos_to_cords(last_tile, px0))
        self.maze_grid.tag_raise('grid_line')

    def toggle_tile(self, tile_x, tile_y):
        """Toggles the tile on the cursor position on the grid on or off.

        Args:
            tile_x: int, x coordinate of the tile on the grid.
            tile_y: int, y coordinate of the tile on the grid.
        """
        if (tile_x, tile_y) in self._tiles:
            self.maze_grid.delete(self._tiles[(tile_x, tile_y)])
            del self._tiles[(tile_x, tile_y)]
        else:
            x = (self._tile_side*tile_x) + self._line_width
            y = (self._tile_side*tile_y) + self._line_width
            x2 = (self._tile_side*tile_x) + self._tile_side + self._line_width
            y2 = (self._tile_side*tile_y) + self._tile_side + self._line_width
            self._tiles[(tile_x, tile_y)] = self.maze_grid.create_rectangle(
                    x, y, x2, y2, fill='red', outline='')
            self.maze_grid.tag_raise('grid_line')
        self._maze.update_walls((tile_x, tile_y))

    def press_tile(self, event):
        """Calls the toggle_tile function if it the pressed tile is not on the edge.
        Bind of <Button1> event, or called by the update_toggle_pos function.

        Args:
            event: The event object of the bind
        """
        tile_x, tile_y = self.pos_to_cords(event.x, event.y)
        self._toggle_pos = (tile_x, tile_y)
        if 0 < tile_x < self._num_tiles-1 and 0 < tile_y < self._num_tiles-1:
            self.toggle_tile(tile_x, tile_y)

    def update_toggle_pos(self, event):
        """Updates the toggle_pos attribute and calls toggle_tile function if
        the coordinate changes while the mouse button1 is pressed. Bind of
        <B1-Motion> event.

        Args:
            event: The event object of the bind
        """
        tile_x, tile_y = self.pos_to_cords(event.x, event.y)
        if (tile_x, tile_y) != self._toggle_pos:
            self._toggle_pos = (tile_x, tile_y)
            self.press_tile(event)

    def clear_toggle_pos(self, event):
        """Clears the toggle_pos attribute setting it with the None value.
        Bind of <ButtonRelease-1> event.

        Args:
            event: The event object of the bind.
        """
        self._toggle_pos = None

if __name__ == '__main__':
    root = tk.Tk()
    MazeGui(root)
    root.mainloop()
