import json
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()


class Coffee:
    def __init__(self, name, price, category=None):
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return f"{self.name} ({self.category}) - ₹{self.price:.2f}" if self.category else f"{self.name} - ₹{self.price:.2f}"

class Order:
    def __init__(self, username):
        self.username = username
        self.items = []

    def add_item(self, coffee, quantity):
        self.items.append((coffee, quantity))
        print(f"Added {quantity} x {coffee.name}")

    def remove_item(self):
        if not self.items:
            print("No items.")
            return
        self.show_order()
        try:
            idx = int(input("Item number to remove: ")) - 1
            if 0 <= idx < len(self.items):
                coffee, qty = self.items.pop(idx)
                print(f"Removed {qty} x {coffee.name}")
        except ValueError:
            print("Invalid input.")

    def total(self):
        return sum(item.price * qty for item, qty in self.items)

    def apply_discount(self):
        total = self.total()
        if total > 100:
            discount = total * 0.2
            print(f"Discount: ₹{discount:.2f}")
            return total - discount
        return total

    # def show_order(self):
    #     if not self.items:
    #         print("\nEmpty cart.")
    #         return
    #     for i, (item, qty) in enumerate(self.items, 1):
    #         print(f"\n{i}. {item.name} x {qty} - ₹{item.price * qty:.2f}")
    #     print(f"Total: ₹{self.apply_discount():.2f}")

    def show_order(self):
        if not self.items:
            console.print("\n[bold red]Empty cart.[/bold red]")
            return
        table = Table(title="Your Order")
        table.add_column("No", justify="center")
        table.add_column("Coffee", justify="left")
        table.add_column("Qty", justify="center")
        table.add_column("Total Price", justify="right")
        for i, (item, qty) in enumerate(self.items, 1):
            table.add_row(str(i), item.name, str(qty), f"₹{item.price * qty:.2f}")
        table.add_row("", "", "[bold]Total[/bold]", f"[bold green]₹{self.apply_discount():.2f}[/bold green]")
        console.print(table)


    def checkout(self):
        if not self.items:
            print("No items to checkout.")
            return
        self.show_order()
        confirm = input("Checkout? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            self.save_receipt()
            self.items.clear()
            print("Order complete!")
        else:
            print("Cancelled.")

    def save_receipt(self):
        data = {
            "user": self.username,
            "items": [{"name": i.name, "qty": q, "price": i.price} for i, q in self.items],
            "total": self.apply_discount(),
            "timestamp": datetime.now().isoformat()
        }
        with open("data/orders.json", "a") as f:
            f.write(json.dumps(data) + "\n")

class User:
    def __init__(self, username):
        self.username = username

class UserManager:
    def __init__(self):
        self.users_file = "data/users.json"
        self.load_users()

    def load_users(self):
        try:
            with open(self.users_file) as f:
                self.users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = []

    def save_users(self):
        with open(self.users_file, "w") as f:
            json.dump(self.users, f, indent=2)

    def login_or_register(self):
        username = input("Enter username: ").strip()
        if username in self.users:
            print("Welcome back!")
        else:
            print("Registering new user.")
            self.users.append(username)
            self.save_users()
        return User(username)

    # def view_history(self, username):
    #     print(f"\n--- Order History for {username} ---")
    #     try:
    #         with open("data/orders.json") as f:
    #             for line in f:
    #                 data = json.loads(line)
    #                 if data["user"] == username:
    #                     print(f"Date: {data['timestamp']}")
    #                     for item in data["items"]:
    #                         print(f"  {item['name']} x {item['qty']} - ₹{item['price'] * item['qty']:.2f}")
    #                     print(f"Total: ₹{data['total']:.2f}\n")
    #     except FileNotFoundError:
    #         print("No history found.")

    def view_history(self, username):
        console.print(f"\n[bold blue]----- Order History for {username} -----[/bold blue]")
        try:
            with open("data/orders.json") as f:
                found = False
                for line in f:
                    data = json.loads(line)
                    if data["user"] == username:
                        found = True
                        console.print(f"[cyan]Date:[/cyan] {data['timestamp']}")
                        for item in data["items"]:
                            console.print(f"  {item['name']} x {item['qty']} - ₹{item['price'] * item['qty']:.2f}")
                        console.print(f"[bold yellow]Total: ₹{data['total']:.2f}[/bold yellow]\n")
                if not found:
                    console.print("No history found.")
        except FileNotFoundError:
            console.print("[red]No order history file found.[/red]")


