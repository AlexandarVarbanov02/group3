from Models.Book import Book
from Factories.GenreFactory import GenreFactory
from Storage_classes.GenreStorage import GenreStorage
from Shared.Defines import WEBSITE_URL
from Shared.WebScrapper import WebScraper
from Shared.HelperFunctions import *
from Managers.SortingManager import SortingManager
from Models.Interface import Interface
from Models.Filter import Filter


class ApplicationManager:

    def __init__(self):
        self.__books = list()
        self.__genre_factory = GenreFactory()
        self.__genre_storage = GenreStorage()
        self.__sorting_manager = SortingManager()
        self.__web_scraper = WebScraper(WEBSITE_URL)
        self.__interface = Interface()

    def produce_book(self, data: list):
        self.__books.append(Book(*data))

    def __get_books_from_specific_genre(self, genre):
        result = []
        for book in self.__books:
            if book.genre == genre:
                result.append(book)
        return result

    def produce_genre(self, name):
        self.__genre_factory.add_genre(name, self.__get_books_from_specific_genre(name))

    def store_genres_with_books(self):
        self.__genre_storage.list_all_genres = self.__genre_factory.list_of_genres
        self.__genre_storage.add_list_to_db()

    def __convert_to_books(self, data_list: list):
        for element in data_list:
            # book_name = lst[0]
            # rating = float(lst[1])
            # genre = lst[2]
            # upc = lst[3]
            # price = get_float_from_string(lst[4])
            # availability = extract_int_from_string(lst[5])
            # reviews = lst[6]
            # description = lst[7]
            # needs to be reworked !!!!!!
            # rework Book constructor and feed it the whole list instead my_book = Book(*data_list)
            self.produce_book(element)

    def start_scraper(self):
        # Starts and provides parameters for webscraper
        args = self.__interface.args  # renaming for readability (input_args)
        filter_list = list()  # == no filters provided

        if args.filter is not None:
            for elem in args.filter.split(', '):  # splitting multiple filters into a list
                filter_list.append(Filter(elem))

        if args.title is not None:
            filter_list.append(Filter(f"name = {args.title}"))

            self.__web_scraper.add_filters(filter_list)  # add filters to the webscraper object

        if args.json is not None:  # read from json here, add filter with names of books
            pass

        if args.genre is not None:  # scrape from main page
            self.__convert_to_books(self.__web_scraper.scrape_by_genre(args.books, args.genre))
        else:  # scrape from genres' pages
            self.__convert_to_books(self.__web_scraper.scrape_books(args.books))

        if args.sort is not None:  # sort if provided
            self.run_sort(args.sort)
        else:
            for book in self.__books:
                print(book, '\n')  # printing output in console

    def run_sort(self, criteria: list):
        self.__sorting_manager.book_collection = self.__books
        result = list()
        criteria = [word for segment in criteria.split(', ') for word in segment.split(' ')]
        # sort by given criteria
        if "name" in criteria:
            idx = criteria.index("name")
            print(criteria[idx], criteria[idx + 1])
            result.append(self.__sorting_manager.sort_books_by_title(criteria[idx + 1]))
        if "price" in criteria:
            idx = criteria.index("price")
            result.append(self.__sorting_manager.sort_books_by_price(criteria[idx + 1]))
        if "available" in criteria:
            idx = criteria.index("available")
            result.append(self.__sorting_manager.sort_books_by_availability(criteria[idx + 1]))
        if "rating" in criteria:
            idx = criteria.index("rating")
            result.append(self.__sorting_manager.sort_books_by_rating(criteria[idx + 1]))
        if "upc" in criteria:
            idx = criteria.index("upc")
            result.append(self.__sorting_manager.sort_books_by_upc(criteria[idx + 1]))

        for lst in result:
            for book in lst:
                print(book, '\n')
            print( "--- End of sort ---")

        # for debugging purposes
        # for i in sorted_book_collection:
        #     print(i)
        # print('-------------')
        # print(self.__sorting_manager.search_book_by_book_title('Sapiens: A Brief History of Humankind'))
        # for book in self.__sorting_manager.search_books_by_list_of_titles():
        #     print(str(book))


