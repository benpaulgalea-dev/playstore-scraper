"""Export every available Google Play review for one app to CSV."""

import csv

from google_play_scraper import Sort, reviews_all


APP_ID = "bov.bankingapp.android"
OUTPUT_FILE = "reviews.csv"

reviews = reviews_all(APP_ID, lang="en", country="mt", sort=Sort.NEWEST)
fields = [
    "reviewId",
    "userName",
    "content",
    "score",
    "reviewCreatedVersion",
    "at",
    "thumbsUpCount",
    "replyContent",
    "repliedAt",
]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    for review in reviews:
        row = {}
        for field in fields:
            row[field] = review.get(field)
        writer.writerow(row)

print(f"Saved {len(reviews)} reviews to {OUTPUT_FILE}")
