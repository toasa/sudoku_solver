class Grid:
    SIZE = 9
    REG_SIZE = 3

    # The Grid consists nine regions. The region consists nine cells.
    # Each region is numbered as follows:
    #
    #     +-----------+
    #     | 1 | 2 | 3 |
    #     |---+---+---|
    #     | 4 | 5 | 6 |
    #     |---+---+---|
    #     | 7 | 8 | 9 |
    #     +-----------+
    #
    # To traverse a region, the R1 to R9 represents upper left cells of each region.
    R1 = [0, 0]
    R2 = [0, 3]
    R3 = [0, 6]
    R4 = [3, 0]
    R5 = [3, 3]
    R6 = [3, 6]
    R7 = [6, 0]
    R8 = [6, 3]
    R9 = [6, 6]
    ULcells = [ [R1, R1, R1, R2, R2, R2, R3, R3, R3],
                [R1, R1, R1, R2, R2, R2, R3, R3, R3],
                [R1, R1, R1, R2, R2, R2, R3, R3, R3],
                [R4, R4, R4, R5, R5, R5, R6, R6, R6],
                [R4, R4, R4, R5, R5, R5, R6, R6, R6],
                [R4, R4, R4, R5, R5, R5, R6, R6, R6],
                [R7, R7, R7, R8, R8, R8, R9, R9, R9],
                [R7, R7, R7, R8, R8, R8, R9, R9, R9],
                [R7, R7, R7, R8, R8, R8, R9, R9, R9] ]

    def __init__(self, grid):
        self.grid = grid

        nfilled = 0
        cells = [ (i, j) for i in range(self.SIZE) for j in range(self.SIZE) ]
        for (i, j) in cells:
            if self.filled(i, j):
                nfilled += 1
        self.nfilled = nfilled
        
    # solve solves sudoku using by backtracking.
    def solve(self, row, col):
        if row == self.SIZE - 1 and col >= self.SIZE:
            return True

        # If col exceeds grid size, we handle row as next line and
        # col as first.
        if col >= self.SIZE:
            row += 1
            col = 0

        # If the cell already filled, we proceed to the next iteration.
        if self.filled(row, col):
            return self.solve(row, col + 1)

        for val in range(1, 10):
            if self.fillable(row, col, val):
                self.set(row, col, val)
                if self.solve(row, col + 1):
                    return True

        self.blank(row, col)

    # fillable returns whether or not the cell positioned by row and col can be filled.
    def fillable(self, row, col, val):
        # row check
        for col_i in range(self.SIZE):
            if self.get(row, col_i) == val:
                return False

        # column check
        for row_i in range(self.SIZE):
            if self.get(row_i, col) == val:
                return False

        # region check
        reg = self.ULcells[row][col]
        row_ul = reg[0]
        col_ul = reg[1]
        for row_i in range(self.REG_SIZE):
            for col_i in range(self.REG_SIZE):
                r = row_ul + row_i
                c = col_ul + col_i
                if self.get(r, c) == val:
                    return False

        return True

    def filled(self, row, col):
        return self.grid[row][col] != 0

    def set(self, row, col, val):
        self.grid[row][col] = val
        self.nfilled += 1

    def get(self, row, col):
        return self.grid[row][col]

    def blank(self, row, col):
        self.grid[row][col] = 0
        self.nfilled -= 1

    def print(self):
        for row in self.grid:
            print(row)

def main():
    grid = [ [3, 0, 6, 5, 0, 8, 4, 0, 0],
             [5, 2, 0, 0, 0, 0, 0, 0, 0],
             [0, 8, 7, 0, 0, 0, 0, 3, 1],
             [0, 0, 3, 0, 1, 0, 0, 8, 0],
             [9, 0, 0, 8, 6, 3, 0, 0, 5],
             [0, 5, 0, 0, 9, 0, 6, 0, 0],
             [1, 3, 0, 0, 0, 0, 2, 5, 0],
             [0, 0, 0, 0, 0, 0, 0, 7, 4],
             [0, 0, 5, 2, 0, 6, 3, 0, 0] ]

    grid = Grid(grid)
    grid.solve(0, 0)
    grid.print()

main()
