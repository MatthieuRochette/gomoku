import sys
X, Y = 0, 1


class Goban():
    def __init__(self, x=None, y=None) -> None:
        if x is None:
            return
        if y is None:
            y = x
        self.reset_to_size(x, y)
        self.debug_print()

    def reset(self) -> None:
        self.board = []
        for _ in range(self.size[Y]):
            self.board += [["_"] * self.size[X]]
        print("DEBUG Goban reset to size:", *self.size, file=sys.stderr)

    def reset_to_size(self, x: int, y: int = None) -> None:
        if y is None:
            y = x
        if x < 5 or y < 5:
            raise ValueError("Invalid size (x or y value too small)")
        self.size = (x, y)
        self.reset()

    def place(self, x: int, y: int, enemy: bool) -> None:
        if x < 0 or y < 0:
            raise IndexError("Negative coordinates received")
        elif self.board[y][x] in ["x", "o"]:
            raise ValueError("Cannot play at given position: already occupied")
        elif enemy:
            self.board[y][x] = "x"
        else:
            self.board[y][x] = "o"

    def debug_print(self) -> None:
        print("DEBUG Goban, size:", *self.size, file=sys.stderr)
        print("DEBUG enemy pos: 'x' | player pos: 'o'", file=sys.stderr)
        for line in self.board:
            print("DEBUG", *(str(elem).rjust(2, ' ') for elem in line), file=sys.stderr)
