import numpy as np
from generate_soduko import generate_soduko

n_num = 9

print("Input the desired difficulty, Easy, Medium, Hard, Insane")
level = input()
board = generate_soduko(level)
print(board)


def row_check_incompleteness(row, board):
    zero_counter = 0
    zero_index = -1
    num_found = []

    for index, num  in enumerate(row):
        if num == 0:
            zero_counter += 1
            zero_index = index
        else:
            num_found.append(num)

    if not zero_counter == 1:
        return False

    
    for num in range(1,n_num+1):
        if num in num_found:
            continue
        row[zero_index] = num
        return True

def col_check_incompleteness(col, board):
    board_transpose = np.transpose(board)
    row = np.transpose(col)
    return row_check_incompleteness(row, board_transpose)

def row_blocked(row, board):
    zero_index = []
    num_found = []

    # Where is it empty
    for index, num in enumerate(row):
        if num == 0:
            zero_index.append(index)
        else:
            num_found.append(num)

    # Which values are possible to enter
    possible_num = []
    for num in range(1,n_num+1):
        if num not in num_found:
            possible_num.append(num)

    update_something = False
    # Loop over all the empty cells and check if the col allows the entrance of the possible_num while the other cols don't
    for i in zero_index:
        col = board[:,i]
        
        for num in possible_num:
            # Is the num in this col
            if num not in col:
                # Is the num in all the other cols with 0 index
                all_other_cols = zero_index.copy()
                all_other_cols.remove(i)
                num_in_all_other_cols = np.sum(board[:,all_other_cols]==num,axis=0)
                num_in_all_other_cols = all(num_in_all_other_cols)
                if num_in_all_other_cols:
                    row[i] = num
                    update_something = True
    
    return update_something


def col_blocked(col, board):
    row = np.transpose(col)
    board_transpose = np.transpose(board)
    return row_blocked(row, board_transpose)


# There should be the number 1-9 in every 3x3 square
def complete_square(square):
    # If the square is already completed
    if 0 not in square:
        return False

    num_not_in_square = 0

    for num in range(1, n_num+1):
        if num not in square:
            if not (num_not_in_square == 0):
                return False

            num_not_in_square = num

    empty_index = np.where(square == 0)
    square[empty_index] = num_not_in_square   
    return True 






done = False
while not done:
    update_something = False
    # Check row incompletness
    for row_i in range(n_num):
        row = board[row_i,:]
        update_something |= row_check_incompleteness(row, board)
        
    # Check col incompletness 
    for col_i in range(n_num):
        col = board[:,col_i]
        update_something |= col_check_incompleteness(col, board)

    # Check if there are any cells in which values can be added because the rest of the row is blocked for 
    for row_i in range(n_num):
        row = board[row_i,:]
        update_something |= row_blocked(row, board)

    # Check if there are any cells in which values can be added because the rest of the row is blocked for 
    for col_i in range(n_num):
        col = board[:,col_i]
        update_something |= col_blocked(col, board)

    # Check for incomplete squares. This only works when it's the full 9x9 grid
    if n_num == 9:
        for square_i in range(0, n_num):
            row_i = (square_i // 3)*3
            col_i = (square_i % 3)*3
            square = board[row_i:row_i+3, col_i:col_i+3]
            update_something |= complete_square(square)


    # If anything was updated then start over if not the soduko is solved
    if update_something:
        done = False
    else:
        done = True



print("Done:")
print(board)



