import re


def extract_int_from_string(string):
    result = ""
    for i in string:
        if i.isdigit():
            result += i
    return int(result)


def get_float_from_string(string):
    result = string[1:]
    return float(result)
