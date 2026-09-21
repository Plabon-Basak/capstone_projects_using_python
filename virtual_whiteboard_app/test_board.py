import json
import tempfile
import unittest

from board import Whiteboard
from commands import BoardCommands
from storage import BoardStorage


class BoardCommandsTest(unittest.TestCase):
    def setUp(self):
        self.board = Whiteboard("Sprint Planning")
        self.commands = BoardCommands(self.board)

    def test_add_increments_ids(self):
        first = self.commands.add("note", 120, 80, "Hello", "yellow")
        second = self.commands.add("rectangle", 360, 80, "Box", "blue")
        self.assertEqual((first.id, second.id), (1, 2))
        self.assertEqual(len(self.board.shapes), 2)

    def test_add_unsupported_shape_raises(self):
        with self.assertRaises(ValueError):
            self.commands.add("triangle", 10, 10)

    def test_move_updates_position(self):
        shape = self.commands.add("circle", 50, 50)
        moved = self.commands.move(shape.id, 200, 300)
        self.assertEqual((moved.x, moved.y), (200, 300))

    def test_move_unknown_shape_raises(self):
        with self.assertRaises(LookupError):
            self.commands.move(999, 0, 0)

    def test_undo_restores_previous_snapshot(self):
        first = self.commands.add("note", 120, 80, "A")
        self.commands.add("rectangle", 360, 80, "B")
        restored = self.commands.undo()
        self.assertEqual(len(restored), 1)
        self.assertEqual(restored[0]["id"], first.id)

    def test_undo_empty_history_raises(self):
        with self.assertRaises(ValueError):
            self.commands.undo()


class BoardStorageTest(unittest.TestCase):
    def test_export_writes_json(self):
        board = Whiteboard("Demo")
        BoardCommands(board).add("note", 10, 10, "Hi")
        with tempfile.TemporaryDirectory() as tmp:
            target = f"{tmp}/out.json"
            result = BoardStorage.export(board, target)
            self.assertEqual(result["shape_count"], 1)
            with open(target, encoding="utf-8") as handle:
                data = json.load(handle)
            self.assertEqual(data["title"], "Demo")
            self.assertEqual(len(data["shapes"]), 1)


if __name__ == "__main__":
    unittest.main()