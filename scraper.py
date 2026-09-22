import requests
import os
import ftfy
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

pound_to_inr = 105.50 #conversation rate from pound to inr
# using response and BeautifulSoup to fetch the HTML content of the main page and parse it to extract the categories and their links. The extracted data is then stored in a SQLite database for further processing.
# considering the constraints like 3 categories and 60 books
# considered side bar for getting categories  using link got the book details and stored in database with the required fields 
# using  of select,list,order by,where,distinct,join clause's

url="https://books.toscrape.com/"
def fetch_url(url):
    # 1. Use a try-except block to handle potential exceptions during the request
    # 2. function returns the HTML content of the page if successful, or an error message if not.
    try:
        print(f"Sending request to {url}...")
        
        # 1. Send GET request with a timeout (Crucial to prevent your script from hanging forever)
        # timeout=10 means if the server doesn't respond in 10 seconds, raise a Timeout error.
        response = requests.get(url, timeout=10)
        
        # 2. Automatically raises an HTTPError if the response was a 404 (Not Found) or 500 (Server Error)
        response.raise_for_status()
        
        # 3. If no errors occurred, fetch the HTML content

        return response.text
        
        
    except HTTPError as http_err:
        # Catches 404 Not Found, 403 Forbidden, 500 Internal Server Error, etc.
        error=f"HTTP error occurred (Status Code: {response.status_code}): {http_err}"

    except ConnectionError as conn_err:
        # Catches network failures, wrong DNS, or if the server refused to connect
        error=f"Connection error occurred (Check your internet or server availability): {conn_err}"

    except Timeout as timeout_err:
        # Catches instances where the server took too long to send data back
        error=f"Timeout error occurred (Server took too long to respond): {timeout_err}"

    except RequestException as req_err:
        # Ambiguous exception that handles any other requests-related errors
        error=f"An error occurred while handling your request: {req_err}"

    except Exception as e:
        # Catches any other standard Python logic errors
        error=f"An unexpected error occurred: {e}"
    return error

def db_connect(db):
    # function to connect to the SQLite database and return the connection and cursor objects. It also handles exceptions related to database connection issues.
    conn = None

    try:
        # 1. Connect to the database (Set a timeout to avoid database locked errors)
        conn = sqlite3.connect(db, timeout=5)
        cursor = conn.cursor()
        print("Successfully connected to the database.")
        return conn, cursor
     

    except sqlite3.Error as e:
        # Catches all SQLite specific errors (e.g., syntax errors, permission denied)
        return f"SQLite Error occurred: {e}"

    except Exception as e:
        # Catches any other unexpected Python errors
        return f"An unexpected error occurred: {e}"

   

def db_create_table(conn, cursor,query):

    # function to create a table in the SQLite database using the provided SQL query. It handles exceptions related to database operations.

    try:
        cursor.execute(query)
        
        # 3. Commit the changes
        conn.commit()
        print("Table created successfully (or it already exists).")

    except sqlite3.Error as e:
        # Catches all SQLite specific errors (e.g., syntax errors, permission denied)
        print(f"SQLite Error occurred: {e}")

    except Exception as e:
        # Catches any other unexpected Python errors
        print(f"An unexpected error occurred: {e}")


def db_insert_list(conn, cursor ,query, data):
    # function to insert multiple records into a SQLite database table using the provided SQL query and data. It handles exceptions related to database operations.
    try:
       
        
        # executemany 
        cursor.executemany(query, data)
        
        
        conn.commit()
        print(f"inserted successfully {cursor.rowcount} new records!")
        
    except sqlite3.Error as e:
        # Catches all SQLite specific errors (e.g., syntax errors, permission denied)
        print(f"SQLite Error occurred: {e}")

    except Exception as e:
        # Catches any other unexpected Python errors
        print(f"An unexpected error occurred: {e}")

def db_fetch_all(cursor, query):
    # function to fetch all records from a SQLite database table using the provided SQL query. returns results as a list. It handles exceptions related to database operations.
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"SQLite Error occurred: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
    
def db_fetch_one(cursor, query):
    # function to fetch single row output from a SQLite database table using the provided SQL query. returns results as a element. It handles exceptions related to database operations.
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]
    except sqlite3.Error as e:
        print(f"SQLite Error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None



if __name__ == "__main__":
    verify_dir = "scraped_html/index.html"
    conn, cursor = db_connect("bookscrap.db")
            
    if not os.path.exists(verify_dir):
        html_content = fetch_url(url) # fetch the HTML content of the main page
        categories = []
        if "error" in html_content: # check if errors occurred during the fetch operation
            print(html_content)  # Print the error message
            exit
        else:
            with open("scraped_html/index.html", "w", encoding="utf-8") as file: # write the fetched HTML content to a local file for future use
                file.write(html_content)
            soap = BeautifulSoup(html_content, 'html.parser') # parse the HTML content using BeautifulSoup to extract the categories and their links
        
            for link in soap.select('ul.nav-list ul li a'):
                categories.append((link.text.strip(), link.get('href')))
            
            print("Successfully downloaded the webpage content!")
            #print(categories)

            query = """CREATE TABLE IF NOT EXISTS categories (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                link TEXT UNIQUE,
                                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )"""
            db_create_table(conn, cursor, query)
            query = "INSERT OR IGNORE INTO categories (title, link) VALUES (?, ?)"
            db_insert_list(conn, cursor, query, categories)
            query_products =  """CREATE TABLE IF NOT EXISTS product_details (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            title TEXT NOT NULL,
                                            rating INTEGER,
                                            price_pound REAL,
                                            price_inr REAL,
                                            availability BOOLEAN,
                                            categorie_id INTEGER,
                                            FOREIGN KEY (categorie_id) REFERENCES categories(id)
                                        )"""        
            db_create_table(conn, cursor, query_products)
            products = []
            for i in range(4):
                category,url_sufix=categories[i]
                products_list=fetch_url(url+url_sufix)
                if "error" in products_list:
                        print(products_list)  # Print the error message
                else:
                        sufix= url_sufix.replace('/',"_")
                        path = f"scraped_html/{sufix}"
                        with open(path, "w", encoding="utf-8") as file:
                                    file.write(products_list)
                        print("Successfully downloaded the webpage content!")
    else:
        print("Using existing HTML files.")
        products=[]
        number_check={ 
                        "One":1,
                        "Two":2,
                        "Three":3,
                        "Four":4,
                        "Five":5
                      }
        # query 1
        q1="select count(*) from product_details;" # select clause for retrieving the count of records in the product_details table to 
        fetch_one=db_fetch_one(cursor, q1)
        print(fetch_one)
        if fetch_one==0:

            query = "select id,link from categories LIMIT 4 " # select clause for retrieving the ID and link of categories with limit of 4 records
            fetch_all=db_fetch_all(cursor, query)
            print(fetch_all)
            for link in fetch_all:
                id,html_link=link
                html_link="scraped_html"+'/'+html_link.replace('/',"_")
                with open(html_link, "rb") as file:
                    soap = BeautifulSoup(file, "html.parser")
                for link in soap.select('article.product_pod'):
                    rateings=number_check.get(link.contents[3].get('class')[1])
                    title=link.contents[5].contents[0].text.strip()
                    fixed_text = ftfy.fix_text(title) # using ftfy library to fix any text encoding issues in the title of the product.
                    clean_text = fixed_text.encode('utf-8', errors='ignore').decode('utf-8')
                    price_gbp=float(link.contents[7].contents[1].text.replace("Â£","")) # remove the pound symbol and convert the price to a float for further calculations.
                    price_inr=round(price_gbp*pound_to_inr,2) # convert the price from GBP to INR using the conversion rate and round it to 2 decimal places for display.
                    in_stock=link.contents[7].contents[3].text.strip()
                    if in_stock=="In stock":
                        status=bool(1)
                    else:
                        status=bool(0)
                    categ_id=id
                    products.append((clean_text,rateings,price_gbp,price_inr,status,categ_id))
            #print(len(products))
            #print(products)
            query = "INSERT OR IGNORE INTO product_details (title, rating, price_pound, price_inr, availability, categorie_id) VALUES (?, ?, ?, ?, ?, ?)"
            db_insert_list(conn, cursor, query, products)
    # using where ,in , order by ,limt
    # query 2
    query = "SELECT title, price_inr FROM product_details WHERE availability = 1 AND rating IN (1, 5) ORDER BY price_inr DESC LIMIT 5" # using select,where,order by,group by,in clause to retrieve the top 5 most expensive available products from the product_details table and display their titles and prices in INR.
    results = db_fetch_all(cursor, query)
    print('--'*32)    
    print(" price,title with rating in(1,5)")
    print('--'*32)  
    headers = [description[0] for description in cursor.description]   
    print(tabulate(results, headers=headers, tablefmt="plain", maxcolwidths=[None, None, 30]))
    



    #for i in results:
       #print(f"Title: {i[0]}, Price (INR): {i[1]}")
    #query="SELECT  categories.title as category,product_details.rating as rating,product_details.title title FROM categories inner JOIN product_details ON categories.id = product_details.categorie_id where (select count(*) from product_details as d where d.categorie_id=product_details.categorie_id and d.rating>product_details.rating order by d.title asc,d.rating limit 10) < 10    order by categories.title asc,product_details.rating  desc ; " # using distinct,select,between,join  to retrieve the count of products for each category from the product_details table and display the category title along with the corresponding product count.
    #query 3
    query="""WITH RankedBooks AS (
    SELECT  
        categories.title AS category,
        product_details.rating AS rating,
        product_details.title AS title,
        ROW_NUMBER() OVER (
            PARTITION BY product_details.categorie_id 
            ORDER BY CAST(product_details.rating AS NUMERIC) DESC, product_details.title ASC
        ) AS row_num 
    FROM categories 
    INNER JOIN product_details ON categories.id = product_details.categorie_id
)
SELECT category,  title,rating
FROM RankedBooks
WHERE row_num <= 10
ORDER BY category ASC, rating DESC;
"""

    results = db_fetch_all(cursor, query)
    print('--'*32)
    print("the 10 highest-rated books per category from sqlite3 python")
    print('--'*32)    
    headers = [description[0] for description in cursor.description]   
    print(tabulate(results, headers=headers, tablefmt="plain", maxcolwidths=[None, None, 30]))
    #for i in results:
       # print(f"Category: {i[0]} rateing :{i[1]}  title :{i[2]}")
    #query 4 left join
    query=" select a.title ,b.title as category from product_details a left join categories b on a.categorie_id=b.id;"
    results = db_fetch_all(cursor, query)
    print('--'*32)
    print("left join ")
    print('--'*32)    
    headers = [description[0] for description in cursor.description]   
    print(tabulate(results, headers=headers, tablefmt="plain", maxcolwidths=[None, None, 30]))
    # query 5 right join
    query=" select a.title,b.title as category from product_details a right join categories b on a.categorie_id=b.id;"
    results = db_fetch_all(cursor, query)
    print('--'*32)
    print("right join ")
    print('--'*32)    
    headers = [description[0] for description in cursor.description]   
    print(tabulate(results, headers=headers, tablefmt="plain", maxcolwidths=[None, None, 30]))
    # query 6  full outer join
    query=" select a.title,b.title as category from product_details a full outer join categories b on a.categorie_id=b.id;"
    results = db_fetch_all(cursor, query)
    print('--'*32)
    print("full outer join ")
    print('--'*32)    
    headers = [description[0] for description in cursor.description]   
    print(tabulate(results, headers=headers, tablefmt="plain", maxcolwidths=[None, None, 30]))



# using panda for sqlite
    query="select id,title from categories ;"
    categories_df=pd.read_sql(query, conn)
    #print(categories_df.to_string(index=False))

    query="select id,title,price_inr,availability,rating,categorie_id from product_details order by price_inr desc;"
    product_details_df=pd.read_sql(query, conn)
    #print(product_details_df.to_string(index=False))

    merge=pd.merge(product_details_df, categories_df, left_on='categorie_id', right_on='id',how='inner')
    merge.drop(columns=['id_y','categorie_id'], inplace=True)
    #print(merge.to_string(index=False))

    #list the 10 highest rated books for each category"
      
    merge["rating"] = pd.to_numeric(merge["rating"], errors="coerce")
    sorted_merge = merge.sort_values(by="rating", ascending=False)
    result = sorted_merge.groupby("title_y").head(10)
    final_result = result[["title_y", "title_x", "rating"]]
    final_result = final_result.sort_values(by=["title_y", "rating"], ascending=[True, False])
    print('--'*32)
    print("the 10 highest-rated books per category using pandas")
    print('--'*32) 
    final_result.rename(columns={"title_y":"categories","title_x":"title"},inplace=True)
    print(final_result.to_string(index=False))

    # panda left join
    left_join=pd.merge(product_details_df, categories_df, left_on='categorie_id', right_on='id',how='left')
    left_join.drop(columns=['id_y','id_x',"price_inr","availability",'rating','categorie_id'], inplace=True)
    print('--'*32)
    print("left join using pandas")
    print('--'*32) 
    left_join.rename(columns={"title_y":"categories","title_x":"title"},inplace=True)
    print(left_join.to_string(index=False))

    # panda right join
    right_join=pd.merge(product_details_df, categories_df, left_on='categorie_id', right_on='id',how='right')
    right_join.drop(columns=['id_y','id_x',"price_inr","availability",'rating','categorie_id'], inplace=True)
    print('--'*32)
    print("right join using pandas")
    print('--'*32) 
    right_join.rename(columns={"title_y":"categories","title_x":"title"},inplace=True)
    print(right_join.to_string(index=False))
    conn.close()      