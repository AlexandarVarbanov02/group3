from Factories.BookFactory import BookFactory
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
        self.__book_factory = BookFactory()
        self.__genre_factory = GenreFactory()
        self.__genre_storage = GenreStorage()
        self.__sorting_manager = SortingManager()
        self.__web_scraper = WebScraper(WEBSITE_URL)
        self.__interface = Interface()

    def produce_book(self, name, rating, genre, upc, price,  availability, reviews, description):
        self.__book_factory.add_book(name, rating, genre, upc, price,  availability, reviews, description)

    def __get_books_from_specific_genre(self, genre):
        result = []
        for i in self.__book_factory.list_of_produced_books:
            if i.genre == genre:
                result.append(i)
        return result

    def produce_genre(self, name):
        self.__genre_factory.add_genre(name, self.__get_books_from_specific_genre(name))

    def store_genres_with_books(self):
        self.__genre_storage.list_all_genres = self.__genre_factory.list_of_genres
        self.__genre_storage.add_list_to_db()

    def __convert_list_of_book_details_to_object(self, collection_of_lists_containing_book_details):
        for lst in collection_of_lists_containing_book_details:
            book_name = lst[0]
            rating = float(lst[1])
            genre = lst[2]
            upc = lst[3]
            price = get_float_from_string(lst[4])
            availability = extract_int_from_string(lst[5])
            reviews = lst[6]
            description = lst[7]
            # needs to be reworked !!!!!!
            # rework Book constructor and feed it the whole list instead my_book = Book(*data_list)
            self.produce_book(book_name, rating, genre, upc, price, availability, reviews, description)

    def scrape_books_from_website(self):
        args = self.__interface.args
        if args.filter is not None:
            filter_list = list()
            for elem in args.filter.split(', '):
                f_args = elem.split(' ')
                filter_list.append(Filter(f_args[0], f_args[1], f_args[2]))
            self.__web_scraper.add_filters(filter_list)
        if args.genre is not None:
            self.__convert_list_of_book_details_to_object(self.__web_scraper.scrape_books(args.books,
                                                            self.__web_scraper.scrape_by_genre(args.genre)))
        else:
            self.__convert_list_of_book_details_to_object(self.__web_scraper.scrape_books(args.books))
        if args.sort is not None:
            self.run_sorting_functionality(*args.sort)

    def run_sorting_functionality(self, criteria, sort_type):
        self.__sorting_manager.book_collection = self.__book_factory.list_of_produced_books

        if criteria == "name":
            sorted_book_collection = self.__sorting_manager.sort_books_by_title(sort_type)
        elif criteria == "price":
            sorted_book_collection = self.__sorting_manager.sort_books_by_price(sort_type)
        elif criteria == "available":
            sorted_book_collection = self.__sorting_manager.sort_books_by_availability(sort_type)
        elif criteria == "rating":
            sorted_book_collection = self.__sorting_manager.sort_books_by_rating(sort_type)
        else:
            sorted_book_collection = self.__sorting_manager.sort_books_by_upc(sort_type)

        # for debugging purposes
        for i in sorted_book_collection:
            print(i)
        print('-------------')
        print(self.__sorting_manager.search_book_by_book_title('Sapiens: A Brief History of Humankind'))
        for book in self.__sorting_manager.search_books_by_list_of_titles():
            print(str(book))


