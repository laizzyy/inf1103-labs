inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity (or type quit): ")

    if stock == "quit":
        print("Total Units Processed:", inventory)
        print("Number of Failed/Rejected Entries:", failed_entries)
        break

    if not stock.isdigit():
        print("Error: Please enter a valid number.")
        failed_entries += 1
        continue

    stock = int(stock)

    if stock < 0:
        print("Error: Stock quantity cannot be negative.")
        failed_entries += 1
        continue

    inventory += stock

    print("Current inventory:", inventory)

    if inventory > 500:
        print("ALERT: Overstock! Inventory exceeds 500 units.")
        break