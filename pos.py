import sqlite3
from datetime import datetime
import os

DB_NAME = os.path.join(os.path.dirname(__file__), 'pos.db')

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                sold_at TEXT NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
            """
        )
        conn.commit()

def add_product(name: str, price: float) -> None:
    """Add a new product to the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products(name, price) VALUES (?, ?)",
            (name, price)
        )
        conn.commit()

def list_products():
    """Return a list of all products."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM products")
        return cursor.fetchall()

def record_sale(product_id: int, quantity: int) -> None:
    """Record a sale for a given product."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sales(product_id, quantity, sold_at) VALUES (?, ?, ?)",
            (product_id, quantity, datetime.now().isoformat())
        )
        conn.commit()

def list_sales():
    """Return a list of all sales with product names."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT sales.id, products.name, sales.quantity, sales.sold_at
            FROM sales
            JOIN products ON products.id = sales.product_id
            ORDER BY sales.id
            """
        )
        return cursor.fetchall()

def main():
    create_tables()
    menu = ("""
Simple POS
1. Add product
2. List products
3. Record sale
4. View sales
5. Exit
Choose an option: """)
    while True:
        choice = input(menu)
        if choice == "1":
            name = input("Product name: ")
            price = float(input("Price: "))
            add_product(name, price)
            print("Product added.\n")
        elif choice == "2":
            for pid, name, price in list_products():
                print(f"{pid}: {name} - ${price:.2f}")
            print()
        elif choice == "3":
            product_id = int(input("Product ID: "))
            qty = int(input("Quantity: "))
            record_sale(product_id, qty)
            print("Sale recorded.\n")
        elif choice == "4":
            for sid, name, qty, sold_at in list_sales():
                print(f"{sid}: {name} x{qty} at {sold_at}")
            print()
        elif choice == "5":
            break
        else:
            print("Invalid option.\n")

if __name__ == "__main__":
    main()
