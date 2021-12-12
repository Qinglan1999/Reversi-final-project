import random
from tkinter import *
from tkinter.messagebox import *

GAME_OVER = False
GAME_OVER_STR = 'Game Over Score '
IMAGES = None
MAIN_BOARD = None
CV = None
PLAYER_TITLE = None
COMPUTER_TITLE = None
TURN = None


def reset_board(board):
    '''
    Set the intial tile on the board
    '''
    for x in range(8):
        for y in range(8):
            board[x][y] = 'none'
    # Set initial tiles
    # 2 white, 2 black
    board[3][3] = 'white'
    board[3][4] = 'black'
    board[4][3] = 'black'
    board[4][4] = 'white'


def get_new_board():
    '''
    Reset the new tile board
    '''
    board = []
    # Set none as no tile
    for i in range(8):
        board.append(['none'] * 8)
    return board


def is_on_board(x, y):
    '''
    Check whether the tiles is in the range
    '''
    return 0 <= x <= 7 and 0 <= y <= 7


def is_valid_move(board, tile, xstart, ystart):
    '''
    Check whether the move is valid
    '''
    # Check if the position already has tile or
    # the position is out of range
    if not is_on_board(xstart, ystart) or board[xstart][ystart] != 'none':
        return False
    # Temporarily store the tile location
    board[xstart][ystart] = tile
    if tile == 'black':
        otherTile = 'white'
    else:
        otherTile = 'black'
    # Find the tiles that needed to flip
    titles_to_flip = []
    direction = [[0, 1], [1, 1], [1, 0],
                 [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
    for xdirection, ydirection in direction:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if is_on_board(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not is_on_board(x, y):
                continue
            # Keep searching until out of range
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not is_on_board(x, y):
                    break
            # Out of range, so no tile needs to flip
            if not is_on_board(x, y):
                continue
            # Find the tile to flip
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    # End searching when reaching start point
                    if x == xstart and y == ystart:
                        break
                    # Record the position tiles needed to filp
                    titles_to_flip.append([x, y])
    # Remove the temporary tile, reset the board
    # Restore the empty space
    board[xstart][ystart] = 'none'  # Restore the empty space
    # If no tiles were flipped, this is not a valid move.
    if len(titles_to_flip) == 0:
        return False
    return titles_to_flip


def get_valid_moves(board, tile):
    '''
    Get the valid position for new tile
    '''
    valid_moves = []
    for x in range(8):
        for y in range(8):
            if is_valid_move(board, tile, x, y):
                valid_moves.append([x, y])
    return valid_moves


def get_score_of_board(board):
    '''
    Calculate the final tile number of black and white,
    record as the final score
    '''
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'black':
                xscore += 1
            if board[x][y] == 'white':
                oscore += 1
    return {'black': xscore, 'white': oscore}


def who_goes_first():
    '''
    Decide who go first(random)
    '''
    if random.randint(0, 1) == 0:
        return 'Computer'
    else:
        return 'Player'


def make_move(board, tile, xstart, ystart):
    '''
    Put one tile into (xstart, ystart) to make a move
    '''
    titles_to_flip = is_valid_move(board, tile, xstart, ystart)
    # Check whether the move is valid
    if titles_to_flip is False:
        return False
    board[xstart][ystart] = tile
    for x, y in titles_to_flip:
        # Make valid the move
        board[x][y] = tile
    return True


def get_board_copy(board):
    '''
    Copy the board
    '''
    dupe_board = get_new_board()
    for x in range(8):
        for y in range(8):
            dupe_board[x][y] = board[x][y]
    return dupe_board


def is_on_corner(x, y):
    '''
    Check whether the tile is at corner
    '''
    return (x == 0 and y == 0) or (
            x == 7 and y == 0) or (
            x == 0 and y == 7) or (
            x == 7 and y == 7)


def get_computer_move(board, computer_tile):
    '''
    Set the logic of computer moves
    '''
    # Get all computer's valid move
    possible_moves = get_valid_moves(board, computer_tile)
    if not possible_moves:
        return None
    # Random select computer moves
    random.shuffle(possible_moves)
    # If the [x, y] is on the corner, choose first
    for x, y in possible_moves:
        if is_on_corner(x, y):
            return [x, y]
    best_score = -1
    for x, y in possible_moves:
        dupe_board = get_board_copy(board)
        make_move(dupe_board, computer_tile, x, y)
        # Select the move base on the socre
        # Simulate the further move on copy board
        # Flip the move with highest score
        score = get_score_of_board(dupe_board)[computer_tile]
        if score > best_score:
            best_move = [x, y]
            best_score = score
    return best_move


def is_no_space(board):
    '''
    Check whether the game is end by all positions are filled
    '''
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'none':
                return False
    return True


def is_only_one_color(event):
    '''
    Check whether the game is end by only one type of tile remains
    '''
    row = int((event.y - 40) / 80)
    temp_list = []
    for row in MAIN_BOARD:
        temp_list.extend(eval(str(row)))
    if 'black' in temp_list and 'white' in temp_list:
        return False
    return True


def draw_chess_board():
    '''
    Set the board
    '''
    img1 = IMAGES[2]
    CV.create_image((360, 360), image=img1)
    CV.pack()


def call_back(event):
    '''
    Move a tile by clicking
    '''
    global TURN
    if GAME_OVER is False and TURN == 'Computer':
        return
    # Switch pixel coordinates to the coordinate of board
    col = int((event.x - 40) / 80)
    row = int((event.y - 40) / 80)
    # Hint the player if the position alredy has tile
    if 0 <= col <= 7 and 0 <= row <= 7:
        if MAIN_BOARD[col][row] != "none":
            showinfo(title="hint", message="Already has tile")
            return
    if make_move(MAIN_BOARD, PLAYER_TITLE, col, row):
        # Put one palyer's tile in the range of board
        # Record player's last move
        row_letter = ("ABCDEFGH")
        row_letter_x = row_letter[col]
        print("****Player's last move: ", row_letter_x, row+1)
        if get_valid_moves(MAIN_BOARD, COMPUTER_TITLE):
            '''
            # Record player's last move
            row_letter = ("ABCDEFGH")
            row_letter_x = row_letter[col]
            print("****Player's last move: ", row_letter_x, row+1)
            '''
            # Switch to computer's move after player's move
            TURN = 'Computer'
    # If computer has no valid move, switch to player's move
    if get_computer_move(MAIN_BOARD, COMPUTER_TITLE) is None:
        TURN = 'Player'
        # Record player's last move
        row_letter = ("ABCDEFGH")
        row_letter_x = row_letter[col]
        print("****Player's last move: ", row_letter_x, row+1)
        if is_no_space(MAIN_BOARD) is False:
            # Hint the player to continue
            # If it's last step, don't hint
            print("Player continues")
            showinfo(title="Player continues", message="Player continues")
    else:
        computer_go()

    # Set the board after new move
    draw_all()
    draw_can_go()
    # Check whether the game is end
    game_over_check(event)


def game_over_check(event):
    '''
    Check whether the game is end
    '''
    if is_only_one_color(event):
        # End the game when there's only one type of tiles
        game_end()
        return True
    if is_no_space(MAIN_BOARD):
        # End the game when there's no position for tiles
        game_end()
        return True
    else:
        return False


def game_end():
    '''
    Show end game score and winner
    '''
    # End the steps recording
    print("Record end")
    # Calculate the tiles number to find winner
    player_score = get_score_of_board(MAIN_BOARD)[PLAYER_TITLE]
    computer_score = get_score_of_board(MAIN_BOARD)[COMPUTER_TITLE]
    if player_score > computer_score:
        out_put_winner = "Winner: Player"
    elif player_score < computer_score:
        out_put_winner = "Winner: Computer"
    else:
        out_put_winner = "Draw"
    # Show the final score and winner in the record
    print("Player: ", player_score, "Computer", computer_score, out_put_winner)
    out_put_str = GAME_OVER_STR + "Player:" + str(
                    player_score) + ":" + "Computer:" + str(computer_score)
    # Show the final score and winner in the window
    showinfo(title="Game is end", message=out_put_str+"\n"+out_put_winner)


def computer_go():
    '''
    Se the computer move
    '''
    global TURN
    if GAME_OVER is False and TURN == 'Computer':
        x, y = get_computer_move(MAIN_BOARD, COMPUTER_TITLE)
        # Record computer's last move
        row_letter = ("ABCDEFGH")
        row_letter_x = row_letter[x]
        print("**Computer's last move: ", row_letter_x, y+1)
        # Use the logic of computer's move
        make_move(MAIN_BOARD, COMPUTER_TITLE, x, y)
        # If player has no possible move, switch to computer's move
        if get_valid_moves(MAIN_BOARD, PLAYER_TITLE):
            TURN = 'Player'
        else:
            if get_valid_moves(MAIN_BOARD, COMPUTER_TITLE):
                if is_no_space(MAIN_BOARD) is False:
                    # Hint the player that computer continues
                    # If it's last step, don't hint
                    print("Computer continues")
                    showinfo(
                            title="Computer continues",
                            message="Computer continues"
                            )
                computer_go()


def draw_all():
    '''
    Set new board and fill tilea
    '''
    draw_chess_board()
    for x in range(8):
        for y in range(8):
            if MAIN_BOARD[x][y] == 'black':
                CV.create_image((x * 80 + 80, y * 80 + 80), image=IMAGES[0])
                CV.pack()
            elif MAIN_BOARD[x][y] == 'white':
                CV.create_image((x * 80 + 80, y * 80 + 80), image=IMAGES[1])
                CV.pack()


def draw_can_go():
    '''
    Label the possible positions to make moves
    '''
    temp_list = get_valid_moves(MAIN_BOARD, PLAYER_TITLE)
    for m in temp_list:
        x = m[0]
        y = m[1]
        CV.create_image((x * 80 + 80, y * 80 + 80), image=IMAGES[3])
        CV.pack()


def main():
    global IMAGES, MAIN_BOARD, CV, PLAYER_TITLE, COMPUTER_TITLE, TURN

    # Initialization, show project's name
    root = Tk('Reversi')
    root.title("Reversi（Zijian Zhong's final project）")
    # Load images
    IMAGES = [
        PhotoImage(file='images/black.png'),
        PhotoImage(file='images/white.png'),
        PhotoImage(file='images/board.png'),
        PhotoImage(file='images/Info.png')
    ]

    # Create board data
    MAIN_BOARD = get_new_board()
    reset_board(MAIN_BOARD)

    # Set window
    CV = Canvas(root, bg='green', width=720, height=780)
    # Set new board and tiles
    draw_all()
    CV.pack()

    # Random select who go first
    TURN = who_goes_first()
    showinfo(title="Game start", message=TURN + " goes first!")
    # Hint the player who go first, and start record
    print(TURN, "goes first!"+"\n"+"Record start")

    # Who go first, who use black tiles
    if TURN == 'Player':
        PLAYER_TITLE = 'black'
        COMPUTER_TITLE = 'white'
    else:
        PLAYER_TITLE = 'white'
        COMPUTER_TITLE = 'black'
        computer_go()

    # Reset all tiles and board
    draw_all()
    draw_can_go()
    # Controll by clicking
    CV.bind("<Button-1>", call_back)
    CV.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
