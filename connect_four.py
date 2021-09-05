import copy
from typing import Sequence

WIDTH = 7
HEIGHT = 6


def find_four(board: Sequence[Sequence[int]]) -> bool:
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if not board[row][col]:
                continue
            # check horizontal
            if (
                col < WIDTH - 3
                and board[row][col]
                == board[row][col + 1]
                == board[row][col + 2]
                == board[row][col + 3]
            ):
                return True
            # check vertical
            if (
                row < HEIGHT - 3
                and board[row][col]
                == board[row + 1][col]
                == board[row + 2][col]
                == board[row + 3][col]
            ):
                return True
            # check diagonal
            if (
                col < WIDTH - 3
                and row < HEIGHT - 3
                and board[row][col]
                == board[row + 1][col + 1]
                == board[row + 2][col + 2]
                == board[row + 3][col + 3]
            ):
                return True
            # check other diagonal
            if (
                col > 2
                and row < HEIGHT - 3
                and board[row][col]
                == board[row + 1][col - 1]
                == board[row + 2][col - 2]
                == board[row + 3][col - 3]
            ):
                return True
    return False


class Board:
    """Connect four board.
    Board represented as 2d matrix.
    Current player represented by 1 or -1.
    """

    def __init__(self, board=None, current_player=1) -> None:
        self.board = board if board else [[0] * WIDTH for _ in range(HEIGHT)]
        self.current_player = current_player

    @classmethod
    def from_string(cls, moves: str) -> "Board":
        """Construct a board from a sequence of moves."""
        board = cls()
        for move in moves:
            board.play(int(move) - 1)
        return board

    def play(self, col: int):
        for row in range(HEIGHT - 1, -1, -1):
            if not self.board[row][col]:
                self.board[row][col] = self.current_player
                break
        self.current_player *= -1

    def is_over(self):
        if all(col != 0 for row in self.board for col in row):
            return True  # draw

        if find_four(self.board):
            return True
        return False

    def score(self):
        if find_four(self.board):
            return -100
        return 0

    def children(self):
        for i in range(WIDTH):
            if not self.board[0][i]:
                new_board = Board(copy.deepcopy(self.board), self.current_player)
                new_board.play(i)
                yield new_board

    def __str__(self):
        board = []
        for row in self.board:
            record = []
            for col in row:
                if col == 1:
                    record.append("O")
                elif col == -1:
                    record.append("X")
                else:
                    record.append(" ")
            board.append("|".join(record))
        return "\n".join(board)

    def __hash__(self) -> int:
        return hash(str(self))