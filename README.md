# 🧩 Sudoku Solver with GUI

A Python-based **Sudoku Solver** that combines **Backtracking Search** and **AC-3 (Arc Consistency)** algorithms to efficiently solve Sudoku puzzles of varying difficulty.  
It also features an **interactive Tkinter GUI** that allows users to load puzzles, view solutions in real time, and clear the grid.

## Features
- Solves Sudoku puzzles using **AI search algorithms**:
  - **AC-3 (Constraint Satisfaction)** to simplify domains before search.
  - **Backtracking** to systematically explore valid number placements.
- Intuitive **Tkinter GUI** interface.
- Load puzzles from `.txt` files with a single click.
- Includes **sample puzzles** (`easy`, `medium`, and `hard`) for quick testing.
- Clear button to reset the grid instantly.

## 📂 File Structure
- sudoku_solver_gui.py # Main code (solver + GUI)
- puzzle_easy.txt # Sample easy puzzle
- puzzle_medium.txt # Sample medium puzzle
- puzzle_hard.txt # Sample hard puzzle

## 💡 How It Works
1. **AC-3 Algorithm:**  
   Reduces possibilities for each cell by enforcing arc consistency rules.

2. **Backtracking Search:**  
   Fills empty cells by recursively testing valid digits based on Sudoku constraints.

3. **GUI System (Tkinter):**  
   - Displays a 9×9 Sudoku grid.  
   - Buttons for **loading**, **solving**, and **clearing** puzzles.  
   - Reads from `.txt` files containing Sudoku puzzles in a simple 9×9 numeric format.


## Sample Input Files
You can use the provided puzzles or create your own.  
Each `.txt` file must contain **9 lines**, each with **9 numbers (0–9)** separated by spaces:
- `0` represents an empty cell.  
Example:
0 0 4 0 5 0 0 0 0
9 0 0 7 3 4 6 0 0
0 0 3 0 2 1 0 4 9
0 3 5 0 9 0 4 8 0
0 9 0 0 0 0 0 3 0
0 7 6 0 1 0 9 2 0
3 1 0 9 7 0 2 0 0
0 0 9 1 8 2 0 0 3
0 0 0 0 6 0 4 0 0


## How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/aushat/Sudoku-Solver.git
   cd Sudoku-Solver
   
2. Run the main code file:
   ```bash
   python sudoku_solver_gui.py

3. Use the GUI buttons:

- Choose Sudoku File: Load a .txt puzzle (sample files included).

- Solve: Automatically fills the Sudoku using Backtracking + AC-3.

- Clear: Resets the board.

## Concepts Used
- Constraint Satisfaction Problems (CSP)
- Arc Consistency (AC-3 Algorithm)
- Depth-First Backtracking Search
- Graphical User Interface (Tkinter)

