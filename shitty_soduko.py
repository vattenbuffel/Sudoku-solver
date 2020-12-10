import numpy as np
from sudoku_generator import generate_sudoko
import itertools

n_num = 9

# print("Input the desired difficulty, easy, medium, hard, extreme")
# level = input()
# board = generate_sudoko(level)
board = np.array([[0, 0, 8, 0, 0, 6, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 7, 0, 0],
[3, 5, 0, 0, 0, 0, 0, 0, 2],
[0, 0, 3, 0, 8, 7, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 0],
[5, 4, 6, 0, 0, 0, 0, 0, 9],
[9, 8, 0, 5, 0, 0, 0, 0, 0],
[1, 0, 0, 7, 0, 0, 6, 0, 5],
[0, 0, 0, 4, 1, 2, 0, 0, 0]])


class Cell():
    def __init__(self,row, col, num=None):
        self.row = row
        self.col = col
        self.num = 0
        self.possible_nums = set(np.arange(1,n_num+1))
        self.solved = False

        # If it gets a num at start it's already solved
        if num is not None:
            self.possible_nums = {num}
            self.solved = True
            self.num = num


    # Returns true of something changes
    def update_possible_num(self, num):
        if self.solved:
            return False

        original_length = len(self.possible_nums)
        self.possible_nums.difference_update(num)
        new_length = len(self.possible_nums)

        if new_length <= 0:
            raise Exception("BALLE")
        return not original_length == new_length

    def check_if_only_one_possible_num(self):
        if len(self.possible_nums) == 1:
            self.num = list(self.possible_nums)[0]
            self.solved = True

    def __str__(self):
        return "Row: " + str(self.row) + ". Col: " + str(self.col) + ". Num: " + str(self.num) + ". Possible nums: " + str(self.possible_nums) 

def cell_board(board):
    board_ = []
    for row_index,row in enumerate(board):
        for col,num_ in enumerate(row):
            num_ = num_ if not num_==0 else None 
            cell = Cell(row_index, col, num = num_)
            board_.append(cell)
    
    board_ = np.array(board_, dtype='object')
    board_ = board_.reshape(board.shape)
    return board_


def get_num_from_cells(cells):
    # Handle case where it's only 1 element
    if cells.size == 1:
        return cells[0].num

    # Handle the case where cells is 1D
    row_vector = False
    col_vector = False
    x = 1
    y = 1
    if len(cells.shape) == 1:
        # If it's a row vector:
        if cells[0].row == cells[1].row:
            row_vector = True
            x = cells.shape[0]
        else:
            col_vector = True
            y = cells.shape[0]
    else:
        y,x = cells.shape

    nums = np.zeros(cells.shape, dtype='int')
    
    for i in range(cells.size):
        cell = cells.reshape(-1)[i]

        if row_vector:
            col = i
            nums[col] = cell.num
        elif col_vector:
            row = i
            nums[row] = cell.num
        else:
            row = (i // x)
            col = (i % x)
            nums[row, col] = cell.num
    
    return nums.reshape(-1)

def cells_print(cells):
    nums = get_num_from_cells(cells)
    nums = nums.reshape(cells.shape)
    
    print(nums)

def board_print(board):
    nums = get_num_from_cells(board)
    n_rows, n_cols = board.shape
    output = ""
    for i in range(nums.size):
        col = (i % n_cols)
        row = i // n_rows

        if col == 0:
            output+="["
        elif col%3 == 0 and not  col == n_cols - 1:
            output+="]["

        output += " " + str(nums[i]) + " "

        if col == n_cols-1:
            output+="]\n"
            if (row+1) %3 == 0 and (not row == 0 and not row == n_rows-1):
                output+="-"*33 + "\n"
        

    print(output)
         
# Remove nums by logic exclusion
def exclusion_cells(cells):
    possible_nums = []

    cells_as_row = cells.reshape(-1)
    for cell in cells_as_row:
        possible_nums.append(cell.possible_nums)
    possible_nums = np.array(possible_nums)

    # Check if multiple sets are the same
    n_copies = np.zeros((cells.size,), dtype='int')
    for i, set_ in enumerate(possible_nums):
        for set__ in possible_nums:
           n_copies[i] += set_==set__ 

    # If there are a possible num set with n elements there needs to be n cells with that possible num sets for anything to be excluded
    good_possible_nums = []
    for i in range(0,cells.size):
        if len(possible_nums[i]) == n_copies[i]:
            good_possible_nums.append(i)
    
    # Remove those possible nums from all cells which don't have exactly them as possible nums
    changed_something = False
    for i in good_possible_nums:
        update_set = possible_nums[i]
        for cell in cells:
            if not cell.possible_nums == update_set:
                changed_something |= cell.update_possible_num(update_set)

    return changed_something

def exclusion_cells_row(row):
    return exclusion_cells(row)
    
def exclusion_cells_col(col):
    return exclusion_cells(col)  

def exclusion_cells_square(square):
    return exclusion_cells(square.reshape(-1))

def print_seed(board):
    output = ""
    for cell in board.reshape(-1):
        if cell.num == 0:
            output += " "
        else:
            output += str(cell.num)
    print(output)

# Solve hidden numbers, https://www.sudoku-solutions.com/index.php?section=solvingHiddenSubsets#hiddenSingle
def find_hidden_num_cells(cells):
    cells = cells.reshape(-1)
    
    # Find n possible nums which are unique to n cells
    cells_with_unique_possible_num = []
    checked_sets = []
    for cell in cells:
        possible_sets = [set(itertools.combinations(cell.possible_nums,i)) for i in range(1,len(list(cell.possible_nums))+1)]

        # Convert the touple in possible_sets to sets
        possible_sets_ = []
        for set_ in possible_sets:
            for set__ in set_:
                if type(set__) == tuple:
                    possible_sets_.append(set(list(set__)))
                else:
                    possible_sets_.append({set__})
        
        possible_sets = possible_sets_
        
        for set_ in possible_sets:
            if not set_ in checked_sets:
                cells_with_sets = []
                checked_sets.append(set_)
                for cell_ in cells:
                    if set_.issubset(cell_.possible_nums):
                        cells_with_sets.append(cell_)
                
                if len(cells_with_sets) == len(list(set_)):
                    cells_with_unique_possible_num.append([set_, cells_with_sets])

    
    # Make sure non of the elements in the unique sets is in any other set
    cells_with_unique_possible_num_ = []
    for list_ in cells_with_unique_possible_num:
        nums = list_[0]
        cells_ = list_[1]
        
        element_possible_in_other_cell = False
        for cell in cells:
            if not cell in cells_:
                if not 0 == len(nums.intersection(cell.possible_nums)):
                    element_possible_in_other_cell = True

        if not element_possible_in_other_cell:
            cells_with_unique_possible_num_.append(list_)

    cells_with_unique_possible_num = cells_with_unique_possible_num_


    # Remove all the non unique possible nums from the cells with unique possible nums
    update_something = False
    for list_ in cells_with_unique_possible_num:
        nums = list_[0]
        cells_ = list_[1]
        for cell in cells_:
            update_set = set([i for i in range(1,n_num+1)]) - nums
            update_something |= cell.update_possible_num(update_set)
    
    return update_something

def find_hidden_num_square(square):
    return find_hidden_num_cells(square)

def find_hidden_num_row(row):
    return find_hidden_num_cells(row)

def find_hidden_num_col(col):
    return find_hidden_num_cells(col)
    
# Find pointing nummbers : https://www.sudoku-solutions.com/index.php?section=solvingInteractions#pointingPair
def pointing_num_cells(board, cells):
    cells = cells.reshape(-1)

    # Find unique 

    # The cells with the unique possible nums have to be on the same row, col or square
    # col_cells = []
    # row_cells = []
    # for list_ in cells_with_unique_possible_num:
    #     nums = list_[0]
    #     cells_ = list_[1]
    #     col = cells_[0].col
    #     row = cells_[0].row
        
    #     if all([cell.col == col for cell in cells_]):
    #         col_cells.append(list_)
    #     elif all([cell.row == row for cell in cells_]):
    #         row_cells.append(list_)

# Handle naked pairs
def naked_pairs_square(board, square):
    possible_nums = []

    cells_as_row = square.reshape(-1)
    for cell in cells_as_row:
        if not cell.possible_nums == set():
            possible_nums.append(cell.possible_nums)
    possible_nums = np.array(possible_nums)

    # Check if multiple sets are the same
    n_copies = np.zeros((square.size,), dtype='int')
    for i, set_ in enumerate(possible_nums):
        for set__ in possible_nums:
           n_copies[i] += set_==set__ 

    # If there are a possible num set with n elements there needs to be n cells with that possible num sets for anything to be excluded
    good_possible_nums = []
    for i in range(0,possible_nums.size):
        if len(possible_nums[i]) == n_copies[i]:
            good_possible_nums.append(possible_nums[i])
    
    # Only if the matching pairs are on the same row or col can they be used. Extract those who are
    row_pairs = []
    col_pairs = []
    pairs = []
    for possible_nums_ in good_possible_nums:
        tmp_list = []
        for cell in cells_as_row:
            if cell.possible_nums == possible_nums_:
               tmp_list.append(cell)
        
        pairs.append(tmp_list)
    
    for pair in pairs:
        row = pair[0].row
        col = pair[0].col 
        
        row_pair = True
        col_pair = True
        for cell in pair:
            if not cell.row == row:
                row_pair = False
            if not cell.col == col:
                col_pair = False
        
        if row_pair:
            row_pairs.append(pair)
        elif col_pair:
            col_pairs.append(pair)
    
    # The other cells in the row/col are blocked because of these row/col pairs
    changed_something = False
    for pair in row_pairs:
        update_set = pair[0].possible_nums
        row = board[pair[0].row, :]
        for cell in row:
            if not cell.possible_nums == update_set:
                changed_something |= cell.update_possible_num(update_set)
    
    for pair in col_pairs:
        update_set = pair[0].possible_nums
        col = board[:,pair[0].col]
        for cell in col:
            if not cell.possible_nums == update_set:
                changed_something |= cell.update_possible_num(update_set)

    return changed_something
    
# Check if any duplicates in cells
def check_correctness_cells(cells):
    cell_num = get_num_from_cells(cells)
    cell_num = list(cell_num)

    # Remove 0 from cell_num
    while 0 in cell_num:
        cell_num.remove(0)

    # Check for duplicates
    return len(cell_num) == len(set(cell_num)) 

def check_correctness_square(square):
    return check_correctness_cells(square.reshape(-1))
    
def check_correctness_row(row):
    return check_correctness_cells(row)
    
def check_correctness_col(col):
    return check_correctness_cells(col)

def check_correctness_of_board(board):
    # Check the corectness
    correct = True
    for i in range(n_num):
        row = board[i,:]
        correct &= check_correctness_row(row)

    for i in range(n_num):
        col = board[:,i]
        correct &= check_correctness_col(col)

    if n_num == 9:
        for square_i in range(0, n_num):
            row_i = (square_i // 3)*3
            col_i = (square_i % 3)*3
            square = board[row_i:row_i+3, col_i:col_i+3]
            correct &= check_correctness_square(square)
    
    return correct

board = cell_board(board)
board_print(board)


done = False
while not done:
    update_something = False

    # Analyze rows
    for i in range(n_num):
        row = board[i,:]
        update_something |= exclusion_cells_row(row)
        # update_something |= naked_pairs_square(board, row)
        update_something |= find_hidden_num_row(row)


    # Analyze cols
    for i in range(n_num):
        col = board[:,i]
        update_something |= exclusion_cells_col(col)
        # update_something |= naked_pairs_square(board, col)
        update_something |= find_hidden_num_col(col)


    # Analyze squares
    if n_num == 9:
        for square_i in range(0, n_num):
            row_i = (square_i // 3)*3
            col_i = (square_i % 3)*3
            square = board[row_i:row_i+3, col_i:col_i+3]
            update_something |= exclusion_cells_square(square)
            update_something |= find_hidden_num_square(square)
            # update_something |= naked_pairs_square(board, square) # Can this be removed, maybe. It seems like a very powerful tool but maybe it's already included in the other stuff. I'm not entierly sure
       

    # Update all of the cells
    for cell in board.reshape(-1):
        cell.check_if_only_one_possible_num()

    # If anything was updated then start over if not the soduko is solved
    if not update_something:
        done = True

for square_i in range(0, n_num):
    row_i = (square_i // 3)*3
    col_i = (square_i % 3)*3
    square = board[row_i:row_i+3, col_i:col_i+3]
    update_something |= exclusion_cells_square(square)

correct = check_correctness_of_board(board)
if not correct:
    print("Incorrect solution generated")
else:
    print("Done:")



# REMOVE THIS
col = board[:,0]
balle = pointing_num_cells(board, col)

###############


board_print(board)



