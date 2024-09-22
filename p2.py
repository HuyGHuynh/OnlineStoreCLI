class Customer:
    def __init__(self, name="", email="", phone="", address=""):  # parameterized constructor
        """
        Constructor for object of Customer class
        :param name: Customer's name (str)
        :param email: Customer's email (str)
        :param phone: Customer's phone number (str)
        :param address: Customer's address (str)
        """
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    def read_info(self, info):
        """
        Read all a list of info, store them into a customer's info
        :param info:
        info: list of info (list)
        :return: None
        """
        self.name = info[0]
        self.email = info[1]
        self.phone = info[2]
        self.address = info[3]

    def display_info(self):
        """
        Display all info of a specific customer
        :return: None
        """
        print("Name: " + self.name)
        print("Email: " + self.email)
        print("Phone number: " + self.phone)
        print("Address: " + self.address)