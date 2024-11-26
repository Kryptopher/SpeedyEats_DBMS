import sqlite3
import datetime


class InventoryManagement:
    def __init__(self, db_name='inventory2.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.create_tables()
        self.tables = [
            'supplier', 'purchase', 'product', 'nutrition', 'warehouse', 
            'warehouse_inventory', 'movement', 'location', 'location_inventory', 
            'user', 'sales', 'product_purchased', 'warehouse_product', 
            'movement_product', 'location_product', 'sales_product'
        ]

    def create_tables(self):
        # Supplier Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS supplier (
            supplier_id INTEGER PRIMARY KEY,
            name TEXT,
            address TEXT
        )''')

        # Warehouse Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS warehouse (
            warehouse_id INTEGER PRIMARY KEY,
            name TEXT,
            address TEXT
        )''')

        # Location Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS location (
            location_id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            address TEXT,
            ip_address TEXT
        )''')

        # Nutrition Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS nutrition (
            nutrition_id INTEGER PRIMARY KEY,
            shelf_life TEXT,
            serving TEXT,
            calories REAL,
            protein REAL,
            fat REAL,
            sugar REAL,
            carbs REAL
        )''')

        # User Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            type TEXT,
            address TEXT,
            phone_number TEXT
        )''')

        # Purchase Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS purchase (
            purchase_id INTEGER PRIMARY KEY,
            supplier_id INTEGER,
            warehouse_id INTEGER,
            purchase_date TEXT,
            FOREIGN KEY(supplier_id) REFERENCES supplier(supplier_id),
            FOREIGN KEY(warehouse_id) REFERENCES warehouse(warehouse_id)
        )''')

        # Products Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            brand TEXT,
            category TEXT,
            cost_price REAL CHECK(cost_price > 0),
            supplier_id INTEGER,
            nutrition_id INTEGER,
            FOREIGN KEY(supplier_id) REFERENCES supplier(supplier_id) ON DELETE RESTRICT,
            FOREIGN KEY(nutrition_id) REFERENCES nutrition(nutrition_id) ON DELETE RESTRICT
        )''')

        # Warehouse Inventory Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS warehouse_inventory (
            warehouse_inventory_id INTEGER PRIMARY KEY,
            warehouse_id INTEGER,
            last_updated TEXT,
            FOREIGN KEY(warehouse_id) REFERENCES warehouse(warehouse_id)
        )''')

        # Movement Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS movement (
            movement_id INTEGER PRIMARY KEY,
            warehouse_id INTEGER,
            location_id INTEGER,
            movement_date TEXT,
            FOREIGN KEY(warehouse_id) REFERENCES warehouse(warehouse_id),
            FOREIGN KEY(location_id) REFERENCES location(location_id)
        )''')




        # Location Inventory Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS location_inventory (
            location_inventory_id INTEGER PRIMARY KEY,
            location_id INTEGER,
            last_updated TEXT,
            FOREIGN KEY(location_id) REFERENCES location(location_id)
        )''')

        # Sales Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
            sales_id INTEGER PRIMARY KEY,
            location_id INTEGER,
            user_id INTEGER,
            sales_date TEXT,
            FOREIGN KEY(location_id) REFERENCES location(location_id),
            FOREIGN KEY(user_id) REFERENCES user(user_id)
        )''')



        # Junction Tables
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS product_purchased (
            product_id INTEGER,
            purchase_id INTEGER,
            quantity INTEGER CHECK(quantity > 0),
            PRIMARY KEY(product_id, purchase_id),
            FOREIGN KEY(product_id) REFERENCES product(product_id) ON DELETE RESTRICT,
            FOREIGN KEY(purchase_id) REFERENCES purchase(purchase_id) ON DELETE CASCADE
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS warehouse_product (
            product_id INTEGER,
            warehouse_inventory_id INTEGER,
            quantity INTEGER CHECK(quantity >= 0),
            PRIMARY KEY(product_id, warehouse_inventory_id),
            FOREIGN KEY(product_id) REFERENCES product(product_id),
            FOREIGN KEY(warehouse_inventory_id) REFERENCES warehouse_inventory(warehouse_inventory_id)
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS movement_product (
            product_id INTEGER,
            movement_id INTEGER,
            quantity INTEGER CHECK(quantity > 0),
            PRIMARY KEY(product_id, movement_id),
            FOREIGN KEY(product_id) REFERENCES product(product_id),
            FOREIGN KEY(movement_id) REFERENCES movement(movement_id)
        )''')

        # Create the trigger after creating the table
        self.cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS reduce_warehouse_quantity
            BEFORE INSERT ON movement_product
            FOR EACH ROW
            BEGIN
                -- Check if there is enough quantity in the warehouse
                SELECT CASE
                    WHEN (SELECT quantity
                        FROM warehouse_product
                        WHERE product_id = NEW.product_id
                            AND warehouse_inventory_id = (SELECT warehouse_inventory_id
                                                        FROM warehouse_inventory
                                                        WHERE warehouse_id = (SELECT warehouse_id
                                                                                FROM movement
                                                                                WHERE movement_id = NEW.movement_id))) < NEW.quantity THEN
                        RAISE (ABORT, 'Insufficient quantity in warehouse to complete the movement')
                END;

                -- Deduct the quantity from the warehouse_product table
                UPDATE warehouse_product
                SET quantity = quantity - NEW.quantity
                WHERE product_id = NEW.product_id
                AND warehouse_inventory_id = (SELECT warehouse_inventory_id
                                                FROM warehouse_inventory
                                                WHERE warehouse_id = (SELECT warehouse_id
                                                                    FROM movement
                                                                    WHERE movement_id = NEW.movement_id));
            END;
        ''')



        self.cursor.execute('''CREATE TABLE IF NOT EXISTS location_product (
            product_id INTEGER,
            location_inventory_id INTEGER,
            quantity INTEGER CHECK(quantity >= 0),
            PRIMARY KEY(product_id, location_inventory_id),
            FOREIGN KEY(product_id) REFERENCES product(product_id),
            FOREIGN KEY(location_inventory_id) REFERENCES location_inventory(location_inventory_id)
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales_product (
            product_id INTEGER,
            sales_id INTEGER,
            quantity INTEGER CHECK(quantity > 0),
            PRIMARY KEY(product_id, sales_id),
            FOREIGN KEY(product_id) REFERENCES product(product_id),
            FOREIGN KEY(sales_id) REFERENCES sales(sales_id)
        )''')

        self.conn.commit()

    def insert_record(self, table):
        print(f"\nInserting record into {table}")
        try:
            if table == 'supplier':
                name = input("Enter supplier name: ")
                address = input("Enter supplier address: ")
                self.cursor.execute("INSERT INTO supplier (name, address) VALUES (?, ?)", 
                                    (name, address))
            elif table == 'warehouse':
                name = input("Enter warehouse name: ")
                address = input("Enter warehouse address: ")
                self.cursor.execute("INSERT INTO warehouse (name, address) VALUES (?, ?)", 
                                    (name, address))
            elif table == 'location':
                name = input("Enter location name: ")
                type_ = input("Enter location type: ")
                address = input("Enter location address: ")
                ip_address = input("Enter IP address: ")
                self.cursor.execute("INSERT INTO location (name, type, address, ip_address) VALUES (?, ?, ?, ?)", 
                                    (name, type_, address, ip_address))
            elif table == 'nutrition':
                shelf_life = input("Enter shelf life: ")
                serving = input("Enter serving size: ")
                calories = float(input("Enter calories: "))
                protein = float(input("Enter protein: "))
                fat = float(input("Enter fat: "))
                sugar = float(input("Enter sugar: "))
                carbs = float(input("Enter carbs: "))
                self.cursor.execute("""INSERT INTO nutrition 
                                    (shelf_life, serving, calories, protein, fat, sugar, carbs) 
                                    VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                                    (shelf_life, serving, calories, protein, fat, sugar, carbs))
            elif table == 'user':
                name = input("Enter user name: ")
                email = input("Enter user email: ")
                type_ = input("Enter user type: ")
                address = input("Enter user address: ")
                phone_number = input("Enter phone number: ")
                self.cursor.execute("""INSERT INTO user 
                                    (name, email, type, address, phone_number) 
                                    VALUES (?, ?, ?, ?, ?)""", 
                                    (name, email, type_, address, phone_number))
            elif table == 'purchase':
                supplier_id = int(input("Enter supplier ID: "))
                warehouse_id = int(input("Enter warehouse ID: "))
                
                purchase_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cursor.execute("""INSERT INTO purchase 
                                    (supplier_id, warehouse_id, purchase_date) 
                                    VALUES (?, ?, ?)""", 
                                    (supplier_id, warehouse_id, purchase_date))
            elif table == 'product':
                product_name = input("Enter product name: ")
                brand = input("Enter brand: ")
                category = input("Enter category: ")
                cost_price = float(input("Enter cost price: "))
                supplier_id = int(input("Enter supplier ID: "))
                nutrition_id = int(input("Enter nutrition ID: "))
                self.cursor.execute("""INSERT INTO product
                                    (product_name, brand, category, cost_price, supplier_id, nutrition_id) 
                                    VALUES (?, ?, ?, ?, ?, ?)""", 
                                    (product_name, brand, category, cost_price, supplier_id, nutrition_id))
            elif table == 'warehouse_inventory':
                warehouse_id = int(input("Enter warehouse ID: "))
                
                last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cursor.execute("""INSERT INTO warehouse_inventory 
                                    (warehouse_id, last_updated) 
                                    VALUES (?, ?)""", 
                                    (warehouse_id, last_updated))
            elif table == 'movement':
                warehouse_id = int(input("Enter warehouse ID: "))
                location_id = int(input("Enter location ID: "))
                
                movement_date = datetime.datetime.now().strftime("%Y-%m-%d")
                self.cursor.execute("""INSERT INTO movement 
                                    (warehouse_id, location_id, movement_date) 
                                    VALUES (?, ?, ?)""", 
                                    (warehouse_id, location_id, movement_date))
            elif table == 'location_inventory':
                location_id = int(input("Enter location ID: "))
                
                
                last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cursor.execute("""INSERT INTO location_inventory 
                                    (location_id, last_updated) 
                                    VALUES (?, ?)""", 
                                    (location_id, last_updated))
            elif table == 'sales':
                location_id = int(input("Enter location ID: "))
                user_id = int(input("Enter user ID: "))
                
                sales_date = datetime.datetime.now().strftime("%Y-%m-%d")
                self.cursor.execute("""INSERT INTO sales 
                                    (location_id, user_id, sales_date) 
                                    VALUES (?, ?, ?)""", 
                                    (location_id, user_id, sales_date))
            else:
                # Junction tables
                if table == 'product_purchased':
                    product_id = int(input("Enter product ID: "))
                    purchase_id = int(input("Enter purchase ID: "))
                    quantity = int(input("Enter purchase quantity: "))
                    self.cursor.execute("""INSERT INTO product_purchased 
                                        (product_id, purchase_id, quantity) VALUES (?, ?, ?)""", 
                                        (product_id, purchase_id, quantity))
                elif table == 'warehouse_product':
                    product_id = int(input("Enter product ID: "))
                    warehouse_inventory_id = int(input("Enter warehouse inventory ID: "))
                    quantity = int(input("Enter quantity: "))
                    self.cursor.execute("""INSERT INTO warehouse_product 
                                        (product_id, warehouse_inventory_id, quantity) VALUES (?, ?, ?)""", 
                                        (product_id, warehouse_inventory_id, quantity))
                elif table == 'movement_product':
                    product_id = int(input("Enter product ID: "))
                    movement_id = int(input("Enter movement ID: "))
                    quantity = int(input("Enter movement quantity: "))
                    self.cursor.execute("""INSERT INTO movement_product 
                                        (product_id, movement_id, quantity) VALUES (?, ?, ?)""", 
                                        (product_id, movement_id, quantity))
                elif table == 'location_product':
                    product_id = int(input("Enter product ID: "))
                    location_inventory_id = int(input("Enter location inventory ID: "))
                    quantity = int(input("Enter quantity: "))
                    self.cursor.execute("""INSERT INTO location_product 
                                        (product_id, location_inventory_id, quantity) VALUES (?, ?, ?)""", 
                                        (product_id, location_inventory_id, quantity))
                elif table == 'sales_product':
                    product_id = int(input("Enter product ID: "))
                    sales_id = int(input("Enter sales ID: "))
                    quantity = int(input("Enter sales quantity: "))
                    self.cursor.execute("""INSERT INTO sales_product 
                                        (product_id, sales_id, quantity) VALUES (?, ?, ?)""", 
                                        (product_id, sales_id))
            self.conn.commit()
            print("Record inserted successfully!")
        except sqlite3.IntegrityError:
            print(f"Error: Cannot insert {table} record.")
            print("This could be due to foreign key constraints.")
            


    def update_record(self, table):
        print(f"\nUpdating record in {table}")
        
        id_column = f"{table}_id"
        record_id = int(input(f"Enter {table} ID to update: "))
        
        if table == 'supplier':
            name = input("Enter new supplier name (press enter to skip): ")
            address = input("Enter new supplier address (press enter to skip): ")
            
            if name:
                self.cursor.execute(f"UPDATE {table} SET name = ? WHERE {id_column} = ?", (name, record_id))
            if address:
                self.cursor.execute(f"UPDATE {table} SET address = ? WHERE {id_column} = ?", (address, record_id))
        
        elif table == 'product':
            fields = ['product_name', 'brand', 'category', 'cost_price', 'supplier_id', 'nutrition_id']
            updates = {}
            
            for field in fields:
                value = input(f"Enter new {field} (press enter to skip): ")
                if value:
                    updates[field] = value
            
            if updates:
                set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
                values = list(updates.values()) + [record_id]
                self.cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {id_column} = ?", values)
        
        else:
            # Dynamically handle updates for other tables
            columns = [desc[0] for desc in self.cursor.execute(f"PRAGMA table_info({table})") if desc[0] != id_column]
            
            updates = {}
            for column in columns:
                value = input(f"Enter new {column} (press enter to skip): ")
                if value:
                    updates[column] = value
            
            if updates:
                set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
                values = list(updates.values()) + [record_id]
                self.cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {id_column} = ?", values)

        self.conn.commit()
        print("Record updated successfully!")

    def delete_record(self, table):
        print(f"\nDeleting record from {table}")
        dict_ids = {"product_purchased":["product_id", "purchase_id"], "warehouse_product":["product_id", "warehouse_inventory_id"], 
        "movement_product":["product_id", "movement_id"], "location_product":["product_id", "location_inventory_id"], 
        "sales_product":["product_id", "sales_id"]}
        if table == "product_purchased" or table == "warehouse_product" or table == 'movement_product' or table == 'location_product' or table == 'sales_product':
            id_column = dict_ids[table]
            
            try:
                # Get the record ID to delete
                record_id1 = int(input(f"Enter {table} {id_column[0]} to delete: "))
                record_id2 = int(input(f"Enter {table} {id_column[1]} ID to delete: "))
                
                # First, check if the record exists
                self.cursor.execute(f"SELECT * FROM {table} WHERE {id_column[0]} = ? AND {id_column[1]} = ?", (record_id1, record_id2))
                existing_record = self.cursor.fetchone()
                
                if not existing_record:
                    print(f"No {table} record found with IDs {record_id1} and {record_id2}")
                    return
                
                # Confirm deletion
                confirm = input(f"Are you sure you want to delete {table} record with IDs {record_id1} and {record_id2}? (yes/no): ").lower()
                
                if confirm != 'yes':
                    print("Deletion cancelled.")
                    return
                
                # Attempt to delete the record
                self.cursor.execute(f"DELETE FROM {table} WHERE {id_column[0]} = ? AND {id_column[1]} = ?", (record_id1, record_id2))
                
                # Check if any rows were actually deleted
                if self.cursor.rowcount > 0:
                    self.conn.commit()
                    print(f"Successfully deleted record with IDs {record_id1} and {record_id2} from {table}")
                else:
                    print(f"No record found with IDs {record_id1} and {record_id2} in {table}")
            
            except sqlite3.IntegrityError:
                print(f"Error: Cannot delete {table} record. It may be referenced by other tables.")
                print("This could be due to foreign key constraints.")
            
            except ValueError:
                print("Invalid ID. Please enter a valid numeric ID.")
            
            except sqlite3.Error as e:
                self.conn.rollback()
                print(f"An error occurred while deleting the record: {e}")

        else:
        
            ###
            id_column = f"{table}_id"
            
            try:
                # Get the record ID to delete
                record_id = int(input(f"Enter {table} ID to delete: "))
                
                # First, check if the record exists
                self.cursor.execute(f"SELECT * FROM {table} WHERE {id_column} = ?", (record_id,))
                existing_record = self.cursor.fetchone()
                
                if not existing_record:
                    print(f"No {table} record found with ID {record_id}")
                    return
                
                # Confirm deletion
                confirm = input(f"Are you sure you want to delete {table} record with ID {record_id}? (yes/no): ").lower()
                
                if confirm != 'yes':
                    print("Deletion cancelled.")
                    return
                
                # Attempt to delete the record
                self.cursor.execute(f"DELETE FROM {table} WHERE {id_column} = ?", (record_id,))
                
                # Check if any rows were actually deleted
                if self.cursor.rowcount > 0:
                    self.conn.commit()
                    print(f"Successfully deleted record with ID {record_id} from {table}")
                else:
                    print(f"No record found with ID {record_id} in {table}")
            
            except sqlite3.IntegrityError:
                print(f"Error: Cannot delete {table} record. It may be referenced by other tables.")
                print("This could be due to foreign key constraints.")
            
            except ValueError:
                print("Invalid ID. Please enter a valid numeric ID.")
            
            except sqlite3.Error as e:
                self.conn.rollback()
                print(f"An error occurred while deleting the record: {e}")


    def display_record(self, table):
        print(f"\nDisplaying records from {table}")
        
        try:
            # Fetch all columns dynamically
            self.cursor.execute(f"PRAGMA table_info({table})")
            columns = [column[1] for column in self.cursor.fetchall()]
            
            # Display column names
            print(" | ".join(columns))
            print("-" * (len(" | ".join(columns))))
            
            # Fetch and display all records
            self.cursor.execute(f"SELECT * FROM {table}")
            records = self.cursor.fetchall()
            
            if not records:
                print("No records found.")
                return
            
            for record in records:
                print(" | ".join(str(item) for item in record))
        
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")



def main():
    inventory_system = InventoryManagement()

    while True:
        print("\n--- Inventory Management System ---")
        print("1. Insert Record")
        print("2. Update Record")
        print("3. Delete Record")
        print("4. Display Records")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '5':
            print("Exiting the system...")
            break
        
        if choice in ['1', '2', '3', '4']:
            print("\nSelect Table:")
            for i, table in enumerate(inventory_system.tables, 1):
                print(f"{i}. {table}")
            
            table_choice = input("Enter table number: ")
            
            try:
                selected_table = inventory_system.tables[int(table_choice) - 1]
                
                if choice == '1':
                    inventory_system.insert_record(selected_table)
                elif choice == '2':
                    inventory_system.update_record(selected_table)
                elif choice == '3':
                    inventory_system.delete_record(selected_table)
                elif choice == '4':
                    inventory_system.display_record(selected_table)
            
            except (ValueError, IndexError):
                print("Invalid table selection!")
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")