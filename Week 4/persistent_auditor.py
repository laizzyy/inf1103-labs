def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            inventory = int(file.readline().strip())
            return inventory
    except FileNotFoundError:
        return 0

def save_inventory(total, history):
    with open("inventory.txt", "w") as file:
        file.write(str(total) + "\n")
        file.write(str(history))

def get_valid_input():
    stock = input("Enter stock quantity (or type quit): ")

    if stock.lower() == "quit":
        return "quit"

    if not stock.isdigit():
        print("Error: Please enter a valid positive number.")
        return None

    return int(stock)


def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * 0.10
    return tax


def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


inventory = load_inventory()
failed_attempts = 0
deliveries_processed = 0
transaction_history = []

while True:
    delivery = get_valid_input()

    if delivery == "quit":
        save_inventory(inventory, transaction_history)
        generate_report(inventory, failed_attempts)
        break

    if delivery is None:
        failed_attempts += 1
        continue

    inventory = process_delivery(inventory, delivery)
    tax = calculate_tax(delivery)

    transaction_history.append(delivery)
    deliveries_processed += 1

    print("Delivery amount:", delivery)
    print("Tax for this delivery: $", tax)
    print("Current inventory:", inventory)

