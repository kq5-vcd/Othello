import random
import copy
import sys
import eel

eel.init('game')

direction = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
val_board = [[120, -20, 20,  5,  5, 20, -20, 120],
             [-20, -40, -5, -5, -5, -5, -40, -20],
             [ 20,  -5, 15,  3,  3, 15,  -5,  20],
             [  5,  -5,  3,  3,  3,  3,  -5,   5],
             [  5,  -5,  3,  3,  3,  3,  -5,   5],
             [ 20,  -5, 15,  3,  3, 15,  -5,  20],
             [-20, -40, -5, -5, -5, -5, -40, -20],
             [120, -20, 20,  5,  5, 20, -20, 120]]
                 
min_eval_board = -1776
max_eval_board = 1776

def print_board(board):
    for x in range(8):
        for y in range(8):
            print(board[x][y], end=" ")
        print()
    print()

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

@eel.expose
def available_tiles(board, player):
    valid_tiles = []
    #print_board(board)

    for x in range(8):
        for y in range(8):
            if(board[x][y] == player): #find in all 8 directions from the existing tiles
                #print(x, y, "available_tiles()")
                one_piece = from_one_piece(board, x, y, player)
                #print(one_piece, "available_tiles()") 

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

def random_move(tiles):
    #print(valid_tiles, "random_move()")

    move = tiles[random.randint(0, len(tiles) - 1)]
    #print(move, "random_move()")

    return move

def move_by_tiles(tiles):
    length = 0
    move = []

    for piece in tiles:
        if(len(piece[2]) > length):
            move = piece
        elif(len(piece[2]) == length):
            if random.randint(0, 1):
                move = piece

    #print(move, "move_by_tiles()")
    return move

def local_maximization(tiles):
    reward = -120
    move = []

    for piece in tiles:
        x = piece[0]
        y = piece[1]

        if(val_board[x][y] > reward):
            reward = val_board[x][y]
            move = piece
        elif(val_board[x][y] == reward):
            if random.randint(0, 1):
                move = piece

    return move

def eval_board(board, player):
    total = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == player:
                total += val_board[x][y]
            elif board[x][y] == 3 - player:
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

def Minimax(board, depth, player, turn):
    valid_tiles = available_tiles(board, player)
    #print(valid_tiles, "Minimax() valid_tiles")
    best_value = 0

    if depth == 0 or len(valid_tiles) == 0:
        return eval_board(board, turn)

    if player == turn:
        best_value = min_eval_board

        for piece in valid_tiles:
            board_temp = copy.deepcopy(board)

            make_move(board_temp, piece, player) 
            val = Minimax(board_temp, depth - 1, 3 - player, turn)
            
            #print(val, "Minimax() val maximize_player")

            if val > best_value:
                best_value = val
            
        #print(best_value, "Minimax() best_value maximize_player")
    else: # minimizingPlayer
        best_value = max_eval_board

        for piece in valid_tiles:
            board_temp = copy.deepcopy(board)

            make_move(board_temp, piece, player) 
            val = Minimax(board_temp, depth - 1, 3 - player, turn)
            
            #print(val, "Minimax() val minimize_player")
            
            if val < best_value:
                best_value = val

        #print(best_value, "Minimax() best_value minimize_player", depth)
    
    #print(best_value, "Minimax()", depth)
    return best_value

def Alpha_Beta(board, depth, player, Alpha, Beta, turn):
    valid_tiles = available_tiles(board, player)
    #print(valid_tiles, "Alpha_Beta() valid_tiles")
    best_value = 0

    if depth == 0 or len(valid_tiles) == 0:
        return eval_board(board, turn)

    if player == turn:
        best_value = min_eval_board

        for piece in valid_tiles:
            board_temp = copy.deepcopy(board)

            make_move(board_temp, piece, player) 
            val = Alpha_Beta(board_temp, depth - 1, 3 - player, Alpha, Beta, turn)
            
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
            val = Alpha_Beta(board_temp, depth - 1, 3 - player, Alpha, Beta, turn)
            
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

def Alpha_Beta_sorted(board, depth, player, Alpha, Beta, turn):
    valid_tiles = available_tiles(board, player)
    #print(valid_tiles, "Alpha_Beta_sorted() valid_tiles")
    best_value = 0

    if depth == 0 or len(valid_tiles) == 0:
        return eval_board(board, turn)

    if player == turn:
        tiles = sort_nodes(valid_tiles)
        best_value = min_eval_board

        for piece in tiles:
            board_temp = copy.deepcopy(board)

            make_move(board_temp, piece, player) 
            val = Alpha_Beta_sorted(board_temp, depth - 1, 3 - player, Alpha, Beta, turn)
            
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
            val = Alpha_Beta_sorted(board_temp, depth - 1, 3 - player, Alpha, Beta, turn)
            
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

def minimax_move(board, tiles, depth, player):
    max_points = min_eval_board
    best_move = []

    for move in tiles:
        board_temp = copy.deepcopy(board)
        make_move(board_temp, move, player) 

        points = Minimax(board_temp, depth, 3 - player, player)
                
        if points > max_points:
            max_points = points
            best_move = move
        elif points == max_points:
            if random.randint(0, 1):
                best_move = move

    #print(best_move, "minimax_move()")
    return best_move

def alpha_beta_move(board, tiles, depth, player):
    max_points = min_eval_board
    best_move = []

    for move in tiles:
        board_temp = copy.deepcopy(board)
        make_move(board_temp, move, player) 

        points = Alpha_Beta(board_temp, depth, 3 - player, max_points, max_eval_board, player)
                
        if points > max_points:
            max_points = points
            best_move = move
        elif points == max_points:
            if random.randint(0, 1):
                best_move = move

    #print(best_move, "alpha_beta_move()")
    return best_move

def alpha_beta_sorted_move(board, tiles, depth, player):
    max_points = min_eval_board
    sorted_tiles = sort_nodes(tiles)
    best_move = []

    for move in sorted_tiles:
        board_temp = copy.deepcopy(board)
        make_move(board_temp, move, player) 

        points = Alpha_Beta_sorted(board_temp, depth, 3 - player, max_points, max_eval_board, player)
                
        if points > max_points:
            max_points = points
            best_move = move
        elif points == max_points:
            if random.randint(0, 1):
                best_move = move

    #print(best_move, "alpha_beta_sorted_move()")
    return best_move

@eel.expose
def computer_move(board, player, tiles, mode):
    #print(mode, "player_mode()")
    if mode == 1:
        return random_move(tiles)
    elif mode == 2:
        return move_by_tiles(tiles)
    elif mode == 3:
        return local_maximization(tiles)
    elif mode == 4:
        return minimax_move(board, tiles, 2, player)
    elif mode == 5:
        return alpha_beta_move(board, tiles, 4, player)
    elif mode == 6:
        return alpha_beta_sorted_move(board, tiles, 6, player)

try:
    eel.start('OTHELLO.html', port=8080, size=(1200, 800))
except (SystemExit, MemoryError, KeyboardInterrupt):
    print ('The game is finished.')
    sys.exit()