from models import Coffee, Order
import json
import os

def load_menu_from_json(filepath="menu.json"):
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
            return [Coffee(item["name"], item["price"]) for item in data]
    except FileNotFoundError:
        print("Menu file not found.")
        return []
    except Exception as e:
        print(f"Error loading menu: {e}")
        return []

def get_valid_int(prompt, min_val=None):
    try:
        val = int(input(prompt))
        if min_val is not None and val < min_val:
            print(f"Value must be at least {min_val}.")
            return None
        return val
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def main():
    menu = load_menu_from_json()
    if not menu:
        print("No menu available. Exiting.")
        return

    order = Order()

    while True:
        print("\n--- Coffee Menu ---")
        print("1. Place Order")
        print("2. View Order")
        print("3. Search for a Coffee by Name")
        print("4. Suggest Cheapest Coffee")
        print("5. Remove Item from Order")
        print("6. Checkout")
        print("7. Exit")

        choice = get_valid_int("Choose an option: ")
        if choice is None:
            continue
        
        if choice == 1:
            for i, coffee in enumerate(menu, 1):
                print(f"{i}. {coffee}")
            choose = get_valid_int("\nChoose an option: ")
            if choose and 1 <= choose <= len(menu):
                coffee = menu[choose - 1]
                qty = get_valid_int(f"Enter quantity for {coffee.name}: ", min_val=1)
                if qty is not None:
                    order.add_item(coffee, qty)

        elif choice == 2:
            order.show_order()
            
        elif choice == 3:
            search_name = input("Enter coffee name to search: ").strip().lower()
            found = False
            for coffee in menu:
                if search_name in coffee.name.lower():
                    print(f"Found: {coffee}")
                    found = True
            if not found:
                print("No matching coffee found.")

        elif choice == 4:
            cheapest = min(menu, key=lambda c: c.price)
            print(f"The cheapest coffee is: {cheapest}")

        elif choice == 5:
            order.remove_item()

        elif choice == 6:
            order.checkout()

        elif choice == 7:
            print("Thanks for visiting. Goodbye.")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
