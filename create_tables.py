import sqlite3

# Products (product_id, product_name, category, brand, supplier_id, cost_price, retail_price, nutrition_id )  
# Nutrition (nutrition_id, shelf_life, serving, calories, protein, fat, sugar, carbs) 
# Suppliers (supplier_id, supplier_name, address, phone_number) 

"""Location (location_id, location_name, location_type, address) 
Warehouse (warehouse_id, warehouse_name, warehouse_address,) 
Suppliers (supplier_id, supplier_name, address, phone_number) 
User (user_id,username, email, user_type, address, phone_number)  
Warehouse inventory( location_id, product_id, quantity, last_updated) 
Location inventory( location_id, product_id, quantity, last_updated) 
Transactions (transaction_id, location_id, user_id, product_id, quantity, transaction_date) 
Purchases ( purchase_id, supplier_id, warehouse_id, product_id, quantity, purchase_date) 
Returns (return_id, supplier_id, warehouse_id, product_id, quantity, return_date) 
Movement( movement_id, warehouse_id, location_id, product_id, quantity, movement_date) """


def create_tables():
    # Connect to the database
    conn = sqlite3.connect("speedy_eats.db")
    cursor = conn.cursor()

    # Define table creation queries
    queries = [
        """
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            brand TEXT NOT NULL,
            supplier_id INTEGER NOT NULL,
            cost_price REAL NOT NULL,
            retail_price REAL NOT NULL,
            nutrition_id INTEGER NOT NULL,
            FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id),
            FOREIGN KEY (nutrition_id) REFERENCES Nutrition(nutrition_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Nutrition (
            nutrition_id INTEGER PRIMARY KEY,
            shelf_life INTEGER NOT NULL,
            serving TEXT NOT NULL,
            calories INTEGER NOT NULL,
            protein REAL NOT NULL,
            fat REAL NOT NULL,
            sugar REAL NOT NULL,
            carbs REAL NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Location (
            location_id INTEGER PRIMARY KEY,
            location_name TEXT NOT NULL,
            location_type TEXT NOT NULL,
            address TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Warehouse (
            warehouse_id INTEGER PRIMARY KEY,
            warehouse_name TEXT NOT NULL,
            warehouse_address TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Suppliers (
            supplier_id INTEGER PRIMARY KEY,
            supplier_name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone_number TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            user_type TEXT NOT NULL,
            address TEXT NOT NULL,
            phone_number TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS WarehouseInventory (
            warehouse_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            last_updated TEXT NOT NULL,
            PRIMARY KEY (warehouse_id, product_id),
            FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS LocationInventory (
            location_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            last_updated TEXT NOT NULL,
            PRIMARY KEY (location_id, product_id),
            FOREIGN KEY (location_id) REFERENCES Location(location_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Transactions (
            transaction_id INTEGER PRIMARY KEY,
            location_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            transaction_date TEXT NOT NULL,
            FOREIGN KEY (location_id) REFERENCES Location(location_id),
            FOREIGN KEY (user_id) REFERENCES User(user_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Purchases (
            purchase_id INTEGER PRIMARY KEY,
            supplier_id INTEGER NOT NULL,
            warehouse_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            purchase_date TEXT NOT NULL,
            FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id),
            FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Returns (
            return_id INTEGER PRIMARY KEY,
            supplier_id INTEGER NOT NULL,
            warehouse_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            return_date TEXT NOT NULL,
            FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id),
            FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Movement (
            movement_id INTEGER PRIMARY KEY,
            warehouse_id INTEGER NOT NULL,
            location_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            movement_date TEXT NOT NULL,
            FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id),
            FOREIGN KEY (location_id) REFERENCES Location(location_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        );
        """
    ]

    # Execute table creation queries
    for query in queries:
        cursor.execute(query)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Tables created successfully.")
