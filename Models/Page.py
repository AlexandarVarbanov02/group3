from bs4 import BeautifulSoup
import requests
from abc import ABC


class Page(ABC):
    def __init__(self, page_url: str):
        self.__page_url = page_url
        self.__html = requests.get(self.__page_url).content.decode('utf-8')
        self.__soup = BeautifulSoup(self.__html, "html.parser")
        # add self.__filters = None

    @property
    def page_url(self):
        return self.__page_url

    @page_url.setter
    def page_url(self, new_value: str):
        if not isinstance(new_value, str):
            raise TypeError("URL is a string")
        if new_value == "":
            raise ValueError("URL cannot be empty")
        self.__page_url = new_value

    @property
    def soup(self):
        return self.__soup

    @soup.setter
    def soup(self, new_value):
        if not isinstance(new_value, BeautifulSoup):
            raise TypeError("Soup is incorrect")
        self.__soup = new_value
