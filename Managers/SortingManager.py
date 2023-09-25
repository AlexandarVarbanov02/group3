import json

from Shared.File_Checker import FileChecker


class SortingManager:
    def __init__(self):
        self.__book_collection = []

    @property
    def book_collection(self):
        return self.__book_collection

    @book_collection.setter
    def book_collection(self, new_book_collection):
        if len(new_book_collection) < 1:
            raise ValueError("There are not any book to be sorted")
        self.__book_collection = new_book_collection

    def sort_books_by_title(self, type_of_sorting):
        result = []
        if type_of_sorting == 'asc':
            result = sorted(self.__book_collection, key=lambda x: x.name.lower())
        else:
            result = sorted(self.__book_collection, key=lambda x: x.name.lower())
            result.reverse()

        return result

    def sort_books_by_price(self, type_of_sorting):
        result = []
        if type_of_sorting == 'asc':
            result = sorted(self.__book_collection, key=lambda x: x.price)
        else:
            result = sorted(self.__book_collection, key=lambda x: x.price)
            result.reverse()

        return result

    def sort_books_by_availability(self, type_of_sorting):
        result = []
        if type_of_sorting == 'asc':
            result = sorted(self.__book_collection, key=lambda x: x.availability)
        else:
            result = sorted(self.__book_collection, key=lambda x: x.availability)
            result.reverse()

        return result

    def filter_books_by_price(self, operation_sign, filter_price):
        result = []
        if operation_sign == '>':
            for book in self.__book_collection:
                if filter_price > book.price:
                    result.append(book)
        elif operation_sign == '<':
            for book in self.__book_collection:
                if filter_price < book.price:
                    result.append(book)
        elif operation_sign == '>=':
            for book in self.__book_collection:
                if filter_price >= book.price:
                    result.append(book)
        elif operation_sign == '<=':
            for book in self.__book_collection:
                if filter_price <= book.price:
                    result.append(book)
        else:
            for book in self.__book_collection:
                if filter_price == book.price:
                    result.append(book)
        return result

    def filter_books_by_availability(self, operation_sign, filter_availability):
        result = []
        if operation_sign == '>':
            for book in self.__book_collection:
                if filter_availability > book.availability:
                    result.append(book)
        elif operation_sign == '<':
            for book in self.__book_collection:
                if filter_availability < book.availability:
                    result.append(book)
        elif operation_sign == '>=':
            for book in self.__book_collection:
                if filter_availability >= book.availability:
                    result.append(book)
        elif operation_sign == '<=':
            for book in self.__book_collection:
                if filter_availability <= book.availability:
                    result.append(book)
        else:
            for book in self.__book_collection:
                if filter_availability == book.availability:
                    result.append(book)
        return result

    def search_book_by_book_title(self, book_title):
        for book in self.__book_collection:
            if book.name == book_title:
                return book

    def search_books_by_list_of_titles(self):
        ch_file = FileChecker("Db_Files/jsonFile.json")
        ch_file.check_file()
        json_file = open("Db_Files/jsonFile.json", 'r')
        json_input = json_file.read()
        data = json.loads(json_input)
        json_file.close()
        result = []

        for book in self.__book_collection:
            for title in data:
                if book.name == title:
                    result.append(book)
        return result

