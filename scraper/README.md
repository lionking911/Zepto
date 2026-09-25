
# Book Scraper

A Python-based web scraper that extracts book data from [books.toscrape.com](https://books.toscrape.com/) and stores it in a SQLite database.

## Overview

This project scrapes book information including titles, ratings, prices (in GBP and INR), and availability status. The data is organized by categories and stored in a relational SQLite database for easy querying and analysis.

## Features

- **Web Scraping**: Fetches book data from books.toscrape.com using BeautifulSoup
- **Error Handling**: Comprehensive exception handling for HTTP errors, connection issues, and timeouts
- **SQLite Database**: Stores scraped data with proper schema and relationships
- **Data Analysis**: Performs complex SQL queries (JOIN, WHERE, ORDER BY, GROUP BY, etc.)
- **Pandas Integration**: Provides additional data manipulation and analysis capabilities
- **Text Encoding Fix**: Uses ftfy library to handle text encoding issues
- **Currency Conversion**: Converts prices from GBP to INR (conversion rate: £1 = ₹105.50)

## Technical Details

### Database Schema

#### `categories` Table
- `id` (INTEGER, PRIMARY KEY)
- `title` (TEXT, NOT NULL)
- `link` (TEXT, UNIQUE)
- `scraped_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

#### `product_details` Table
- `id` (INTEGER, PRIMARY KEY)
- `title` (TEXT, NOT NULL)
- `rating` (INTEGER, 1-5 stars)
- `price_pound` (REAL, in GBP)
- `price_inr` (REAL, converted to INR)
- `availability` (BOOLEAN)
- `categorie_id` (INTEGER, FOREIGN KEY)

### Key Functions

| Function | Purpose |
|----------|---------|
| `fetch_url(url)` | Sends HTTP GET requests with timeout and error handling |
| `db_connect(db)` | Establishes SQLite database connection |
| `db_create_table(conn, cursor, query)` | Creates database tables using SQL queries |
| `db_insert_list(conn, cursor, query, data)` | Inserts multiple records using `executemany()` |
| `db_fetch_all(cursor, query)` | Retrieves all matching records from database |
| `db_fetch_one(cursor, query)` | Retrieves a single record from database |

## Queries Included

1. **Query 1**: Count total products in database
2. **Query 2**: Products with specific ratings and price range (WHERE, IN, BETWEEN, ORDER BY, LIMIT)
3. **Query 3**: Top 10 highest-rated books per category (WITH, ROW_NUMBER, PARTITION BY, INNER JOIN)
4. **Query 4**: All products with categories (LEFT JOIN)
5. **Query 5**: All categories with products (RIGHT JOIN)
6. **Query 6**: Complete product-category relationship (FULL OUTER JOIN)
7. **Pandas Queries**: Same operations using pandas DataFrames and merge operations

## Dependencies

```
requests
beautifulsoup4
ftfy
pandas
tabulate
sqlite3 (built-in)
```

## Usage

```bash
python scraper.py
```

### First Run
- Fetches the main page and all category pages
- Extracts book information
- Stores data in SQLite database
- Creates local HTML cache in `scraped_html/` directory

### Subsequent Runs
- Uses cached HTML files if available
- Runs all analytical queries on existing data
- Displays results in formatted tables

## Output

The script generates formatted tables showing:
- Available books by rating and price range
- Top-rated books per category
- Various JOIN operations results
- Pandas-based analysis

## Project Constraints

- Limited to **3 categories**
- Maximum **60 books** per category
- Uses **sidebar navigation** for category discovery
- Timeout limit: **10 seconds per request**

## File Structure

```
scraper/
├── scraper.py           # Main scraper script
├── scraped_html/        # Cached HTML files (auto-generated)
│   ├── index.html
│   └── category_pages/
└── bookscrap.db         # SQLite database file (auto-generated)
```

## Error Handling

The scraper handles the following exceptions:
- **HTTPError**: Invalid HTTP responses (404, 500, etc.)
- **ConnectionError**: Network or DNS issues
- **Timeout**: Server response delay
- **RequestException**: Other request-related errors
- **SQLite3.Error**: Database operation failures

## Notes

- HTML content is cached locally to reduce network requests
- Text encoding issues are automatically fixed using ftfy
- All prices are rounded to 2 decimal places
- Results are displayed using the tabulate library for clean formatting
