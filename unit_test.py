import unittest
import sqlite3
from unittest.mock import patch
from setup_db import init_database, is_database_valid, create_table, drop_table, insert_data
from main import Game


class TestSetupDB(unittest.TestCase):

    def setUp(self):
        # Create an in-memory database for testing
        self.test_connection = sqlite3.connect(":memory:")
        create_table(self.test_connection)

    def tearDown(self):
        # Close the in-memory database
        self.test_connection.close()

    def test_init_database_existing_database(self):
        # Test initializing an existing database
        with patch("builtins.input", return_value="N"):
            result = init_database("test_url", self.test_connection, 1, 100000)
            self.assertTrue(result)

    def test_init_database_new_database(self):
        # Test initializing an existing database
        with patch("builtins.input", return_value="N"):
            drop_table(self.test_connection)
            result = init_database("https://www.gamestop.com/on/demandware.store/Sites-gamestop-us-Site/default/Tile-ShowJSON?pid=", self.test_connection, 344868, 344868)
            self.assertTrue(result)

    def test_is_database_valid_valid(self):
        # Test checking the validity of a valid database
        cursor = self.test_connection.cursor()
        cursor.execute("INSERT INTO games (Upc, Sku, Product_Id, Title, Price, Condition, Category_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       ("12345", 1, "P123", "Test Game", 49.99, "New", "video-games"))
        self.test_connection.commit()

        with patch("builtins.input", return_value="N"):
            result = is_database_valid("test_url", self.test_connection, min_sku=123456, max_sku=123456)
            self.assertTrue(result)

    def test_is_database_valid_invalid(self):
        # Test checking the validity of an invalid database
        with patch("builtins.input", return_value="N"):
            result = is_database_valid("test_url", self.test_connection,min_sku=123456, max_sku=123456)
            self.assertTrue(result)

    def test_create_table(self):
        # Test creating a table and checking its columns
        create_table(self.test_connection)
        cursor = self.test_connection.cursor()
        cursor.execute("PRAGMA table_info(games)")
        columns = cursor.fetchall()
        self.assertEqual(len(columns), 9)

    def test_insert_data(self):
        # Test inserting data into the database
        data = Game("12345", 1, "P123", "Test Game", 49.99, "New", "video-games")
        insert_data(self.test_connection, data)
        cursor = self.test_connection.cursor()
        cursor.execute("SELECT * FROM games WHERE Sku=?", (1,))
        result = cursor.fetchone()
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()