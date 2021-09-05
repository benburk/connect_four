import math
from collections import namedtuple

from connect_four import Board

visits = 0


def negamax(board: Board, depth: int) -> float:
    global visits
    visits += 1

    if depth == 0 or board.is_over():
        return board.score()

    value = -math.inf
    for child in board.children():
        value = max(value, -negamax(child, depth - 1))
    return value


def negabeta(board: Board, alpha: int, beta: int, depth: int) -> int:
    global visits
    visits += 1

    if depth == 0 or board.is_over() or visits > 200:
        return board.score()

    value = -math.inf
    for child in board.children():
        value = max(value, -negabeta(child, -beta, -alpha, depth - 1))
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return value


Entry = namedtuple("Entry", "value flag depth")

table = {}


def transposition(board: Board, alpha: int, beta: int, depth: int) -> int:
    global visits
    visits += 1

    alpha_original = alpha

    if (entry := table.get(board)) and entry.depth >= depth:
        if entry.flag == "exact":
            return entry.value
        if entry.flag == "lower":
            alpha = max(alpha, entry.value)
        elif entry.flag == "upper":
            beta = min(beta, entry.value)
        if alpha >= beta:
            return entry.value

    if depth == 0 or board.is_over():
        return board.score()

    value = -math.inf
    for child in board.children():
        value = max(value, -negabeta(child, -beta, -alpha, depth - 1))
        alpha = max(alpha, value)
        if alpha >= beta:
            break

    if value <= alpha_original:
        table[board] = Entry(value, "upper", depth)
    elif value >= beta:
        table[board] = Entry(value, "lower", depth)
    else:
        table[board] = Entry(value, "exact", depth)

    return value


def iterative(board: Board, alpha: int, beta: int, depth: int) -> int:
    global visits
    visits += 1

    if depth == 0 or board.is_over():
        return board.score()

    value = -math.inf
    for child in board.children():
        value = max(value, -negabeta(child, -beta, -alpha, depth - 1))
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return value



def main() -> None:
    """Main method."""
    global visits
    board = Board.from_string("34544455332525534114373777771")
    board = Board.from_string("32164625366433")
    board = Board.from_string("243335424257")

    board = "26575651254343224"
    board = Board.from_string(board)


    # print(board.score())
    # return

    # visits = 0
    # score = negamax(board, 8)
    # print(f"Negamax: score: {score}, visits: {visits}")

    visits = 0
    score = negabeta(board, -1000, 1000, 5)
    print(f"Negabeta: score: {score}, visits: {visits}")

    # visits = 0
    # score = transposition(board, -100, 100, 8)
    # print(f"Transposition: score: {score}, visits: {visits}")


def test():
    # test all the R1
    global visits
    
    test_files = ["Test_L1_R1", "Test_L2_R1", "Test_L3_R1"]
    for test_file in test_files:
        with open(f"test_cases/{test_file}", encoding="utf-8") as file:
            for line in file:
                moves, score = line.split()
                depth = 22 - round(len(moves) / 2) - int(score)
                if depth > 2:
                    continue
                board = Board.from_string(moves)
                visits = 0
                score = negabeta(board, -1, 1, 7)
                print(f"board: {moves}, score: {score}, visits: {visits}")


if __name__ == "__main__":
    # test()
    main()
