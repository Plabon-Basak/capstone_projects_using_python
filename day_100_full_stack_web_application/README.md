# Day 100: Full-Stack Web Application

A complete dependency-free task board with a Python HTTP backend, JSON API, in-memory data store, and responsive HTML/CSS/JavaScript frontend.

## Structure
- `server.py` — HTTP server, static hosting, and API routes
- `store.py` — task model and application data
- `static/index.html` — browser interface
- `static/app.js` — frontend API integration
- `static/styles.css` — responsive visual styling

## Run
```bash
cd /Users/arjunvaid/Desktop/sucess_plan/python_mastery_100_days_100_projects/day_100_full_stack_web_application
python3 server.py
```
Open http://localhost:8000 in your browser. Click a task to toggle completion.

## Verify without starting the server
```bash
python3 server.py --check
```

Requires Python 3.10+ and no third-party packages.
