import sqlite3

def place_order():
    customer_id = int(input("Enter customer ID: "))
    pizza_id = int(input("Enter pizza ID: "))
    quantity = int(input("Enter quantity: "))

    conn = sqlite3.connect("pizza_store.db")
    cursor = conn.cursor()

    # Get pizza price
    cursor.execute("SELECT price FROM pizzas WHERE id = ?", (pizza_id,))
    result = cursor.fetchone()
    if result:
        price = result[0]
        total_price = price * quantity
        cursor.execute("INSERT INTO orders (customer_id, pizza_id, quantity, total_price) VALUES (?, ?, ?, ?)",
                       (customer_id, pizza_id, quantity, total_price))
        conn.commit()
        print(f"Order placed successfully! Total price: ${total_price:.2f}")
    else:
        print("Invalid pizza ID.")

    conn.close()