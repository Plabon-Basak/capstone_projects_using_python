import json
from pathlib import Path


class BoardStorage:
    APP_DIR = Path(__file__).resolve().parent

    @staticmethod
    def export(board, path="whiteboard.json"):
        target = Path(path)
        if not target.is_absolute():
            target = BoardStorage.APP_DIR / target
        data = {"title": board.title, "shapes": board.snapshot()}
        target.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return {"saved_to": path, "shape_count": len(board.shapes)}
