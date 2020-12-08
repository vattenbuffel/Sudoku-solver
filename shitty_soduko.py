import numpy as np
from generate_soduko import generate_soduko

n_num = 9

#print("Input the desired difficulty, Easy, Medium, Hard, Insane")
#level = input()
#board = generate_soduko(level)
board = generate_soduko("Medium")



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
    board_ = board_.reshape(n_num,n_num)
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


def get_num_from_list_of_cells(list_of_cells):
    nums = np.zeros(board.shape, dtype='int')
    for cell in list_of_cells.reshape(-1):
        nums[cell.row, cell.col] = cell.num

    return nums.reshape(-1)


def row_check_incompleteness(row):
    nums = get_num_from_list_of_cells(row)

    changed_something = False
    for cell in row:
        changed_something |= cell.update_possible_num(nums)
    
    return changed_something
    

def col_check_incompleteness(col):
    return row_check_incompleteness(col)


# There should be the number 1-9 in every 3x3 square
def complete_square(square):
    nums = get_num_from_list_of_cells(square)
    
    # If the square is already completed
    if 0 not in nums:
        return False

    changed_something = False
    for cell in square.reshape(-1):
        changed_something |= cell.update_possible_num(nums)
    
    return changed_something


board = cell_board(board)
cells_print(board)

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


    # Update all of the cells
    for cell in board.reshape(-1):
        cell.check_if_only_one_possible_num()

    # If anything was updated then start over if not the soduko is solved
    if not update_something:
        done = True



print("Done:")
cells_print(board)



