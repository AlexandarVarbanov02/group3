class Book:
    def __init__(self, name: str, rating: float, genre: str, upc: str, price: float, availability: int, reviews: int,
                 description: str):
        self.__name = name
        self.__rating = rating
        self.__genre = genre
        self.__upc = upc
        self.__price = price
        self.__availability = availability
        self.__reviews = reviews
        self.__description = description

    def __str__(self):
        return (self.__name + "\n" + self.__genre + "\n" + self.__upc + "\n" + str(self.__price) + "\n" + str(
            self.__availability)
                + "\n" + str(self.__reviews) + "\n" + self.__description + "\n")

    # getter and setter for name
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str):
            raise TypeError("Name can only be a string!")
        if new_name == "":
            raise ValueError("Book name cannot be empty!")
        self.__name = new_name

    # getter and setter for rating
    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, float):
            raise TypeError("Rating can only be a float!")
        if value < 0:
            raise ValueError("Rating cannot be less than 0!")
        self.__rating = value

    # getter and setter for upc
    @property
    def upc(self):
        return self.__upc

    @upc.setter
    def upc(self, new_upc):
        if not isinstance(new_upc, str):
            raise TypeError("UPC can only be a string!")
        if new_upc == "":
            raise ValueError("UPC cannot be empty!")
        self.__upc = new_upc

    # getter and setter for price
    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if not isinstance(new_price, float):
            raise TypeError("Price needs to be a float!")
        if new_price < 0:
            raise ValueError("Price cannot be less than 0!")
        self.__price = new_price

    # getter and setter for genre
    @property
    def genre(self):
        return self.__genre

    @genre.setter
    def genre(self, new_genre):
        if not isinstance(new_genre, str):
            raise TypeError("Genre can only be a string!")
        if new_genre == "":
            raise ValueError("Genre cannot be empty.")
        self.__genre = new_genre

    # getter and setter for availability
    @property
    def availability(self):
        return self.__availability

    @availability.setter
    def availability(self, new_availability):
        if not isinstance(new_availability, int):
            raise TypeError("Availability can only be an int!")
        if new_availability < 0:
            raise ValueError("The availability cannot be a negative number.")
        self.__availability = new_availability

    # getter and setter for review
    @property
    def reviews(self):
        return self.__reviews

    @reviews.setter
    def reviews(self, new_reviews):
        if not isinstance(new_reviews, int):
            raise TypeError("Number of reviews can only be an int!")
        if new_reviews < 0:
            raise ValueError("The number of reviews cannot be a negative number.")
        self.__reviews = new_reviews

    # getter and setter for description
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, new_description):
        if not isinstance(new_description, str):
            raise TypeError("Description can only be string!")
        if new_description == "":
            raise ValueError("The description cannot be empty")
        self.__description = new_description


