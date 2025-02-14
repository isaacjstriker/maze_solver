from cell import Cell
import random
import time


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = seed
        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0) # Starts breaking walls from the top left corner
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()
    
    def _break_walls_r(self, i, j):
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
        random.shuffle(directions)  # Shuffle directions to ensure randomness

        self._cells[i][j].visited = True

        for direction in directions:
            ni, nj = i + direction[0], j + direction[1]

            if 0 <= ni < self._num_cols and 0 <= nj < self._num_rows and not self._cells[ni][nj].visited:
                if direction == (0, -1):  # Up
                    self._cells[i][j].has_top_wall = False
                    self._cells[ni][nj].has_bottom_wall = False
                elif direction == (1, 0):  # Right
                    self._cells[i][j].has_right_wall = False
                    self._cells[ni][nj].has_left_wall = False
                elif direction == (0, 1):  # Down
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[ni][nj].has_top_wall = False
                elif direction == (-1, 0):  # Left
                    self._cells[i][j].has_left_wall = False
                    self._cells[ni][nj].has_right_wall = False

                self._draw_cell(i, j)
                self._draw_cell(ni, nj)
                self._break_walls_r(ni, nj)

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False
    
    def solve(self):
        self._reset_cells_visited()
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()  # Call the _animate method
        self._cells[i][j].visited = True  # Mark the current cell as visited

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True  # If you are at the "end" cell (the goal) then return True

        # Define possible directions: Right, Down, Left, Up
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for direction in directions:
            ni, nj = i + direction[0], j + direction[1]

            if 0 <= ni < self._num_cols and 0 <= nj < self._num_rows and not self._cells[ni][nj].visited:
                if direction == (1, 0) and not self._cells[i][j].has_right_wall:  # Right
                    self._cells[i][j].draw_move(self._cells[ni][nj])  # Draw a move between the current cell and that cell
                    if self._solve_r(ni, nj):
                        return True
                    self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)  # Draw an "undo" move
                elif direction == (0, 1) and not self._cells[i][j].has_bottom_wall:  # Down
                    self._cells[i][j].draw_move(self._cells[ni][nj])  # Draw a move between the current cell and that cell
                    if self._solve_r(ni, nj):
                        return True
                    self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)  # Draw an "undo" move
                elif direction == (-1, 0) and not self._cells[i][j].has_left_wall:  # Left
                    self._cells[i][j].draw_move(self._cells[ni][nj])  # Draw a move between the current cell and that cell
                    if self._solve_r(ni, nj):
                        return True
                    self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)  # Draw an "undo" move
                elif direction == (0, -1) and not self._cells[i][j].has_top_wall:  # Up
                    self._cells[i][j].draw_move(self._cells[ni][nj])  # Draw a move between the current cell and that cell
                    if self._solve_r(ni, nj):
                        return True
                    self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)  # Draw an "undo" move

        return False  # If none of the directions worked out, return False