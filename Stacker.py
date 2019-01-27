#coded by Benjamin Hatch in 2018, High School Senior @ Granada
import pygame as pg

window = pg.display.set_mode((210,450))
timer = pg.time.Clock()
pg.init()

#colors
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
colorList = [RED, GREEN, BLUE]

#global vars
heading = 1
run = True
shiftTimer = 0
shiftSpeed = 300

#block class
class Block:
    def __init__(self,row,col,char):
        self.row = row
        self.col = col
        self.char = char

    def placeBlock(self):
        grid[self.row][self.col] = self.char

    def increaseRow(self,num):
        global run
        if self.row != 0:
            self.row = self.row + num
        else:
            run = False

    def increaseCol(self,num):
        self.col = self.col + num

    def checkBelow(self):
        if self.row >= len(grid) - 1:
            return True
        elif grid[self.row+1][self.col] == self.char:
            return True
        return False

#important functions
def fillGrid(rows,cols):
    array = []
    for r in range(rows):
        array.append([])
        for c in range(cols):
            array[r].append("_")
    return array

def refreshPart():
    for i in range(len(blockList)):
        blockList[i].placeBlock()

def placeAtNewRow():
    global blockList
    for block in blockList:
        block.increaseRow(-1)

def newMoving():
    global blockList
    newParts = []
    for i in range(len(blockList)):
        if blockList[i].checkBelow():
            newParts.append(blockList[i])
        else:
            grid[blockList[i].row][blockList[i].col] = "_"
    blockList = newParts
    placeAtNewRow()

def shiftPart():
    global run
    global heading
    if len(blockList) == 0:
        run = False
    else:
        row = blockList[0].row
        for i in range(len(grid[row])):
            grid[row][i] = "_"
        if blockList[len(blockList) - 1].col == len(grid[0]) - 1:
            heading = -1
        elif blockList[0].col == 0:
            heading = 1
        for block in blockList:
            block.increaseCol(heading)


def printGrid():
    for r in grid:
        for c in r:
            print(c, end = "")
        print()

def findSymbols(character):
    output = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == character:
                output.append(r)
                output.append(c)
    return output

def getColor(row):
    if len(blockList) == 0:
        return BLACK
    if row % 5 == 0:
        return YELLOW
    elif row > 10:
        return colorList[0]
    elif row > 5:
        return colorList[1]
    else:
        return colorList[2]

def displayPieces():
    #800 by 600
    coords = findSymbols("O")
    #print(coords)
    window.fill(BLACK)
    for i in range(len(coords)):
        if i % 2 == 0:
            pg.draw.rect(window, getColor(coords[i]), (coords[i + 1] * 30, coords[i] * 30, 28, 28))
    pg.display.update()

#other important vars  
grid = fillGrid(15,7)
blockList = [Block(14,0,"O"), Block(14,0,"O"), Block(14,1,"O"), Block(14,2,"O")]

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                newMoving()
                shiftSpeed -= 20
                #print(shiftSpeed)
    timer.tick()
    shiftTimer += timer.get_rawtime()
    if shiftTimer > shiftSpeed:
        shiftPart()
        shiftTimer = 0
    refreshPart()
    displayPieces()
    #printGrid()
    pg.display.update()

