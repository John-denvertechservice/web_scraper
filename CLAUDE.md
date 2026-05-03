# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the project

Full daily pipeline (scrape → text report):
```bash
python scripts/daily_run.py
```

HTML report from database (run after `daily_run.py`):
```bash
python src/reporter_html.py
```

Inspect database contents:
```bash
python scripts/check_db.py
```

All scripts must be run from the project root — paths are relative (e.g., `data/database.db`, `data/raw/*.json`).

## Architecture

The project is a two-phase daily pipeline:

**Phase 1 — Scrape & store** (`scripts/daily_run.py` orchestrates):
1. `src/scraper.py` — fetches pages from `books.toscrape.com` (pages 1–3), parses titles/prices with BeautifulSoup, writes raw JSON to `data/raw/multi_scrape_<timestamp>.json`, then calls `src/database.py` to persist to SQLite.
2. `src/reporter.py` — reads the latest JSON file, uses pandas to compute summary stats (total, avg price, most expensive), prints to stdout.

**Phase 2 — HTML report** (run separately):
- `src/reporter_html.py` — queries the SQLite DB for the top 5 most expensive books, renders an MJML email template, and writes the compiled HTML to `data/report/<YYYY-MM-DD>.html`.

**Data layer** (`src/database.py`):
- SQLite at `data/database.db`, single `books` table with `title` (UNIQUE), `price_raw`, `price_float`, `scraped_at`.
- `INSERT OR IGNORE` prevents duplicate titles across runs.
- Price cleaning strips `£`/`Â£` encoding artifacts and stores as float.

**Logging**: `scripts/daily_run.py` writes to `logs/automation.log` (excluded from git).

## Key notes

- `scraper.py` imports `database` directly (not `src.database`) — it must be run with `src/` on the Python path, which `daily_run.py` handles via `subprocess.run(['python3', 'src/scraper.py'])` from the project root.
- The politeness delay in `scraper.py` uses `random.uniform(1, 3)` seconds between pages to avoid rate-limiting.
- `data/` is gitignored — the database and raw JSON files are not committed.
