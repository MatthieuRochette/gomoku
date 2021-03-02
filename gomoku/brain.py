import sys

from .goban import Goban
from .evaluate import evaluate_board


class Brain():
    """
    A Gomoku algorithm brain based on the Piskvork protocol
    """
    def __init__(self) -> None:
        self.goban: Goban = Goban()
        self.commands = {
            "START": self.start,
            "RECTSTART": self.rectstart,
            "TURN": self.turn,
            "BEGIN": self.begin,
            "BOARD": self.board,
            "INFO": self.info,
            "END": self.end,
            "ABOUT": self.about
        }
        self.infos = {
            "timeout_turn": 0,
            "timeout_match": 0,
            "max_memory": 0,
            "time_left": 2147483647,
            "game_type": 0,
            "rule": 1,
            "folder": None
        }

    @staticmethod
    def _get_coordinates_from_arg(arg) -> tuple:
        coords = arg.split(',')
        if len(coords) != 2:
            raise ValueError(
                "Incorrectly formatted or wrong number of arguments"
            )
        return int(coords[0]), int(coords[1])

    def _play(self, fake=False) -> str:
        # evaluate board
        play_x, play_y = evaluate_board(self.goban)

        if not fake:
            # make best move available
            self.goban.place(play_x, play_y, False)
            # print("DEBUG real move:")
            # self.goban.debug_print()

        # return move made as "x,y"
        return str(play_x) + "," + str(play_y)

    def start(self, size: str = "20") -> str:
        return self.rectstart(size + ',' + size)

    def rectstart(self, size: str = "20,20") -> str:
        size_x, size_y = self._get_coordinates_from_arg(size)
        self.goban.reset_to_size(size_x, size_y)
        return "OK"

    def turn(self, turn) -> str:
        turn_x, turn_y = self._get_coordinates_from_arg(turn)
        # set turn on the board
        self.goban.place(turn_x, turn_y, True)
        # play
        # print("DEBUG Playing at end of turn")
        return self._play()

    def begin(self) -> str:
        play_x = self.goban.size[0] // 2
        play_y = self.goban.size[1] // 2

        self.goban.place(play_x, play_y, False)
        # self.goban.debug_print()

        # return move made as "x,y"
        return str(play_x) + "," + str(play_y)

    def board(self) -> str:
        input_str = input()
        while input_str != "DONE":
            params = input_str.split(",")
            if len(params) != 3:
                raise ValueError("Wrong number of parameters during BOARD")
            place_x, place_y = int(params[0]), int(params[1])
            if params[2] == "1":
                enemy = False
            elif params[2] == "2":
                enemy = True
            else:
                raise ValueError("Not supported yet")
            self.goban.place(place_x, place_y, enemy)
            input_str = input()
        return self._play()

    def info(self, key, value) -> None:
        if key == "evaluate":
            return
        try:
            if key != "folder":
                self.infos[key] = int(value)
            else:
                self.infos[key] = value
        except Exception:
            pass

    def end(self):
        # delete temp files if any
        # exit
        sys.exit(0)

    def about(self):
        pass

    @staticmethod
    def _parse_command(input_str):
        # tokenize the input
        return input_str.split(" ")

    def start_loop(self):
        try:
            while True:
                # parse command
                command, *args = self._parse_command(input())
                # print("DEBUG command:", command, file=sys.stderr)
                # print("DEBUG args:", args, file=sys.stderr)

                # execute command
                try:
                    output = self.commands[command](*args)
                    # print("DEBUG output:", output, file=sys.stderr)
                except KeyError:
                    print("UNKNOWN")
                except Exception as err:
                    print("ERROR", err)

                # print function output
                else:
                    if output is None:
                        continue
                    elif isinstance(output, (list, tuple)):
                        print(*output)
                    else:
                        print(output)
        except EOFError:
            sys.exit(0)
