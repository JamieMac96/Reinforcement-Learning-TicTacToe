import numpy as np

BOARD_LENGTH = 3


class AiPlayer:

    # epsilon is the probability of choosing a random action instead of
    # choosing the best option available
    # alpha is the learning rate of the AI
    def __init__(self, sym, epsilon=.1, alpha=.5):
        self.epsilon = epsilon
        self.alpha = alpha
        self.symbol = sym
        self.state_history = []

        # Dictionary that maps from state number to state value
        self.state_values = {}

    def take_action(self, game_board):
        r = np.random.rand()
        possible_moves = []

        if r < self.epsilon:
            print("Taking random action")
            for i in range(BOARD_LENGTH):
                for j in range(BOARD_LENGTH):
                    if game_board.is_clear(i, j):
                        possible_moves.append((i, j))

            move_index = np.random.randint(len(possible_moves))
            next_move = possible_moves[move_index]
        else:
            print("Taking best action")
            best_move_value = 0.0
            best_move = None
            for i in range(BOARD_LENGTH):
                for j in range(BOARD_LENGTH):
                    if game_board.is_clear(i, j):
                        game_board.squares[i][j] = self.symbol
                        state = game_board.get_state()
                        if self.state_values[state] > best_move_value:
                            best_move = (i, j)
                        game_board.squares[i][j] = 0
            next_move = best_move
        game_board.add_move(self.symbol, next_move)

    def update_state_history(self, state):
        self.state_history.append(state)

    def update(self):
        pass

    def reset_state_history(self):
        self.state_history = []

    def initialize_state_values(self, board):

        for i in range(board.num_states):
            board.set_state(i)
            self.state_values[i] = board.get_initial_state_value(self.symbol)

        board.set_state(0)


class Human:
    def __init__(self, symbol):
        self.symbol = symbol

    def take_action(self, board):
        move = input("Player " + str(self.symbol)
                     + ". Enter your move (i,j): ")

        coordinates = [int(res) for res in move.split(",")]

        if not board.is_clear(coordinates[0], coordinates[1]):
            self.take_action(board)

        board.add_move(self.symbol, coordinates)


class Board:
    def __init__(self):
        self.squares = np.zeros((BOARD_LENGTH, BOARD_LENGTH))
        self.x = 1
        self.o = -1
        self.num_states = 3**(BOARD_LENGTH*BOARD_LENGTH)

    def print(self):
        output_items = np.empty([BOARD_LENGTH, BOARD_LENGTH], dtype='str')
        output_items[:] = ' '

        for i in range(BOARD_LENGTH):
            for j in range(BOARD_LENGTH):
                if self.squares[i][j] == self.x:
                    output_items[i][j] = 'X'
                elif self.squares[i][j] == self.o:
                    output_items[i][j] = 'O'

        print_items(output_items)

    def get_winner(self):
        linear_values = []

        # Process rows and columns
        linear_values.extend([sum(row) for row in self.squares])
        linear_values.extend([sum(column) for column in zip(*self.squares)])

        # Process diagonals
        bl = BOARD_LENGTH  # For reduced line length
        diagonals = [sum(self.squares[i][i] for i in range(bl)),
                     sum(self.squares[i][bl - i - 1] for i in range(bl))]

        linear_values.extend(diagonals)

        for line_sum in linear_values:
            if line_sum == (BOARD_LENGTH * self.x):
                return self.x
            if line_sum == (BOARD_LENGTH * self.o):
                return self.o

        return None

    def add_move(self, symbol, location):
        if symbol not in (self.x, self.o):
            raise ValueError("Invalid symbol used")

        i, j = location

        if self.is_clear(i, j):
            self.squares[i][j] = symbol

    def is_clear(self, i, j):
        return self.squares[i][j] == 0

    def clear_board(self):
        self.squares = np.zeros((BOARD_LENGTH, BOARD_LENGTH))

    # This method returns a numeric value for the current state.
    # There are 3^9(19683) total states in the game.
    # This is because for each space on the board there are three
    # possibilities:
    #   - The square is empty
    #   - There is an O in the square
    #   - There is a X in the square
    #
    # As such we can map the board configuration to a numeric value.
    # This is then used as a way of identifying this board
    # configuration.
    # Each board configuration will have an associated value
    # which the AI will modify over time in order to get
    # better at the game
    def get_state(self):
        square_number = 0 # Current position on the board (0-8)
        state_number = 0

        for i in range(BOARD_LENGTH):
            for j in range(BOARD_LENGTH):
                square_value = 0  # X = 2, O = 1, blank = 0
                if self.squares[i][j] == 1:
                    square_value = 2
                elif self.squares[i][j] == -1:
                    square_value = 1
                state_number += (3**square_number)*square_value
        return state_number

    # This method will set the board configuration to
    # that of the number passed
    def set_state(self, state_num):
        if state_num >= self.num_states:
            raise ValueError("Error! board state does not exist")

        # Converting the state number to ternary makes it
        # very easy to populate the tic-tac-toe board
        ternary_state = ternary(state_num).zfill(9)

        for i, char in enumerate(ternary_state):
            board_val = int(char)
            row_index = i / 3
            column_index = i % 3

            if board_val == 2:
                self.squares[row_index][column_index] = 1
            elif board_val == 1:
                self.squares[row_index][column_index] = -1
            else:
                self.squares[row_index][column_index] = 0

    # This method returns the initial value of the state for
    # a specific symbol.
    # States with no winner have a value of .5 with
    # winning and losing states having values of 0 and 1
    def get_initial_state_value(self, symbol):
        winner = self.get_winner()

        if winner is None:
            return .5
        elif winner == symbol:
            return 1
        else:
            return 0


# This function prints a list of items in the
# configuration of a tic-tac-toe board.
# The items passed should be in the format of a
# 3x3 2d string array
def print_items(items):
    print("-----------")
    for i in range(BOARD_LENGTH):
        print(" ", end='')
        for j in range(BOARD_LENGTH):
            print("{:<4}".format(items[i][j]), end='')
        print("\n-----------")


def ternary(n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))


def play_game(player1, player2, board):
    winner = None

    current_player = player1
    player2.initialize_state_values(board)
    print("Starting new game")

    board.print()

    while winner is None:
        if current_player == player1:
            player1.take_action(board)
            current_player = player2
        else:
            player2.take_action(board)
            current_player = player1
        board.print()
        winner = board.get_winner()

    print("player " + str(winner) + " won the game!")


if __name__ == "__main__":
    p1 = Human(1)
    p2 = AiPlayer(-1)

    brd = Board()

    play_game(p1, p2, brd)
