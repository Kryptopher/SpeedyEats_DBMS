import sqlite3

def add_pizza():
    name = input("Enter pizza name: ")
    size = input("Enter pizza size (Small/Medium/Large): ")
    price = float(input("Enter pizza price: "))

    conn = sqlite3.connect("pizza_store.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pizzas (name, size, price) VALUES (?, ?, ?)", (name, size, price))
    conn.commit()
    conn.close()
    print(f"Pizza '{name}' added successfully!")


def add_customer():
    name = input("Enter customer name: ")
    phone = input("Enter customer phone number: ")

    conn = sqlite3.connect("pizza_store.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()
    print(f"Customer '{name}' added successfully!")