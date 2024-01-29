import pygame, sys, time, random, math
from square import *

pygame.init()
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
FONT = pygame.font.Font(None, 60)
SMALL_FONT = pygame.font.Font(None, 48)
MINE_FONT = pygame.font.Font(None, 36)

def drawMainMenu():
    title = FONT.render("Minesweeper", True, (150, 150, 150))
    WIN.blit(title, (170, 230))
    toPlayText = FONT.render("Press ENTER to play", True, (150, 150, 150))
    WIN.blit(toPlayText, (100, 290))

def drawGridOutline(rows: int, cols: int):
    for i in range(0, rows):
        for j in range(0, cols):
            pygame.draw.rect(WIN, (55, 55, 55), (i * 25, topBarHeight + (j * 25), 25, 25), 1)

def drawGameOverScreen():
    gameover = SMALL_FONT.render("GAME OVER!", True, (255, 0, 0))
    WIN.blit(gameover, (200, 200))

def format(num: int, length: int):
    """Length is how many places you want the string to return. For example, length = 3 with time 9 returns 009."""
    numStr = str(num)
    newStr = ""
    for _ in range(0,  length - len(numStr)):
        newStr += "0"
    return newStr + numStr

def generateGrid(rows: int, cols: int, mines: int):
    global grid
    # need to make a way to ensure that all 100 mines are used
    numMines = mines
    for i in range(0, rows):
        row = []
        for j in range(0, cols):
            row.append(Square(pygame, WIN, grid, MINE_FONT, rows, cols,  i, j, False))
        grid.append(row)
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            grid[i][j].updateGrid(grid)
    while numMines >= 0:
        randomPos = [random.randint(0, rows - 1), random.randint(0, cols - 1)]
        grid[randomPos[0]][randomPos[1]].isMine = True
        numMines -= 1
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            grid[i][j].updateGrid(grid)
            
def revealSquare(target: Square, grid):
    global isAlive
    if target.isRevealed or target.isFlagged:
        return
    target.isRevealed = True
    if target.isMine:
        isAlive = False
    if target.countSurroundingMines(grid) == 0:
        for i in range(0, len(target.getNeighbors(grid))):
            revealSquare(target.getNeighbors(grid)[i], grid)

def convertMouseToSquarePos():
    coors = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
    return [math.floor(coors[0] / 25), math.floor(coors[1] / 25) - 2]

topBarHeight = 50
rows = 25
cols = 27
mines = 112 # about 1/6 of the 25x27 grid
flags = mines
state = 'main'
isMining = True
isAlive = True
grid = []
startTime = 0

def main():
    global state, isAlive, rows, cols, grid, startTime, mines, isMining, flags
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        WIN.fill((217, 217, 217))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if state == 'main' and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = 'play'
                    generateGrid(rows, cols, mines)
                    startTime = time.time()
            if state == 'play' and event.type == pygame.MOUSEBUTTONDOWN and not isMining:
                grid[convertMouseToSquarePos()[0]][convertMouseToSquarePos()[1]].isFlagged = not grid[convertMouseToSquarePos()[0]][convertMouseToSquarePos()[1]].isFlagged
                if grid[convertMouseToSquarePos()[0]][convertMouseToSquarePos()[1]].isFlagged:
                    flags -= 1
                else: 
                    flags += 1
            if state == 'play' and event.type == pygame.MOUSEBUTTONDOWN and isMining:
                revealSquare(grid[convertMouseToSquarePos()[0]][convertMouseToSquarePos()[1]], grid)
            if state == 'play' and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    isMining = not isMining
        if state == 'main':
            drawMainMenu()
        if state == 'play':
            if isAlive == False:
                state = 'game over'
            currentTime = time.time()
            timeDifference = int(currentTime - startTime)
            timeText = SMALL_FONT.render(format(timeDifference, 3), True, (255, 44, 44))
            if isMining:
                text = 'Mine'
            else:
                text = 'Flag'
            sweepModeText = SMALL_FONT.render(f'Mode: {text}', True, (255, 44, 44))
            flagsLeft = SMALL_FONT.render(format(flags, 3), True, (255, 44, 44))
            WIN.blit(sweepModeText, (20, 5))
            WIN.blit(flagsLeft, (410, 5))
            WIN.blit(timeText, (280, 5))
            for i in range(0, len(grid)):
                for j in range(0, len(grid[i])):
                    grid[i][j].updateGrid(grid)
                    grid[i][j].draw()
            drawGridOutline(rows, cols)
        if state == 'game over':
            drawGameOverScreen()
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()