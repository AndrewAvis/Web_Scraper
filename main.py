# Author: Andrew Avis
# Date:
# Assignment: Final Project:
# Class: Data Structures

import sqlite3

class Game:
    def __init__(self, _upc, _sku, _product_id, _title, _base_price, _condition, _category_id):
        # Constructor for the Game class
        self.upc = _upc
        self.sku = _sku
        self.product_id = _product_id
        self.title = _title
        self.base_price = _base_price
        self.condition = _condition
        self.category_id = _category_id

    def peek_data(self):
        # Print information about the Game object
        print(type(self.upc), self.upc)
        print(type(self.sku), self.sku)
        print(type(self.product_id), self.product_id)
        print(type(self.title), self.title)
        print(type(self.base_price), self.base_price)
        print(type(self.condition), self.condition)
        print(type(self.category_id), self.category_id)

# GameStop API URL and SQLite database connection
gamestop_api_url = "https://www.gamestop.com/on/demandware.store/Sites-gamestop-us-Site/default/Tile-ShowJSON?pid="
gamestop_connection = sqlite3.connect("gamestop.db")
# Define minimum and maximum SKU values
MIN_SKU = 400246
MAX_SKU = 500000


if __name__ == "__main__":
    # Import necessary functions for database initialization and GUI setup
    from setup_db import init_database
    from setup_gui import init_user_interface

    # Initialize the database with GameStop API data
    start_db_file = init_database(gamestop_api_url, gamestop_connection, MIN_SKU, MAX_SKU)
    # Check if the database initialization was successful
    if start_db_file == True:
        print("Press Start")
    # Initialize the user interface
    start_gui = init_user_interface()





