import random
import copy
import sys
import time

t0 = time.process_time()

game_board = [[0 for x in range(8)] for y in range(8)]
val_board = [[120, -20, 20,  5,  5, 20, -20, 120],
             [-20, -40, -5, -5, -5, -5, -40, -20],
             [ 20,  -5, 15,  3,  3, 15,  -5,  20],
             [  5,  -5,  3,  3,  3,  3,  -5,   5],
             [  5,  -5,  3,  3,  3,  3,  -5,   5],
             [ 20,  -5, 15,  3,  3, 15,  -5,  20],
             [-20, -40, -5, -5, -5, -5, -40, -20],
             [120, -20, 20,  5,  5, 20, -20, 120]]
direction = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
turn = 0
end = 0
p1 = 1
p2 = 1
mode = 0

def print_board(board):
    for x in range(8):
        for y in range(8):
            print(board[x][y], end = " ")
        print()

def init_board():
    game_board[3][3] = game_board[4][4] = 1
    game_board[3][4] = game_board[4][3] = 2

def set_turn():
    start = random.randint(1, 2)

    #print("Start: ", start)
    return start

def is_on_board(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8

def is_corner(x, y):
    return [x, y] in [[0, 0], [0, 7], [7, 0], [7, 7]]

def tile_is_available(board, x , y, x_dir, y_dir, player):
    flipped_tiles = []
    other = 3 - player
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
    
    if(board[dx][dy] == player):
        return []
    
    if(board[dx][dy] == 0):
        #print([dx, dy, flipped_tiles], "tile_is_available()")
        return [dx, dy, flipped_tiles]
    
    return []

def from_one_piece(board, x, y, player):
    valid_tiles = []
    
    for dir_x, dir_y in direction: #find in all 8 directions
        tile = tile_is_available(board, x, y, dir_x, dir_y, player)
        
        if(len(tile) > 0):
            #print(tile, "from_one_piece() tile")
            valid_tiles.append(tile)

    #print(valid_tiles, "from_one_piece() valid_tiles") 
    return valid_tiles

def available_tiles(board, player):
    valid_tiles = []

    for x in range(8):
        for y in range(8):
            if(board[x][y] == turn): #find in all 8 directions from the existing tiles
                one_piece = from_one_piece(board, x, y, player) 

                if(len(one_piece) > 0):
                    #print(one_piece, "available_tiles() one_piece")

                    for case in valid_tiles:
                        for piece in one_piece:
                            #print(case, "This is a case", case[0:2], piece[0:2])

                            if case[0:2] == piece[0:2]:
                                case[2].extend(lst for lst in piece[2] if lst not in case[2])
                                one_piece.remove(piece)
                                break
                    else:
                        valid_tiles = valid_tiles + one_piece

                    #print(valid_tiles, "available_tiles() valid_tiles")
    
    return valid_tiles

def make_move(board, piece, player):
    #print(piece, "make_move()")

    x = piece[0]
    y = piece[1]
    flip = piece[2]

    board[x][y] = player
    for i, j in flip:
        board[i][j] = player
      
    #print_board(board)
    #print("Move made")

min_eval_board = -1776
max_eval_board = 1776

def eval_board(board):
    total = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == turn:
                total += val_board[x][y]
            elif board[x][y] == 3 - turn:
                total -= val_board[x][y]

    #print(total, "eval_board()")
    return total

def sort_nodes(tiles):
    sorted_nodes = []

    for piece in tiles:
        x = piece[0]
        y = piece[1]
        sorted_nodes.append([piece, val_board[x][y]])

    #print(sorted_nodes, "sort_nodes()")
    sorted_nodes = sorted(sorted_nodes, key = lambda node: node[1], reverse = True)
    sorted_nodes = [node[0] for node in sorted_nodes]
    #print(sorted_nodes, "sort_nodes()")

    return sorted_nodes

def Minimax(board, depth, player):
    valid_tiles = available_tiles(board, player)
    #print(valid_tiles, "Minimax() valid_tiles")
    best_value = 0

    if depth == 0 or len(valid_tiles) == 0:
        return eval_board(board)

    if player == turn:
        best_value = min_eval_board

        for piece in valid_tiles:
            board_temp = copy.deepcopy(board)

            make_move(board_temp, piece, player) 
            val = Minimax(board_temp, depth - 1, 3 - player)
            
            #print(val, "Minimax() val maximize_player")

            if val > best_value:
                best_value = val
            
        #print(best_value, "Minimax() best_value maximize_player")
    else: # minimizingPlayer
        best_value = max_eval_board

        for piece in valid_tiles:
            board_temp = copy.deepcopy(board)

            make_move(board_temp, piece, player) 
            val = Minimax(board_temp, depth - 1, 3 - player)
            
            #print(val, "Minimax() val minimize_player")
            
            if val < best_value:
                best_value = val

        #print(best_value, "Minimax() best_value minimize_player", depth)
    
    #print(best_value, "Minimax()", depth)
    return best_value

def Alpha_Beta(board, depth, player, Alpha, Beta):
    valid_tiles = available_tiles(board, player)
    #print(valid_tiles, "Alpha_Beta() valid_tiles")
    best_value = 0

    if depth == 0 or len(valid_tiles) == 0:
        return eval_board(board)

    if player == turn:
        best_value = min_eval_board

        for piece in valid_tiles:
            board_temp = copy.deepcopy(board)

            make_move(board_temp, piece, player) 
            val = Alpha_Beta(board_temp, depth - 1, 3 - player, Alpha, Beta)
            
            #print(val, "Alpha_Beta() val maximize_player")

            if val > best_value:
                best_value = val

            if val > Alpha:
                Alpha = val

            if Alpha >= Beta:
                break #beta cut-off
            
        #print(Alpha, "Alpha_Beta() Alpha maximize_player")
    else: # minimizingPlayer
        best_value = max_eval_board

        for piece in valid_tiles:
            board_temp = copy.deepcopy(board)

            make_move(board_temp, piece, player) 
            val = Alpha_Beta(board_temp, depth - 1, 3 - player, Alpha, Beta)
            
            #print(val, "Alpha_Beta() val minimize_player")

            if val < best_value:
                best_value = val
            
            if val < Beta:
                Beta = val

            if Alpha >= Beta:
                break #alpha cut-off

        #print(Beta, "Alpha_Beta() Beta minimize_player")
    
    #print(best_value, "Alpha_Beta()", depth)
    return best_value

def Alpha_Beta_sorted(board, depth, player, Alpha, Beta):
    valid_tiles = available_tiles(board, player)
    #print(valid_tiles, "Alpha_Beta_sorted() valid_tiles")
    best_value = 0

    if depth == 0 or len(valid_tiles) == 0:
        return eval_board(board)

    if player == turn:
        tiles = sort_nodes(valid_tiles)
        best_value = min_eval_board

        for piece in tiles:
            board_temp = copy.deepcopy(board)

            make_move(board_temp, piece, player) 
            val = Alpha_Beta_sorted(board_temp, depth - 1, 3 - player, Alpha, Beta)
            
            #print(val, "Alpha_Beta_sorted() val maximize_player")

            if val > best_value:
                best_value = val

            if val > Alpha:
                Alpha = val

            if Alpha >= Beta:
                break #beta cut-off
            
        #print(Alpha, "Alpha_Beta_sorted() Alpha maximize_player")
    else: # minimizingPlayer
        tiles = sort_nodes(valid_tiles)
        best_value = max_eval_board

        for piece in tiles:
            board_temp = copy.deepcopy(board)

            make_move(board_temp, piece, player) 
            val = Alpha_Beta_sorted(board_temp, depth - 1, 3 - player, Alpha, Beta)
            
            #print(val, "Alpha_Beta_sorted() val minimize_player")

            if val < best_value:
                best_value = val
            
            if val < Beta:
                Beta = val

            if Alpha >= Beta:
                break #alpha cut-off

        #print(Beta, "Alpha_Beta_sorted() Beta minimize_player")
    
    #print(best_value, "Alpha_Beta_sorted()", depth)
    return best_value

def random_move():
    valid_tiles = available_tiles(game_board, turn)
    #print(valid_tiles, "random_move()")

    move = valid_tiles[random.randint(0, len(valid_tiles) - 1)]
    #print(move, "random_move()")

    return move

def move_by_tiles():
    valid_tiles = available_tiles(game_board, turn)
    #print(valid_tiles, "move_by_tiles()")

    length = 0
    move = []

    for piece in valid_tiles:
        if(len(piece[2]) > length):
            move = piece
        elif(len(piece[2]) == length):
            if random.randint(0, 1):
                move = piece

    #print(move, "move_by_tiles()")
    return move

def local_maximization():
    valid_tiles = available_tiles(game_board, turn)

    reward = -120
    move = []

    for piece in valid_tiles:
        x = piece[0]
        y = piece[1]

        if(val_board[x][y] > reward):
            reward = val_board[x][y]
            move = piece
        elif(val_board[x][y] == reward):
            if random.randint(0, 1):
                move = piece

    return move

def minimax_move(depth):
    max_points = min_eval_board
    valid_tiles = available_tiles(game_board, turn)
    #print(valid_tiles, "minimax_move() valid_tiles")
    best_move = []

    for move in valid_tiles:
        board_temp = copy.deepcopy(game_board)
        make_move(board_temp, move, turn) 

        points = Minimax(board_temp, depth, 3 - turn)
                
        if points > max_points:
            max_points = points
            best_move = move
        elif points == max_points:
            if random.randint(0, 1):
                best_move = move

    #print(best_move, "minimax_move()")
    return best_move

def alpha_beta_move(depth):
    max_points = min_eval_board
    valid_tiles = available_tiles(game_board, turn)
    #print(valid_tiles, "alpha_beta_move() valid_tiles")
    best_move = []

    for move in valid_tiles:
        board_temp = copy.deepcopy(game_board)
        make_move(board_temp, move, turn) 

        points = Alpha_Beta(board_temp, depth, 3 - turn, max_points, max_eval_board)
                
        if points > max_points:
            max_points = points
            best_move = move
        elif points == max_points:
            if random.randint(0, 1):
                best_move = move

    #print(best_move, "alpha_beta_move()")
    return best_move

def alpha_beta_sorted_move(depth):
    max_points = min_eval_board
    valid_tiles = available_tiles(game_board, turn)
    tiles = sort_nodes(valid_tiles)
    #print(valid_tiles, "alpha_beta_move() valid_tiles")
    best_move = []

    for move in tiles:
        board_temp = copy.deepcopy(game_board)
        make_move(board_temp, move, turn) 

        points = Alpha_Beta_sorted(board_temp, depth, 3 - turn, max_points, max_eval_board)
                
        if points > max_points:
            max_points = points
            best_move = move
        elif points == max_points:
            if random.randint(0, 1):
                best_move = move

    #print(best_move, "alpha_beta_sorted_move()")
    return best_move

def score():
    scores = [0 , 0]

    for x in range(8):
        for y in range(8):
            if game_board[x][y] != 0:
                scores[game_board[x][y] - 1] += 1 

    #print("Player 1: ", scores[0], " Player 2: ", scores[1])
    return scores

def switch_player():
    global turn, end, mode
    turn = 3 - turn
    
    if turn == 1:
        mode = p1
    else:
        mode = p2

    scores = score()

    if end == 2:
        #print("No more possible moves")

        if scores[0] == scores[1]:
            print("It's a tie.")
        elif scores[0] < scores[1]:
            print("Player 2 wins.")
        else: 
            print("Player 1 wins.")

        t1 = time.process_time()
        print("Time elapsed: ", t1 - t0)

        sys.exit()

    valid_tiles = available_tiles(game_board, turn)

    if len(valid_tiles) == 0:
        #print("No move possible. Switch player.")
        end += 1
        switch_player()

    end = 0

def set_mode():
    return (random.randint(1, 4), random.randint(1, 4))

def player_mode():
    #print(mode, "player_mode()")
    if mode == 1:
        return random_move()
    elif mode == 2:
        return move_by_tiles()
    elif mode == 3:
        return local_maximization()
    elif mode == 4:
        return minimax_move(2)
    elif mode == 5:
        return alpha_beta_move(2)
    elif mode == 6:
        return alpha_beta_sorted_move(2)
    elif mode == 7:
        return alpha_beta_move(4)
    elif mode == 8:
        return alpha_beta_sorted_move(4)
    elif mode == 9:
        return alpha_beta_sorted_move(6)

def go():
    #print("TURN: ", turn)
    
    make_move(game_board, player_mode(), turn)

    #print_board(board)
    #print()
    #print("Result")

    switch_player()

#(p1, p2) = set_mode()
#print("Player1: ", p1, " Player2: ", p2)
mode = p1
turn = set_turn()
init_board()
#print_board(game_board)

#print("BEGIN")

while True:
    go()
