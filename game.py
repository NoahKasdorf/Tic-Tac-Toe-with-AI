

PLAYER = 'X'
COMPUTER = 'O'
EMPTY = ' '

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

def playGame():
    printBoard(BOARD)
    
    print("--------")
    
    while isMoveAvailable(BOARD):
        playerMove()
        printBoard(BOARD)
        
        print("--------")
        
        if checkWinner(BOARD,PLAYER):
            print("You win!")
            return
        
        if not isMoveAvailable(BOARD):
            break
        
        computerMove()
        printBoard(BOARD)

        print("--------")
        if checkWinner(BOARD, COMPUTER):
            print("Computer wins!")
            return
    
    print("It's a draw!")

playGame()