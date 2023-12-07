import sqlite3
from gamestop_scraper import gamestop_scrape_backend, loop_gamestop_scrape


def init_database(url, connection, min_sku, max_sku):
    # Initialize the database
    if is_database_valid(url, connection, min_sku, max_sku) is True:
        add_record_input = str(input(f"Would you like to add more records? ('Y' or 'N'):"))
        if add_record_input.lower() == "y":
            #Call func to scrape
            loop_gamestop_scrape(url, connection, min_sku, max_sku)
        return True

    elif is_database_valid(url, connection, min_sku, max_sku) is False:
        # Create table then scrape
        create_table(connection)
        loop_gamestop_scrape(url, connection, min_sku, max_sku)
        return True

    else:
        print("Error occurred")
        return None


def is_database_valid(url, connection, min_sku, max_sku):
    # Check if the database is valid
    cursor = connection.cursor()
    try:
        cursor.execute("PRAGMA table_info(games)")
        sku_count = cursor.fetchone()
        update_input = str(input(f"Total SKUs: {sku_count[0]}\nWould you like to update records?('Y' or 'N') :"))
        if update_input.lower() == 'y':
            update_records(url, connection)
        return True

    except sqlite3.OperationalError as e:
        print(e)
        return False



def create_table(connection):
    # Create the 'games' table if it does not exist
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
               Id INTEGER PRIMARY KEY AUTOINCREMENT,
               Upc TEXT NOT NULL,
               Sku INTEGER NOT NULL,
               Product_Id TEXT NOT NULL,
               Title TEXT,
               Price FLOAT NOT NULL,
               Condition TEXT NOT NULL,
               Category_id TEXT,
               Last_Updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        
           )
    ''')


def drop_table(connection):
    # Drop the 'games' table if it exists
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS games
    ''')
    connection.commit()


def insert_data(connection, data):
    # Insert data into the 'games' table
    cursor = connection.cursor()
    cursor.execute(''' 
    INSERT INTO games (Upc, Sku, Product_Id, Title, Price, Condition, Category_id, Last_Updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (data.upc, data.sku, data.product_id, data.title, data.base_price, data.condition, data.category_id))

    connection.commit()


def get_record_upc(upc):
    # Retrieve a record by UPC
    connection = sqlite3.connect("gamestop.db")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM games WHERE Upc = ?', (upc,))
    record = cursor.fetchone()
    connection.close()

    return record


def get_record_sku(sku):
    # Retrieve a record by SKU
    connection = sqlite3.connect("gamestop.db")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM games WHERE Sku = ?', (int(sku),))
    record = cursor.fetchone()
    connection.close()

    return record

def update_records(url, connection):
    # Update records by scraping data from URL
    cursor = connection.cursor()
    cursor.execute('SELECT Sku FROM games')
    all_skus = cursor.fetchall()

    for sku_tuple in all_skus:
        sku = sku_tuple[0]
        scrapped_data = gamestop_scrape_backend(url, sku)
        if scrapped_data:
            existing_record = get_record_sku(sku)  # Get the existing record from the database
            if existing_record:
                # Record already exists, update it
                update_data(connection, scrapped_data)
                print(f"Sku:{scrapped_data.sku} updated")
            else:
                # Record does not exist, insert it
                insert_data(connection, scrapped_data)
                print(f"Sku:{scrapped_data.sku} added")
        elif scrapped_data is None:
            continue

def update_data(connection, data):
    # Update data in the 'games' table
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE games
        SET Upc=?, Product_Id=?, Title=?, Price=?, Condition=?, Category_id=?, Last_Updated=CURRENT_TIMESTAMP
        WHERE Sku=?
    ''', (data.upc, data.product_id, data.title, data.base_price, data.condition, data.category_id, data.sku))

    connection.commit()



