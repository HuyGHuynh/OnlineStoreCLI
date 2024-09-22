class item_control:
    def __init__(self):
        self.item_name_list = []    # Create the list of name of the item
        self.item_info_list = []    # Create the list of the lists of all info of an item
        self.item_id_list = []  # Create the list of ID of the items

        # Update the item list, the 2d list of item info, and the item ID list
        f = open("item.txt", "r")
        self.lines = f.readlines()
        for raw_info in self.lines:
            raw_info = raw_info.replace("\n", "")
            raw_info = raw_info.split(";")
            self.item_name_list.append(raw_info[0])
            self.item_id_list.append(raw_info[1])
            self.item_info_list.append(raw_info)
        f.close()

    def show_all_item(self):
        """
        This function will display all the item we have in store
        :return:
        """
        print('')
        # Get all the item in the item list and display it
        for i in range(len(self.item_name_list)):
            print(self.item_name_list[i])
            print('\tID: '+ self.item_id_list[i])

    def show_info(self):
        """
        This function will display all the info of a specific item in store
        :return:
        """
        wanted_item = input("\nEnter your wanted item (Or x to exit): ").lower()  # Ask for the name and lower the name input
        temp_item_name_list = list((map(lambda x: x.lower(), self.item_name_list)))  # Make another list of lowered item name for easier searching process

        while wanted_item not in temp_item_name_list:   # Check if the item searched is not in the store
            if wanted_item == 'x':  # Exit if the user press x (meaning exit)
                return
            else:   # If the user enter the wrong input
                print("Please enter a valid item")
                wanted_item = input("\nEnter your wanted item (Or to exit): ").lower()
        else:   # Item is in the store
            item_index = temp_item_name_list.index(wanted_item)  # Get the index in the item list
            w = self.item_info_list[item_index]  # Get the info of the item in the 2d info list
            # Print info
            print(w[0])
            print('ID: ' + w[1])
            print('Quantity: ' + w[2])
            print('Size: ' + w[3])
            print('Description: ' + w[4])

    def search_item_name(self):
        """
        This function will display the related item to the user's searched keyword
        :return:
        """
        temp_item_name_list = list((map(lambda x: x.lower(), self.item_name_list)))  # Make another list of lowered item name for easier searching process
        index = -1  # Setting the index for later use
        while True:
            wanted_item = input("\nEnter your keyword (Or x to exit): ").lower()
            if wanted_item == 'x':  # Exit when the user enter x
                return
            elif wanted_item in '                                  ':   # If the user enter a blank space
                print('Please input something')
            else:   # The input is valid
                for k in temp_item_name_list:   # Loop through the item list
                    if wanted_item in k:    # If the keyword matches any character in item, display the item and the info
                        index = temp_item_name_list.index(k)    # Change the index to the index of the item being processed
                        print(self.item_name_list[index])   # Print the correctly capitalized name of the item
                        print("\tID: " + self.item_id_list[index])  # Print the item's ID
                if index == -1:  # When no item matches the search
                    print("No related item was found")
                else:   # When an item is found
                    break

    def search_item_id(self):
        """
        This function will display the item with the ID the user input
        :return:
        """
        while True:
            try:
                wanted_item = str(input("\nEnter the ID (Or x to exit): "))
                if wanted_item == 'x' or wanted_item == 'X':    # If the user want to exit
                    return
                elif wanted_item in self.item_id_list:  # If the user input a number
                    index = self.item_id_list.index(wanted_item)    # Get the index of the item in the ID list
                    print("Item: " + self.item_name_list[index])    # Print the item name with the index
                    print("\tID: " + wanted_item)   # Print the ID
                    break
                elif int(wanted_item) in range(1, 10):  # When the input is a number from 1-9 without 0 in front
                    wanted_item = '0' + wanted_item  # Add 0 to the front
                    index = int(wanted_item) - 1    # Change the index
                    print("Item: " + self.item_name_list[index])  # Print name
                    print("\tID: " + wanted_item)   # Print ID
                    break
                else:   # When no ID was found
                    print("No item was found, please enter a valid ID")
            except Exception:   # If the user input anything other than a number
                print("Please enter an ID number")


request = item_control()