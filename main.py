from create_tables import create_tables
from insert import add_pizza, add_customer
from display import display_all_pizzas, display_all_customers
from order import place_order

if __name__ == "__main__":
    create_tables()
    while True:
        print("\n--- Pizza Store Management ---")
        print("1. Add a new pizza")
        print("2. Add a new customer")
        print("3. Place an order")
        print("4. Display all pizzas")
        print("5. Display all customers")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_pizza()
        elif choice == "2":
            add_customer()
        elif choice == "3":
            place_order()
        elif choice == "4":
            display_all_pizzas()
        elif choice == "5":
            display_all_customers()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")