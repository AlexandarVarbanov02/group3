import json


class FileOpenError(Exception):
    def __init__(self, filename, reason):
        self.filename = filename
        self.reason = reason
        super().__init__(f"Error opening file '{filename}': {reason}")


class FileReader:
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

    def read_file(self):
        json_file = open(self.filename, 'r')
        json_input = json_file.read()
        data = json.loads(json_input)
        json_file.close()
        return data



