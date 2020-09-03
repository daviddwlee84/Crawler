from news_crawler import NewsCrawler
from bs4 import BeautifulSoup
import datefinder
import re


class TencentNewsCrawler(NewsCrawler):
    def __init__(self, store_in_memory: bool = True, store_in_file: str = '../../../result/news/tencent_news.json'):
        super().__init__(store_in_memory, store_in_file)

    def _get_title(self, html_body_soup: BeautifulSoup) -> str:
        """
        https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class
        """
        return html_body_soup.find('h1').text

    def _get_author(self, html_body_soup: BeautifulSoup):
        """
        TODO: seems this need some NLP method to extract from content or something
        """
        return None

    def _get_date(self, html_body_soup: BeautifulSoup):
        """
        TODO: seems this need some NLP method to extract from content or something

        Information can be found in <head> <meta name="apub:time">
        """
        # time_span = html_body_soup.find('div', {'class': 'a_Info'}).find(
        #     'span', {'class', 'a_time'})
        time_span = html_body_soup.find('span', {'class', 'a_time'})
        if not time_span:
            time_span = html_body_soup.find('span', {'class', 'pubTime'})
        return next(datefinder.find_dates(time_span.text))

    def _get_content(self, html_body_soup: BeautifulSoup) -> str:
        """
        Information can be found in <head> <meta name="description">

        TODO: or we can try to do like this
        https://stackoverflow.com/questions/18725760/beautifulsoup-findall-given-multiple-classes
        """

        def clean_up(text: str) -> str:
            # https://stackoverflow.com/questions/16720541/python-string-replace-regular-expression
            tab = re.compile('#TAB#')
            rchar = re.compile('#R#')
            newline = re.compile('#N#')

            text = tab.sub('\t', text)
            text = rchar.sub('\r', text)
            text = newline.sub('\n', text)

            return text

        article = html_body_soup.find('div', {'class': 'content-article'})
        if not article:
            article = html_body_soup.find(
                'div', {'class': 'Cnt-Main-Article-QQ'})
        if not article:
            article = html_body_soup.find('div', {'class': 'bd'})
        return clean_up(article.text)


if __name__ == "__main__":
    crawler = TencentNewsCrawler()

    # https://new.qq.com/omn/TWF20200/TWF2020081900691700.html

    crawler.crawl_single_url(
        'https://new.qq.com/rain/a/20200819A0DOVH00')  # success!!

    # TODO: write Testcase by evaluate parse result with test_html_body/tencent.json
    with open('test_html_body/tencent.html', 'r') as fp:
        html = fp.read()

    crawler.crawl_html(
        html, url='https://new.qq.com/omn/TEC20200/TEC2020081900692600.html')
    print(crawler.data)
    import ipdb
    ipdb.set_trace()
