import z3
import numpy as np


m=z3.Solver()


#For a 9x9 sodk
n=9
board = np.array(  [[6, 0, 3, 0, 0, 0, 0, 7, 0],
                    [7, 2, 0, 0, 0, 0, 3, 0, 0],
                    [5, 0, 0, 0, 3, 7, 1, 0, 9],
                    [0, 0, 0, 5, 0, 2, 6, 3, 0],
                    [0, 1, 0, 0, 7, 6, 0, 9, 0],
                    [0, 3, 0, 0, 4, 0, 0, 2, 7],
                    [8, 4, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 4, 0, 0, 0, 0, 0],
                    [0, 0, 0, 9, 2, 0, 8, 4, 3]])



#Create decision vars

xy=[[z3.Int(f'Pos{j}_{i}') for i in range(n)] for j in range(n)]

xy=np.array(xy)


#add constraints

#numbers must be >=1
for i in range(n):
    for j in range(n):
        m.add(xy[i][j] >= 1)

#Numbers must be <=9
for i in range(n):
    for j in range(n):
        m.add(xy[i][j] <= 9)


#Each row must have unique numbers / distinct 

for row in range(n):
    #xy[row] returns array in row row
    #convert to list coz z3 syntax
    m.add(z3.Distinct(list(xy[row])))
        
#Each colulm must have unique numbers /distinct

for col in range(n):
    m.add(z3.Distinct(list(xy[col])))


#Each 3x3 submatrix must have unique numbers
#convert to list coz z3 syntax, [0] at the end coz reshape func
#print(list(xy[:3,:3].reshape(1,n)[0])) gives
#[Pos0_0, Pos0_1, Pos0_2, Pos1_0, Pos1_1, Pos1_2, Pos2_0, Pos2_1, Pos2_2]


for i in range(0,n,3):
    for j in range(0,n,3):
        m.add(z3.Distinct(list(xy[i:i+3,j:j+3].reshape(1,n)[0]))) 

#Decision vars must be equal to given init soduku
for i in range(n):
    for j in range(n):

        #0 means empty pos
        if board[i][j] != 0:
            m.add(xy[i][j] == int(board[i][j]))



print(f"Model is : {m.check()}")

sol=m.model()
#print(sol)
#todo, readable print
sol_readable=np.zeros([n,n],dtype=int)
for row in range(n):
    for col in range(n):
        sol_readable[row][col]=str(sol.evaluate(xy[row][col]))


print(sol_readable)