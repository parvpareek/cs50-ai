import tictactoe 

X = "X"
O = "O"
EMPTY = None

board =     [[O, X, X],
            [X, O, EMPTY],
            [O, X, EMPTY]]


print(tictactoe.minimax(board))
