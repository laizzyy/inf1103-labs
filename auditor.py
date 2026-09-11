inventory = 0

while True:
    stock = input("Enter stock quantity (or type quit): ")

    if stock == "quit":
        break
    
    stock = int(stock)