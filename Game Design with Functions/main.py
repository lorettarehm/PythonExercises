# Imports
from random import choice


def initialize(board):
    # Initialize game
    # Initialize grid
    initialize_grid(board)
    # Initialize score
    global gv_score
    gv_score = 0
    # Initialize turn number
    global gv_turn
    gv_turn = 1


def initialize_grid(board):
    # Initialize grid by reading in from file
    for i in range(gv_board_size):
        for j in range(len(board[i])):
            board[i][j] = choice(['Q', 'R', 'S', 'T', 'U'])


def continue_game(current_score, goal_score=100):
    # Return false if game should end, true if game is not over
    if current_score >= goal_score:
        return False
    else:
        return True


def draw_board(board):
    # Display the board to the screen
    # Draw blank line first
    print("\n")
    # Calculate 4 characters per column on first row
    print("  " + ((4 * gv_board_size) + 1) * "-")
    # Print board header
    print("   | a | b | c | d | e | f | g | h |")
    print(" " + ((4 * gv_board_size) + 3) * "-")
    # Now draw rows from 8 down to 1
    for i in range(gv_board_size - 1, -1, -1):
        # Draw each row
        line_to_draw = " " + str(i + 1)
        for j in range(gv_board_size):
            line_to_draw += " | " + board[i][j]
        line_to_draw += " | "
        print(line_to_draw)
        print(" " + ((4 * gv_board_size) + 3) * "-")


def is_valid(move):
    # Returns true if the move is valid, false otherwise
    # Check length of move
    if len(move) != 3:
        return False

    # Check that the space and direction are valid
    if not (move[0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']):
        return False
    if not (move[1] in ['1', '2', '3', '4', '5', '6', '7', '8']):
        return False
    if not (move[2] in ['u', 'd', 'l', 'r']):
        return False

    # Check that the direction is valid for the given row/column
    # Check that first column moves are not left
    if (move[0] == 'a') and (move[2] == 'l'):
        return False
    # Check that last column moves are not right
    if (move[0] == 'h') and (move[2] == 'r'):
        return False
    # Check that bottom row moves are not down
    if (move[0] == '1') and (move[2] == 'd'):
        return False
    # Check that top row moves are not up
    if (move[0] == '8') and (move[2] == 'u'):
        return False

    # No problems, so the move is valid
    return True


def get_move():
    # Get the move from the user
    # Print instructions
    print("Enter a move by specifying the space and the direction (u, d, l, r). Spaces should list column then row:")
    print("For example, e3u would swap position e3 with the one above and f7r would swap f7 to the right")

    # Get Move
    print("\n")
    move = input("Enter move: ")

    # Loop until move is valid
    while not is_valid(move):
        move = input("That is not a valid move! Enter another move: ")

    return move


def remove_pieces(board):
    # Remove 3-in-a-row and 3-in-a-column pieces
    # Create board to store remove-or-not
    remove = [[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]

    # Go through rows
    for i in range(gv_board_size):
        for j in range(gv_board_size - 2):
            if (board[i][j] == board[i][j + 1]) and (board[i][j] == board[i][j + 2]):
                # Three in a row are the same!
                remove[i][j] = 1
                remove[i][j + 1] = 1
                remove[i][j + 2] = 1

    # Go through columns
    for j in range(gv_board_size):
        for i in range(gv_board_size - 2):
            if (board[i][j] == board[i + 1][j]) and (board[i][j] == board[i + 2][j]):
                # Three in a column are the same!
                remove[i][j] = 1
                remove[i + 1][j] = 1
                remove[i + 2][j] = 1

    # Eliminate those marked
    global gv_score
    removed_any = False
    for i in range(gv_board_size):
        for j in range(gv_board_size):
            if remove[i][j] == 1:
                board[i][j] = 0
                gv_score += 10
                removed_any = True
    return removed_any


def drop_pieces(board):
    # Drop pieces to fill in blanks
    for j in range(gv_board_size):
        # Make list of pieces in the column
        list_of_pieces = []
        for i in range(gv_board_size):
            if board[i][j] != 0:
                list_of_pieces.append(board[i][j])
        # Copy that list into column
        for i in range(len(list_of_pieces)):
            board[i][j] = list_of_pieces[i]
        # Fill in remainder of columns with 0s
        for i in range(len(list_of_pieces), 8):
            board[i][j] = 0


def fill_blanks(board):
    # Fill blanks with random pieces
    for i in range(gv_board_size):
        for j in range(gv_board_size):
            if board[i][j] == 0:
                board[i][j] = choice(['Q', 'R', 'S', 'T', 'U'])


def update_board(board, move):
    # Update the board according to move
    swap_pieces(board, move)
    pieces_eliminated = True
    while pieces_eliminated:
        pieces_eliminated = remove_pieces(board)
        drop_pieces(board)
        fill_blanks(board)


def convert_letter_to_col(col):
    # Valid range is a to h (8 columns)
    if col == 'a':
        return 0
    elif col == 'b':
        return 1
    elif col == 'c':
        return 2
    elif col == 'd':
        return 3
    elif col == 'e':
        return 4
    elif col == 'f':
        return 5
    elif col == 'g':
        return 6
    elif col == 'h':
        return 7
    else:
        # Not a valid column
        return -1


def swap_pieces(board, move):
    # Swap pieces on board according to move
    # Get original position
    origrow = int(move[1]) - 1
    origcol = convert_letter_to_col(move[0])

    # Get adjacent position
    # Up
    if move[2] == 'u':
        newrow = origrow + 1
        newcol = origcol
    # Down
    elif move[2] == 'd':
        newrow = origrow - 1
        newcol = origcol
    # Left
    elif move[2] == 'l':
        newrow = origrow
        newcol = origcol + 1
    # Right
    elif move[2] == 'r':
        newrow = origrow
        newcol = origcol - 1
    else:
        # Value not valid
        newrow = origrow
        newcol = origcol

    # Swap objects in two positions
    temp = board[origrow][origcol]
    board[origrow][origcol] = board[newrow][newcol]
    board[newrow][newcol] = temp


def do_round(board):
    # Perform one round of the game
    # Display current round
    draw_board(board)
    # Get move
    move = get_move()
    # Update board
    update_board(gv_board, move)
    # Update turn number
    global gv_turn
    gv_turn += 1


# State main variables
gv_score = 0
gv_goal_score = 100
gv_turn = 0
gv_board = [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]
gv_board_size = len(gv_board)

# Initialize game
initialize(gv_board)

# Loop while game not over
while continue_game(gv_score, gv_goal_score):
    # Print current score
    print("Score: " + str(gv_score))
    # Do a round of the game
    do_round(gv_board)
