# Sudoku
A sudoku solver which applies common algorithms to the greatest extent possible before using brute force

The game state is captured in an 81x9 array - one row for each cell, one column for each available number
By examining the numbers were's sure of using a series of algorithms we can rule out which numbers are not
possible in each cell

When only one number is available for a cell we know that's the right number

The user techniques described on https://www.conceptispuzzles.com/index.aspx?uri=puzzle/sudoku/techniques
are translated into a set of algorithms which

1. Scan locked cells for rows, columns, and squares (scan_cells())
2. Find single candidates (find_last_standing())
3. Scan for pairs of numbers (scan_pairs())

Set comparisons are used to check the values as this seems to be quicker than iterating through the individual numbers
After each iteration of scans the game state is examined and any cells which can have their number locked are (pop_lock_cells())

If 5 iterations pass without any additional cells being locked we apply brute force (solve_me())

If we get a solution we print the completed grid (sudoku_grid())
