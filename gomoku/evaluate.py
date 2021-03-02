import sys
from random import randint, choice

from copy import deepcopy

from .goban import Goban

X, Y = 0, 1
NEG_INF = -9999999999
POS_INF = 8999999999


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
    # print("DEBUG board before cleaning", file=sys.stderr)
    # goban.debug_print()
    # for j in range(min_y, max_y + 1):
    #     for i in range(min_x, max_x + 1):
    #         if str(goban.board[j][i]) not in [goban.self_char, goban.base_char, goban.enemy_char]:
    #             # print("DEBUG cleaning pos (", i, j, ")", file=sys.stderr)
    #             goban.board[j][i] = goban.base_char
    # print("DEBUG cleaned board", file=sys.stderr)
    # goban.debug_print()
    offset_x = 0
    diago_1 = ""
    for offset_y in range(range_y):
        diago_1 += str(goban.board[min_y + offset_y][min_x + offset_x])
        offset_x += 1
        if offset_x > range_x:
            break
    # print("DEBUG diago_1", diago_1, file=sys.stderr)
    diago_2 = ""
    offset_x = 0
    for offset_y in range(range_y):
        diago_2 += str(goban.board[max_y - offset_y - 1][min_x + offset_x])
        offset_x += 1
        if offset_x > range_x:
            break
    # print("DEBUG diago_2", diago_2, file=sys.stderr)
    hori = ""
    for offset_x in range(range_x):
        hori += str(goban.board[pos[Y]][min_x + offset_x])
    # print("DEBUG hori", hori, file=sys.stderr)
    verti = ""
    for offset_y in range(range_y):
        verti += str(goban.board[min_y + offset_y][pos[X]])
    # print("DEBUG verti", verti, file=sys.stderr)

    lines = [diago_1, diago_2, hori, verti]
    ret_val = 0
    for line in lines:
        for pattern, value in patterns.items():
            # print("DEBUG pattern:", pattern, "| line:", line)
            if pattern in line:
                ret_val += value
    # print("DEBUG retval:", ret_val, file=sys.stderr)
    return ret_val


def static_eval(eval_goban: Goban, pos: tuple):
    # print("DEBUG char at pos", pos, ":", eval_goban.board[pos[Y]][pos[X]], file=sys.stderr)
        # print("DEBUG evaluating for self", file=sys.stderr)
    return find_patterns(eval_goban, pos, {
        "ooooo": POS_INF,

        "xxxxo": 410000,
        "xxxox": 410000,
        "xxoxx": 410000,
        "xoxxx": 410000,
        "oxxxx": 410000,

        "_xxxo": 105000,
        "oxxx_": 105000,
        "xxox_": 101000,
        "_xoxx": 101000,
        "xoxx_": 101000,
        "_xxox": 101000,

        "_oooo": 100000,
        "oooo_": 100000,
        "ooo_o": 49000,
        "o_ooo": 49000,
        "oo_oo": 49000,

        "_ooo_": 1800,
        "o_o_o": 1000,
        "__ooo": 1000,
        "ooo__": 1000,

        "ooo__": 700,
        "__ooo": 700,
        "xooo_": 500,
        "_ooox": 500,

        "oo___": 10,
        "_oo__": 10,
        "__oo_": 10,
        "___oo": 10,

        "oooxo": -2000,
        "oxooo": -2000,
    })


# def minmax(eval_goban: Goban, pos: tuple, depth: int, alpha: int, beta: int,
#            maximizing: bool) -> int:

#     child_goban = deepcopy(eval_goban)
#     child_goban.place(pos[X], pos[Y], not maximizing)
#     # print("DEBUG depth:", depth, "pos:", pos, "maximizin:", maximizing, file=sys.stderr)
#     # child_goban.debug_print()

#     if depth <= 0:
#         s_eval = static_eval(child_goban, pos)
#         # print("DEBUG static_eval:", s_eval, file=sys.stderr)
#         return s_eval
#     # if find_patterns(child_goban, pos, {"ooooo": POS_INF, "xxxxx": NEG_INF}) != 0:
#     #     return find_patterns(child_goban, pos, {"ooooo": POS_INF, "xxxxx": NEG_INF})

#     if not maximizing:
#         max_eval = NEG_INF
#         for child_pos in get_golden_zone(child_goban):
#             _eval = minmax(
#                 child_goban, child_pos, depth - 1, alpha, beta, not maximizing
#             )
#             # print("DEBUG maximizing _eval:", _eval, file=sys.stderr)
#             max_eval = max(_eval, max_eval)
#             alpha = max(max_eval, alpha)
#             if beta <= alpha:
#                 break
#         # print("DEBUG max_eval:", max_eval, file=sys.stderr)
#         return max_eval
#     else:
#         min_eval = POS_INF
#         for child_pos in get_golden_zone(child_goban):
#             _eval = minmax(
#                 child_goban, child_pos, depth - 1, alpha, beta, not maximizing
#             )
#             # print("DEBUG minimizing _eval:", _eval, file=sys.stderr)
#             min_eval = min(_eval, min_eval)
#             beta = min(min_eval, beta)
#             if beta <= alpha:
#                 break
#         # print("DEBUG min_eval:", min_eval, file=sys.stderr)
#         return min_eval


def get_best_move_from_eval(eval_goban: Goban) -> tuple:
    best_pos_list = []
    best_value = NEG_INF
    goban_chars = [eval_goban.self_char, eval_goban.enemy_char, eval_goban.base_char]
    for j in range(eval_goban.size[Y]):
        for i in range(eval_goban.size[X]):
            if eval_goban.board[j][i] in goban_chars:
                continue
            elif int(eval_goban.board[j][i]) > best_value:
                best_pos_list = [(i, j)]
                best_value = int(eval_goban.board[j][i])
            elif int(eval_goban.board[j][i]) == best_value:
                best_pos_list.append((i, j))
    return choice(best_pos_list)


def evaluate_board(goban: Goban) -> tuple:
    # print("DEBUG beginning eval", file=sys.stderr)
    eval_goban = deepcopy(goban)
    # print("DEBUG check board of eval_goban", file=sys.stderr)
    # eval_goban.debug_print()
    # print("DEBUG end check of eval_board")
    # print(get_golden_zone(eval_goban))
    # print("DEBUG", get_golden_zone(eval_goban))
    for pos in get_golden_zone(eval_goban):
        # eval_goban.board[pos[Y]][pos[X]] = minmax(
        #     eval_goban, pos, 3, NEG_INF, POS_INF, True
        # )
        copy_goban = deepcopy(goban)
        copy_goban.place(pos[X], pos[Y], False)
        # copy_goban.debug_print()
        eval_goban.board[pos[Y]][pos[X]] = static_eval(copy_goban, pos)
    # print("DEBUG Printing eval board", file=sys.stderr)
    # eval_goban.debug_print()
    return get_best_move_from_eval(eval_goban)
    # return randint(0, 19), randint(0, 19)
