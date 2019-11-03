import random
import copy
import sys

board_oc = [[0 for x in range(8)] for y in range(8)]
"""board_oc = [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 2, 1, 0, 0],
            [0, 0, 0, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]"""
dir = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
turn = 1
end = 0
p1 = 4
p2 = 4
mode = 0

def print_board(board):
    for x in range(8):
        for y in range(8):
            print(board[x][y], end=" ")
        print()

def init_board():
    board_oc[3][3] = board_oc[4][4] = 1
    board_oc[3][4] = board_oc[4][3] = 2

def set_turn():
    turn = random.randint(1, 2)

def is_on_board(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8

def is_corner(x, y):
    return [x, y] in [[0, 0], [0, 7], [7, 0], [7, 7]]

def tile_is_available(board, x , y, x_dir, y_dir):
    flipped_tiles = []
    other = 3 - turn
    dx = x
    dy = y
    
    dx += x_dir
    dy += y_dir
    
    if(is_on_board(dx,dy) == False):
        return []
    if(board[dx][dy] == 0):
        return []
    
    while(board[dx][dy] == other):
        flipped_tiles.append([dx,dy])
        dx += x_dir
        dy += y_dir
        if(is_on_board(dx,dy) == False):
            return []
    
    if(board[dx][dy] == turn):
        return []
    
    if(board[dx][dy] == 0):
        print([dx, dy, flipped_tiles], "tile_is_available()")
        return [dx, dy, flipped_tiles]
    
    return []

def from_one_piece(board, x, y):
    valid_tiles = []
    
    for dir_x, dir_y in dir: #find in all 8 directions
        tile = tile_is_available(board, x, y, dir_x, dir_y)
        
        if(len(tile)>0):
            print(tile, "from_one_piece() tile")
            valid_tiles.append(tile)

            print(valid_tiles, "from_one_piece() valid_tiles")
    
    return valid_tiles

def available_tiles(board):
    valid_tiles = []

    for x in range(8):
        for y in range(8):
            if(board[x][y] == turn): #find in all 8 directions from the existing tiles
                one_piece = from_one_piece(board, x, y) 

                if(len(one_piece)>0):
                    print(one_piece, "available_tiles() one_piece")

                    for case in valid_tiles:
                        for piece in one_piece:
                            print(case, "This is a case", case[0:2], piece[0:2])

                            if case[0:2] == piece[0:2]:
                                case[2].extend(lst for lst in piece[2] if lst not in case[2])
                                break
                        else:
                            continue
                        break
                    else:
                        valid_tiles = valid_tiles + one_piece

                    print(valid_tiles, "available_tiles() valid_tiles")
    
    return valid_tiles

def make_move(board, piece):
    print(piece, "make_move()")

    x = piece[0]
    y = piece[1]
    flip = piece[2]

    board[x][y] = turn
    for i, j in flip:
        board[i][j] = turn
      
    print_board(board)
    print("Move made")

min_eval_board = -1
max_eval_board = 101 #(8 + 2)^2 + 1

def eval_board(board):
    total = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == turn:
                if is_corner(x, y):
                    total += 4 # corner
                elif (x in [0, 7]) or (y in [0, 7]):
                    total += 2 # side
                else:
                    total += 1
    print(total, "eval_board()")
    return total

def Minimax(board, depth, maximizing_player):
    valid_tiles = available_tiles(board)
    print(valid_tiles, "Minimax() valid_tiles")
    best_value = 0

    if depth == 0 or len(valid_tiles) == 0:
        return eval_board(board)

    if maximizing_player:
        best_value = min_eval_board

        for piece in valid_tiles:
            board_temp = copy.deepcopy(board)

            make_move(board_temp, piece) 
            val = Minimax(board_temp, depth - 1, False)
            print(val, "Minimax() val maximize_player")

            if val > best_value:
                best_value = val
            print(best_value, "Minimax() best_value maximize_player")
    else: # minimizingPlayer
        best_value = max_eval_board

        for piece in valid_tiles:
            board_temp = copy.deepcopy(board)

            make_move(board_temp, piece) 
            val = Minimax(board_temp, depth - 1, True)
            print(val, "Minimax() val minimize_player")
            
            if val < best_value:
                best_value = val
            print(best_value, "Minimax() best_value minimize_player", depth)
    
    print(best_value, "Minimax()", depth)
    return best_value

def best_move(board, depth):
    maxPoints = 0
    valid_tiles = available_tiles(board)
    print(valid_tiles, "best_move() valid_tiles")
    best_move = []

    for move in valid_tiles:
        board_temp = copy.deepcopy(board)
        make_move(board_temp, move) 

        points = Minimax(board_temp, depth, True)
                
        if points > maxPoints:
            maxPoints = points
            best_move = move

    print(best_move, "best_move()")
    return best_move

def random_move(board):
    valid_tiles = available_tiles(board)
    print(valid_tiles, "random_move()")

    move = valid_tiles[random.randint(0, len(valid_tiles) - 1)]
    print(move, "random_move()")
    return move

def score(board):
    scores = [0 , 0]

    for x in range(8):
        for y in range(8):
            if board[x][y] != 0:
                scores[board[x][y] - 1] += 1 

    print("Player 1: ", scores[0], " Player 2: ", scores[1])
    return scores

def switch_player(board):
    global turn, end 
    turn = 3 - turn
    
    if turn == 1:
        mode = p1
    else:
        mode = p2

    scores = score(board)
    valid_tiles = available_tiles(board)

    if end == 2:
        print("No more possible moves")

        if scores[0] == scores[1]:
            print("It's a tie.")
        elif scores[0] < scores[1]:
            print("Player 2 wins.")
        else: 
            print("Player 1 wins.")

        sys.exit()

    if len(valid_tiles) == 0:
        print("No move possible. Switch player.")
        end += 1
        switch_player(board)

    end = 0

def set_mode():
    return (random.randint(1, 4), random.randint(1, 4))

def player_mode(board):
    print(mode, "player_mode()")
    if mode == 1:
        return random_move(board)
    elif mode == 2:
        return best_move(board, 0)
    elif mode == 3:
        return best_move(board, 2)
    elif mode == 4:
        return best_move(board, 4)

def go(board):
    print("TURN: ", turn)
    
    piece = make_move(board, player_mode(board))

    print("Result")

    switch_player(board)

#(p1, p2) = set_mode()
print("Player1: ", p1, " Player2: ", p2)
mode = p1

init_board()
print_board(board_oc)

print("BEGIN")

while True:
    go(board_oc)

"""init_board()
print_board(board_oc)
turn = 1
print(turn)
from_one_piece(board, 3, 3)
available_tiles(board_oc)
make_move(board_oc, 5, 5)"""