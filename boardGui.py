import pygame

pygame.font.init()

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
lightgrey = (200,200,200)
green = (22, 165, 137)
red = (255, 0, 0)

table = [
    [0,3,0,2,8,7,0,5,0], 
    [5,8,0,6,4,1,9,0,0], 
    [1,0,6,9,0,0,0,2,4], 
    [2,0,0,0,6,0,3,0,8], 
    [0,9,5,0,7,0,2,6,0], 
    [8,0,4,0,3,0,0,0,9], 
    [6,2,0,0,0,5,4,0,3], 
    [0,0,3,8,2,6,0,1,5], 
    [0,5,0,3,1,4,0,9,0]
]

# find empty spot and assign to l to be returned back to solve_game along with value "true". Meaning "true" there is a 0 value
def find_empty_spots(grid):
    for row in range(9):
        for col in range(9):
            if(grid[row][col] == 0):
                #loc[0] = row
                #loc[1] = col
                return (row, col)
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

    find = find_empty_spots(grid)
    # if no empty spots then we are done
    if (not find):
        return True
    else:
        # get the position when you find a 0
        row, col = find

    # look for digits between 1 and 9
    for num in range(1,10):
        # check if number is promising
        if(is_spot_safe(grid, row, col, num)):

            # temporarily assign num
            grid[row][col] = num
            #print(grid[row][col])

            # recursive. return true is success
            if(solve_game(grid)):
                return True

            grid[row][col] = 0

    return False


class getTable:

    def __init__(self, row, col, width, height, table):
        # assign default param
        self.rows = row
        self.cols = col
        self.width = width
        self.height = height
        self.selected = None
        self.emptySlots = [[]]
        self.table = table
        self.cubes = [[Cube(self.table[i][j], i, j, width, height) for j in range(col)] for i in range(row)]

    def draw(self, window):
        # draw the grid
        gaps = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                lineThick = 4
            else:
                lineThick = 1
            
            # draw horizontal and vertical lines
            pygame.draw.line(window, black, (0, i*gaps), (self.width, i*gaps), lineThick)
            pygame.draw.line(window, black, (i*gaps, 0), (i*gaps, self.height), lineThick)

        # draw cubes
        for i in range(self.rows):
            for j in range(self.cols):
                # call draw from cube class
                self.cubes[i][j].draw(window)


    def select(self, row, col):

        #print("inside select func"+ str(row) + " "+ str(col))
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    # used to create green squares around each empty slot
    def find_emptySlots(self, grid):
        for i in range(self.rows):
            for j in range(self.cols):
                if (grid[i][j] == 0):
                    print("empty slot "+ str([i]) + " _ " + str([j]))
                    print(" ")
                    self.select(i, j)
                    self.emptySlots += [[i,j]]
        


class Cube:
    cols = 9
    rows = 9

    def __init__(self, value, row, col, width, height):
        # assign default param
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.temp = 0

    def draw(self, window):
        font = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            # creates a new object which you can call the render object
            text = font.render(str(self.temp), 1, lightgrey)
            # blit the text onto your main screen
            window.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = font.render(str(self.value), 1, black)
            window.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(window, green, (x, y, gap, gap), 3)

def redraw_game(win, board):
    win.fill(white)
    # draw grid
    board.draw(win)


######## main function where the magic happens ########
def main():

    # define window size 
    width = 540
    height = 540
    
    window = pygame.display.set_mode((width, height))

    pygame.display.set_caption("Sudoku Solver")

    keepRunning = True

    if (solve_game(table)):
        #print(table)
        board = getTable(9, 9, width, height, table)
    else:
        print("something went wrong")


    while keepRunning:
        # allow user to close window to exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepRunning = False


        redraw_game(window, board)
        pygame.display.update()
    

main()
pygame.quit()
