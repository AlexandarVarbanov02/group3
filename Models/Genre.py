class Genre:
    def __init__(self, name, list_of_books):
        self._name = name
        self._list_of_books = list_of_books

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if new_name == "":
            raise ValueError("The genre cannot be empty")

    @property
    def list_of_books(self):
        return self._list_of_books

    @list_of_books.setter
    def list_of_books(self, new_list_of_books):
        self._list_of_books = new_list_of_books

    def __str__(self):
        string_with_books = ""
        for i in self._list_of_books:
            string_with_books += str(i)
        return "Genre info: \n" + self._name + "\n" + string_with_books
