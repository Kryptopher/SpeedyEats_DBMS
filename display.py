import sqlite3

def display_all_pizzas():
    conn = sqlite3.connect("pizza_store.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pizzas")
    pizzas = cursor.fetchall()
    conn.close()
    if pizzas:
        for pizza in pizzas:
            print(pizza)
    else:
        print("No pizzas in the database.")

def display_all_customers():
    conn = sqlite3.connect("pizza_store.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    conn.close()
    if customers:
        for customer in customers:
            print(customer)
    else:
        print("No customers in the database.")
