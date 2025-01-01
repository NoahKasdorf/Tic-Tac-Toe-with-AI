
import pygame
import sys

from constants import *


BOARD = [
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY], 
    [EMPTY, EMPTY, EMPTY]
    ]


# checks to see if a move can me made on the board
def isMoveAvailable(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return True
    return False

# checks to see if a player can make a move in that spot
def canMakeMove(row, column):
    if BOARD[row][column] == EMPTY:
        return True 
    return False

def checkWinner(BOARD,PLAYER):
    for i in range(3):
        if BOARD[i][0] == BOARD[i][1] and BOARD[i][1] == BOARD[i][2] and BOARD[i][0] == PLAYER:
            return True
    for i in range(3):
        if BOARD[0][i] == BOARD[1][i] and BOARD[1][i] == BOARD[2][i] and BOARD[0][i] == PLAYER:
            return True
    if BOARD[0][0] == BOARD[1][1] and BOARD[1][1] == BOARD[2][2] and BOARD[0][0] == PLAYER:
        return True
    if BOARD[0][2] == BOARD[1][1] and BOARD[1][1] == BOARD[2][0] and BOARD[0][2] == PLAYER:
        return True
    return False

def printBoard(board):
    for i in range(3):
        for j in range(3):
            print(board[i][j], end=" ")
        print()

def playerMove():
    row = int(input("Enter row: "))
    col = int(input("Enter col: "))
    if(canMakeMove(row, col)):
        BOARD[row][col] = PLAYER
    else:
        print("That move is not available")
        playerMove()


def minimax(board, depth, isMaximizing, alpha, beta):
    if checkWinner(board, PLAYER):
        return -10 + depth
    if checkWinner(board, COMPUTER):
        return 10 - depth
    if not isMoveAvailable(board):
        return 0

    if isMaximizing:
        bestScore = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = COMPUTER
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = EMPTY
                    bestScore = max(bestScore, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return bestScore
    else:
        bestScore = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = EMPTY
                    bestScore = min(bestScore, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return bestScore
    
    
# computer move will use minimax algorithm with alpha beta pruning to make move
def computerMove():
    bestScore = float('-inf')
    move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if BOARD[i][j] == EMPTY:
                BOARD[i][j] = COMPUTER
                score = minimax(BOARD, 0, False, float('-inf'), float('inf'))
                BOARD[i][j] = EMPTY
                if score > bestScore:
                    bestScore = score
                    move = (i, j)
    
    if move != (-1, -1):
        BOARD[move[0]][move[1]] = COMPUTER


def drawBoard(screen, font):
    screen.fill(WHITE)
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (BOARD_SIZE, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_SIZE), LINE_WIDTH)

    for row in range(3):
        for col in range(3):
            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = row * CELL_SIZE + CELL_SIZE // 2
            if BOARD[row][col] == PLAYER:
                text = font.render(PLAYER, True, RED)
                screen.blit(text, text.get_rect(center=(center_x, center_y)))
            elif BOARD[row][col] == COMPUTER:
                text = font.render(COMPUTER, True, BLACK)
                screen.blit(text, text.get_rect(center=(center_x, center_y)))

def playGame():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption("Tic-Tac-Toe")
    
    font = pygame.font.Font(None, 72)
    
    running = True
    player_turn = True
    
    while running:
        drawBoard(screen, font)
        pygame.display.flip()
        
        pygame.time.wait(500)
        
        if checkWinner(BOARD, PLAYER):
            screen.fill(BLACK)
            text = font.render("You win!", True, GREEN)
            screen.blit(text, text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2)))
            pygame.display.flip()
            pygame.time.wait(2000)
            
        elif checkWinner(BOARD, COMPUTER):
            screen.fill(BLACK)
            text = font.render("You Lose!", True, GREEN)
            screen.blit(text, text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2)))
            pygame.display.flip()
            pygame.time.wait(2000)
            
        elif not isMoveAvailable(BOARD):
            screen.fill(BLACK)
            text = font.render("Draw!", True, GREEN)
            screen.blit(text, text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2)))
            pygame.display.flip()
            pygame.time.wait(2000)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if canMakeMove(row, col):
                    BOARD[row][col] = PLAYER
                    player_turn = False
        
        drawBoard(screen, font)
        pygame.display.flip()

        if not player_turn:
            pygame.time.wait(500)
            computerMove()
            player_turn = True
    


playGame()