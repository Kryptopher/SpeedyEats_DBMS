import sqlite3

db_name ='inventory-final2.db'
conn = sqlite3.connect(db_name)

# Printing tables to verify if queries are working.
def print_table(cursor, table):
    # Fetch all columns dynamically
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [column[1] for column in cursor.fetchall()]

    # Display column names
    print(" | ".join(columns))
    print("-" * (len(" | ".join(columns))))

    # Fetch and display all records
    cursor.execute(f"SELECT * FROM {table}")
    records = cursor.fetchall()

    for record in records:
        print(" | ".join(str(item) for item in record))


cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")



"""QUERY 1 - INSERT PRODUCT (ID=31) AND TEST IF PUTTING EMPTY PRODUCT NAME GIVES ERROR; 
   EXPECTED OUTPUT - ERROR """

print(f"""QUERY 1 - INSERT PRODUCT (ID=31) AND TEST IF PUTTING EMPTY PRODUCT NAME GIVES ERROR;\nEXPECTED OUTPUT - ERROR """)
print()
print("Running QUERY 1")


try:
    cursor.execute("""INSERT INTO product
                        (product_name, brand, category, cost_price, supplier_id, nutrition_id) 
                        VALUES (?, ?, ?, ?, ?, ?)""", 
                        ('', 'delete', 'delete', 1, 1, 1))

    conn.commit()

except sqlite3.Error as e:
    print(f"QUERY1 result: An error occurred: {e}")

print()

print("---------QUERY2--------")
print()
"""QUERY 2 - INSERT PRODUCT (ID=31) AND TEST IF PUTTING CORRECTLY FORMATED INSERTION QUERY WORKS; 
   EXPECTED OUTPUT - SUCCESSFUL INSERTION """

print(f"""QUERY 2 - INSERT PRODUCT (ID=31) AND TEST IF PUTTING CORRECTLY FORMATED INSERTION QUERY WORKS;\nEXPECTED OUTPUT - SUCCESSFUL INSERTION """)
print()
print("PRODUCT TABLE BEFORE INSERTION")
print_table(cursor, "product")
print()
print("Running QUERY 2")


try:
    cursor.execute("""INSERT INTO product
                        (product_name, brand, category, cost_price, supplier_id, nutrition_id) 
                        VALUES (?, ?, ?, ?, ?, ?)""", 
                        ('delete', 'delete', 'delete', 1, 1, 1))

    conn.commit()
    print("INSERTION SUCCESSFUL")
    print("PRODUCT TABLE AFTER INSERTION")
    print_table(cursor, "product")
    print()

except sqlite3.Error as e:
    print(f"QUERY2 result: An error occurred: {e}")
    

print()
print("---------QUERY 3--------")
print()
"""QUERY 3 - UPDATE PRODUCT NAME (ID=31), BRAND AND CATEGORY, AND TEST IF UPDATE QUERY WORKS; 
   EXPECTED OUTPUT - SUCCESSFUL UPDATE """

print(f"""QUERY 3 - UPDATE PRODUCT NAME (ID=31), BRAND AND CATEGORY, AND TEST IF UPDATE QUERY WORKS;\nEXPECTED OUTPUT - SUCCESSFUL UPDATE """)
print()
print("PRODUCT TABLE BEFORE UPDATE")
print_table(cursor, "product")
print()
print("Running QUERY 3")


try:
    # Define the SQL UPDATE query
    update_query = '''
        UPDATE product
        SET product_name = ?, brand = ?, category = ?, cost_price = ?, supplier_id = ?, nutrition_id = ?
        WHERE product_id = ?
    '''

    # Parameters to update in the table
    parameters = ('updated', 'updated', 'updated', 1.0, 1, 1, 31)  # Update values for product with ID 31

    # Execute the UPDATE query
    cursor.execute(update_query, parameters)
    conn.commit()
    print("UPDATE SUCCESSFUL")
    print("PRODUCT TABLE AFTER UPDATE")
    print_table(cursor, "product")
    print()

except sqlite3.Error as e:
    print(f"QUERY3 result: An error occurred: {e}")


print()
print("---------QUERY 4--------")
print()
"""QUERY 4 - DELETE PRODUCT (ID=1) AND TEST IF DELETING PRODUCT THAT HAS DEPENDENTS GIVES ERROR; 
   EXPECTED OUTPUT - ERROR """

print(f"""QUERY 4 - DELETE PRODUCT (ID=1) AND TEST IF DELETING PRODUCT THAT HAS DEPENDENTS GIVES ERROR;\nEXPECTED OUTPUT - ERROR """)
print()
print("Running QUERY 4")


try:
    cursor.execute(f"DELETE FROM product WHERE product_id = ?", (1,))
    conn.commit()
except sqlite3.Error as e:
    print(f"QUERY 4 result: An error occurred: {e}")

print()


print()
print("---------QUERY 5--------")
print()
"""QUERY 5 - DELETE PRODUCT (ID=31) AND TEST IF DELETING PRODUCT THAT HAS NO DEPENDENTS WORKS; 
   EXPECTED OUTPUT - DELETION SUCCESSFUL"""

print(f"""QUERY 5 - DELETE PRODUCT (ID=31) AND TEST IF DELETING PRODUCT THAT HAS NO DEPENDENTS WORKS;\nEXPECTED OUTPUT - DELETION SUCCESSFUL""")
print()
print("PRODUCT TABLE BEFORE DELETION")
print_table(cursor, "product")
print()
print("Running QUERY 5")


try:
    cursor.execute(f"DELETE FROM product WHERE product_id = ?", (31,))
    conn.commit()
    print("DELETION SUCCESSFUL")
    print("PRODUCT TABLE AFTER DELETION")
    print_table(cursor, "product")
    print()

except sqlite3.Error as e:
    print(f"QUERY 5 result: An error occurred: {e}")














