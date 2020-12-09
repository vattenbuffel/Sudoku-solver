import numpy as np
from generate_soduko import generate_soduko

n_num = 9

# print("Input the desired difficulty, Easy, Medium, Hard, Insane")
# level = input()
# board = generate_soduko(level)
board = generate_soduko("Medium")

# board = np.array([  [0 ,9 ,0 ,0 ,0 ,0 ,0 ,1 ,0],
#                     [1 ,8 ,0 ,6 ,0 ,0 ,2 ,0 ,0],
#                     [0 ,0 ,0 ,0 ,0 ,0 ,6 ,0 ,0],
#                     [0 ,0 ,1 ,0 ,0 ,0 ,5 ,3 ,8],
#                     [0 ,0 ,2 ,5 ,0 ,0 ,7 ,0 ,0],
#                     [7 ,6 ,0 ,0 ,8 ,1 ,0 ,0 ,0],
#                     [5 ,0 ,0 ,0 ,4 ,0 ,9 ,0 ,6],
#                     [0 ,0 ,0 ,0 ,0 ,9 ,0 ,7 ,0],
#                     [0 ,7 ,0 ,0 ,0 ,0 ,0 ,0 ,3]])



class Cell():
    def __init__(self,row, col, num=None):
        self.row = row
        self.col = col
        self.num = 0
        self.possible_nums = set(np.arange(1,n_num+1))
        self.solved = False

        # If it gets a num at start it's already solved
        if num is not None:
            self.possible_nums = set()
            self.solved = True
            self.num = num


    # Returns true of something changes
    def update_possible_num(self, num):
        original_length = len(self.possible_nums)
        self.possible_nums.difference_update(num)
        return not original_length == len(self.possible_nums)

    def check_if_only_one_possible_num(self):
        if len(self.possible_nums) == 1:
            self.num = list(self.possible_nums)[0]
            self.solved = True

    def __str__(self):
        return "Row: " + str(self.row) + ". Col: " + str(self.col) + ". Num: " + str(self.num) 

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


def cells_print(cells):
    # Handle case where it's only 1 element
    if cells.size == 1:
        print(cells.num)
        return

    # Handle the case where cells is 1D
    row_vector = False
    col_vector = False
    if len(cells.shape) == 1:
        # If it's a row vector:
        if cells[0].row == cells[1].row:
            row_vector = True
        else:
            col_vector = True

    cells_ = np.zeros(cells.shape, dtype='int')
    for cell in cells.reshape(-1):
        if row_vector:
            cells_[cell.col] = cell.num
        elif col_vector:
            cells_[cell.row] = cell.num
        else:
            cells_[cell.row, cell.col] = cell.num
    
    print(cells_)

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
        x,y = cells.shape

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
            row = (i // y)
            col = (i % x)
            nums[row, col] = cell.num
    
    return nums.reshape(-1)


def row_check_incompleteness(row):
    nums = get_num_from_cells(row)

    changed_something = False
    for cell in row:
        changed_something |= cell.update_possible_num(nums)
    
    return changed_something
    

def col_check_incompleteness(col):
    return row_check_incompleteness(col)


# There should be the number 1-9 in every 3x3 square
def complete_square(square):
    nums = get_num_from_cells(square)
    
    # If the square is already completed
    if 0 not in nums:
        return False

    changed_something = False
    for cell in square.reshape(-1):
        changed_something |= cell.update_possible_num(nums)
    
    return changed_something


# This functions shouldn't be necessary. How ever the sudoko generator is a bit buggy it seems.
# I don't know if these can only appears on rows or if the can happen on cols as well. 
# I don't know either if they can only happen with 2 numbers
def unavoidable_squares(board):
    # Extract all cells with 2 possible num
    cell_with_duo_possible_nums = []
    for cell in board.reshape(-1):
        if len(cell.possible_nums) == 2:
            cell_with_duo_possible_nums.append(cell)

    # Group them into groups where they have the same possible_num
    same_possible_num = []
    for cell in cell_with_duo_possible_nums:
        tmp_list = [cell]
        for cell_ in cell_with_duo_possible_nums:
            if cell.possible_nums == cell_.possible_nums:
                tmp_list.append(cell_)
            
            # There must be 4 cells for it to be possible
            if len(tmp_list) == 4:
                same_possible_num.append(tmp_list)
    
    # Make sure the lists in same_possible_num is unique. There will always be 4 duplicates
    same_possible_num_unique = []
    for i in range(len(same_possible_num)):
        if i % 4 == 0:
            same_possible_num_unique.append(same_possible_num[i])

    # Make sure they are actually unavoidable squares, i.e. there are 2 at each row and each column
    unavoidable_squares_list = []
    for list_ in same_possible_num_unique:
        rows = set()
        cols = set()
        for cell in list_:
            rows.add(cell.row)
            cols.add(cell.col)

        correct_rows = len(list(rows)) == 2
        correct_cols = len(list(cols)) == 2
        if correct_cols and correct_rows:
            unavoidable_squares_list.append(list_)


    # If there are any lists in same_possible_num that means the numbers can be input in any way
    update_something = False
    for list_ in unavoidable_squares_list:
        num = list_[0].possible_nums
        num = list(num)[0]

        list_[0].update_possible_num([num])
        update_something = True

    return update_something
    
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
cells_print(board)

def update_and_error_check(board):
    # Update all of the cells
    for cell in board.reshape(-1):
        cell.check_if_only_one_possible_num()

    # Check if the board is a correct one
    correct = check_correctness_of_board(board)
    return correct



done = False
while not done:
    update_something = False

    # Check row incompletness
    for i in range(n_num):
        row = board[i,:]
        update_something |= row_check_incompleteness(row)
    

    # Check col incompletness
    for i in range(n_num):
        col = board[:,i]
        update_something |= col_check_incompleteness(col)
    

    # Check for incomplete squares. This only works when it's the full 9x9 grid
    if n_num == 9:
        for square_i in range(0, n_num):
            row_i = (square_i // 3)*3
            col_i = (square_i % 3)*3
            square = board[row_i:row_i+3, col_i:col_i+3]
            update_something |= complete_square(square)
    

    # If nothing updated with the above that means the normal operators didn't find anything. 
    # Then analyzing techniques will have to be used. These are slower, I think.
    if not update_something:
        # Analyze rows
        for i in range(n_num):
            row = board[i,:]
            update_something |= exclusion_cells_row(row)


        # Analyze cols
        for i in range(n_num):
            col = board[:,i]
            update_something |= exclusion_cells_col(col)


        # Check for incomplete squares. This only works when it's the full 9x9 grid
        last_good_board = np.copy(board)
        if n_num == 9:
            for square_i in range(0, n_num):
                row_i = (square_i // 3)*3
                col_i = (square_i % 3)*3
                square = board[row_i:row_i+3, col_i:col_i+3]
                update_something |= exclusion_cells_square(square)


    # If even the analyzing techniques didn't find anything we need to move on to the ever slower things.
    if not update_something:
        # That this has to be done is actually a bug
        update_something |= unavoidable_squares(board)
       


    # Update all of the cells
    for cell in board.reshape(-1):
        cell.check_if_only_one_possible_num()

    # Check if the board is a correct one
    correct = check_correctness_of_board(board)
    if not correct:
        break

    # If anything was updated then start over if not the soduko is solved
    if not update_something:
        done = True



correct = check_correctness_of_board(board)
if not correct:
    print("Incorrect solution generated")
else:
    print("Done:")
cells_print(board)



