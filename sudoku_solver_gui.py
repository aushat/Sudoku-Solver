# Sudoku Solver 

import time   
import tkinter as tk
from tkinter import filedialog, messagebox


# creating a class for the Sudoku Solver
class SudokuSolver:
    def __init__(self, grid):
        # store the input Sudoku grid
        self.grid = grid
        # domains include the possible values for each cell
        self.domains = {}
        # neighbors are the cells that share row, column or 3x3 box
        self.neighbors = {}
        # counters for tracking performance
        self.recursive_calls = 0
        self.backtracks = 0
        self.steps = 0  # keeps track of total steps
        
    # this function prepares domains and neighbor relationships for all cells
    def setup(self):
        for r in range(9):                 # loop through rows
            for c in range(9):             # loop through columns
                pos = (r, c)               # represents the position of the cell
                val = self.grid[r][c]      # value at that cell
                # if the cell already has a number (not 0), domain is just that number
                # otherwise the domain is any value from 1–9 
                self.domains[pos] = {val} if val != 0 else set(range(1, 10))
                
                nbs = set()  # this will hold all neighboring cell positions
                
                # add all cells in the same row and column as neighbors
                for i in range(9):
                    if i != c: nbs.add((r, i))  # same row
                    if i != r: nbs.add((i, c))  # same column

                # find which 3x3 box the cell belongs to
                br, bc = (r//3)*3, (c//3)*3
                # add all cells from that 3x3 box
                for i in range(br, br+3):
                    for j in range(bc, bc+3):
                        if (i, j) != (r, c): nbs.add((i, j))
                # save all these neighbors for this cell
                self.neighbors[pos] = nbs

    # AC-3
    def ac3(self):
        # queue stores all pairs of cells to check consistency
        queue = [(xi, xj) for xi in self.domains for xj in self.neighbors[xi]]
        while queue:                      
            xi, xj = queue.pop(0)         # take one arc from the queue

            # we count this as a step to measure total work done
            self.steps += 1

            # to check if the domain of xi can be reduced on xj
            if self.reduce_domain(xi, xj):
                # if a domain becomes empty, that means inconsistency is found
                if len(self.domains[xi]) == 0:
                    return False
                # if xi’s domain changed, then add all its neighbors back to the queue
                for xk in self.neighbors[xi] - {xj}:
                    queue.append((xk, xi))
        return True  

    def reduce_domain(self, xi, xj):
        # revise removes invalid values from xi's domain based on xj
        changed = False
        # only apply constraint if xj has a single fixed value
        if len(self.domains[xj]) == 1:
            val = next(iter(self.domains[xj]))
            # if xi also has that value, remove it (since they can’t be the same)
            if val in self.domains[xi]:
                self.domains[xi].remove(val)
                changed = True
        return changed

    # Backtracking search 
    def backtrack(self):
        # to count how many recursive calls are there
        self.recursive_calls += 1

        # if every domain has one value the puzzle will be solved
        if all(len(dom) == 1 for dom in self.domains.values()):
            return True

        # MRV heuristic where we pick the cell with the least possible values
        var = min((p for p in self.domains if len(self.domains[p]) > 1),
                  key=lambda p: len(self.domains[p]))

        # trying all the possible values for this variable
        for val in sorted(self.domains[var]):
            self.steps += 1  # to count every step

            # to make a copy of the current state 
            saved = {p: self.domains[p].copy() for p in self.domains}

            # here we assign this value to the variable
            self.domains[var] = {val}

            # now run AC-3 again to make this change
            if self.ac3() and self.backtrack():
                return True  

            # we start to backtrack if the value doesn't work
            self.domains = saved
            self.backtracks += 1
        return False  
    
    def solve(self):
        # setup domains and neighbors before solving
        self.setup()
        start = time.perf_counter()  # start timer

        # first apply AC-3 to reduce the search space
        self.ac3()

        # then start backtracking search
        solved = self.backtrack()

        # calculate total execution time
        total_time = (time.perf_counter() - start) * 1000  # convert to ms

        # store all the metrics in a dictionary
        metrics = {
            "status": "solved" if solved else "no solution",
            "time_ms": round(total_time, 2),
            "recursive_calls": self.recursive_calls,
            "backtracks": self.backtracks,
            "total_steps": self.steps
        }
        # return solved board and metrics
        return self.to_grid(), metrics
    
    def to_grid(self):
        return [[next(iter(self.domains[(r, c)])) for c in range(9)] for r in range(9)]

 
def read_txt(path):
    # this function will read the example input Sudoku puzzle from text file
    grid = []
    with open(path) as f:
        for line in f:
            # this will remove spaces and line breaks
            line = line.strip().replace(' ', '')
            if line:
                # convert the digits to integers and blanks to 0
                grid.append([int(ch) if ch.isdigit() else 0 for ch in line])
    return grid

# Sudoku display in GUI format
class SudokuDisplay:
    def __init__(self, root):
        self.root = root
        root.title("Sudoku Solver")  

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        # button to choose the Sudoku text file
        tk.Button(btn_frame, text="Choose Sudoku File", command=self.load_file).grid(row=0, column=0, padx=5)

        # button to solve the Sudoku 
        tk.Button(btn_frame, text="Solve", command=self.solve_puzzle).grid(row=0, column=1, padx=5)

        # button to clear everytging
        tk.Button(btn_frame, text="Clear", command=self.clear).grid(row=0, column=2, padx=5)

        # Sudoku grid display
        self.grid_line = tk.Frame(root)
        self.grid_line.pack(pady=10)

        self.cells = [[tk.Label(self.grid_line, text="", width=2, height=1,
                                font=("Arial", 18), borderwidth=1, relief="solid", bg="white")
                       for _ in range(9)] for _ in range(9)]

        # placing each label in a 9x9 grid layout
        for r in range(9):
            for c in range(9):
                label = self.cells[r][c]
                label.grid(row=r, column=c, padx=2, pady=2)

        # to show metrics
        self.metrics_label = tk.Label(root, text="")
        self.metrics_label.pack(pady=10)

        self.grid = None  # stores the loaded Sudoku puzzle


    # to load Sudoku text file
    def load_file(self):
        # to choose the Sudoku text file
        path = filedialog.askopenfilename(title="Select Sudoku File", filetypes=[("Text Files", "*.txt")])

        # to stop program if no file was chosen 
        if not path:
            return
        try:
            # read the Sudoku file and store it as a grid
            self.grid = read_txt(path)
            # to display the unsolved Sudoku 
            self.display_grid(self.grid, unsolved=True)
        except Exception as e:
            # show an error popup if something goes wrong
            messagebox.showerror("Error", f"Could not load file:\n{e}")


    # to display Sudoku grid 
    def display_grid(self, grid, unsolved=False):
        for r in range(9):
            for c in range(9):
                value = grid[r][c]
                if value == 0:
                    # if its 0 will show blank space as it represents empty cell
                    self.cells[r][c].config(text="", bg="#FFFFFF")
                else:
                    # shows number if cell isn't empty
                    self.cells[r][c].config(text=value, bg="#FFFFFF")


    # function to solve Sudoku 
    def solve_puzzle(self):
        
        solver = SudokuSolver(self.grid)
        solved_grid, metrics = solver.solve()
        
        # update the Sudoku grid with the solved values
        self.display_grid(solved_grid)

        # show metrics of puzzle solved
        self.metrics_label.config(
            text=f"Status: {metrics['status']} "
                 f"Execution Time: {metrics['time_ms']} ms "
                 f"Recursive Calls: {metrics['recursive_calls']} "
                 f"Backtracks: {metrics['backtracks']} "
                 f"Total Steps: {metrics['total_steps']}"
        )


    # function to clear the grid
    def clear(self):
        # remove all numbers from the grid 
        for r in range(9):
            for c in range(9):
                self.cells[r][c].config(text="", bg="white")

        # clear the metrics label
        self.metrics_label.config(text="")

        # reset grid variable
        self.grid = None

# main program 
if __name__ == "__main__":
    root = tk.Tk()         # to create the main window
    SudokuDisplay(root)    # initialize the Sudoku GUI
    root.mainloop()      
