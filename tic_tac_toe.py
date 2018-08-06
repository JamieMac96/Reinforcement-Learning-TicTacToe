import numpy as np

BOARD_LENGTH = 3


class ArtificialPlayer:
    def __init__(self, sym, eps=.1, alpha=.5):
        self.eps = eps
        self.alpha = alpha
        self.symbol = sym
        self.state_history = []
        self.values = []

    def take_action(self, game_board):
        pass

    def update_state_history(self):
        pass

    def reset_state_history(self):
        self.state_history = []

    def initialize_state_values(self):
        pass


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
        n = BOARD_LENGTH  # For shorter line length
        diagonals = [sum(self.squares[i][i] for i in range(n)),
                     sum(self.squares[i][n - i - 1] for i in range(n))]

        linear_values.extend(diagonals)

        print(linear_values)

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


def play_game(player1, player2, board):
    winner = None

    current_player = player1
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
    p2 = Human(-1)

    brd = Board()

    play_game(p1, p2, brd)
