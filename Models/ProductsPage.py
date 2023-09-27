from Models.BookPage import BookPage
from Models.Page import Page
from Shared import Defines
from word2number import w2n
from Models.Filter import Filter
import re


class ProductsPage(Page):
    def __init__(self, page_url: str, filters=None):
        super().__init__(page_url)
        self.filters = filters

    # Finds book's href and coverts it to a usable url
    def find_url(self, book):
        page_url = book.find("h3").find("a").get("href")
        page_url = page_url.replace("catalogue/", "")
        book_url = self.page_url.replace(Defines.INDEX_URL, "/catalogue/")
        book_url = re.sub(r'/catalogue/.*$', f"/catalogue/{page_url}", book_url)
        book_url = book_url.replace("..", "")
        return book_url


    @staticmethod
    def get_basic_info(book_html):
        book_info = dict()

        # print(book_html.find('p', recursive=False).get('class'))
        rating = book_html.find('p', recursive=False).get('class')[1]
        rating = w2n.word_to_num(rating)
        book_info['rating'] = rating

        price = book_html.find('p', class_='price_color').text
        book_info['price'] = float(price[1:])

        return book_info

    def find_genre(self, genre: str):
        genres = self.soup.find("div", class_='container-fluid page', recursive=True)
        genres = genres.find("aside", class_='sidebar col-sm-4 col-md-3', recursive=True)
        genres = genres.find_all("a", recursive=True)

        for item in genres:
            if item.text.strip() == genre:
                return re.sub(r'/catalogue/.*$', f"/catalogue/" + item.get("href"), self.page_url)
        raise ValueError(f"{genre} not found!")

    def scrape_books(self, count: int):
        if not isinstance(count, int):
            raise TypeError("Count can only be an int!")
        if count < 0:
            raise ValueError("Cannot scrape less than 0 books!")

        scraped_books_counter = 0
        books_data = list()
        books_html = self.soup.find_all("article", class_="product_pod", recursive=True)

        for book in books_html:
            if scraped_books_counter == count:
                return books_data

            if self.filter_book(book):
                print(len(books_data))
                book_page = BookPage(self.find_url(book))
                books_data.append(book_page.scrape_book_info())
                scraped_books_counter += 1

        return books_data

    def filter_book(self, book_html):
        book_info = ProductsPage.get_basic_info(book_html)
        if self.filters is None:
            return True
        for filter_elem in self.filters:
            if not (filter_elem(book_info)):
                # print("False filter")
                return False
            # print("Filter cycle")
        return True

