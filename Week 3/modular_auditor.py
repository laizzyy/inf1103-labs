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


