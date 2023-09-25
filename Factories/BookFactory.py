from Models.Book import Book


class BookFactory:

    def __init__(self):
        self.__list_of_produced_books = []

    def __create_book(self, name, genre, upc, price,  availability, reviews, description):
        return Book(name, genre, upc, price,  availability, reviews, description)

    def add_book(self, name, genre, upc, price,  availability, reviews, description):
        self.__list_of_produced_books.append(
            self.__create_book(name, genre, upc, price,  availability, reviews, description))

    @property
    def list_of_produced_books(self):
        return self.__list_of_produced_books
