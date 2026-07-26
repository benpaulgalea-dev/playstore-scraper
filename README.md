# Malta Play Store Review Scraper

A small Python scraper that downloads Google Play reviews for mobile apps
published by Malta-licensed banks and stores them in SQLite.

## Features

- Downloads reviews newest-first
- Saves each downloaded page immediately
- Avoids duplicate reviews on later runs
- Continues scraping the other apps if one app fails
- Stores results locally in `data/reviews.sqlite3`

## Setup

Python 3.10 or later is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Configuration

Edit `apps_to_scan.py` to change the display names, Google Play package IDs,
language, or country.

## Usage

```bash
python scrape_reviews.py
```

The local database is excluded from Git because reviews can contain personal
information. See `PYTHON_COMMANDS.md` for additional usage notes.

## Disclaimer

This project uses the unofficial `google-play-scraper` package. Use it
responsibly and comply with applicable terms, laws, and data-protection
requirements.
