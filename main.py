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
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self.filled(row, col):
                    nfilled += 1
        self.nfilled = nfilled

    def solve(self):
        self.solve_definite()
        self.solve_by_backtrack()

    def solve_definite(self):
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if not self.filled(row, col):
                    T, val = self.fillable(row, col)
                    if T:
                        self.set(row, col, val)
            else:
                continue

    # fillable returns whether or not the cell positioned by row and col can be filled,
    # and if so, returns a value, otherwise None.
    def fillable(self, row, col):
        nums = self.legal_numbers(row, col)
        
        # If there is only one possibility in the cell, then fillable.
        if len(nums) == 1:
            return True, nums[0]
        else:
            return False, None

    # legal_numbers returns the numbers that can fit in the cell.
    def legal_numbers(self, row, col):
        if self.filled(row, col):
            return [self.get(row, col)]

        num_exists = [False] * self.SIZE

        # row check
        for col_i in range(self.SIZE):
            if self.filled(row, col_i):
                n = self.get(row, col_i)
                num_exists[n-1] = True

        # column check
        for row_i in range(self.SIZE):
            if self.filled(row_i, col):
                n = self.get(row_i, col)
                num_exists[n-1] = True

        # region check
        reg = self.ULcells[row][col]
        row_ul = reg[0]
        col_ul = reg[1]
        for row_i in range(self.REG_SIZE):
            for col_i in range(self.REG_SIZE):
                r = row_ul + row_i
                c = col_ul + col_i
                if self.filled(r, c):
                    n = self.get(r, c)
                    num_exists[n-1] = True

        return [ i+1 for i in range(self.SIZE) if not num_exists[i] ]

    def solve_by_backtrack(self):
        if self.full():
            return True

        cells = [ (i, j) for i in range(self.SIZE) for j in range(self.SIZE) ]
        cells = [ (i, j) for (i, j) in cells if not self.filled(i, j) ]
        nums = [ self.legal_numbers(r, c) for (r, c) in cells ]
        cells_with_legal_nums = list(zip(cells, nums))

        # all cells sort by length of legal numbers.
        cells_with_legal_nums.sort(key=lambda p: len(p[1]))

        for ((row, col), nums) in cells_with_legal_nums:
            for n in nums:
                self.set(row, col, n)
                if self.solve_by_backtrack():
                    return True
                self.blank(row, col)

    def filled(self, row, col):
        return self.grid[row][col] != 0

    def full(self):
        return self.nfilled == self.SIZE * self.SIZE

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
             [5, 2, 0, 0, 0, 4, 0, 6, 8],
             [0, 8, 7, 0, 0, 9, 0, 3, 1],
             [0, 0, 3, 0, 1, 5, 0, 8, 0],
             [9, 0, 0, 8, 6, 3, 0, 0, 5],
             [0, 5, 0, 0, 9, 2, 6, 0, 0],
             [1, 3, 0, 0, 0, 7, 2, 5, 0],
             [6, 9, 2, 0, 0, 1, 0, 7, 4],
             [0, 0, 5, 2, 0, 6, 3, 0, 0] ]

    grid = Grid(grid)
    grid.solve()
    grid.print()

main()
