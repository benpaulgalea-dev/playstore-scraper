# Commands

Run these commands from the project folder.

## Create the Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

The first command creates an isolated environment. Run the second whenever you
open a new Terminal window.

## Install the scraper

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

This installs the unofficial Google Play review scraper. SQLite is included
with Python.

## Choose the apps

Edit `apps_to_scan.py`. Each entry contains a display name and Google Play
package ID. `LANGUAGE` and `COUNTRY` control the Google Play review market.

## Run the scraper

```bash
python scrape_reviews.py
```

The scraper starts with the newest reviews, saves every page immediately to
`data/reviews.sqlite3`, and stops when it reaches reviews already stored.
The first run retrieves all pages Google Play exposes; later runs only collect
new pages.

## Read reviews in Python

```python
from database import connect, read_reviews

with connect() as database:
    all_reviews = read_reviews(database)
    bov_reviews = read_reviews(database, "bov.bankingapp.android")
```

## Stop the environment

```bash
deactivate
```

## Start again later

```bash
source .venv/bin/activate
python scrape_reviews.py
```
