

class Filter:
    def __init__(self, criteria, operator, value):
        self.__criteria = criteria
        self.__operator = operator
        self.__value = float(value)

    def __call__(self, book_info):
        # print(book_info, self.__criteria, self.__value)
        if self.__operator == '<':
            # print(self.__value, book_info[self.__criteria])
            return self.__value > book_info[self.__criteria]
        elif self.__operator == '>':
            return self.__value < book_info[self.__criteria]
        elif self.__operator == '<=':
            return self.__value >= book_info[self.__criteria]
        elif self.__operator == '>=':
            return self.__value <= book_info[self.__criteria]
        else:
            return self.__value == book_info[self.__criteria]

    @property
    def criteria(self):
        return self.__criteria

    @criteria.setter
    def criteria(self, value):
        if not isinstance(value, str):
            raise TypeError("Filter Criteria needs to be a string!")
        if value != "rating" or value != "price":
            raise ValueError("Can only filter by price and rating!")
        self.__criteria = value

    @property
    def operator(self):
        return self.__operator

    @operator.setter
    def operator(self, value):
        if value not in ('<', '>', '<=', '>=', '='):
            raise ValueError("Incorrect operator for criteria!")
        self.__operator = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not isinstance(new_value, int) or not isinstance(new_value, float):
            raise TypeError("Filter value can only be numeric!")
        self.__value = new_value
