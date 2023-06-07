import datetime

# Vending machine program for ITO4133

# Define product list, their corresponding prices, and stock availability
products = {
    'tea': {'price': 1.00, 'stock': 5},
    'coffee': {'price': 1.50, 'stock': 5},
    'coke': {'price': 2.00, 'stock': 5},
    'juice': {'price': 2.50, 'stock': 5}
}

maintenance_mode = False
transactions = []


# Define a function to display the product list and their prices, considering stock availability
def display_products():
    # Display the list of products and their prices, taking into account stock availability.
    print('PRODUCTS:')
    for product, details in products.items():
        if details['stock'] > 0:
            print(product.capitalize(), f': ${details["price"]:.2f}')
        else:
            print(product.capitalize(), '- Out of stock')


def process_choice(choice, credit, total_price):
    # Process the user's choice and perform the necessary actions based on the choice.
    if choice in products:
        details = products[choice]
        if details['stock'] > 0:
            price = details['price']
            remaining_price = price - total_price
            if credit >= remaining_price:
                print(f'Dispensing {choice}...')
                details['stock'] -= 1  # Reduce the stock by 1
                return price
            else:
                print('Not enough credit. Please insert more coins.')
                return 0
        else:
            print('Sorry, this item is out of stock.')
            return 0
    elif choice == 'cancel':
        print('Purchase cancelled.')
        return 0
    else:
        print('Invalid choice. Please try again.')
        return 0


def reset_transaction():
    # Reset the transaction by clearing the selected products and resetting the total price.
    print('Transaction reset.')


def cancel_purchase(payment, total_price):
    # Cancel the current purchase and return the payment.
    refund = payment
    print(f'Purchase cancelled. Refund: ${refund:.2f}')


def validate_coin(coin):
    # Validate if the coin value is valid.
    valid_coins = [0.05, 0.10, 0.20, 0.50, 1.0, 2.0]
    return coin in valid_coins


def select_products():
    # Allow the user to select products and calculate the total price.
    total_price = 0
    selected_products = []

    while True:
        if maintenance_mode:
            print('The vending machine is currently under maintenance.')
            admin_mode()
            break

        choice = input('Enter your choice (press f to finish selection, c to cancel, or a for admin mode): ').lower()

        if choice == 'f':
            break

        if choice == 'reset':
            total_price = 0
            selected_products.clear()
            print('Transaction reset.')
            continue

        if choice == 'c':
            total_price = 0
            selected_products.clear()
            cancel_purchase()
            break

        if choice == 'a':
            admin_mode()
            display_products()  # Display the product list after exiting admin mode
            continue

        if choice in products:
            if products[choice]['stock'] > 0:
                if choice in ['tea', 'coffee']:
                    sugar_choice = input('Would you like sugar? (y/n): ').lower()
                    if sugar_choice == 'y':
                        selected_products.append(choice + ' with sugar')
                        total_price += products[choice]['price']
                    elif sugar_choice == 'n':
                        selected_products.append(choice)
                        total_price += products[choice]['price']
                    else:
                        print('Invalid choice. Please try again.')
                        continue

                    milk_choice = input('Would you like milk for 50¢ extra? (y/n): ').lower()
                    if milk_choice == 'y':
                        selected_products[-1] += ' with milk'
                        total_price += 0.50
                    elif milk_choice != 'n':
                        print('Invalid choice. Please try again.')
                        continue
                else:
                    selected_products.append(choice)
                    total_price += products[choice]['price']

                products[choice]['stock'] -= 1
                print(f'{choice.capitalize()} added to the selection.')
            else:
                print('Sorry, this item is out of stock.')
        else:
            print('Invalid choice. Please try again.')

    return total_price, selected_products


def process_payment(total_price, selected_products):
    # Process the payment for the selected products.
    payment = 0.0

    while payment < total_price:
        coin = input('Insert coin (in dollars), enter b to edit selection, or enter c to cancel: ')
        if coin == 'c':
            cancel_purchase(payment, total_price)
            return False
        elif coin == 'b':
            display_current_selection(selected_products)
            total_price, selected_products = edit_selection(total_price, selected_products)
            print(f'Updated total price: ${total_price:.2f}')
            continue

        try:
            coin = float(coin)
            if coin > 0 and validate_coin(coin):
                payment += coin
                if payment >= total_price:
                    break
            else:
                print('Invalid coin value. Please enter a valid amount.')
        except ValueError:
            print('Invalid input. Please enter a valid coin amount.')

    change = payment - total_price
    if change > 0:
        print(f'Change: ${change:.2f}')
    return True


def display_current_selection(selected_products):
    # Display the current selected products and their corresponding numbers.
    print('Current Selection:')
    for i, product in enumerate(selected_products, start=1):
        print(f'{i}. {product.capitalize()}')


def edit_selection(total_price, selected_products):
    # Allow the user to edit their current selection by removing a numbered item.
    while True:
        try:
            selection_number = int(input('Enter the number of the item to remove: '))
            if 1 <= selection_number <= len(selected_products):
                removed_product = selected_products.pop(selection_number - 1)
                total_price -= products[removed_product.split(' ')[0]]['price']
                print(f'{removed_product.capitalize()} removed from the selection.')
                return total_price, selected_products
            else:
                print('Invalid selection number. Please enter a valid number.')
        except ValueError:
            print('Invalid input. Please enter a valid number.')


def admin_mode():
    # Enter admin mode with password verification and perform administrative actions.
    password = input('Enter the password [admin123] (or enter c to cancel): ')
    if password == 'admin123':
        print('Welcome to admin mode!')
        while True:
            print('ADMIN MENU:')
            print('1. Restock items')
            print('2. Place/Lift maintenance mode')
            print('3. View transaction history')
            print('4. Exit admin mode')

            admin_choice = input('Enter your choice: ')

            if admin_choice == '1':
                restock_items()
            elif admin_choice == '2':
                place_lift_maintenance_mode()
            elif admin_choice == '3':
                display_transactions()
            elif admin_choice == '4':
                print('Exiting admin mode...')
                break
            else:
                print('Invalid choice. Please try again.')

    elif password != 'c':
        print('Incorrect password.')


def restock_items():
    # Restock items by adding stock to the existing products.
    print('RESTOCK ITEMS:')
    for product, details in products.items():
        restock_amount = int(input(f'Enter the restock amount for {product.capitalize()}: '))
        details['stock'] += restock_amount
        print(f'{restock_amount} {product.capitalize()} added to stock.')


def place_lift_maintenance_mode():
    # Place or lift the vending machine maintenance mode.
    global maintenance_mode
    maintenance_choice = input('Enter 1 to place the vending machine under maintenance, or 2 to lift maintenance mode: ')
    if maintenance_choice == '1':
        maintenance_mode = True
        print('The vending machine is now under maintenance.')
    elif maintenance_choice == '2':
        maintenance_mode = False
        print('Maintenance mode lifted.')
    else:
        print('Invalid choice. Please try again.')


def display_transactions():
    # Display the transaction history.
    print('TRANSACTION HISTORY:')
    if len(transactions) > 0:
        for i, transaction in enumerate(transactions, start=1):
            print(f'Transaction {i}:')
            print(f'Timestamp: {transaction["timestamp"]}')
            print('Selected products:')
            for product in transaction['products']:
                print(f'- {product.capitalize()}')
            print(f'Total price: ${transaction["total_price"]:.2f}')
            print('-------------------------')
    else:
        print('No transaction history.')


def print_receipt(total_price, selected_products):
    # Print the receipt for the current transaction.
    print('-------------------------')
    print('RECEIPT')
    print('-------------------------')
    print('Selected products:')
    for product in selected_products:
        print(f'- {product.capitalize()}')
    print(f'Total price: ${total_price:.2f}')
    print('-------------------------')
    print('Thank you for your purchase! Enjoy your day!')


def vending_machine():
    # Main function to run the vending machine program.
    print('\n---------------------------')
    print('VENDING MACHINE')
    print('---------------------------\n')
    print('Welcome to the Vending Machine!')

    while True:
        display_products()

        total_price, selected_products = select_products()
        if len(selected_products) == 0:
            print('No products selected. Please make a valid selection.')
            continue

        print(f'Total price: ${total_price:.2f}')
        if process_payment(total_price, selected_products):
            print_receipt(total_price, selected_products)

        # Save the transaction details
        transaction = {
            'timestamp': datetime.datetime.now(),
            'products': selected_products,
            'total_price': total_price
        }
        transactions.append(transaction)

        reset_transaction()

        restart = input('Would you like to make another purchase? (y/n): ')
        if restart.lower() != 'y':
            break

    print('Thank you for using the Vending Machine! Have a great day!')


vending_machine()
