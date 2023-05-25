"""
Tic Tac Toe Player
"""
import copy
import random
import math

X = "X"
O = "O"
EMPTY = None
 
moves = {}
     

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_moves = 0
    o_moves = 0

    if terminal(board):
        return 'Game Over'

    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x_moves += 1
            elif board[i][j] == O:
                o_moves += 1
    
    return O if x_moves > o_moves else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    if terminal(board):
        return 'Game Over'

    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                actions.add((i, j))

    return actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    row = action[0]
    col = action[1]

    
    if board[row][col] is not None or row > 2 or col > 2 or terminal(board):
        raise ValueError("The action is not valid or the game has ended")
    
    
    playr = player(board)

    copy_board = copy.deepcopy(board)


    copy_board[row][col] = playr
    
    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    players = [X, O]

    

    for player in players:

        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            return player

        if board[0][2] == player and board[1][1] == player and board[2][0] == player:
            return player

        for i in range(0,3):
            if board[i][0] == player and board[i][1] == player and board[i][2] == player:
                return player
            if board[0][i] == player and board[1][i] == player and board[2][i] == player:
                return player
            
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is None:
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j] == EMPTY:
                    return False
                
    return True
            
    



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_p = winner(board)

    if winner_p == X:
        return 1
    
    elif winner_p == O:
        return -1
    
    else:
        return 0
    

def MaxValue(board):

    v = -3

    if terminal(board):
        return utility(board)
    
    for action in actions(board):

        v = max(MinValue(result(board, action)), v)
    
    return v

def MinValue(board):

    v = 3

    if terminal(board):
        return utility(board)
    
    for action in actions(board):

        v = min(MaxValue(result(board, action)), v)
    return v
    
def minimax(board):

    turn = player(board)

    moves = {}

    if turn == X:
        for action in actions(board):
            v = MinValue(result(board, action))
            moves.update({v : action})

        move = max(moves)
        return moves[move]


    if turn == O:
        for action in actions(board):
            v = MaxValue(result(board, action))
            moves.update({v : action})

        move = min(moves)
        return moves[move]
    
    

