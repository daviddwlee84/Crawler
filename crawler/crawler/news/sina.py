from news_crawler import NewsCrawler
from bs4 import BeautifulSoup
import datefinder
from urllib.parse import urlparse
import re


class SinaNewsCrawler(NewsCrawler):
    def __init__(self, store_in_memory: bool = True, store_in_file: str = '../../../result/news/sina_news.json'):
        super().__init__(store_in_memory, store_in_file)

    def _get_title(self, html_body_soup: BeautifulSoup):
        return html_body_soup.find('h1', {'class': 'main-title'}).text

    def _get_author(self, html_body_soup: BeautifulSoup):
        date_source = html_body_soup.find('div', {'class': 'date-source'})
        return date_source.find('a').text

    def _get_date(self, html_body_soup: BeautifulSoup):
        date_source = html_body_soup.find('div', {'class': 'date-source'})
        if not date_source:
            date_source = html_body_soup.find('span', {'class': 'date'})
        return next(datefinder.find_dates(date_source.text))

    def _get_content(self, html_body_soup: BeautifulSoup):

        def clean_up(text: str) -> str:
            tab = re.compile('#TAB#')
            rchar = re.compile('#R#')
            newline = re.compile('#N#')

            text = tab.sub('\t', text)
            text = rchar.sub('\r', text)
            text = newline.sub('\n', text)

            return text

        article = html_body_soup.find('div', {'id': 'article_content'})
        if not article:
            article = html_body_soup.find('div', {'id': 'article'})
        return clean_up(article.text.strip())


if __name__ == "__main__":
    crawler = SinaNewsCrawler()
    crawler.crawl_single_url(
        'https://news.sina.com.cn/w/2020-08-19/doc-iivhuipn9517117.shtml')  # success!!!

    # TODO: write Testcase by evaluate parse result with test_html_body/cctv.json
    with open(f'test_html_body/sina.html', 'r') as fp:
        html = fp.read()

    crawler.crawl_html(
        html, url='https://news.sina.com.cn/s/2020-08-19/doc-iivhuipn9534743.shtml')

    print(crawler.data)
    import ipdb
    ipdb.set_trace()
