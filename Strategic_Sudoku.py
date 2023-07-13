import numpy as np
import pandas as pd

def initiate_grid():
    my_grid = []
    my_grid.append([0,0,0,4,0,0,0,0,0])
    my_grid.append([5,6,1,0,0,0,0,7,3])
    my_grid.append([0,0,9,0,0,0,0,0,1])
    my_grid.append([8,3,0,0,0,0,6,0,4])
    my_grid.append([0,4,0,0,9,0,8,0,0])
    my_grid.append([0,9,0,2,0,0,0,0,0])
    my_grid.append([0,0,0,6,0,0,0,3,5])
    my_grid.append([0,0,0,5,0,0,0,0,0])
    my_grid.append([0,0,0,0,3,0,9,0,0])
    return my_grid

# work_grid holds our knowledge of the game state, with one row per square on the 9x9 grid
# 0 = row, 1 = col, 2 = sq, 3 = entered value
# 4-12 = available values
# 13 = the most recent occasion this row was updated
# 14 = the order in which this cell was locked
# 15 = the id of numbers available in 4-12 (use this for finding pairs)
# 16 = how many cells have this number id (ie - the same numbers available)
 
labels = ["Row", "Col", "Sq", "Num", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Ord", "Lock", "Avl","Av_ID", "Common"] 
work_grid = np.full((81,18),0)
row_sets = []
col_sets = []
sq_sets = []
for elements in range(9):
    row_sets.append(set())
    col_sets.append(set())
    sq_sets.append(set())
locked_set = set()
order = 0
lock = 1

# Use this id_key to generate an ID which will match where the same numbers are available to a cell

id_key = [1000000000,100000000,10000000,100000,10000,1000,100,10,1]
# Set up the grid

def set_up():
    global work_grid
    global order
    global lock
    global locked_set
    my_grid = initiate_grid()
    for i in range(9):
        for j in range(9):
            work_grid[j+(i*9)][0] = i
            work_grid[j+(i*9)][1] = j
            work_grid[j+(i*9)][2] = ((i//3)*3) + (j//3)
            work_grid[j+(i*9)][3] = my_grid[i][j]
            order +=1   
            work_grid[j+(i*9)][13] = order
            if work_grid[j+(i*9)][3] == 0:
                for k in range(4,13):
                    work_grid[j+(i*9)][k] = k-3
            else:       
                work_grid[j+(i*9)][14] = lock
                if locked_set is None:
                    locked_set={j+(i*9)}
                else:
                    locked_set.add(j+(i*9))
            row_sets[i] |= {j+(i*9)}
            col_sets[j] |= {j+(i*9)}
            sq_sets[((i//3)*3) + (j//3)] |= {j+(i*9)}         

def is_valid_val(row,col,val):
    global work_grid
    valid_str = ""
    bln_valid = True
    if len(row_sets[row] & set(np.argwhere(work_grid[...,3]==val)[...,0]))>0:
        valid_str = valid_str + f"{val} has already been entered in row {row}\n"
        bln_valid = False          
    if len(col_sets[col] & set(np.argwhere(work_grid[...,3]==val)[...,0]))>0:
        valid_str = valid_str + f"{val} has already been entered in col {col}\n"
        bln_valid = False        
    if len(sq_sets[(row//3)*3+col//3] & set(np.argwhere(work_grid[...,3]==val)[...,0]))>0:
        valid_str = valid_str + f"{val} has already been entered in square {(row//3)*3+col//3}"   
        bln_valid = False
    if not bln_valid:
        valid_str = f"You tried to enter {val} in cell {row}, {col} but\n" + valid_str     
    return bln_valid, valid_str

def is_valid_guess(val,row,col):
    global work_grid
    bln_valid = True
    if len(row_sets[row] & set(np.argwhere(work_grid[...,3]==val)[...,0]))>0:
        bln_valid = False          
    if len(col_sets[col] & set(np.argwhere(work_grid[...,3]==val)[...,0]))>0:
        bln_valid = False        
    if len(sq_sets[(row//3)*3+col//3] & set(np.argwhere(work_grid[...,3]==val)[...,0]))>0:
        bln_valid = False
    return bln_valid

def assess_grid():
    global work_grid
    global id_key
    global locked_set
    # Check how many numbers are available in each cell and also create the numbers available ID
    if locked_set is None:
        check_set = set(range(81))
    else:
        check_set = set(range(81)) - locked_set
    for row in check_set:
        cell = work_grid[row]
        cell[15] = np.count_nonzero(cell[4:13:]>0)
        cell[16] = np.sum(cell[4:13:]*id_key)
        # Check how many cells have the same numbers available ID
    for row in check_set:
        cell = work_grid[row]
        cell[17] = np.count_nonzero(work_grid[::,16]==cell[16])
    return set(np.argwhere(work_grid[...,15]==1)[...,0])    
                
# Scan through the cells

def scan_cells():
    global work_grid
    global order
    global lock
    # We only want to do this for the cells that were locked in the last iteration, no need to keep redoing
    check_set = set(np.argwhere(work_grid[...,14]==lock)[...,0])
    for i in check_set:
        cell = work_grid[i]
        row = cell[0]
        col = cell[1]
        sq = cell[2]
        num = cell[3]
        # Iterate through the cells. Remove the locked number from all cells in the same row, column or square
        ################ UPDATE THIS TO USE INTERSECTION OF RELEVANT ROW_SET LES ACTIVE CELL
        target_set = row_sets[row] - locked_set
        for target_indx in target_set: 
            work_grid[target_indx][3+num] = 0
            order += 1
            work_grid[target_indx][13] = order
        target_set = col_sets[col] - locked_set
        for target_indx in target_set: 
            work_grid[target_indx][3+num] = 0
            order += 1
            work_grid[target_indx][13] = order
        target_set = sq_sets[sq] - locked_set
        for target_indx in target_set: 
            work_grid[target_indx][3+num] = 0
            order += 1
            work_grid[target_indx][13] = order


def find_last_standing():
    # This procedure needs to find cells which are the only cell in the row, column or square where one of the available
    # numbers can be placed
    global work_grid
    global order
    for i in range(9):
        for j in range(9):
            num_set = set(np.argwhere(work_grid[...,j+4]==(j+1))[...,0])
            cell_indx = (row_sets[i] & num_set)
            if len(cell_indx) == 1:
                for indx in cell_indx:
                    for k in set(range(9))-{j}:
                        work_grid[indx][k+4]=0
                    order+=1
                    work_grid[indx][13]=order
            cell_indx = (col_sets[i] & num_set)
            if len(cell_indx) == 1:
                for indx in cell_indx:
                    for k in set(range(9))-{j}:
                        work_grid[indx][k+4]=0
                    order+=1
                    work_grid[indx][13]=order
            cell_indx = (sq_sets[i] & num_set)
            if len(cell_indx) == 1:
                for indx in cell_indx:
                    for k in set(range(9))-{j}:
                        work_grid[indx][k+4]=0
                    order+=1
                    work_grid[indx][13]=order
                                        
def scan_pairs():
    global work_grid
    global order
    # First create the set of cell ids which have pairs
    pairs = set(np.argwhere(work_grid[...,17]==2)[...,0])
    for pair in pairs:
        cell = work_grid[pair]
        if len((sq_sets[cell[2]] - locked_set) 
                & set(np.argwhere(work_grid[...,15]==2)[...,0]) 
                & set(np.argwhere(work_grid[...,16]==cell[16])[...,0])) == 2:
            target_set = sq_sets[cell[2]] - locked_set - set(np.argwhere(work_grid[...,16]==cell[16])[...,0])
            for id in target_set:
                order += 1
                work_grid[id][4:13] -= cell[4:13]
                for j in range(4,14):
                    work_grid[id][j] = max(0,work_grid[id][j])
                work_grid[id][13] = order
        if len((row_sets[cell[2]] - locked_set)                
                & set(np.argwhere(work_grid[...,15]==2)[...,0]) 
                & set(np.argwhere(work_grid[...,16]==cell[16])[...,0])) == 2:
            target_set = row_sets[cell[2]] - locked_set - set(np.argwhere(work_grid[...,16]==cell[16])[...,0])
            for id in target_set:
                order += 1
                work_grid[id][4:13] -= cell[4:13]
                for j in range(4,14):
                    work_grid[id][j] = max(0,work_grid[id][j])
                work_grid[id][13] = order
        if len((col_sets[cell[2]] - locked_set) 
                & set(np.argwhere(work_grid[...,15]==2)[...,0]) 
                & set(np.argwhere(work_grid[...,16]==cell[16])[...,0])) == 2:
            target_set = col_sets[cell[2]] - locked_set - set(np.argwhere(work_grid[...,16]==cell[16])[...,0])
            for id in target_set:
                order += 1
                work_grid[id][4:13] -= cell[4:13]
                for j in range(4,14):
                    work_grid[id][j] = max(0,work_grid[id][j])
                work_grid[id][13] = order

                    
# See if we've found any sure things
def pop_lock_cells(certain_cells):
    global lock
    global order
    global work_grid
    global locked_set
    lock += 1
    for i in certain_cells:
        order+=1
        val = np.argwhere(work_grid[i][4:13:]>0)[0][0]+1
        bln_valid, valid_str = is_valid_val(work_grid[i][0],work_grid[i][1],val)
        if not bln_valid:
            print(valid_str)
        work_grid[i][3] = val
        work_grid[i][work_grid[i][3]+3] = 0
        work_grid[i][13] = order
        work_grid[i][14] = lock
        work_grid[i][15]=0
        work_grid[i][16]=0
        if locked_set is None:
            locked_set = {i}
        else:
            locked_set.add(i)


def sudoku_grid():
    global work_grid
    grid_str = " "
    for i in range(9):
        for j in range(9):
            if (j==3) or (j==6):
                grid_str = "".join([grid_str,"  | "])
            grid_str = " ".join([grid_str,str(work_grid[(i*9)+j][3])])
        if (i==2) or (i==5):
            grid_str = "".join([grid_str,"\n "])
            for j in range(9):
                grid_str = "".join([grid_str,"---"])
        grid_str = "".join([grid_str,"\n "])
    print(grid_str) 

def export_df():
    global work_grid
    global labels
    my_df = pd.DataFrame(work_grid)
    my_df.columns = labels
    my_df.to_clipboard(sep=",")

def solve_me():
    if np.count_nonzero(work_grid[...,3]>0)==81:
        return True
    index = np.argwhere(work_grid[...,3]==0)[0][0]
    for num in range(1,10):
        if is_valid_guess(num, work_grid[index][0], work_grid[index][1]):
            work_grid[index][3] = num
            if solve_me():
                return True
            work_grid[index][3] = 0
                         
def main(game_grid, exportit=False):
    global my_grid
    global lock
    global work_grid
    my_grid = game_grid
    set_up()
    null_iterations=0
    if exportit:
        export_df()
    while len(locked_set)<81 and null_iterations<5:
        scan_cells()
        if exportit:
            export_df()
        find_last_standing()
        if exportit:
            export_df()
        scan_pairs()
        certain_cells = assess_grid()
        if exportit:
            export_df()
        if len(certain_cells) > 0:
            null_iterations = 0
            pop_lock_cells(certain_cells)
        else:
            null_iterations += 1
        if exportit:
            export_df()

    if null_iterations==5:
        print("No solution found through strategy")
        if solve_me():
            print("Solution found through brute force")
    else:
        print("Solution found through strategy")
    sudoku_grid()
    return True
    
print(main(initiate_grid))








        




        