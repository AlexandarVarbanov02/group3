from Models.Book import Book
from Shared.Defines import WEBSITE_URL
from Shared.WebScrapper import WebScraper
from Shared.HelperFunctions import *
from Managers.SortingManager import SortingManager
from Models.Interface import Interface
from Models.Filter import Filter
from Shared.FileReader import FileReader

import gspread
import json


class ApplicationManager:

    def __init__(self):
        self.__books = list()
        self.__sorting_manager = SortingManager()
        self.__web_scraper = WebScraper(WEBSITE_URL)
        self.__interface = Interface()
        self.__service_account = gspread.service_account(filename="service_account.json")
        self.__sh = self.__service_account.open("ScrapeBooks")
        self.__worksheet = self.__sh.worksheet("ScrappeSheet")
        self.__headers = ["title", "rating", "genre", "upc", "price", "availability", "reviews", "description"]
        self.__list_for_google_sheets = [self.__headers]
        self.__output_json_file = "Db_Files/Output.json"

    def produce_book(self, data: list):
        self.__books.append(Book(*data))

    def __get_books_from_specific_genre(self, genre):
        result = []
        for book in self.__books:
            if book.genre == genre:
                result.append(book)
        return result

    def __convert_to_books(self, data_list: list):
        for element in data_list:
            self.produce_book(element)

    def __add_to_google_sheet(self, values):
        self.__worksheet.insert_rows(values)

    def start_scraper(self):
        # Starts and provides parameters for webscraper
        args = self.__interface.args  # renaming for readability (input_args)
        filter_list = list()  # == no filters provided
        name_list = list()  # list of titles we search for

        if args.filter is not None:
            for elem in args.filter.split(', '):  # splitting multiple filters into a list
                filter_list.append(Filter(elem))

        if args.title is not None:
            name_list.append(Filter(f"name = {args.title}"))

        if args.json is not None:  # read from json here, add filter with names of books
            json_file = FileReader(args.json)
            json_data = json_file.read_file()
            books_counter = 0
            for data in json_data:
                name_list.append(data)
                books_counter += 1
            args.books = books_counter

        self.__web_scraper.add_names(name_list)
        self.__web_scraper.add_filters(filter_list) # add filters to the webscraper object

        if args.genre is not None:  # scrape from main page
            self.__convert_to_books(self.__web_scraper.scrape_by_genre(args.books, args.genre))
        else:  # scrape from genres' pages
            self.__convert_to_books(self.__web_scraper.scrape_books(args.books))

        if args.sort is not None:  # sort if provided
            self.run_sort(args.sort)
        else:

            for book in self.__books:
                print(book, '\n') # printing output in console
                self.__list_for_google_sheets.append(book.to_list())
            self.__worksheet.clear()
            self.__add_to_google_sheet(self.__list_for_google_sheets)
            file_checker = FileReader(self.__output_json_file)
            file_checker.check_file()

            with open(self.__output_json_file, 'w') as json_file:
                json.dump(self.__list_for_google_sheets, json_file)

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

        if len(result) == 0:
            print("No results were found!")
        for lst in result:
            for book in lst:
                print(book, '\n')
                self.__list_for_google_sheets.append(book.to_list())
            self.__worksheet.clear()
            self.__add_to_google_sheet(self.__list_for_google_sheets)
            file_checker = FileReader(self.__output_json_file)
            file_checker.check_file()

            with open(self.__output_json_file, 'w') as json_file:
                json.dump(self.__list_for_google_sheets, json_file)

            print( "--- End of sort ---")

        # for debugging purposes
        # for i in sorted_book_collection:
        #     print(i)
        # print('-------------')
        # print(self.__sorting_manager.search_book_by_book_title('Sapiens: A Brief History of Humankind'))
        # for book in self.__sorting_manager.search_books_by_list_of_titles():
        #     print(str(book))


