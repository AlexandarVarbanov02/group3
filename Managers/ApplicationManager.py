from Factories.BookFactory import BookFactory
from Factories.GenreFactory import GenreFactory
from Storage_classes.GenreStorage import GenreStorage
from Shared.Defines import WEBSITE_URL
from Shared.WebScrapper import WebScraper
from Shared.HelperFunctions import *
from Managers.SortingManager import SortingManager

import argparse


class ApplicationManager:

    def __init__(self):
        self.__book_factory = BookFactory()
        self.__genre_factory = GenreFactory()
        self.__genre_storage = GenreStorage()
        self.__sorting_manager = SortingManager()

    def produce_book(self, name, genre, upc, price,  availability, reviews, description):
        self.__book_factory.add_book(name, genre, upc, price,  availability, reviews, description)

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
            genre = lst[1]
            upc = lst[2]
            price = get_float_from_string(lst[3])

            availability = extract_int_from_string(lst[4])

            reviews = lst[5]
            description = lst[6]

            self.produce_book(book_name, genre, upc, price, availability, reviews, description)

    def scrape_books_from_website(self):
        parser = argparse.ArgumentParser()
        web_scraper = WebScraper(WEBSITE_URL)

        parser.add_argument("-b", type=int, help="Number of books to be scraped")
        parser.add_argument("-g", type=str, help="Genre to be scraped")
        args = parser.parse_args()

        if args.b is not None:
            if args.g is not None:
                print(web_scraper.scrape_books(args.b, web_scraper.scrape_by_genre(args.g)))
            else:
                self.__convert_list_of_book_details_to_object(web_scraper.scrape_books(args.b))
                self.run_sorting_functionality()
                # book_manager.add_books(web_scraper.scrape_books(args.b))
                # for book in book_manager.books:
                #     print(book)
        else:
            print("Number of books arguement is required!")

    def run_sorting_functionality(self):
        type_of_sorting = 'asc'
        self.__sorting_manager.book_collection = self.__book_factory.list_of_produced_books


        sorted_book_collection = self.__sorting_manager.sort_books_by_title(type_of_sorting)
        #sorted_book_collection = self.__sorting_manager.sort_books_by_price(type_of_sorting)
        #sorted_book_collection = self.__sorting_manager.sort_books_by_availability(type_of_sorting)
        #sorted_book_collection = self.__sorting_manager.filter_books_by_availability('==', 20)
        for i in sorted_book_collection:
            print(i)
        print('-------------')
        print(self.__sorting_manager.search_book_by_book_title('Sapiens: A Brief History of Humankind'))
        for book in self.__sorting_manager.search_books_by_list_of_titles():
            print(str(book))


