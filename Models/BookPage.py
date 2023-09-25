from Shared.Defines import DIV_HTML_TAG, DIV_HTML_BOOK_CLASS, H1_HTML_TAG, LINK_HTML_TAG, PARAGRAPH_HTML_TAG, \
    TABLE_HTML_TAG, TABLE_HTML_BOOK_INFO_CLASS, DATA_CELL_HTML_TAG, ARTICLE_HTML_TAG, UNORDERED_LIST_HTML_TAG
from Models.Page import Page
import re


class BookPage(Page):

    def __init__(self, page_url: str):
        super().__init__(page_url)
        self.__page_content = self.get_content()

    def scrape_name(self):
        divs_sm6 = self.__page_content.find_all(DIV_HTML_TAG, class_=DIV_HTML_BOOK_CLASS,
                                                recursive=True)
        book_name = [div.find(H1_HTML_TAG).text for div in divs_sm6 if div.find(H1_HTML_TAG)]
        return book_name

    def scrape_genre(self):
        breadcrumb = self.soup.find(UNORDERED_LIST_HTML_TAG, class_="breadcrumb", recursive=True)
        hrefs = [href for href in breadcrumb.find_all(LINK_HTML_TAG, recursive=True)]
        return hrefs[-1].text

    def scrape_description(self):
        paragraph = self.__page_content.find(PARAGRAPH_HTML_TAG, class_='', recursive=True).text
        return paragraph

    def scrape_table(self):
        table_info = list()
        table_html = self.__page_content.find(TABLE_HTML_TAG, class_=TABLE_HTML_BOOK_INFO_CLASS,
                                              recursive=False)
        counter = 0
        for td in table_html:
            if td.find(DATA_CELL_HTML_TAG):
                if counter in (1, 7, 11, 13):
                    table_info.extend(re.findall(r'<td>(.*?)</td>', str(td)))
                counter += 1
        return table_info

    def scrape_book_info(self):
        result = list()
        result.extend(self.scrape_name())
        result.append(self.scrape_genre())
        result.extend(self.scrape_table())
        result.append(self.scrape_description())

        return result

    def get_content(self):
        content = self.soup.find(DIV_HTML_TAG, class_="container-fluid page", recursive=True)
        content = content.find(DIV_HTML_TAG, class_="page_inner", recursive=False)
        content = content.find(DIV_HTML_TAG, class_="content", recursive=False)
        content = content.find(DIV_HTML_TAG, id="content_inner", recursive=False)
        content = content.find(ARTICLE_HTML_TAG, class_="product_page", recursive=False)
        return content
