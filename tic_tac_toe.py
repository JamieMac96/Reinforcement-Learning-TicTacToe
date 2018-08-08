import numpy as np

BOARD_LENGTH = 3
VAL_SYM = {
    1: "X",
    -1: "O"
}
SYM_VAL = {
    "X": 1,
    "O": -1
}


class AiPlayer:

    # epsilon is the probability of choosing a random action instead of
    # choosing the best option available
    # alpha is the learning rate of the AI
    def __init__(self, sym, epsilon=.1, alpha=.5, verbose=False):
        self.epsilon = epsilon
        self.alpha = alpha
        self.verbose = verbose
        self.symbol = sym
        self.state_history = []

        # Dictionary that maps from state number to state value
        self.state_values = {}

    def set_verbose(self, verbose):
        self.verbose = verbose

    def take_action(self, board):
        r = np.random.rand()
        possible_moves = []

        if r < self.epsilon:
            if self.verbose:
                print("Taking random action")
            for i in range(BOARD_LENGTH):
                for j in range(BOARD_LENGTH):
                    if board.is_clear(i, j):
                        possible_moves.append((i, j))

            move_index = np.random.randint(0, len(possible_moves))
            next_move = possible_moves[move_index]
        else:
            move_values, best_move = self.get_move_values_and_best_move(board)

            next_move = best_move
            if self.verbose:
                print("Taking best action")
                print_items(move_values)

        board.add_move(self.symbol, next_move)

    def update_state_history(self, state):
        self.state_history.append(state)

    def update(self, board):
        reward = board.reward(self.symbol)
        target = reward
        for prev in reversed(self.state_history):
            value = self.state_values[prev] \
                  + self.alpha*(target - self.state_values[prev])
            self.state_values[prev] = value
            target = value

        self.reset_state_history()

    def reset_state_history(self):
        self.state_history = []

    def initialize_state_values(self, board):

        for i in range(board.num_states):
            board.set_state(i)
            self.state_values[i] = board.get_initial_state_value(self.symbol)

        board.set_state(0)

    def get_move_values_and_best_move(self, board):
        best_move_value = -1
        best_move = None
        move_values = []
        states = []

        for i in range(BOARD_LENGTH):
            move_values.append([])
            for j in range(BOARD_LENGTH):
                if board.is_clear(i, j):
                    board.add_move(self.symbol, (i, j))
                    state = board.get_state()
                    states.append(state)
                    move_values[i].append("{:.2f}".format(self.state_values[state]))
                    if self.state_values[state] >= best_move_value:
                        best_move = (i, j)
                        best_move_value = self.state_values[state]
                    board.squares[i][j] = 0
                else:
                    move_values[i].append(VAL_SYM[board.squares[i][j]])

        return move_values, best_move


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

    def update_state_history(self, state):
        pass

    def update(self, board):
        pass


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

        # 0 indicates a draw
        if self.is_full():
            return 0

        return None

    def add_move(self, symbol, location):
        if symbol not in (self.x, self.o):
            raise ValueError("Invalid symbol used: " + str(symbol))

        i, j = location

        if self.is_clear(i, j):
            self.squares[i][j] = symbol

    def is_clear(self, i, j):
        return self.squares[i][j] == 0

    def reset(self):
        self.squares = np.zeros((BOARD_LENGTH, BOARD_LENGTH))

    def is_full(self):

        for row in self.squares:
            for item in row:
                if item == 0:
                    return False

        return True

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
        square_number = 0  # Current position on the board (0-8)
        state_number = 0

        for i in range(BOARD_LENGTH):
            for j in range(BOARD_LENGTH):
                square_value = 0  # X = 2, O = 1, blank = 0
                if self.squares[i][j] == 1:
                    square_value = 2
                elif self.squares[i][j] == -1:
                    square_value = 1
                state_number += (3**square_number)*square_value
                square_number += 1
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

    def reward(self, symbol):
        winner = self.get_winner()

        if winner != 1:
            return 0
        else:
            return 1


# This function prints a list of items in the
# configuration of a tic-tac-toe board.
# The items passed should be in the format of a
# 3x3 2d string array
def print_items(items):
    print("----------------")
    for i in range(BOARD_LENGTH):
        print(" ", end='')
        for j in range(BOARD_LENGTH):
            print("{:<5}".format(items[i][j]), end='')
        print("\n----------------")


def ternary(n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))


def play_game(player1, player2, board, verbose=False):
    winner = None

    current_player = player1

    if verbose:
        print("Starting new game")

    while winner is None:
        current_player.take_action(board)
        if current_player == player1:
            current_player = player2
        else:
            current_player = player1
        if verbose:
            board.print()

        current_state = board.get_state()

        player1.update_state_history(current_state)
        player2.update_state_history(current_state)
        winner = board.get_winner()

    player1.update(board)
    player2.update(board)
    board.reset()

    if verbose:
        if winner == 0:
            print("It's a draw!")
        else:
            print("player " + VAL_SYM[winner] + " won the game!")


if __name__ == "__main__":
    p1 = AiPlayer(1)
    p2 = AiPlayer(-1)
    brd = Board()

    p1.initialize_state_values(brd)
    p2.initialize_state_values(brd)

    for g in range(50000):
        if g % 200 == 0:
            print(g)
        play_game(p1, p2, brd)

    p1.set_verbose(True)
    keep_playing = input("continue playing? [y/n]: ")

    while keep_playing == "y":
        p2 = Human(-1)

        play_game(p1, p2, brd, verbose=True)
        keep_playing = input("continue playing? [y/n]: ")

