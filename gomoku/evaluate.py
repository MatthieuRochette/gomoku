import sys
from random import randint

from copy import deepcopy

from .goban import Goban

X, Y = 0, 1
NEG_INF = -10000000000
POS_INF = 10000000000


def pos_is_near_played(goban: Goban, pos: tuple, distance: int = 1) -> bool:
    min_x = pos[X] - distance if pos[X] - distance >= 0 else 0
    min_y = pos[Y] - distance if pos[Y] - distance >= 0 else 0
    max_x = pos[X] + distance if pos[X] + distance < goban.size[X]\
        else goban.size[X] - 1
    max_y = pos[Y] + distance if pos[Y] + distance < goban.size[Y]\
        else goban.size[Y] - 1
    # print("pos", pos)
    # print("xmin, xmax, ymin, ymax:", min_x, max_x, min_y, max_y)
    partial_board = [line[min_x:max_x + 1] for line in goban.board[min_y:max_y + 1]]
    # print(*partial_board, sep='\n')
    for row in partial_board:
        if goban.self_char in row or goban.enemy_char in row:
            # print("DEBUG  -> is near played")
            return True
    return False


def get_golden_zone(goban: Goban) -> list:
    golden_pos_list = []
    for j in range(goban.size[Y]):
        # print("DEBUG j:", j)
        for i in range(goban.size[X]):
            # print("DEBUG    i:", i)
            if goban.board[j][i] != goban.base_char:
                continue
            if goban.board[j][i] == goban.base_char\
                    and pos_is_near_played(goban, (i, j)):
                golden_pos_list.append((i, j))
    return golden_pos_list


def static_eval(eval_goban: Goban, pos: tuple):
    return randint(0, 5) - int(randint(0, 5) * 1.2)


def test_game_over(eval_goban: Goban, pos: tuple) -> bool:
    return False


def minmax(eval_goban: Goban, pos: tuple, depth: int, alpha: int, beta: int,
           maximizing: bool) -> int:

    # print("DEBUG print deepcopied goban in minmax")
    # eval_goban.debug_print()
    # print("DEBUG end of deepcopied goban in minmax")

    if depth == 0 or test_game_over(eval_goban, pos):
        return static_eval(eval_goban, pos)

    child_goban = deepcopy(eval_goban)
    child_goban.place(pos[X], pos[Y], False)

    if maximizing:
        max_eval = NEG_INF
        for child_pos in get_golden_zone(child_goban):
            _eval = minmax(
                child_goban, child_pos, depth - 1, alpha, beta, False
            )
            max_eval = max(_eval, max_eval)
            alpha = max(max_eval, alpha)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = POS_INF
        for child_pos in get_golden_zone(child_goban):
            _eval = minmax(
                child_goban, child_pos, depth - 1, alpha, beta, True
            )
            min_eval = min(_eval, min_eval)
            beta = min(min_eval, beta)
            if beta <= alpha:
                break
        return min_eval


def get_best_move_from_eval(eval_goban: Goban) -> tuple:
    best_pos = (0, 0)
    best_value = NEG_INF
    goban_chars = [eval_goban.self_char, eval_goban.enemy_char, eval_goban.base_char]
    for j in range(eval_goban.size[Y]):
        for i in range(eval_goban.size[X]):
            if eval_goban.board[j][i] in goban_chars:
                continue
            if int(eval_goban.board[j][i]) > best_value:
                best_value = int(eval_goban.board[j][i])
                best_pos = (i, j)
    return best_pos


def evaluate_board(goban: Goban) -> tuple:
    print("DEBUG beginning eval", file=sys.stderr)
    eval_goban = deepcopy(goban)
    # print("DEBUG check board of eval_goban", file=sys.stderr)
    # eval_goban.debug_print()
    # print("DEBUG end check of eval_board")
    # print(get_golden_zone(eval_goban))
    # print("DEBUG", get_golden_zone(eval_goban))
    for pos in get_golden_zone(eval_goban):
        eval_goban.board[pos[Y]][pos[X]] = minmax(
            deepcopy(eval_goban), pos, 2, NEG_INF, POS_INF, True
        )
    print("DEBUG Printing eval board", file=sys.stderr)
    eval_goban.debug_print()
    return get_best_move_from_eval(eval_goban)
    # return randint(0, 19), randint(0, 19)
