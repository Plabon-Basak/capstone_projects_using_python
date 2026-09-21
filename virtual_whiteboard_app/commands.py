from board import Shape


class BoardCommands:
    def __init__(self, board):
        self.board = board
        self._next_id = 1

    def add(self, kind, x, y, text="", color="black"):
        if kind not in {"note", "rectangle", "circle", "line"}:
            raise ValueError("Unsupported shape type")
        self.board.history.append(self.board.snapshot())
        shape = Shape(self._next_id, kind, x, y, text, color)
        self._next_id += 1
        self.board.shapes.append(shape)
        return shape

    def move(self, shape_id, x, y):
        shape = next((s for s in self.board.shapes if s.id == shape_id), None)
        if shape is None:
            raise LookupError("Shape not found")
        self.board.history.append(self.board.snapshot())
        shape.x, shape.y = x, y
        return shape

    def undo(self):
        if not self.board.history:
            raise ValueError("Nothing to undo")
        previous = self.board.history.pop()
        self.board.shapes = [Shape(**item) for item in previous]
        self._next_id = max((shape.id for shape in self.board.shapes), default=0) + 1
        return self.board.snapshot()
