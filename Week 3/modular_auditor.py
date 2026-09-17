inventory = 0
failed_attempts = 0
deliveries_processed = 0

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

while True:
    delivery = get_valid_input()

    if delivery == "quit":
        generate_report(inventory, failed_attempts)
        break

    if delivery is None:
        failed_attempts += 1
        continue

    inventory = process_delivery(inventory, delivery)
    tax = calculate_tax(delivery)

    deliveries_processed += 1

    print("Delivery amount:", delivery)
    print("Tax for this delivery: $", tax)
    print("Current inventory:", inventory)
    

