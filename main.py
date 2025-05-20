from models import Coffee, Order, UserManager
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
        raise []

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
    os.makedirs('data', exist_ok=True)
    user_manager = UserManager()
    current_user = user_manager.login_or_register()

    menu = load_menu_from_json()
    if not menu:
        print("No manu available. Exiting.")
        return None



    order = Order(current_user.username)

    while True:
        print(f"\n--- Welcome, {current_user.username}! ---")
        print("1. Place Order")
        print("2. View Current Order")
        print("3. Search Coffee")
        print("4. Suggest Cheapest")
        print("5. Remove Item")
        print("6. Checkout")
        print("7. View Order History")
        print("8. Logout")
        print("9. Exit")

        choice = get_valid_int("Choose an option: ")
        if choice is None:
            continue

        # if choice == 1:
        #     categories = sorted(set(coffee.category for coffee in menu))
            
        #     for i, cat in enumerate(categories, 1):
        #         print(f"{i}. {cat}")
                
        #     cat_choice = get_valid_int("Select category: ", min_val=1)
            
        #     if cat_choice and cat_choice <= len(categories):
        #         selected = [c for c in menu if c.category == categories[cat_choice-1]]
        #         for i, coffee in enumerate(selected, 1):
        #             print(f"{i}. {coffee}")
        #         c_choice = get_valid_int("Select coffee: ", min_val=1)
        #         if c_choice and c_choice <= len(selected):
        #             qty = get_valid_int("Enter quantity: ", min_val=1)
        #             if qty:
        #                 order.add_item(selected[c_choice-1], qty)

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
            search = input("Search coffee name: ").lower()
            found = [c for c in menu if search in c.name.lower()]
            if found:
                for c in found:
                    print(c)
            else:
                print("No match found.")

        elif choice == 4:
            cheapest = min(menu, key=lambda x: x.price)
            print(f"Cheapest coffee is: {cheapest}")

        elif choice == 5:
            order.remove_item()

        elif choice == 6:
            order.checkout()

        elif choice == 7:
            user_manager.view_history(current_user.username)

        elif choice == 8:
            print("Logging out...")
            current_user = user_manager.login_or_register()

        elif choice == 9:
            print("Exiting app. Goodbye!")
            break

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
    # menu =  load_menu_from_json()
    # print(menu)

