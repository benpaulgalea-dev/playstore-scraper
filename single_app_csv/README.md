# Single-app CSV proof of concept

This minimal version downloads all available reviews for one Google Play app
and writes them directly to `reviews.csv`.

1. Change `APP_ID` in `scrape_to_csv.py`.
2. Install the project requirement with `pip install -r ../requirements.txt`.
3. Run `python scrape_to_csv.py`.

The generated CSV is ignored by Git.
