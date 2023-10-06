import argparse
import re
from Shared.FileReader import FileReader

FILTER_TYPES = ("available", "rating", "price")
OPERATOR_TYPES = ('<', '<=', '>', '>=', '=')


class Interface:
    def __init__(self):
        self.__parser = argparse.ArgumentParser()
        self.__add_arguments()
        self.__validate_input()

    def __add_arguments(self):
        self.__parser.add_argument("-b", dest="books", type=int, help="Number of books to be scraped")
        self.__parser.add_argument("-g", dest="genre", type=str, help="Genres to be scraped")
        self.__parser.add_argument("-f", dest="filter", type=str, help="Filter books by criteria")
        self.__parser.add_argument("-s", dest="sort", type=str, help="Sort book result")
        self.__parser.add_argument("-d", dest="description", type=str, help="Keywords in description")
        self.__parser.add_argument("-t", dest="title", type=str, help="Search book by title")
        self.__parser.add_argument("-w", dest="json", type=str, help="Search titles from json")
        self.__args = self.__parser.parse_args()

    @staticmethod
    def __validate_filter_format(keywords):
        for i in range(len(keywords) // 3):  # if len % 3 != 0
            if keywords[3 * i + 1] not in OPERATOR_TYPES:
                raise ValueError("Second argument of filter needs to be an operator!")

            try:
                number = float(keywords[3 * i + 2])
            except ValueError:
                raise ValueError("Third argument of filter needs to be a number!")

            if keywords[3 * i] not in FILTER_TYPES:
                raise ValueError("Filter criteria is invalid!")

    @staticmethod
    def __check_filter_contradiction(keywords):
        for filter_type in FILTER_TYPES:  # idx[] + 0 = criteria    -f "rating < 3"
            if keywords.count(filter_type) == 2:
                idx = [i for i, value in enumerate(keywords) if value == filter_type]
                if keywords[idx[0] + 1] in FILTER_TYPES[0:2] and keywords[idx[1] + 1] in FILTER_TYPES[2:4]:
                    if not float(keywords[idx[0] + 2]) > float(keywords[idx[1] + 2]):
                        raise ValueError("Filter contradiction!")
                elif keywords[idx[1] + 1] in FILTER_TYPES[0:2] and keywords[idx[0] + 1] in FILTER_TYPES[2:4]:
                    if not float(keywords[idx[1] + 2]) > float(keywords[idx[0] + 2]):
                        raise ValueError("Filter contradiction!")
                # > 2
            elif keywords.count(filter_type) >= 3:  # 3 is magic number constant needed
                raise ValueError("Cannot have three filters with the same criteria!")

    def __validate_filter(self):
        filters = self.__args.filter.split(', ')
        keywords = list()
        for f in filters:
            keywords.extend(f.split(' '))
        self.__validate_filter_format(keywords)
        self.__check_filter_contradiction(keywords)

    def __validate_sort(self):
        sort_criteria = ("name", "rating", "price", "available", "upc")
        sort_args = [word for segment in self.__args.sort.split(', ') for word in segment.split(' ')]
        # splitting sort arg to keywords
        if len(sort_args) % 2 == 1:
            raise ValueError("Invalid amount of arguments!")
        for i in range(0, len(sort_args), 2):
            if sort_args[i] not in sort_criteria:
                raise ValueError("Sorting criteria is invalid!")
            if sort_args[i + 1] not in ("ascending", "descending"):
                raise ValueError("Invalid sort input! Expected input: 'criteria' 'ascending/descending'")

    def __validate_input(self):
        result = list()
        if (self.__args.books, self.__args.title, self.__args.json).count(None) != 2:
            raise TypeError("Invalid input! Must have only one of: -b, -t, -w")
        if self.__args.books is not None:
            if self.__args.filter is not None:
                self.__validate_filter()
            if self.__args.sort is not None:
                self.__validate_sort()
        elif self.__args.title is not None:
            self.__args.books = 1
            self.__validate_filter()
        elif self.__args.json is not None:
            json_file = FileReader(self.__args.json).check_file()
            if self.__args.filter is not None:
                self.__validate_filter()
            if self.__args.sort is not None:
                self.__validate_sort()

            # validate file path, in AppM. read file, make args.books = amount of titles we search for!!!
            # self.__args.books is not None:
            # raise ValueError("Number of results needed!") remove this line later
            # search for description keywords needs to be implemented
    @property
    def args(self):
        return self.__args

