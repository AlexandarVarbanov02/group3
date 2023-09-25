from Shared.File_Checker import FileChecker


class GenreStorage:

    def __init__(self):
        self.__list_of_genres = []
        self.__db_filename = "venv/Db_Files/Genres.txt"

    @property
    def list_all_genres(self):
        return self.__list_of_genres

    @list_all_genres.setter
    def list_all_genres(self, new_list):
        self.__list_of_genres = new_list

    def add_list_to_db(self):
        ch_file = FileChecker(self.__db_filename)
        ch_file.check_file()
        db_file = open(self.__db_filename, "w")
        for i in self.__list_of_genres:
            db_file.writelines(str(i))
        db_file.close()
