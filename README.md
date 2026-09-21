# Zepto
3 in 1 project

#1 st stage
#Tasks
#Using the requests and BeautifulSoup libraries, scrape all books listed across at least 3 different book categories (or, if you prefer, the first 5 paginated listing pages of the "All products" catalogue — either scope is #acceptable as long as your final dataset has at least 60 books). For each book capture: title, price (as listed, in GBP), star_rating (as text, e.g. "Three"), availability (as listed text), and category.

#Clean the scraped fields into proper types:

#Strip the currency symbol from price and convert it to a float column price_gbp.
#Convert the text star rating (One…Five) into an integer column rating (1–5).
#Parse the availability text into a boolean column in_stock.
#If any field fails to parse for a given row (e.g., unexpected text), handle it with the median-imputation approach for numeric fields or drop the row (state and justify your choice) — do not leave the pipeline crashing on #messy rows.

#Convert price_gbp to a price_inr column using the project's fixed baseline conversion rate: 1 GBP = 105.50 INR. This is an artificial, project-defined constant for this assignment, not a live or historical market rate, so it #never needs a lookup or a date reference. This fixed-rate conversion is the required, keyless baseline and is what gets graded for this task — it requires no external API call and no network access; simply state this exact #rate in your README. (Optional, ungraded stretch — must not affect your required submission: if you want extra practice with the requests library and explicit HTTP status-code handling, you may additionally look up any free, #keyless currency-conversion API of your own choosing, check its response status code explicitly, and fall back to the fixed rate above on any failure. This is entirely optional; your price_inr column must be fully correct #using only the required fixed-rate baseline, since that path alone is what gets graded.)

#Design a normalized SQLite schema with at least two tables sharing a primary/foreign key relationship, for example:

#categories(category_id INTEGER PRIMARY KEY, category_name TEXT UNIQUE)
#books(book_id INTEGER PRIMARY KEY, title TEXT, price_gbp REAL, price_inr REAL, rating INTEGER, in_stock INTEGER, category_id INTEGER REFERENCES categories(category_id))
#(You may rename columns/tables, but the two-table PK/FK structure is required.)

#Using Python's sqlite3 (or pandas.DataFrame.to_sql), insert your cleaned, converted data into this schema. Then write and execute at least 5 SQL queries against the database that collectively demonstrate: SELECT/WHERE, ORDER #BY, LIMIT, DISTINCT, and (IN or BETWEEN) — plus at least one JOIN between your two tables (e.g., "list the 10 highest-rated books per category"). Save each query string and its output.

#Read back at least two of the above query results into pandas DataFrames using pd.read_sql(...), and separately reproduce the join-query's result using pd.merge(...) directly on your in-memory DataFrames (no SQL) — show that #both approaches produce equivalent output.

#Acceptance criteria (your submission is complete when…)
#The scraping script/notebook runs end to end without manual copy-pasting and yields ≥ 60 book rows across ≥ 3 categories.
##price_gbp, rating (int 1–5), in_stock (bool), and price_inr columns are all present and correctly typed; price_inr is computed from the required fixed-rate baseline (1 GBP = 105.50 INR, a fixed project-defined constant with #no date reference), with that exact rate stated in the README.
#The repository includes the SQLite database file or the exact script that regenerates it from scratch, implementing the two-table PK/FK schema described above.
#≥ 5 SQL queries are present with their printed/logged output, collectively covering every required clause, plus at least one JOIN.
#The pd.read_sql and pd.merge outputs for the join query are shown side by side and match.
#README documents install/run steps and any parsing/cleaning decisions you made.
#The overall repository's commit history shows a feature branch created, committed to at least twice, and merged back into main — checked once across the whole repository, not per module.
