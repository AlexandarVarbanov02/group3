class FileOpenError(Exception):
    def __init__(self, filename, reason):
        self.filename = filename
        self.reason = reason
        super().__init__(f"Error opening file '{filename}': {reason}")


class FileChecker:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        try:
            with open(self.filename, 'r') as file:

                return True


        except FileNotFoundError:
            raise FileOpenError(self.filename, "File not found")

        except IOError as e:
            raise FileOpenError(self.filename, str(e))


