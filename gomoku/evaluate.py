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


def find_patterns(goban: Goban, pos: tuple, patterns: dict) -> int:
    # goban.debug_print()
    # print("DEBUG", pos)
    min_x = pos[X] - 4 if pos[X] - 4 >= 0 else 0
    min_y = pos[Y] - 4 if pos[Y] - 4 >= 0 else 0
    max_x = pos[X] + 5 if pos[X] + 5 < goban.size[X]\
        else goban.size[X] - 1
    max_y = pos[Y] + 5 if pos[Y] + 5 < goban.size[Y]\
        else goban.size[Y] - 1
    range_x = max_x - min_x
    range_y = max_y - min_y
    for j in range(range_y):
        for i in range(range_x):
            if goban.board[j][i] not in [goban.self_char, goban.base_char, goban.enemy_char]:
                goban.board[j][i] = goban.base_char
    offset_x = 0
    diago_1 = ""
    for offset_y in range(range_y):
        diago_1 += str(goban.board[min_y + offset_y][min_x + offset_x])
        offset_x += 1
        if offset_x > range_x:
            break
    # print("DEBUG diago_1", diago_1)
    diago_2 = ""
    offset_x = 0
    for offset_y in range(range_y):
        diago_2 += str(goban.board[max_y - offset_y - 1][min_x + offset_x])
        offset_x += 1
        if offset_x > range_x:
            break
    # print("DEBUG diago_2", diago_2)
    hori = ""
    for offset_x in range(range_x):
        hori += str(goban.board[pos[Y]][min_x + offset_x])
    # print("DEBUG hori", hori)
    verti = ""
    for offset_y in range(range_y):
        verti += str(goban.board[min_y + offset_y][pos[X]])
    # print("DEBUG verti", verti)

    lines = [diago_1, diago_2, hori, verti]
    ret_val = 0
    for line in lines:
        for pattern, value in patterns.items():
            # print("DEBUG pattern:", pattern, "| line:", line)
            if pattern in line:
                ret_val += value
    # print("DEBUG retval:", ret_val)
    return ret_val


def static_eval(eval_goban: Goban, pos: tuple):
    self_value = find_patterns(deepcopy(eval_goban), pos, {
        "ooooo": POS_INF,
        "_oooo_": 100000,
        "oo_oo_oo": 100000,
        "oo_oo": 9000,
        "xoooo_": 1200,
        "_oooox": 1200,
        "_ooo_": 1000,
        "xooo__": 100,
        "__ooox": 100,
        "oo": 10,
    })
    enemy_value = find_patterns(deepcopy(eval_goban), pos, {
        "xxxxx": POS_INF,
        "_xxxx_": 100000,
        "xx_xx_xx": 100000,
        "xx_xx": 9000,
        "oxxxx_": 1200,
        "_xxxxo": 1200,
        "_xxx_": 1000,
        "oxxx__": 100,
        "__xxxo": 100,
        "xx": 10,
    })
    return self_value - int(enemy_value * 1.1)


def minmax(eval_goban: Goban, pos: tuple, depth: int, alpha: int, beta: int,
           maximizing: bool) -> int:

    # print("DEBUG print deepcopied goban in minmax")
    # eval_goban.debug_print()
    # print("DEBUG end of deepcopied goban in minmax")

    child_goban = deepcopy(eval_goban)
    child_goban.place(pos[X], pos[Y], not maximizing)

    if depth == 0:
        return static_eval(child_goban, pos)
    if find_patterns(child_goban, pos, {"ooooo": POS_INF, "xxxxx": POS_INF}) >= POS_INF:
        return POS_INF

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
