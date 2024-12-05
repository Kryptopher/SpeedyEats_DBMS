import sqlite3
import datetime


class InventoryManagement:
    def __init__(self, db_name='inventory-final2.db'):
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
            name TEXT CHECK(name != ''),
            address TEXT CHECK(address != '')
        )''')

        # Warehouse Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS warehouse (
            warehouse_id INTEGER PRIMARY KEY,
            name TEXT CHECK(name != ''),
            address TEXT CHECK(address != '')
        )''')

        # Location Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS location (
            location_id INTEGER PRIMARY KEY,
            name TEXT CHECK(name != ''),
            type TEXT CHECK(type != ''),
            address TEXT CHECK(address != ''),
            ip_address TEXT CHECK(ip_address != '')
        )''')

        # Nutrition Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS nutrition (
            nutrition_id INTEGER PRIMARY KEY,
            shelf_life TEXT CHECK(shelf_life != ''),
            serving TEXT CHECK(serving != ''),
            calories REAL CHECK(calories != ''),
            protein REAL CHECK(protein != ''),
            fat REAL CHECK(fat != ''),
            sugar REAL CHECK(sugar != ''),
            carbs REAL CHECK(carbs != '')
        )''')

        # User Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY,
            name TEXT CHECK(name != ''),
            email TEXT CHECK(email != ''),
            type TEXT CHECK(type != ''),
            address TEXT CHECK(address != ''),
            phone_number TEXT CHECK(phone_number != '')
        )''')

        # Purchase Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS purchase (
            purchase_id INTEGER PRIMARY KEY,
            supplier_id INTEGER,
            warehouse_id INTEGER,
            purchase_date TEXT CHECK(purchase_date != ''),
            FOREIGN KEY(supplier_id) REFERENCES supplier(supplier_id),
            FOREIGN KEY(warehouse_id) REFERENCES warehouse(warehouse_id)
        )''')

        # Products Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT CHECK(product_name != ''),
            brand TEXT CHECK(brand != ''),
            category TEXT CHECK(category != ''),
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
            movement_date TEXT CHECK(movement_date != ''),
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
            sales_date TEXT CHECK(sales_date != ''),
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

    # def adjust_inventory_for_product_purchased(self, product_id, purchase_id, quantity):
    #     """
    #     Adjust warehouse inventory when products are purchased
        
    #     Args:
    #         product_id (int): ID of the product purchased
    #         purchase_id (int): ID of the purchase
    #         quantity (int): Quantity of product purchased
        
    #     Returns:
    #         bool: True if adjustment successful, False otherwise
    #     """
    #     try:
    #         # Find the warehouse associated with this purchase
    #         self.cursor.execute("""
    #             SELECT warehouse_id FROM purchase 
    #             WHERE purchase_id = ?
    #         """, (purchase_id,))
    #         warehouse_result = self.cursor.fetchone()
            
    #         if not warehouse_result:
    #             print("Error: No warehouse found for this purchase.")
    #             return False
            
    #         warehouse_id = warehouse_result[0]
            
    #         # Find warehouse inventories for this warehouse
    #         self.cursor.execute("""
    #             SELECT warehouse_inventory_id FROM warehouse_inventory 
    #             WHERE warehouse_id = ?
    #         """, (warehouse_id,))
    #         inventories = self.cursor.fetchall()
            
    #         if not inventories:
    #             # Create a new warehouse inventory if none exists
    #             self.cursor.execute("""
    #                 INSERT INTO warehouse_inventory (warehouse_id, last_updated) 
    #                 VALUES (?, datetime('now'))
    #             """, (warehouse_id,))
    #             warehouse_inventory_id = self.cursor.lastrowid
    #         else:
    #             # Use the first warehouse inventory
    #             warehouse_inventory_id = inventories[0][0]
            
    #         # Insert into product_purchased
    #         self.cursor.execute("""
    #             INSERT INTO product_purchased (product_id, purchase_id, quantity) 
    #             VALUES (?, ?, ?)
    #         """, (product_id, purchase_id, quantity))
            
    #         # Update or insert into warehouse_product
    #         self.cursor.execute("""
    #             INSERT INTO warehouse_product (product_id, warehouse_inventory_id, quantity)
    #             VALUES (?, ?, ?)
    #             ON CONFLICT(product_id, warehouse_inventory_id) DO UPDATE SET
    #             quantity = quantity + ?
    #         """, (product_id, warehouse_inventory_id, quantity, quantity))
            
    #         self.conn.commit()
    #         print(f"Successfully added {quantity} units of product {product_id} to warehouse inventory")
    #         return True
        
    #     except sqlite3.Error as e:
    #         self.conn.rollback()
    #         print(f"An error occurred during product purchase: {e}")
    #         return False

    def adjust_inventory_for_movement(self, product_id, movement_id, quantity):
        """
        Adjust warehouse and location inventory when products are moved
        
        Args:
            product_id (int): ID of the product being moved
            movement_id (int): ID of the movement
            quantity (int): Quantity of product moved
        
        Returns:
            bool: True if adjustment successful, False otherwise
        """
        try:
            # Find the warehouse and location for this movement
            self.cursor.execute("""
                SELECT warehouse_id, location_id FROM movement 
                WHERE movement_id = ?
            """, (movement_id,))
            movement_result = self.cursor.fetchone()
            
            if not movement_result:
                print("Error: No warehouse or location found for this movement.")
                return False
            
            warehouse_id, location_id = movement_result
            
            # Reduce warehouse inventory
            # Find warehouse inventories for this product in this warehouse
            self.cursor.execute("""
                SELECT warehouse_inventory_id, quantity 
                FROM warehouse_product 
                WHERE product_id = ? AND warehouse_inventory_id IN (
                    SELECT warehouse_inventory_id 
                    FROM warehouse_inventory 
                    WHERE warehouse_id = ?
                )
                ORDER BY quantity DESC
            """, (product_id, warehouse_id))
            
            warehouse_inventories = self.cursor.fetchall()
            
            if not warehouse_inventories:
                print(f"Error: No warehouse inventory found for product {product_id}")
                return False
            
            # Calculate total available quantity
            total_available = sum(inv[1] for inv in warehouse_inventories)
            
            if quantity > total_available:
                print(f"Error: Not enough inventory. Requested: {quantity}, Available: {total_available}")
                return False
            
            # Reduce warehouse inventory
            remaining_to_reduce = quantity
            for inv_id, inv_quantity in warehouse_inventories:
                reduce_amount = min(remaining_to_reduce, inv_quantity)
                
                self.cursor.execute("""
                    UPDATE warehouse_product 
                    SET quantity = quantity - ? 
                    WHERE product_id = ? AND warehouse_inventory_id = ?
                """, (reduce_amount, product_id, inv_id))
                
                remaining_to_reduce -= reduce_amount
                
                if remaining_to_reduce <= 0:
                    break
            
            # Find or create location inventory
            self.cursor.execute("""
                SELECT location_inventory_id FROM location_inventory 
                WHERE location_id = ?
            """, (location_id,))
            location_inventories = self.cursor.fetchall()
            
            if not location_inventories:
                # Create a new location inventory if none exists
                self.cursor.execute("""
                    INSERT INTO location_inventory (location_id, last_updated) 
                    VALUES (?, datetime('now'))
                """, (location_id,))
                location_inventory_id = self.cursor.lastrowid
            else:
                # Use the first location inventory
                location_inventory_id = location_inventories[0][0]
            
            # Update or insert location product
            self.cursor.execute("""
                INSERT INTO location_product (product_id, location_inventory_id, quantity)
                VALUES (?, ?, ?)
                ON CONFLICT(product_id, location_inventory_id) DO UPDATE SET
                quantity = quantity + ?
            """, (product_id, location_inventory_id, quantity, quantity))
            
            # Insert movement product record
            self.cursor.execute("""
                INSERT INTO movement_product (product_id, movement_id, quantity) 
                VALUES (?, ?, ?)
            """, (product_id, movement_id, quantity))
            
            self.conn.commit()
            print(f"Successfully moved {quantity} units of product {product_id}")
            return True
        
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"An error occurred during movement: {e}")
            return False

    def adjust_inventory_for_product_purchased(self, product_id, purchase_id, quantity):
        """
        Adjust warehouse inventory when products are purchased
        
        Args:
            product_id (int): ID of the product purchased
            purchase_id (int): ID of the purchase
            quantity (int): Quantity of product purchased
        
        Returns:
            bool: True if adjustment successful, False otherwise
        """
        try:
            # Find the warehouse associated with this purchase
            self.cursor.execute("""
                SELECT warehouse_id FROM purchase 
                WHERE purchase_id = ?
            """, (purchase_id,))
            warehouse_result = self.cursor.fetchone()
            
            if not warehouse_result:
                print(f"Error: No warehouse found for purchase {purchase_id}")
                return False
            
            warehouse_id = warehouse_result[0]
            print(f"Found warehouse {warehouse_id} for purchase {purchase_id}")
            
            # Find or create warehouse inventory
            self.cursor.execute("""
                SELECT warehouse_inventory_id FROM warehouse_inventory 
                WHERE warehouse_id = ?
            """, (warehouse_id,))
            inventories = self.cursor.fetchall()
            print("inventories ", inventories)
            if not inventories:
                # Create a new warehouse inventory if none exists
                self.cursor.execute("""
                    INSERT INTO warehouse_inventory (warehouse_id, last_updated) 
                    VALUES (?, datetime('now'))
                """, (warehouse_id,))
                warehouse_inventory_id = self.cursor.lastrowid
                print(f"Created new warehouse inventory {warehouse_inventory_id}")
            else:
                # Use the first warehouse inventory
                warehouse_inventory_id = inventories[0][0]
                print(f"Using existing warehouse inventory {warehouse_inventory_id}")
            
            # Insert into product_purchased
            self.cursor.execute("""
                INSERT INTO product_purchased (product_id, purchase_id, quantity) 
                VALUES (?, ?, ?)
            """, (product_id, purchase_id, quantity))
            print(f"Inserted product_purchased record for product {product_id}, purchase {purchase_id}, quantity {quantity}")
            
            # Check if a record exists
            self.cursor.execute("""
                SELECT quantity FROM warehouse_product 
                WHERE product_id = ? AND warehouse_inventory_id = ?
            """, (product_id, warehouse_inventory_id))
            existing_record = self.cursor.fetchone()
            
            if existing_record:
                # Update existing record
                self.cursor.execute("""
                    UPDATE warehouse_product 
                    SET quantity = quantity + ? 
                    WHERE product_id = ? AND warehouse_inventory_id = ?
                """, (quantity, product_id, warehouse_inventory_id))
                print(f"Updated existing warehouse_product record. Added {quantity} units")
            else:
                # Insert new record
                self.cursor.execute("""
                    INSERT INTO warehouse_product (product_id, warehouse_inventory_id, quantity)
                    VALUES (?, ?, ?)
                """, (product_id, warehouse_inventory_id, quantity))
                print(f"Inserted new warehouse_product record with {quantity} units")
            
            self.conn.commit()
            print(f"Successfully added {quantity} units of product {product_id} to warehouse inventory")
            return True
        
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"An error occurred during product purchase: {e}")
            return False
    
    def adjust_inventory_for_sales(self, product_id, sales_id, quantity):
        """
        Adjust location and sales inventory when products are sold
        
        Args:
            product_id (int): ID of the product being sold
            sales_id (int): ID of the sale
            quantity (int): Quantity of product sold
        
        Returns:
            bool: True if adjustment successful, False otherwise
        """
        try:
            # Find the location for this sale
            self.cursor.execute("""
                SELECT location_id FROM sales 
                WHERE sales_id = ?
            """, (sales_id,))
            sales_result = self.cursor.fetchone()
            
            if not sales_result:
                print("Error: No location found for this sale.")
                return False
            
            location_id = sales_result[0]
            
            # Find location inventories for this product in this location
            self.cursor.execute("""
                SELECT location_inventory_id, quantity 
                FROM location_product 
                WHERE product_id = ? AND location_inventory_id IN (
                    SELECT location_inventory_id 
                    FROM location_inventory 
                    WHERE location_id = ?
                )
                ORDER BY quantity DESC
            """, (product_id, location_id))
            
            location_inventories = self.cursor.fetchall()
            
            if not location_inventories:
                print(f"Error: No location inventory found for product {product_id}")
                return False
            
            # Calculate total available quantity
            total_available = sum(inv[1] for inv in location_inventories)
            
            if quantity > total_available:
                print(f"Error: Not enough inventory. Requested: {quantity}, Available: {total_available}")
                return False
            
            # Reduce location inventory
            remaining_to_reduce = quantity
            for inv_id, inv_quantity in location_inventories:
                reduce_amount = min(remaining_to_reduce, inv_quantity)
                
                self.cursor.execute("""
                    UPDATE location_product 
                    SET quantity = quantity - ? 
                    WHERE product_id = ? AND location_inventory_id = ?
                """, (reduce_amount, product_id, inv_id))
                
                remaining_to_reduce -= reduce_amount
                
                if remaining_to_reduce <= 0:
                    break
            
            # Insert sales product record
            self.cursor.execute("""
                INSERT INTO sales_product (product_id, sales_id, quantity) 
                VALUES (?, ?, ?)
            """, (product_id, sales_id, quantity))
            
            self.conn.commit()
            print(f"Successfully sold {quantity} units of product {product_id}")
            return True
        
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"An error occurred during sales: {e}")
            return False



    def insert_record(self, table):
        print(f"\nInserting record into {table}")
        try:
            if table == 'supplier':
                name = input("Enter supplier name: ")
                address = input("Enter supplier address: ")
                self.cursor.execute("INSERT INTO supplier (name, address) VALUES (?, ?)", 
                                    (name, address))
                self.display_record("supplier") ###

            elif table == 'warehouse':
                name = input("Enter warehouse name: ")
                address = input("Enter warehouse address: ")
                self.cursor.execute("INSERT INTO warehouse (name, address) VALUES (?, ?)", 
                                    (name, address))
                self.display_record("warehouse") ###

            elif table == 'location':
                name = input("Enter location name: ")
                type_ = input("Enter location type: ")
                address = input("Enter location address: ")
                ip_address = input("Enter IP address: ")
                self.cursor.execute("INSERT INTO location (name, type, address, ip_address) VALUES (?, ?, ?, ?)", 
                                    (name, type_, address, ip_address))
                self.display_record("location") ###

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
                self.display_record("nutrition") ###

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
                self.display_record("user") ###

            elif table == 'purchase':
                self.display_record("supplier") ###
                supplier_id = int(input("Enter supplier ID: "))
                self.display_record("warehouse") ###
                warehouse_id = int(input("Enter warehouse ID: "))
                
                purchase_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cursor.execute("""INSERT INTO purchase 
                                    (supplier_id, warehouse_id, purchase_date) 
                                    VALUES (?, ?, ?)""", 
                                    (supplier_id, warehouse_id, purchase_date))
                
                self.display_record("purchase") ###
                
            elif table == 'product':
                product_name = input("Enter product name: ")
                brand = input("Enter brand: ")
                category = input("Enter category: ")
                cost_price = float(input("Enter cost price: "))
                self.display_record("supplier") ###
                supplier_id = int(input("Enter supplier ID: "))
                self.display_record("nutrition") ###
                nutrition_id = int(input("Enter nutrition ID: "))
                self.cursor.execute("""INSERT INTO product
                                    (product_name, brand, category, cost_price, supplier_id, nutrition_id) 
                                    VALUES (?, ?, ?, ?, ?, ?)""", 
                                    (product_name, brand, category, cost_price, supplier_id, nutrition_id))
                self.display_record("product") ###

            elif table == 'warehouse_inventory':
                self.display_record("warehouse") ###
                warehouse_id = int(input("Enter warehouse ID: "))
                
                last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cursor.execute("""INSERT INTO warehouse_inventory 
                                    (warehouse_id, last_updated) 
                                    VALUES (?, ?)""", 
                                    (warehouse_id, last_updated))
                self.display_record("warehouse_inventory") ###

            elif table == 'movement':
                self.display_record("warehouse") ###
                warehouse_id = int(input("Enter warehouse ID: "))
                self.display_record("location") ###
                location_id = int(input("Enter location ID: "))
                
                movement_date = datetime.datetime.now().strftime("%Y-%m-%d")
                self.cursor.execute("""INSERT INTO movement 
                                    (warehouse_id, location_id, movement_date) 
                                    VALUES (?, ?, ?)""", 
                                    (warehouse_id, location_id, movement_date))
                self.display_record("movement") ###

            elif table == 'location_inventory':
                self.display_record("location") ###
                location_id = int(input("Enter location ID: "))
                
                last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.cursor.execute("""INSERT INTO location_inventory 
                                    (location_id, last_updated) 
                                    VALUES (?, ?)""", 
                                    (location_id, last_updated))
                self.display_record("location_inventory") ###

            elif table == 'sales':
                self.display_record("location") ###
                location_id = int(input("Enter location ID: "))
                self.display_record("user") ###
                user_id = int(input("Enter user ID: "))
                
                sales_date = datetime.datetime.now().strftime("%Y-%m-%d")
                self.cursor.execute("""INSERT INTO sales 
                                    (location_id, user_id, sales_date) 
                                    VALUES (?, ?, ?)""", 
                                    (location_id, user_id, sales_date))
                self.display_record("sales") ###
            else:
                # Junction tables

                if table == 'warehouse_product':
                    self.display_record("product") ###
                    product_id = int(input("Enter product ID: "))
                    self.display_record("warehouse_inventory") ###
                    warehouse_inventory_id = int(input("Enter warehouse inventory ID: "))
                    quantity = int(input("Enter quantity: "))
                    self.cursor.execute("""INSERT INTO warehouse_product 
                                        (product_id, warehouse_inventory_id, quantity) VALUES (?, ?, ?)""", 
                                        (product_id, warehouse_inventory_id, quantity))
                    
                    self.display_record("warehouse_product") ###

                elif table == 'product_purchased':
                    self.display_record("product") ###
                    product_id = int(input("Enter product ID: "))
                    self.display_record("purchase") ###
                    purchase_id = int(input("Enter purchase ID: "))
                    quantity = int(input("Enter purchase quantity: "))
                    
                    success = self.adjust_inventory_for_product_purchased(product_id, purchase_id, quantity)
                    
                    if not success:
                        print("Failed to process product purchased record.")
                    else:
                        self.display_record("product_purchased") ###
    
                elif table == 'movement_product':
                    self.display_record("product") ###
                    product_id = int(input("Enter product ID: "))
                    self.display_record("movement") ###
                    movement_id = int(input("Enter movement ID: "))
                    quantity = int(input("Enter movement quantity: "))
                    
                    success = self.adjust_inventory_for_movement(product_id, movement_id, quantity)
                    
                    if not success:
                        print("Failed to process movement product record.")
                    else:
                        self.display_record("movement_product") ###
    
                elif table == 'sales_product':
                    self.display_record("product") ###
                    product_id = int(input("Enter product ID: "))
                    self.display_record("sales") ###
                    sales_id = int(input("Enter sales ID: "))
                    quantity = int(input("Enter sales quantity: "))
                    
                    success = self.adjust_inventory_for_sales(product_id, sales_id, quantity)
                    
                    if not success:
                        print("Failed to process sales product record.")
                    else:
                        self.display_record("sales_product") ###
                    


                elif table == 'location_product':
                    self.display_record("product") ###
                    product_id = int(input("Enter product ID: "))
                    self.display_record("location_inventory") ###
                    location_inventory_id = int(input("Enter location inventory ID: "))
                    quantity = int(input("Enter quantity: "))
                    self.cursor.execute("""INSERT INTO location_product 
                                        (product_id, location_inventory_id, quantity) VALUES (?, ?, ?)""", 
                                        (product_id, location_inventory_id, quantity))
                    self.display_record("location_product") ###
                elif table == 'sales_product':
                    self.display_record("product") ###
                    product_id = int(input("Enter product ID: "))
                    self.display_record("sales") ###
                    sales_id = int(input("Enter sales ID: "))
                    quantity = int(input("Enter sales quantity: "))
                    self.cursor.execute("""INSERT INTO sales_product 
                                        (product_id, sales_id, quantity) VALUES (?, ?, ?)""", 
                                        (product_id, sales_id))
                    self.display_record("sales_product") ###
            self.conn.commit()
            print("Record inserted successfully!")

        except sqlite3.IntegrityError as e:
            print(f"Error: Cannot insert {table} record. {e}")
            print("This could be due to foreign key constraints.")

            


    def update_record(self, table):
        print(f"\nUpdating record in {table}")
        
        self.display_record(table)
        if table == "location_product":
            record_id1 = int(input(f"Enter product ID to update: "))
            record_id2 = int(input(f"Enter location_inventory ID to update: "))

        elif table == "warehouse_product":
            record_id1 = int(input(f"Enter product ID to update: "))
            record_id2 = int(input(f"Enter warehouse_inventory ID to update: "))

        else:
            id_column = f"{table}_id"
            record_id = int(input(f"Enter {table} ID to update: "))
        
        if table == 'supplier':
            name = input("Enter new supplier name: ")
            address = input("Enter new supplier address: ")
            
            if name:
                self.cursor.execute(f"UPDATE {table} SET name = ? WHERE {id_column} = ?", (name, record_id))
            if address:
                self.cursor.execute(f"UPDATE {table} SET address = ? WHERE {id_column} = ?", (address, record_id))
        
        elif table == 'product':
            fields = ['product_name', 'brand', 'category', 'cost_price', 'nutrition_id']
            updates = {}
            
            for field in fields:
                if field == "nutrition_id":
                    self.display_record("nutrition")
                value = input(f"Enter new {field}: ")
                if value:
                    updates[field] = value
            
            if updates:
                set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
                values = list(updates.values()) + [record_id]
                self.cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {id_column} = ?", values)

        elif table == 'nutrition':

            fields = ['shelf_life', 'serving', 'calories', 'protein', 'fat', 'sugar', 'carbs']
            updates = {}
            
            for field in fields:
                value = input(f"Enter new {field}: ")
                if value:
                    updates[field] = value
            
            if updates:
                set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
                values = list(updates.values()) + [record_id]
                self.cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {id_column} = ?", values)

        elif table == 'warehouse':
            
            fields = ['name', 'address']
            updates = {}
            
            for field in fields:
                value = input(f"Enter new {field}: ")
                if value:
                    updates[field] = value
            
            if updates:
                set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
                values = list(updates.values()) + [record_id]
                self.cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {id_column} = ?", values)

        elif table == 'user':
            
            fields = ['name', 'email', 'type', 'address', 'phone_number']
            updates = {}
            
            for field in fields:
                value = input(f"Enter new {field}: ")
                if value:
                    updates[field] = value
            
            if updates:
                set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
                values = list(updates.values()) + [record_id]
                self.cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {id_column} = ?", values)

        elif table == 'location':
            
            fields = ['name', 'type', 'address', 'ip_address']
            updates = {}
            
            for field in fields:
                value = input(f"Enter new {field}: ")
                if value:
                    updates[field] = value
            
            if updates:
                set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
                values = list(updates.values()) + [record_id]
                self.cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {id_column} = ?", values)

        elif table == "location_product":
            quantity = input("Enter quantity update: ")
            
            # if quantity:
            #     self.cursor.execute(f"UPDATE {table} SET quantity = ? WHERE location_inventory_id = ? AND product_id = ?", (quantity, record_id1, record_id2))

            if quantity:
                self.cursor.execute(
                    "SELECT * FROM location_product WHERE location_inventory_id = ? AND product_id = ?", 
                    (record_id2, record_id1)
                )
                if self.cursor.fetchone():
                    self.cursor.execute(
                        f"UPDATE {table} SET quantity = ? WHERE location_inventory_id = ? AND product_id = ?", 
                        (quantity, record_id2, record_id1)
                    )
                    print("Quantity updated successfully.")
                else:
                    print("No matching record found for the given location_inventory_id and product_id.")

        elif table == "warehouse_product":
            quantity = input("Enter quantity update: ")
            
            if quantity:
                self.cursor.execute(f"UPDATE {table} SET quantity = ? WHERE warehouse_inventory_id = ? AND product_id = ?", (quantity, record_id2, record_id1))
        
        # else:
        #     # Dynamically handle updates for other tables
        #     columns = [desc[0] for desc in self.cursor.execute(f"PRAGMA table_info({table})") if desc[0] != id_column]
            
        #     updates = {}
        #     for column in columns:
        #         value = input(f"Enter new {column} (press enter to skip): ")
        #         if value:
        #             updates[column] = value
            
        #     if updates:
        #         set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        #         values = list(updates.values()) + [record_id]
        #         self.cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {id_column} = ?", values)
        self.display_record(table)
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
                self.display_record(table)
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
                    self.display_record(table)
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
        
            
            id_column = f"{table}_id"
            
            try:
                self.display_record(table)
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
                    self.display_record(table)
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

        if table == "product_purchased":
            try:
                # Step 2: Fetch and display joined records
                print("\nDisplaying joined records from product_purchased:")
                display_query = '''
                SELECT 
                    pp.product_id,
                    p.product_name,
                    pp.purchase_id,
                    pu.purchase_date,
                    s.name AS supplier_name,
                    w.name AS warehouse_name,
                    pp.quantity
                FROM product_purchased pp
                JOIN product p ON pp.product_id = p.product_id
                JOIN purchase pu ON pp.purchase_id = pu.purchase_id
                JOIN supplier s ON pu.supplier_id = s.supplier_id
                JOIN warehouse w ON pu.warehouse_id = w.warehouse_id
                '''
                self.cursor.execute(display_query)
                joined_records = self.cursor.fetchall()

                # Step 3: Display headers
                headers = ["Product ID", "Product Name", "Purchase ID", "Purchase Date", "Supplier Name", "Warehouse Name", "Quantity"]
                print(" | ".join(headers))
                print("-" * len(" | ".join(headers)))

                # Step 4: Display records
                if not joined_records:
                    print("No records found.")
                else:
                    for record in joined_records:
                        print(" | ".join(str(item) for item in record))

            except sqlite3.Error as e:
                print(f"An error occurred: {e}")

        elif table == "movement_product":
            try:
                # Step 2: Fetch and display joined records
                print("\nDisplaying joined records from movement_product:")
                display_query = '''
                SELECT 
                    mp.product_id,
                    p.product_name,
                    mp.movement_id,
                    m.movement_date,
                    w.name AS warehouse_name,
                    l.name AS location_name,
                    mp.quantity
                FROM movement_product mp
                JOIN product p ON mp.product_id = p.product_id
                JOIN movement m ON mp.movement_id = m.movement_id
                JOIN warehouse w ON m.warehouse_id = w.warehouse_id
                JOIN location l ON m.location_id = l.location_id
                '''
                self.cursor.execute(display_query)
                joined_records = self.cursor.fetchall()

                # Step 3: Display headers
                headers = ["Product ID", "Product Name", "Movement ID", "Movement Date", "Warehouse Name", "Location Name", "Quantity"]
                print(" | ".join(headers))
                print("-" * len(" | ".join(headers)))

                # Step 4: Display records
                if not joined_records:
                    print("No records found.")
                else:
                    for record in joined_records:
                        print(" | ".join(str(item) for item in record))

            except sqlite3.Error as e:
                print(f"An error occurred: {e}")

        elif table == "sales_product":
            try:
                # Step 2: Fetch and display joined records
                print("\nDisplaying joined records from sales_product:")
                display_query = '''
                SELECT 
                    sp.product_id,
                    p.product_name,
                    sp.sales_id,
                    s.sales_date,
                    u.name AS customer_name,
                    l.name AS location_name,
                    sp.quantity
                FROM sales_product sp
                JOIN product p ON sp.product_id = p.product_id
                JOIN sales s ON sp.sales_id = s.sales_id
                JOIN user u ON s.user_id = u.user_id
                JOIN location l ON s.location_id = l.location_id
                '''
                self.cursor.execute(display_query)
                joined_records = self.cursor.fetchall()

                # Step 3: Display headers
                headers = ["Product ID", "Product Name", "Sales ID", "Sales Date", "Customer Name", "Location Name", "Quantity"]
                print(" | ".join(headers))
                print("-" * len(" | ".join(headers)))

                # Step 4: Display records
                if not joined_records:
                    print("No records found.")
                else:
                    for record in joined_records:
                        print(" | ".join(str(item) for item in record))

            except sqlite3.Error as e:
                print(f"An error occurred: {e}")

        elif table == "warehouse_product":
            try:
                # Step 2: Fetch and display joined records
                print("\nDisplaying joined records from warehouse_product:")
                display_query = '''
                SELECT 
                    wp.product_id, 
                    p.product_name, 
                    wi.warehouse_inventory_id, 
                    w.warehouse_id, 
                    w.name AS warehouse_name, 
                    wp.quantity
                FROM warehouse_product wp
                JOIN product p ON wp.product_id = p.product_id
                JOIN warehouse_inventory wi ON wp.warehouse_inventory_id = wi.warehouse_inventory_id
                JOIN warehouse w ON wi.warehouse_id = w.warehouse_id
                '''
                self.cursor.execute(display_query)
                joined_records = self.cursor.fetchall()

                # Step 3: Display headers
                headers = ["Product ID", "Product Name", "Warehouse Inventory ID", "Warehouse ID", "Warehouse Name", "Quantity"]
                print(" | ".join(headers))
                print("-" * len(" | ".join(headers)))

                # Step 4: Display records
                if not joined_records:
                    print("No records found.")
                else:
                    for record in joined_records:
                        print(" | ".join(str(item) for item in record))

            except sqlite3.Error as e:
                print(f"An error occurred: {e}")

        elif table == "location_product":
            try:
                # Fetch and display the joined results
                print("\nDisplaying joined records from location_product:")
                display_query = '''
                SELECT 
                    lp.product_id, 
                    p.product_name, 
                    li.location_inventory_id, 
                    l.location_id, 
                    l.name AS location_name, 
                    lp.quantity
                FROM location_product lp
                JOIN product p ON lp.product_id = p.product_id
                JOIN location_inventory li ON lp.location_inventory_id = li.location_inventory_id
                JOIN location l ON li.location_id = l.location_id
                '''
                self.cursor.execute(display_query)
                joined_records = self.cursor.fetchall()

                # Display headers
                headers = ["Product ID", "Product Name", "Location Inventory ID", "Location ID", "Location Name", "Quantity"]
                print(" | ".join(headers))
                print("-" * len(" | ".join(headers)))

                # Display records
                if not joined_records:
                    print("No records found.")
                else:
                    for record in joined_records:
                        print(" | ".join(str(item) for item in record))

            except sqlite3.Error as e:
                print(f"An error occurred: {e}")

        else:        
        
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
        
        if choice in ['1', '3', '4']:
            print("\nSelect Table:")
            # for i, table in enumerate(inventory_system.tables, 1):
            #     print(f"{i}. {table}")

            # tl = ['Create Supplier Entity', 'Create Purchases Entity', 'Create Product Entity', 'Create Nutrition Entity', 'Create Warehouse Entity', 
            # 'Create Warehouse_inventory Entity', 'Create Movement Entity', 'Create Retail location Entity', 'Create Retail location inventory Entity', 
            # 'Create User Entity', ' Create Sales Entity', 'Buy product from supplier and store in warehouse', 'Directly insert product to the warehouse inventory', 
            # 'Move product from warehouse to destination (Retail location)', 'Directly insert product to the retail inventory', 'Sell product to the user from the retail inventory.'
            # ]

            # for i, table in enumerate(tl,1):
            #     print(f"{i}. {table}")

            # table_choice = input("Enter table number: ")

            if choice=='1':
                tl = ['Create Supplier Entity', 'Create Purchases Entity', 'Create Product Entity', 'Create Nutrition Entity', 'Create Warehouse Entity', 
                'Create Warehouse_inventory Entity', 'Create Movement Entity', 'Create Retail location Entity', 'Create Retail location inventory Entity', 
                'Create User Entity', ' Create Sales Entity', 'Buy product from supplier and store in warehouse', 'Directly insert product to the warehouse inventory', 
                'Move product from warehouse to destination (Retail location)', 'Directly insert product to the retail inventory', 'Sell product to the user from the retail inventory.'
                ]
                for i, table in enumerate(tl,1):
                    print(f"{i}. {table}")
                table_choice = input("Enter table number: ")
            
            elif choice=='3':
                tl = ['Delete Supplier Entity', 'Delete Purchases Entity', 'Delete Product Entity', 'Delete Nutrition Entity', 'Delete Warehouse Entity', 
                'Delete Warehouse_inventory Entity', 'Delete Movement Entity', 'Delete Retail location Entity', 'Delete Retail location inventory Entity', 
                'Delete User Entity', ' Delete Sales Entity', 'Delete product purchased record', 'Delete product in warehouse inventory record', 
                'Delete Movement of product from warehouse to destination (Retail location) record', 'Delete product in retail inventory record', 'Delete sales record from the retail inventory to the user.'
                ]
                for i, table in enumerate(tl,1):
                    print(f"{i}. {table}")
                table_choice = input("Enter table number: ")

            elif choice=='4':
                tl = ['Display Supplier Entity', 'Display Purchases Entity', 'Display Product Entity', 'Display Nutrition Entity', 'Display Warehouse Entity', 
                'Display Warehouse_inventory Entity', 'Display Movement Entity', 'Display Retail location Entity', 'Display Retail location inventory Entity', 
                'Display User Entity', ' Display Sales Entity', 'Display product purchased records', 'Display product in warehouse inventory records', 
                'Display Movement of product from warehouse to destination (Retail location) records', 'Display product in retail inventory records', 'Display sales records from the retail inventory to the user.'
                ]
                for i, table in enumerate(tl,1):
                    print(f"{i}. {table}")
                table_choice = input("Enter table number: ")

            
            try:
                selected_table = inventory_system.tables[int(table_choice) - 1]
                
                if choice == '1':
                    inventory_system.insert_record(selected_table)
                elif choice == '3':
                    inventory_system.delete_record(selected_table)
                elif choice == '4':
                    inventory_system.display_record(selected_table)

            
            # except (ValueError, IndexError):
            #     print("Invalid table selection!")
            except ValueError:
                print("Caught a ValueError: Invalid value provided.")

            except IndexError:
                print("Caught an IndexError: Index out of range!")

        elif choice == '2':
            print("\nSelect Table:")
            # up_list = ["supplier", "product", "nutrition", "warehouse", "user", "location", "location_product", "warehouse_product"]
            # for i, table in enumerate(up_list, 1):
            #     print(f"{i}. {table}")      
            # table_choice = input("Enter table number: ")  

            up_list = ['Update Supplier Entity', 'Update Product Entity', 'Update Nutrition Entity', 'Update Warehouse Entity', 
            'Update User Entity', 'Update Retail location Entity', 'Update product in retail inventory record',
            'Update product in warehouse inventory record'
            ]

            up_dict = {'Update Supplier Entity':"supplier", 'Update Product Entity':"product", 'Update Nutrition Entity':"nutrition", 
            'Update Warehouse Entity':"warehouse", 
            'Update User Entity':"user", 'Update Retail location Entity':"location", 'Update product in retail inventory record':"location_product",
            'Update product in warehouse inventory record':"warehouse_product"
            }

            for i, table in enumerate(up_list,1):
                print(f"{i}. {table}")
            table_choice = input("Enter table number: ")


            try:
                selected_table = up_list[int(table_choice) - 1]
                
                if choice == '2':
                    inventory_system.update_record(up_dict[selected_table])
            
            # except (ValueError, IndexError):
            #     print("Invalid table selection!")
            except ValueError:
                print("Caught a ValueError: Invalid value provided.")

            except IndexError:
                print("Caught an IndexError: Index out of range!")
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")