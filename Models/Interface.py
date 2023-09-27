import argparse


class Interface:
    def __init__(self):
        self.__parser = argparse.ArgumentParser()
        self.__args = self.__add_arguments()
        self.__validate_input()

    def __add_arguments(self):
        self.__parser.add_argument("-b", dest="books", type=int, help="Number of books to be scraped")
        self.__parser.add_argument("-g", dest="genre", type=str, help="Genre to be scraped")
        self.__parser.add_argument("-f", dest="filter", type=str, help="Filter books by criteria")
        self.__parser.add_argument("-s", dest="sort", type=str, help="Sort book result")
        return self.__parser.parse_args()

    def __validate_filter(self):
        filter_types = ("available", "rating", "price")
        operator_types = ('<', '>', '<=', '>=', '=')
        filters = self.__args.filter.split(', ')
        keywords = list()
        if len(filters) > 3:
            raise ValueError("Too many filters! (max 3)")
        for f in filters:
            keywords.extend(f.split(' '))

        for filter_type in filter_types:
            if keywords.count(filter_type) > 1:
                raise ValueError("Cannot have two filters with the same criteria!")

        for i in range(len(keywords) // 3):
            if keywords[3 * i + 1] not in operator_types:
                raise ValueError("Second argument of filter needs to be an operator!")

            try:
                number = float(keywords[3 * i + 2])
            except ValueError:
                raise ValueError("Third argument of filter needs to be a number!")

            if keywords[3 * i] not in filter_types:
                raise ValueError("Filter criteria is invalid!")

    def __validate_sort(self):
        sort_criteria = ("name", "rating", "price", "available", "upc")
        sort_args = list(self.__args.sort.split(' '))
        if len(sort_args) == 1:
            sort_args.append("ascending")
        elif len(sort_args) != 2:
            raise ValueError("Too many sorting arguments!")
        if sort_args[0] not in sort_criteria:
            raise ValueError("Sorting criteria is invalid!")
        self.__args.sort = sort_args

    def __validate_input(self):
        result = list()
        if self.__args.books is not None:
            # if self.__args.genre is not None:
            #   self.__validate_genre() needs to be implemented
            if self.__args.filter is not None:
                self.__validate_filter()
            if self.__args.sort is not None:
                self.__validate_sort()
        else:
            raise ValueError("Number of results needed!")

    @property
    def args(self):
        return self.__args

