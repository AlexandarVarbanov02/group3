from Models.BookPage import BookPage
from Models.Page import Page
from Shared import Defines
from word2number import w2n
from Models.Filter import Filter
import re


class ProductsPage(Page):
    def __init__(self, page_url: str, filters=None):
        super().__init__(page_url, filters)
        self.books_data = list()
        self.__names = list()
        self.scraped_books_counter = 0
        self.results = self.__get_results()
        print(self.page_url)

    # Finds book's href and coverts it to a usable url
    def find_url(self, book):
        page_url = book.find("h3").find("a").get("href")
        page_url = page_url.replace("catalogue/", "")
        book_url = self.page_url.replace(Defines.INDEX_URL, "/catalogue/")
        book_url = re.sub(r'/catalogue/.*$', f"/catalogue/{page_url}", book_url)
        book_url = book_url.replace("..", "")
        return book_url

    def add_names(self, names):
        self.__names = names

    def last_page(self):
        current_page = self.soup.find('li', class_='current').text
        if current_page == "":
            return True
        current_page = current_page.split()
        if int(current_page[1]) == int(current_page[3]):
            return True
        return False

    def __get_results(self):
        result = self.soup.find('div', class_='container-fluid page', recursive=True)
        result = result.find('div', class_='row', recursive=True)
        result = result.find('div', class_='col-sm-8 col-md-9').find('form', class_='form-horizontal', recursive=True)
        return int(result.find_next('strong').text)

    @staticmethod
    def get_basic_info(book_html):
        book_info = dict()

        title = book_html.find('h3', recursive=False).find('a')['title']
        book_info['name'] = title
        print(title)

        rating = book_html.find('p', recursive=False).get('class')[1]
        rating = w2n.word_to_num(rating)  # switch to dict instead of w2n
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

        books_html = self.soup.find_all("article", class_="product_pod", recursive=True)

        for book in books_html:
            if self.scraped_books_counter >= count or self.scraped_books_counter >= self.results:
                return self.books_data
            print(self.scraped_books_counter, count)
            if self.filter_book(book):
                book_page = BookPage(self.find_url(book), self.filters)
                # if return is not None
                data = book_page.scrape_book_info()
                if data is not None:
                    self.books_data.append(data)
                    self.scraped_books_counter += 1

        return self.books_data

    def filter_book(self, book_html):
        book_info = ProductsPage.get_basic_info(book_html)
        if self.filters is None and self.__names is None:
            return True
        if book_info['name'] in self.__names:
            # print(book_info['name'], self.__names[-1])
            for filter_elem in self.filters:
                if filter_elem.criteria == "available":
                    continue
                if not (filter_elem(book_info)):  # if the book doesn't meet all filter conditions return False
                    self.scraped_books_counter += 1
                    return False
            return True
        return False

