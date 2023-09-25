from Models.Genre import Genre


class GenreFactory:
    def __init__(self):
        self.__list_of_genres = []

    def __create_genre(self, name, list_of_books):
        return Genre(name, list_of_books)

    def add_genre(self, name, list_of_books):
        self.__list_of_genres.append(self.__create_genre(name, list_of_books))

    @property
    def list_of_genres(self):
        return self.__list_of_genres
