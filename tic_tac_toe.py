import numpy as np

BOARD_LENGTH = 3


class ArtificialPlayer:
    def __init__(self):
        pass


class Human:
    def __init__(self):
        pass

    def take_action(self):
        pass


class Board:
    def __init__(self):
        self.squares = np.zeros((BOARD_LENGTH, BOARD_LENGTH))
        self.x = 1
        self.o = -1

    def print(self):

        for i in range(BOARD_LENGTH):
            for j in range(BOARD_LENGTH):
                print(self.squares[i][j])


def play_game(p1, p2, board):
    pass

if __name__ == "__main__":
    p1 = ArtificialPlayer()
    p2 = ArtificialPlayer()

