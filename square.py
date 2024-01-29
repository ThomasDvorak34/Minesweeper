COLOR_INDEX = [
    (200, 200, 200),
    (18, 2, 235), 
    (36, 130, 19),
    (240, 39, 39),
    (34, 11, 136),
    (127, 2, 2),
    (71, 157, 165),
    (13, 6, 12),
    (73, 73, 73)
]

class Square:
    def __init__(self, pygame, window, grid, font, rows: int, cols: int, rowPos: int, colPos: int, isMine: bool):
        self.win = window
        self.pygame = pygame
        self.grid = grid
        self.rows = rows - 1 
        self.cols = cols - 1
        self.row = rowPos
        self.col = colPos
        self.font = font
        self.isMine = isMine
        self.isRevealed = False
        self.isFlagged = False
        self.rect = self.pygame.rect.Rect(self.getXYCoordinates(), (25, 25))
    
    def draw(self):
        # counts for hover effects
        if self.rect.collidepoint(self.pygame.mouse.get_pos()) and not self.isRevealed:
            if self.isFlagged:
                self.pygame.draw.rect(self.win, (255, 90, 90), self.rect)
            else:
                self.pygame.draw.rect(self.win, (180, 180, 180), self.rect)
        elif self.isRevealed:
            numMinesAround = self.countSurroundingMines(self.grid)
            mineText = self.font.render(str(numMinesAround), True, COLOR_INDEX[numMinesAround])
            self.win.blit(mineText, (self.getXYCoordinates()[0] + 5, self.getXYCoordinates()[1] + 1))
            if self.isMine:
                self.pygame.draw.rect(self.win, (255, 255, 255), self.rect)
        elif self.isFlagged:
            self.pygame.draw.rect(self.win, (255, 33, 33), self.rect)
        else: 
            self.pygame.draw.rect(self.win, (200, 200, 200), self.rect)

    def getXYCoordinates(self):
        return (self.row * 25, 50 + (self.col * 25))
    
    def updateGrid(self, grid):
        self.grid = grid
    
    def countSurroundingMines(self, grid):
        # covers ALL cases
        surroundingSquares = []
        total = 0
        if self.col == 0 and self.row == 0:
            surroundingSquares = [
                grid[self.row][self.col + 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col + 1]
            ]
        elif self.col == self.cols and self.row == 0:
            surroundingSquares = [
                grid[self.row][self.col - 1],
                grid[self.row + 1][self.col - 1],
                grid[self.row + 1][self.col]
            ]
        elif self.col == 0 and self.row == self.rows:
            surroundingSquares = [
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col + 1],
                grid[self.row][self.col + 1]
            ]
        elif self.col == self.cols and self.row == self.rows:
            surroundingSquares = [
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col - 1],
                grid[self.row][self.col - 1]
            ]
        elif self.col == 0: 
            surroundingSquares = [
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col + 1],
                grid[self.row][self.col + 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col + 1]
            ]
        elif self.col == self.cols:
            surroundingSquares = [
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col - 1],
                grid[self.row][self.col - 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col - 1]
            ]
        elif self.row == 0:
            surroundingSquares = [
                grid[self.row][self.col - 1],
                grid[self.row][self.col + 1],
                grid[self.row + 1][self.col - 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col + 1]
            ]
        elif self.row == self.rows:
            surroundingSquares = [
                grid[self.row][self.col - 1],
                grid[self.row][self.col + 1],
                grid[self.row - 1][self.col - 1],
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col + 1]
            ]
        else:
            surroundingSquares = [
                grid[self.row - 1][self.col - 1],  
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col + 1],
                grid[self.row][self.col - 1],
                grid[self.row][self.col + 1],
                grid[self.row + 1][self.col - 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col + 1]
            ]
        for i in range(0, len(surroundingSquares)):
            if surroundingSquares[i].isMine:
                total += 1
        return total
    
    def getNeighbors(self, grid):
        # it was easier to just copy the others, but return the neighbors
        surroundingSquares = []
        if self.col == 0 and self.row == 0:
            surroundingSquares = [
                grid[self.row][self.col + 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col + 1]
            ]
        elif self.col == self.cols and self.row == 0:
            surroundingSquares = [
                grid[self.row][self.col - 1],
                grid[self.row + 1][self.col - 1],
                grid[self.row + 1][self.col]
            ]
        elif self.col == 0 and self.row == self.rows:
            surroundingSquares = [
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col + 1],
                grid[self.row][self.col + 1]
            ]
        elif self.col == self.cols and self.row == self.rows:
            surroundingSquares = [
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col - 1],
                grid[self.row][self.col - 1]
            ]
        elif self.col == 0: 
            surroundingSquares = [
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col + 1],
                grid[self.row][self.col + 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col + 1]
            ]
        elif self.col == self.cols:
            surroundingSquares = [
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col - 1],
                grid[self.row][self.col - 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col - 1]
            ]
        elif self.row == 0:
            surroundingSquares = [
                grid[self.row][self.col - 1],
                grid[self.row][self.col + 1],
                grid[self.row + 1][self.col - 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col + 1]
            ]
        elif self.row == self.rows:
            surroundingSquares = [
                grid[self.row][self.col - 1],
                grid[self.row][self.col + 1],
                grid[self.row - 1][self.col - 1],
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col + 1]
            ]
        else:
            surroundingSquares = [
                grid[self.row - 1][self.col - 1],  
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col + 1],
                grid[self.row][self.col - 1],
                grid[self.row][self.col + 1],
                grid[self.row + 1][self.col - 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col + 1]
            ]
        return surroundingSquares