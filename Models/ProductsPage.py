from Models.BookPage import BookPage
from Models.Page import Page
from Shared.Defines import DIV_HTML_TAG, ASIDE_HTML_TAG, LINK_HTML_TAG, HREF_HTML, ARTICLE_HTML_TAG, ARTICLE_HTML_CLASS, \
    H3_HTML_TAG, INDEX_URL
import re


class ProductsPage(Page):
    def __init__(self, page_url: str, genre=""):
        super().__init__(page_url)

    def find_genre(self, genre: str):
        genres = self.soup.find(DIV_HTML_TAG, class_='container-fluid page', recursive=True)
        genres = genres.find(ASIDE_HTML_TAG, class_='sidebar col-sm-4 col-md-3', recursive=True)
        genres = genres.find_all(LINK_HTML_TAG, recursive=True)

        for item in genres:
            if item.text.strip() == genre:
                return re.sub(r'/catalogue/.*$', f"/catalogue/" + item.get(HREF_HTML), self.page_url)
        raise ValueError(f"{genre} not found!")

    def scrape_books(self, count: int):
        if not isinstance(count, int):
            raise TypeError("Count can only be an int!")
        if count < 0:
            raise ValueError("Cannot scrape less than 0 books!")

        scraped_books_counter = 0
        books_data = list()

        books_html = self.soup.find_all(ARTICLE_HTML_TAG, class_=ARTICLE_HTML_CLASS, recursive=True)

        for book in books_html:
            if scraped_books_counter == count:
                return books_data

            page_url = book.find(H3_HTML_TAG).find(LINK_HTML_TAG).get(HREF_HTML)
            page_url = page_url.replace("catalogue/", "")
            book_url = self.page_url.replace(INDEX_URL, "/catalogue/")
            book_url = re.sub(r'/catalogue/.*$', f"/catalogue/{page_url}", book_url)
            book_url = book_url.replace("..", "")

            book_page = BookPage(book_url)
            books_data.append(book_page.scrape_book_info())
            scraped_books_counter += 1

        return books_data
