# Capstone Projects Using Python

A collection of 10 dependency-free capstone projects from **Python Mastery: 100 Days, 100 Projects** (Days 91–100). Each project is a self-contained, runnable demo of a real-world backend system — CLI tools and a full-stack web app — built only with the Python standard library.

## Projects

| Day | Project | What it does |
| --- | ------- | ------------ |
| 91 | [Personal Finance Dashboard](personal_finance_dashboard) | Manage accounts, record transactions, and report net worth, cash flow, spending categories, savings rate, and budget status. |
| 92 | [Online Quiz App](online_quiz_app) | Question bank, answer validation, scoring, and explanations. |
| 93 | [Virtual Whiteboard App](virtual_whiteboard_app) | Shapes, notes, movement, undo history, and JSON export. |
| 94 | [Weather Monitoring Dashboard](weather_monitoring_dashboard) | Ingest station readings, validate measurements, produce alerts, and build a live dashboard snapshot. |
| 95 | [Stock Price Prediction Tool](stock_price_prediction_tool) | Linear-trend forecasting with backtesting (mean absolute error) and moving averages. |
| 96 | [Online Voting System](online_voting_system) | Eligibility tokens, one-vote enforcement, candidate validation, anonymized receipts, and an audit log. |
| 97 | [Restaurant Ordering System](restaurant_ordering_system) | Menu, table orders, line-item totals, availability checks, and kitchen status progression. |
| 98 | [Fitness Tracker App](fitness_tracker_app) | Log workouts and build dashboards of totals and weekly goal progress. |
| 99 | [AI Customer Service Chatbot](ai_customer_service_chatbot) | Keyword-based intent scoring, grounded answers, confidence reporting, and escalation to support tickets. |
| 100 | [Full-Stack Web Application](day_100_full_stack_web_application) | A browser task board with a Python HTTP backend, JSON API, and responsive HTML/CSS/JS frontend. |

## Requirements

- Python 3.10 or newer
- No third-party packages

## Running the projects

Each project is an independent folder with its own `README.md` describing structure and usage.

CLI projects (Days 91–99) run with:

```bash
cd <project_name>
python app.py
```

The Day 100 project starts a local web server:

```bash
cd day_100_full_stack_web_application
python server.py
```

Then open <http://localhost:8000> in your browser. Run `python server.py --check` to verify the backend without starting the server.

## Notes

- These projects are educational demos that exercise software design patterns (data models, validations, state machines, service layers, and API-shaped output) — they are not production deployments.
- The Day 100 server holds data in memory, so state resets on restart.