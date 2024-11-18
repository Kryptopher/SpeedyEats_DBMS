from create_tables import create_tables
from display import display_table


import sqlite3

# Database connection setup
def connect_db():
    return sqlite3.connect("speedy_eats.db")

# Common Input Helper
def get_input(fields):
    return tuple(input(f"Enter {field}: ") for field in fields)

# Operations for each table
def add_record(cursor, table, fields):
    values = get_input(fields)
    placeholders = ", ".join(["?"] * len(fields))
    query = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})"
    cursor.execute(query, values)
    print(f"Record added to {table}.")

def update_record(cursor, table, id_field, id_value, fields):
    values = get_input(fields)
    set_clause = ", ".join([f"{field} = ?" for field in fields])
    query = f"UPDATE {table} SET {set_clause} WHERE {id_field} = ?"
    cursor.execute(query, (*values, id_value))
    print(f"Record in {table} updated.")

def delete_record(cursor, table, id_field):
    id_value = input(f"Enter {id_field} to delete: ")
    query = f"DELETE FROM {table} WHERE {id_field} = ?"
    cursor.execute(query, (id_value,))
    print(f"Record deleted from {table}.")




# Menu Options
def manage_products(cursor):
    print("\nManaging Products")
    fields = ["product_name", "category", "brand", "supplier_id", "cost_price", "retail_price", "nutrition_id"]
    id_field = "product_id"
    table = "Products"
    manage_table(cursor, table, id_field, fields)


def manage_nutrition(cursor):
    print("\nManaging Nutrition")
    fields = ["shelf_life", "serving", "calories", "protein", "fat", "sugar", "carbs"]
    id_field = "nutrition_id"
    table = "Nutrition"
    manage_table(cursor, table, id_field, fields)

def manage_locations(cursor):
    print("\nManaging Locations")
    fields = ["location_name", "location_type", "address"]
    id_field = "location_id"
    table = "Location"
    manage_table(cursor, table, id_field, fields)

def manage_warehouses(cursor):
    print("\nManaging Warehouses")
    fields = ["warehouse_name", "warehouse_address"]
    id_field = "warehouse_id"
    table = "Warehouse"
    manage_table(cursor, table, id_field, fields)

def manage_suppliers(cursor):
    print("\nManaging Suppliers")
    fields = ["supplier_name", "address", "phone_number"]
    id_field = "supplier_id"
    table = "Suppliers"
    manage_table(cursor, table, id_field, fields)

def manage_users(cursor):
    print("\nManaging Users")
    fields = ["username", "email", "user_type", "address", "phone_number"]
    id_field = "user_id"
    table = "User"
    manage_table(cursor, table, id_field, fields)

def manage_warehouse_inventory(cursor):
    print("\nManaging Warehouse Inventory")
    fields = ["warehouse_id", "product_id", "quantity", "last_updated"]
    id_field = "warehouse_id"
    table = "WarehouseInventory"
    manage_table(cursor, table, id_field, fields, composite=True)

def manage_location_inventory(cursor):
    print("\nManaging Location Inventory")
    fields = ["location_id", "product_id", "quantity", "last_updated"]
    id_field = "location_id"
    table = "LocationInventory"
    manage_table(cursor, table, id_field, fields, composite=True)

def manage_transactions(cursor):
    print("\nManaging Transactions")
    fields = ["location_id", "user_id", "product_id", "quantity", "transaction_date"]
    id_field = "transaction_id"
    table = "Transactions"
    manage_table(cursor, table, id_field, fields)

def manage_purchases(cursor):
    print("\nManaging Purchases")
    fields = ["supplier_id", "warehouse_id", "product_id", "quantity", "purchase_date"]
    id_field = "purchase_id"
    table = "Purchases"
    manage_table(cursor, table, id_field, fields)

def manage_returns(cursor):
    print("\nManaging Returns")
    fields = ["supplier_id", "warehouse_id", "product_id", "quantity", "return_date"]
    id_field = "return_id"
    table = "Returns"
    manage_table(cursor, table, id_field, fields)

def manage_movements(cursor):
    print("\nManaging Movements")
    fields = ["warehouse_id", "location_id", "product_id", "quantity", "movement_date"]
    id_field = "movement_id"
    table = "Movement"
    manage_table(cursor, table, id_field, fields)

# Helper function for table operations
def manage_table(cursor, table, id_field, fields, composite=False):
    print(f"\n1. Add {table}")
    print(f"2. Update {table}")
    print(f"3. Delete {table}")
    choice = input("Enter your choice: ")

    if choice == "1":
        add_record(cursor, table, fields)
    elif choice == "2":
        id_value = input(f"Enter {id_field} to update: ")
        update_record(cursor, table, id_field, id_value, fields)
    elif choice == "3":
        delete_record(cursor, table, id_field)
    else:
        print("Invalid choice.")

# Display table
def display_table(cursor):
    print("\nSelect what table to display.")
    print("1. Products")
    print("2. Nutrition")
    print("3. Locations")
    print("4. Warehouses")
    print("5. Suppliers")
    print("6. Users")
    print("7. Warehouse Inventory")
    print("8. Location Inventory")
    print("9. Transactions")
    print("10. Purchases")
    print("11. Returns")
    print("12. Movements")

    choice = input("Enter your choice: ")

    if choice == "1":
        table = "Products"
        display_table_contents(table,cursor)
    elif choice == "2":
        table = "Nutrition"
        display_table_contents(table,cursor)
    elif choice == "3":
        table = "Location"
        display_table_contents(table,cursor)
    elif choice == "4":
        table = "Warehouse"
        display_table_contents(table,cursor)
    elif choice == "5":
        table = "Suppliers"
        display_table_contents(table,cursor)
    elif choice == "6":
        table = "User"
        display_table_contents(table,cursor)
    elif choice == "7":
        table = "WarehouseInventory"
        display_table_contents(table,cursor)
    elif choice == "8":
        table = "LocationInventory"
        display_table_contents(table,cursor)
    elif choice == "9":
        table = "Transactions"
        display_table_contents(table,cursor)
    elif choice == "10":
        table = "Purchases"
        display_table_contents(table,cursor)
    elif choice == "11":
        table = "Returns"
        display_table_contents(table,cursor)
    elif choice == "12":
        table = "Movement"
        display_table_contents(table,cursor)
    else:
        print("Invalid choice.")
    
# Display table contents
def display_table_contents(table,cursor):
    #conn = sqlite3.connect("speedy_eats.db")
    #cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        if rows:
            print(f"\nContents of {table}:")
            for row in rows:
                print(row)
        else:
            print(f"\nNo data found in {table}.")
    except Exception as e:
        print(f"An error occurred while displaying {table}: {e}")

# Main menu
def main():
    connection = connect_db()
    cursor = connection.cursor()

    while True:
        print("\nSpeedy Eats Database Management")
        print("1. Manage Products")
        print("2. Manage Nutrition")
        print("3. Manage Locations")
        print("4. Manage Warehouses")
        print("5. Manage Suppliers")
        print("6. Manage Users")
        print("7. Manage Warehouse Inventory")
        print("8. Manage Location Inventory")
        print("9. Manage Transactions")
        print("10. Manage Purchases")
        print("11. Manage Returns")
        print("12. Manage Movements")
        print("13. Display tables")
        print("14. Exit")
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                manage_products(cursor)
            elif choice == "2":
                manage_nutrition(cursor)
            elif choice == "3":
                manage_locations(cursor)
            elif choice == "4":
                manage_warehouses(cursor)
            elif choice == "5":
                manage_suppliers(cursor)
            elif choice == "6":
                manage_users(cursor)
            elif choice == "7":
                manage_warehouse_inventory(cursor)
            elif choice == "8":
                manage_location_inventory(cursor)
            elif choice == "9":
                manage_transactions(cursor)
            elif choice == "10":
                manage_purchases(cursor)
            elif choice == "11":
                manage_returns(cursor)
            elif choice == "12":
                manage_movements(cursor)
            elif choice == "13":
                display_table(cursor)
            elif choice == "14":
                connection.commit()
                connection.close()
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

            # Commit after every operation
            connection.commit()

        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()

# Run the main menu
if __name__ == "__main__":
    create_tables()
    main()
