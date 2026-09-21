# Day 93: Virtual Whiteboard App

A CLI whiteboard model supporting shapes, notes, movement, undo history, and JSON export.

## Structure
- `app.py` — request/response demo
- `board.py` — board and shape models
- `commands.py` — drawing, movement, and undo commands
- `storage.py` — board export

## Run
```bash
cd virtual_whiteboard_app
python app.py
```

Export always writes `whiteboard.json` next to `storage.py`, regardless of the
directory you launch from.

Requires Python 3.10+ and no third-party packages.
