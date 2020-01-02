import pygame

pygame.font.init()

'''
table = [[0 for x in range(9)] for y in range(9)]

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
''' 
# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
lightgrey = (200,200,200)
green = (22, 165, 137)
red = (255, 0, 0)

# define window size 
width = 540
height = 540

class getTable:

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

    def __init__(self, row, col, width, height):
        # assign default param
        self.rows = row
        self.cols = col
        self.width = width
        self.height = height
        self.selected = None
        self.cubes = [[Cube(self.table[i][j], i, j, width, height) for j in range(col)] for i in range(row)]
        

    def click(self, pos):
        # make sure the click is within the game window
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            # debug what are the coordinates
            #print("getTable : " + str(int(x)) + " , " + str(int(y)))
            # return (row, col)
            return (int(y), int(x))
        else:
            return None

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

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
            pygame.draw.rect(window, red, (x, y, gap, gap), 3)

def redraw_game(win, board):
    win.fill(white)
    # draw grid
    board.draw(win)

# main function where the magic happens
def main():
    window = pygame.display.set_mode((width, height))
    board = getTable(9, 9, width, height)

    pygame.display.set_caption("Sudoku Solver")

    keepRunning = True

    while keepRunning:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepRunning = False

            # get mouse button action
            if event.type == pygame.MOUSEBUTTONDOWN:
                # get mouse position
                pos = pygame.mouse.get_pos()
                #print("pos inside main : "+str(pos))
                clickPos = board.click(pos)

                if clickPos:
                    board.select(clickPos[0], clickPos[1])

        '''if getTable.selected:
            # draw table with cube selected
            getTable.sketch()
        '''

        redraw_game(window, board)
        pygame.display.update()

# call the game
main()
pygame.quit()