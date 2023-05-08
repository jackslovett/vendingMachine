# Vending machine program

# Define product list and their corresponding prices
products = {
    'tea': 1.00,
    'coffee': 1.50,
    'snacks': 2.00,
    'cold drinks': 2.50
}

# Define a function to display the product list and their prices
def display_products():
    print('PRODUCTS:')
    for product, price in products.items():
        print(product.capitalize(), f': ${price:.2f}')

# Define a function to process the user's choice
def process_choice(choice, credit):
    if choice in products:
        price = products[choice]
        if credit >= price:
            print(f'Dispensing {choice}...')
            print(f'Change: ${credit - price:.2f}')
            return True
        else:
            print('Not enough credit. Please insert more coins.')
            return False
    else:
        print('Invalid choice. Please try again.')
        return False

# Define a function to start the vending machine
def start_vending_machine():
    print('Welcome to the vending machine!')
    display_products()

    credit = 0  # initialize credit to 0

    while True:
        # Prompt the user for input
        choice = input('Enter your choice (or q to quit): ').lower()

        # If the user chooses to quit, break out of the loop
        if choice == 'q':
            break

        # If the user chooses a product, process the choice
        if choice in products:
            price = products[choice]
            print(f'The price of {choice} is ${price:.2f}')
            while credit < price:
                # Prompt the user to insert coins until they have enough credit
                coin = input('Insert coin (in dollars): ')
                credit += float(coin)

            # Dispense the product and calculate the change
            print(f'Dispensing {choice}...')
            change = credit - price
            if change > 0:
                print(f'Change: ${change:.2f}')
            credit = 0  # reset credit to 0 after the transaction

        # If the user chooses an invalid option, print an error message
        else:
            print('Invalid choice. Please try again.')

# Call the start_vending_machine function to start the program
start_vending_machine()
