# Book Scraper and SQLite Analytics

A Python project that scrapes book data from [books.toscrape.com](https://books.toscrape.com/) and stores it in a SQLite database for analysis.

## Overview

This script downloads the main catalog page and selected category pages, extracts book details, saves the HTML locally for reuse, and stores the data in a SQLite database. It also runs several SQL and pandas-based queries to demonstrate filtering, aggregation, and join operations.

The project is designed to:
- collect book title, rating, price, and availability
- convert GBP prices to INR using a fixed rate
- organize books by category
- manage local HTML caching for repeat runs
- run analytical queries against the generated SQLite data

## Features

- Web scraping using `requests` and `BeautifulSoup`
- HTML caching in a local folder to avoid repeated downloads
- SQLite database creation and insert helpers
- Data cleaning with `ftfy`
- Currency conversion: `GBP -> INR` using `£1 = ₹105.50`
- Query examples using SQL and pandas
- Console output formatted with `tabulate`

## Database Schema

### `categories`

- `id` (INTEGER, PRIMARY KEY AUTOINCREMENT)
- `title` (TEXT, NOT NULL)
- `link` (TEXT, UNIQUE)
- `scraped_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

### `product_details`

- `id` (INTEGER, PRIMARY KEY AUTOINCREMENT)
- `title` (TEXT, NOT NULL)
- `rating` (INTEGER)
- `price_pound` (REAL)
- `price_inr` (REAL)
- `availability` (BOOLEAN)
- `categorie_id` (INTEGER)
- `FOREIGN KEY (categorie_id) REFERENCES categories(id)`

## Key Functions

| Function | Purpose |
|----------|---------|
| `fetch_url(url)` | Sends an HTTP GET request with timeout and error handling |
| `db_connect(db)` | Connects to the SQLite database |
| `db_create_table(conn, cursor, query)` | Creates a table from a SQL query |
| `db_insert_list(conn, cursor, query, data)` | Inserts multiple rows using `executemany()` |
| `db_fetch_all(cursor, query)` | Returns all rows from a SQL query |
| `db_fetch_one(cursor, query)` | Returns the first value from a query result |

## What the Script Does

On the first run, the script:
1. fetches the homepage from `books.toscrape.com`
2. extracts category links from the sidebar navigation
3. creates the `categories` table if needed
4. saves the homepage HTML to a local cache
5. downloads selected category pages
6. saves those category pages locally
7. creates the `product_details` table if needed
8. inserts book records into SQLite

On later runs, it checks whether the database and cached HTML already exist. If they do, it reuses them and runs the analysis queries without scraping again.

## Query Examples Included

The script demonstrates:

1. Total record count in `product_details`
2. Count of products per category (`GROUP BY`)
3. Books with a specific rating and price range (`WHERE`, `IN`, `BETWEEN`, `ORDER BY`, `LIMIT`)
4. Top 10 highest-rated books per category using `ROW_NUMBER()` and `PARTITION BY`
5. Left join analysis
6. Right join analysis
7. Full outer join pattern example
8. Equivalent analysis using pandas `merge()` and `groupby()`

## Dependencies

```bash
requests
beautifulsoup4
ftfy
pandas
tabulate
sqlite3
```

## Usage

From the repo root:

```bash
python data_pipeline/scraper.py
```

Or from inside the folder:

```bash
cd data_pipeline
python scraper.py
```

## Output Files

The script creates the following local files in the project folder:

```text
data_pipeline/
├── scraper.py
├── bookscrap.db
├── scraper_html/
│   ├── index.html
│   └── category_pages / (stored by URL suffix)
└── README.md
```

Note: the script currently names the cache folder `scraper_html` and the database `bookscrap.db`, so those are the actual generated artifacts in this version.

## Error Handling

The script includes exception handling for:
- `HTTPError`
- `ConnectionError`
- `Timeout`
- `RequestException`
- `sqlite3.Error`

## Notes

- The script uses a timeout of 10 seconds for HTTP requests.
- It fixes text encoding issues with `ftfy` before inserting titles.
- It stores prices in both GBP and INR.
- It formats output to the console using `tabulate`.
- The current implementation loads the first few category pages when the database is empty, which is reflected in the code logic.

## Project Status

This version is a working SQLite + web scraping demo focused on extracting structured data and analyzing it with SQL and pandas. It is useful as a learning project and a simple data pipeline example.
