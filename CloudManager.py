# services/CloudManager.py
import psycopg2
import os
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

CATEGORIES = {
    'Fruit': ['apple', 'banana', 'orange', 'pear', 'kiwi'],
    'Bakery': ['bread', 'croissant', 'baguette', 'cake'],
    'Drink': ['water', 'soda', 'beer', 'wine']
}

class CloudManager:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
        except Exception as e:
            print(f"Unable to connect to the database: {e}")
            self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            purchase_id VARCHAR(255) PRIMARY KEY,
            store VARCHAR(255),
            date DATE,
            total_price FLOAT
        );
        CREATE TABLE IF NOT EXISTS categories (
            category_id SERIAL PRIMARY KEY,
            category_name VARCHAR(255) UNIQUE
        );
        CREATE TABLE IF NOT EXISTS products (
            product_id VARCHAR(255),
            purchase_id VARCHAR(255) REFERENCES purchases(purchase_id),
            name VARCHAR(255),
            price FLOAT,
            category_id INTEGER REFERENCES categories(category_id)
        );
        """)
        self.connection.commit()

    def insert_category(self, category_name):
        cursor = self.connection.cursor()
        cursor.execute("""
        INSERT INTO categories (category_name) VALUES (%s)
        ON CONFLICT (category_name) DO NOTHING
        RETURNING category_id
        """, (category_name,))
        result = cursor.fetchone()
        self.connection.commit()
        if result:
            return result[0]
        else:
            cursor.execute("SELECT category_id FROM categories WHERE category_name = %s", (category_name,))
            return cursor.fetchone()[0]

    def insert_purchase(self, purchase_id, store, date, total_price):
        if not self.connection:
            raise Exception("No database connection")
        cursor = self.connection.cursor()
        cursor.execute("""
        INSERT INTO purchases (purchase_id, store, date, total_price)
        VALUES (%s, %s, %s, %s)
        """, (purchase_id, store, date, total_price))
        self.connection.commit()

    def insert_product(self, product_id, purchase_id, name, price, category):
        if not self.connection:
            raise Exception("No database connection")
        category_id = self.insert_category(category)
        cursor = self.connection.cursor()
        cursor.execute("""
        INSERT INTO products (product_id, purchase_id, name, price, category_id)
        VALUES (%s, %s, %s, %s, %s)
        """, (product_id, purchase_id, name, price, category_id))
        self.connection.commit()

def get_category(product_name):
    product_name = product_name.lower()
    for category, products in CATEGORIES.items():
        if product_name in products:
            return category
    return 'Unknown'
