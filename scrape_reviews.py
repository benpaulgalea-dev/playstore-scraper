"""Download every available review for the configured banking apps."""

import time

from google_play_scraper import Sort, reviews

from apps_to_scan import APPS, COUNTRY, LANGUAGE
from database import connect, count_reviews, newest_review_date, save_reviews


PAGE_SIZE = 200
MAX_RETRIES = 4


def download_page(app_id, continuation_token):
    """Download one page, retrying temporary failures."""
    for attempt in range(MAX_RETRIES):
        try:
            return reviews(
                app_id,
                lang=LANGUAGE,
                country=COUNTRY,
                sort=Sort.NEWEST,
                count=PAGE_SIZE,
                continuation_token=continuation_token,
            )
        except Exception:
            if attempt == MAX_RETRIES - 1:
                raise
            wait = 2**attempt
            print(f"    Request failed; retrying in {wait}s.", flush=True)
            time.sleep(wait)


def scrape_app(connection, app_name, app_id):
    """Scrape one app and commit each page immediately."""
    previous_newest = newest_review_date(connection, app_id)
    continuation_token = None
    page_number = 0
    new_total = 0

    while True:
        page, next_token = download_page(app_id, continuation_token)
        page_number += 1
        inserted = save_reviews(connection, app_name, app_id, page)
        new_total += inserted
        print(
            f"    Page {page_number}: {len(page)} downloaded, "
            f"{inserted} new, {count_reviews(connection, app_id)} stored",
            flush=True,
        )

        if not page or next_token is None:
            break

        page_dates = [
            review["at"].isoformat()
            for review in page
            if review.get("at")
        ]
        reached_old_data = (
            previous_newest
            and page_dates
            and min(page_dates) <= previous_newest
            and inserted == 0
        )
        if reached_old_data:
            print("    Reached reviews already stored; stopping.", flush=True)
            break
        continuation_token = next_token

    return new_total


def scrape_apps(apps=APPS):
    """Scrape the supplied list without command-line arguments."""
    started = time.monotonic()
    failures = []

    with connect() as connection:
        for position, (app_name, app_id) in enumerate(apps, start=1):
            print(f"[{position}/{len(apps)}] {app_name}", flush=True)
            try:
                added = scrape_app(connection, app_name, app_id)
                print(f"    Complete: {added} new reviews.", flush=True)
            except Exception as error:
                failures.append((app_name, str(error)))
                print(f"    Failed: {error}", flush=True)

        print(
            f"Finished with {count_reviews(connection)} reviews in "
            f"{time.monotonic() - started:.1f}s.",
            flush=True,
        )

    if failures:
        print("\nFailed apps:")
        for app_name, error in failures:
            print(f"  {app_name}: {error}")


if __name__ == "__main__":
    scrape_apps()
