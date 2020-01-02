'''
Games Rules:

The goal is to assign numbers (from 1 to 9) in the empty cells so that every column, row, and subgrid (3x3) contains exactly one instance of the digits 1 to 9.

Simple board game:

board = [
    . 3 . | 2 8 7 | . 5 .
    5 8 . | 6 4 1 | 9 . .
    1 . 6 | 9 . . | . 2 4
    --------------------- 
    2 . . | . 6 . | 3 . 8
    . 9 5 | . . . | 2 6 .
    8 . 4 | . 3 . | . . 9
    ---------------------
    6 2 . | . . 5 | 4 . 3
    . . 3 | 8 2 6 | . 1 5
    . 5 . | 3 1 4 | . 9 .
 ]

'''

import boardVisual

# find empty spot and assign to l to be returned back to solve_game along with value "true". Meaning "true" there is a 0 value
def find_empty_spots(grid, loc):
    for row in range(9):
        for col in range(9):
            if(grid[row][col] == 0):
                loc[0] = row
                loc[1] = col
                return True
    return False

# print game table
def print_table(grid): 
	for x in range(9): 
		for y in range(9): 
			print(grid[x][y], end=" "),
		print ('') 

# check if the num exists in the row
def exist_in_row(grid, row, num):
    for i in range(9):
        if(grid[row][i] == num):
            return True
    return False

# check if the num exists in the col
def exist_in_col(grid, col, num):
    for i in range(9):
        if(grid[i][col] == num):
            return True
    return False

# check if the num exists in the 3x3 grid
def exist_in_sm_box(grid, row, col, num):
    for i in range(3):
        for x in range(3):
            if(grid[i+row][x+col] == num):
                return True
    return False

# is it safe to input num to row / col
def is_spot_safe(grid, row, col, num):

    # check that num doesn't already exist in same row / col and 3x3 grid. all functions need to return false in order to pass
    return not exist_in_row(grid, row, num) and not exist_in_col(grid, col, num) and not exist_in_sm_box(grid, row - row%3, col - col%3, num)

# the important function
# use backtracking algorithm to try and solve the sudoku
def solve_game(grid):

    # record row and col from find_empty_spots function
    t = [0,0]

    # if no empty spots then we are done
    if (not find_empty_spots(grid, t)):
        return True

    # assign the value to row and col from function above
    row = t[0]
    col = t[1]
    #print(t)
    #print("this is the row: "+ str(row) + " this is the col "+ str(col))

    # look for digits between 1 and 9
    for num in range(1,10):

        # check if number is promising
        if(is_spot_safe(grid, row, col, num)):

            # temporarily assign num
            grid[row][col] = num
            '''# debug
            print("***")
            print(str([row]) + " _ " + str([col]))
            print(num)

            print(grid[row])
            '''
            # recursive. return true is success
            if(solve_game(grid)):
                '''print("***")
                print("true - inside if")
                print(grid[row])
                print("***")
                '''
                return True

            # if fails, unassign and try again
            #print("assigning 0 to: "+ str([row]) + " _ " + str([col]))
            grid[row][col] = 0

    # trigger backtracking
    #print("false - backtracking")
    return False

# if this code is being run directly it will call this main 
if __name__=="__main__":

    # create table for the game
    table = [[0 for x in range(9)] for y in range(9)]

    # add values for the game

    table=[[0,3,0,2,8,7,0,5,0], 
		  [5,8,0,6,4,1,9,0,0], 
		  [1,0,6,9,0,0,0,2,4], 
		  [2,0,0,0,6,0,3,0,8], 
		  [0,9,5,0,7,0,2,6,0], 
		  [8,0,4,0,3,0,0,0,9], 
		  [6,2,0,0,0,5,4,0,3], 
		  [0,0,3,8,2,6,0,1,5], 
		  [0,5,0,3,1,4,0,9,0]]

    if(solve_game(table)):
        print_table(table)
    else:
        print ("Something wrong - No solution found")
