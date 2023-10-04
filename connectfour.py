import numpy as np
import itertools
import pygame
import sys
import math
from variables import ROW_COUNT, COLUMN_COUNT, SQUARESIZE, size, RADIUS, colors, height, width

def createBoard():
    return np.zeros((ROW_COUNT,COLUMN_COUNT))

board = createBoard()
gameOver = False
turn = 0

# Checking if the top row of a selected column is empty or not
def isValidLocation(board, col):
    return board[ROW_COUNT-1][col] == 0

# Getting the lowest empty slot of the selected column
def getNextOpenRow(board, col):
    for slot in range(ROW_COUNT):
        if board[slot][col] == 0:
            return slot

# Dropping the piece in the board
def dropPiece(board, row, col, piece):
    board[row][col] = piece

# Flipping the board before printing it because numpy starts 0,0 index from top left instaed of bottom left
def printBoard(board):
    print(np.flip(board, 0))

# Checking if the game is over
def gameOverCheck(board, piece):
    
    # Checking horizontal win
    for c, r in itertools.product(range(COLUMN_COUNT - 3), range(ROW_COUNT)):
        if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
            return True

    # Checking vertical win
    for c, r in itertools.product(range(COLUMN_COUNT), range(ROW_COUNT - 3)):
        if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
            return True

    # Checking positive slop diagonal win
    for c, r in itertools.product(range(COLUMN_COUNT - 3), range(ROW_COUNT - 3)):
        if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
            return True
        
    # Checking negative slop diagonal win
    for c, r in itertools.product(range(COLUMN_COUNT - 3), range(3, ROW_COUNT)):
        if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
            return True

# Drawing board graphics
def drawBoard(board):

    for c, r in itertools.product(range(COLUMN_COUNT), range(ROW_COUNT)):
        pygame.draw.rect(screen, colors["BLUE"], (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
        pygame.draw.circle(screen, colors["BLACK"], (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
        
    for c, r in itertools.product(range(COLUMN_COUNT), range(ROW_COUNT)):
        if board[r][c] == 1:
            pygame.draw.circle(screen, colors["RED"], (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
        elif board[r][c] == 2: 
            pygame.draw.circle(screen, colors["YELLOW"], (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()

printBoard(board)

# Initialising the game
pygame.init()

# Setting screen size
screen = pygame.display.set_mode(size)

# Drawing board
drawBoard(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 80)

# Game loop
while not gameOver:

    # Getting the events
    for event in pygame.event.get():

        # Checking if the game has been quit
        if event.type == pygame.QUIT:
            sys.exit()

        # Checking mouse hover event
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, colors["BLACK"], (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, colors["RED"], (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, colors["YELLOW"], (posx, int(SQUARESIZE/2)), RADIUS)
        
        pygame.display.update()

        # Checking mouse click event
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, colors["BLACK"], (0, 0, width, SQUARESIZE))
            posx = event.pos[0]

            # Ask for player 1 input
            if turn == 0:
                col = int(math.floor(posx/SQUARESIZE))

                if isValidLocation(board, col):
                    row = getNextOpenRow(board, col)
                    dropPiece(board, row, col, 1)

                    if gameOverCheck(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, colors["RED"])
                        screen.blit(label, (40, 10))
                        gameOver = True

            # Ask for player 2 input
            else:
                col = int(math.floor(posx/SQUARESIZE))

                if isValidLocation(board, col):
                    row = getNextOpenRow(board, col)
                    dropPiece(board, row, col, 2)

                    if gameOverCheck(board, 2):
                        label = myfont.render("Player 1 wins!!", 1, colors["YELLOW"])
                        screen.blit(label, (40, 10))
                        gameOver = True

            printBoard(board)
            drawBoard(board)

            # Switching turns between players
            turn += 1
            turn %= 2

            # Wait after game is over 
            if gameOver:
                pygame.time.wait(3000)











