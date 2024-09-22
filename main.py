import p1
from p2 import Customer
import os
import time
import datetime


def announcement():
    """
    Toggle store menu and retrieve user choice
    :return: User choice (int)
    """
    print("\nWelcome to ABCXYZ Gear Store")
    print("Enter an option below")
    print("1. List all items ")
    print("2. List all info of a specific item (quantity, colors, sizes/dims, specs, descriptions, etc.) ")
    print("3. Search item by name ")
    print("4. Search item by item id ")
    print("5. List all info of a specific customer (name, email address, shipping address, etc.) ")
    print("6. Placing orders (the quantity must be updated when an item is bought)")
    print("7. Sign up for a new customer")

    # print("\nEnter your choice")
    option = input("\nInput your choice (Input X to exit): ")
    return option


def save_customer(list_customer):
    """
    Save a list of customer into customer.txt (override if file already exists)
    :param list_customer: List of customer (list)
    :return: None
    """
    with open("customer.txt", "w") as save_all:  # Open customer.txt in write mode
        # Store the first customer
        saveline = str(
            list_customer[0].name + ";" + list_customer[0].email + ";" + list_customer[0].phone + ";" + list_customer[0].address)
        save_all.write(saveline)
        for customer in list_customer[1:]:  # Loop through every customer in customer list
            saveline = str(
                "\n" + customer.name + ";" + customer.email + ";" + customer.phone + ";" + customer.address)
            save_all.write(saveline)


def list_specific_customer(list_customer):
    """
    Display all info of a specific customer, searching by their phone number
    :param list_customer: list of customer objects (list)
    :return: None
    """
    flag = False  # This flag will keep track if there's a customer match the search
    phone = input("Input customer phone number to search: ")
    for customer in list_customer:  # Loop through a list of customer
        if customer.phone == phone:  # If customer found by phone
            flag = True  # Customer found
            customer.display_info()  # Display that matching customer
            print("\n")

    if not flag:  # If no customer found
        print("No customer matches phone number: " + phone)


def add_purchase_history(customer, item_dict):
    """
    This function will run if a purchase has been made, create a history.txt and append purchase history to that file
    :param customer: A customer who made the purchase (Customer)
    :param item_dict: A dictionary of purchase item, contains their name and quantity (dict)
    :return: None
    """
    # For command line formatting purpose only
    print("Writing to purchase history file")
    for i in range(3):
        time.sleep(0.5)
        print(".")

    # Open history.txt to append purchase
    # If history.txt does not exist, new file will be created.
    # Else, program will append to that file without overwriting the previous file.
    with open("history.txt", "a") as append_file:
        append_file.write(str(datetime.datetime.now()))  # Write current date & time
        append_file.write("\nName: " + customer.name)
        append_file.write("\nEmail: " + customer.email)
        append_file.write("\nPhone number: " + customer.phone)
        append_file.write("\nAddress: " + customer.address)
        append_file.write("\nPurchased item:")
        for item, quantity in item_dict.items():  # Write items to purchase history
            append_file.write("\n" + str(quantity) + "\t" + item)
        append_file.write("\n\n")  # Line section break

    time.sleep(0.5)
    print("Write successfully!")


def placing_order(list_customer):
    """
    Placing order for a customer, searching customer by phone number, choose item and its quantity to order
    :param list_customer: list of customer objects (list)
    :return: None
    """
    item_name_list, item_info_list = get_item_list()
    temp_item_name_list = list((map(lambda x: x.lower(), item_name_list)))
    flag = False  # This flag will keep track if there's a customer match the search
    phone = input("\nPlease input your customer phone number: ")
    bought_customer = Customer()
    bought_dict = {}
    # Search customer
    for customer in list_customer:
        if customer.phone == phone:  # If customer found by phone
            flag = True  # Customer found
            bought_customer = customer
            customer.display_info()  # Display that matching customer
            buy = 'y'
            # Manual check if this is the correct customer
            while True:
                choice = input("\nIs this the correct customer? (Y/N): ")
                if choice == 'N' or choice == 'n':
                    return
                elif choice == 'Y' or choice == 'y':
                    break
                else:
                    print("Invalid choice")

            # Insert item and start searching item
            while buy == 'y':
                item = input("\nInsert the item you want to purchase (Or x to exit): ").lower()  # Name
                while item not in temp_item_name_list:  # Check if the item is valid
                    if item == 'x' or item == 'X':  # Check if the user want to exit
                        return
                    print("No item was found")
                    item = input(
                        "\nInsert the item you want to purchase (Or x to exit): ").lower()  # Ask for item again
                else:  # Item is valid
                    index = temp_item_name_list.index(item)
                    item_quantity = int(item_info_list[index][2])
                    order_amount = 0
                    if item_quantity > 0:  # Check for availability of item
                        order_amount = order_amount_calc(order_amount)  # Get the order amount of the user
                        if order_amount is None:
                            return
                        while order_amount > item_quantity:  # Check if the buyer's purchase is more than stock
                            print("We only have " + str(item_quantity) + " in stock")
                            answer = input(
                                "\nDo you want to buy all? (Y/N)").lower()  # Ask if want to buy all or buy another amount
                            while answer != 'y' and answer != 'n':  # Invalid answer
                                answer = input("\nPlease enter the right choice: ").lower()
                            else:
                                if answer == 'y':  # Buy all
                                    order_amount = item_quantity
                                else:  # Buy another amount
                                    order_amount = 0
                                    order_amount = int(order_amount_calc(order_amount))
                        if order_amount == 0:  # If the buyer change mind and don't want to buy the item
                            pass
                        else:
                            quantity_update(item_quantity, index, item_info_list, order_amount)
                            print("Purchased successfully")
                            if item_name_list[index] in list(bought_dict.keys()):
                                bought_dict[item_name_list[index]] += order_amount
                            else:
                                bought_dict[item_name_list[index]] = order_amount
                    else:
                        print("Item is currently out of stock")
                buy = input("\nDo you want to buy anything else? (Y/N): ").lower()
                while buy != 'y' and buy != 'n':
                    print("Invalid option")
                    buy = input("\nDo you want to buy anything else? (Y/N): ").lower()
                else:
                    pass

    if not flag:  # If no customer found
        print("No customer matches phone number: " + phone)
        return
    else:
        # Write the purchase history to file history.txt
        add_purchase_history(bought_customer, bought_dict)


def order_amount_calc(order_amount):
    """
    This function will take the amount the user ordered
    :param order_amount: Take in the order amount from function placing_order
    :return:
    """
    while order_amount == 0:
        try:
            order_amount = input("\nInsert the amount you want to purchase (Or x to exit): ")
            if order_amount == 'x' or order_amount == 'X':  # The user wants to exit
                return
            order_amount = int(order_amount)    # If the user input a number, then turn it into int
            return order_amount
        except Exception:   # If the user input anything else than a number, return to line 161
            print("Please enter a number")
            order_amount = 0


def sign_up(list_customer):
    """
    Sign up a new customer and store their information into database (customer.txt)
    :param list_customer: List of customer (list)
    :return: None
    """
    new_customer = Customer()  # Create a new customer
    print("Insert info for new customer")
    new_customer.name = input("Customer name: ")
    new_customer.email = input("Email address: ")
    new_customer.phone = input("Phone number: ")
    new_customer.address = input("Address: ")
    list_customer.append(new_customer)  # Append the retrieved one to the customer list

    # Save new customer to file customer.txt (append to file)
    saveline = str(
        "\n" + new_customer.name + ";" + new_customer.email + ";" + new_customer.phone + ";" + new_customer.address)
    with open("customer.txt", "a") as save_file:
        save_file.write(saveline)


def menu_choice(list_customer):
    """
    Call distinct functions based on user choice
    :return: None
    """
    while True:
        option = announcement()  # Retrieve the option choice returned from the function announcement()
        if option == "1":  # List all item
            p1.request.show_all_item()
        elif option == "2":  # List all info of a specific item
            p1.request.show_info()
        elif option == "3":  # Search item by name
            p1.request.search_item_name()
        elif option == "4":  # Search item by item id
            p1.request.search_item_id()
        elif option == "5":  # List all info of a specific customer
            list_specific_customer(list_customer)
        elif option == "6":  # Placing order
            placing_order(list_customer)
            p1.request.__init__()
        elif option == "7":  # Sign up for a new customer
            sign_up(list_customer)
        elif option == "X" or option == "x":  # Exit the function
            break
        else:   # Invalid choice
            print("Invalid option!")
            time.sleep(2)

        os.system('pause')  # Press any key to continue


def read_customer_file():
    """
    Read the customers' information database and append customers into a list
    :return: customer_list: a list of customers from database (list)
    """
    customer_list = []
    in_file = open("customer.txt", "r")
    linelist = in_file.readlines()  # Split the file to a list, each list element contains one line
    for line in linelist:  # Loop through every line
        line = line.replace("\n", "")  # Replace \n in string
        line = line.split(';')  # Split the string to list with delimiter ";"

        temp_cus = Customer()  # Create a temporary customer
        temp_cus.read_info(line)  # Retrieve customer information from current reading line to the temporary object
        customer_list.append(temp_cus)  # Append the retrieved one to the customer list
    in_file.close()
    return customer_list


def get_item_list():
    """
    This function will make a list of item, and a 2d list of all the item and its info
    :return: The item list, and the item info list
    """
    item_name_list = []
    item_info_list = []
    f = open("item.txt", "r")
    lines = f.readlines()
    for raw_info in lines:
        raw_info = raw_info.replace("\n", "")
        raw_info = raw_info.split(";")
        item_name_list.append(raw_info[0])
        item_info_list.append(raw_info)
    f.close()
    return item_name_list, item_info_list


def quantity_update(item_quantity, index, item_info_list, order_amount):
    """
    This function will update the quantity of an item in the data file
    :param item_quantity: The amount of item available in the store
    :param index: The position of the item and its info in the data file
    :param item_info_list: The list of the info of all the items
    :param order_amount: The amount of an item ordered
    :return:
    """
    item_quantity = item_quantity - order_amount    # Calculate the amount of item left after purchase
    item_info_list[index][2] = str(item_quantity)   # Update the amount of the item in the item info list

    f = open("item.txt", "r")
    item_info_update = f.readlines()
    item_info_update[index] = ';'.join(map(str, item_info_list[index])) + '\n'  # Make the list of info of the item into a string
    g = open("item.txt", "w")
    g.writelines(item_info_update)  # Write the new info of the item in the data file
    f.close()
    g.close()


# Main start from here
# Open customer file and initialize a list of Customer class objects
c_list = read_customer_file()

# Display menu
menu_choice(c_list)

# Save file
save_customer(c_list)
