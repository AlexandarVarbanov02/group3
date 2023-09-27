from Shared import Defines
from Models.Page import Page
from word2number import w2n
import re


class BookPage(Page):

    def __init__(self, page_url: str):
        super().__init__(page_url)
        self.__page_content = self.get_content()

    def scrape_name(self):
        divs_sm6 = self.__page_content.find_all("div", class_="col-sm-6 product_main",
                                                recursive=True)
        book_name = [div.find("h1").text for div in divs_sm6 if div.find("h1")]
        return book_name

    def scrape_genre(self):
        breadcrumb = self.soup.find("ul", class_="breadcrumb", recursive=True)
        hrefs = [href for href in breadcrumb.find_all("a", recursive=True)]
        return hrefs[-1].text

    def scrape_rating(self):
        rating = (self.__page_content.find("div", class_="col-sm-6 product_main", recursive=True).
                  find_all("p", recursive=False))
        return w2n.word_to_num(rating[2].get('class')[1])

    def scrape_description(self):
        paragraph = self.__page_content.find("p", class_='', recursive=True).text
        return paragraph

    def scrape_table(self):
        table_info = list()
        table_html = self.__page_content.find("table", class_="table table-striped",
                                              recursive=False)
        counter = 0
        for td in table_html:
            if td.find("td"):
                if counter in (1, 7, 11, 13):
                    table_info.extend(re.findall(r'<td>(.*?)</td>', str(td)))
                counter += 1
        return table_info

    def scrape_book_info(self):
        result = list()
        result.extend(self.scrape_name())
        result.append(self.scrape_rating())
        result.append(self.scrape_genre())
        result.extend(self.scrape_table())
        result.append(self.scrape_description())

        return result

    def get_content(self):
        content = self.soup.find("div", class_="container-fluid page", recursive=True)
        content = content.find("div", class_="page_inner", recursive=False)
        content = content.find("div", class_="content", recursive=False)
        content = content.find("div", id="content_inner", recursive=False)
        content = content.find("article", class_="product_page", recursive=False)
        return content
