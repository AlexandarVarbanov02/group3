from Models.ProductsPage import ProductsPage
from Shared import Defines
import re


class WebScraper:
    def __init__(self, page_url: str):
        self.__home_page_url = page_url
        self.__data = list()
        self.__filters = None

    def add_filters(self, filters):
        self.__filters = filters

    def scrape_books(self, count: int, link=""):
        if not isinstance(count, int):
            raise TypeError("Count can only be an int!")
        if count < 0:
            raise ValueError("Cannot scrape less than 0 books!")

        if link == "":
            link = self.__home_page_url.replace("catalogue", str(Defines.INDEX_URL))

        product_page = ProductsPage(link, self.__filters)
        self.__data.extend(product_page.scrape_books(count))

        page_number = 1
        link = link.replace("index.html", "catalogue")

        while count > len(self.__data):
            url = self.get_next_page(page_number)
            product_page = ProductsPage(link + url, self.__filters)
            self.__data.extend(product_page.scrape_books(count - len(self.__data)))
            page_number += 1

        return self.__data

    def scrape_by_genre(self, genre: str):
        if not isinstance(genre, str):
            raise TypeError("Genre can only be a string!")
        if genre == "":
            raise ValueError("Genre cannot be empty!")
        product_page = ProductsPage(self.__home_page_url + self.get_next_page(0), self.__filters)
        return product_page.find_genre(genre)

    @staticmethod
    def get_next_page(number: int):
        pattern = r"/page-(\d+)\.html"
        page_url = Defines.NEXT_PAGE_URL
        page_number = fr"/page-{1 + number}.html"
        return re.sub(pattern, page_number, page_url)
