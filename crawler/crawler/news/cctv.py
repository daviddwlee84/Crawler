from news_crawler import NewsCrawler
from bs4 import BeautifulSoup
import datefinder
from urllib.parse import urlparse
import re


def clean_up(text: str) -> str:
    tab = re.compile('#TAB#')
    rchar = re.compile('#R#')
    newline = re.compile('#N#')

    text = tab.sub('\t', text)
    text = rchar.sub('\r', text)
    text = newline.sub('\n', text)

    return text


class CCTVNewsCrawler(NewsCrawler):
    def __init__(self, store_in_memory: bool = True, store_in_file: str = '../../../result/news/cctv_news.json', domain_prefix: str = 'news'):
        """
        news.cctv.com
        m.news.cctv.com
        tv.cctv.com (don't consider)
        """
        super().__init__(store_in_memory, store_in_file)
        self.domain_prefix = domain_prefix

    def _get_raw_html(self, url: str) -> str:
        # return super()._get_raw_html(url, specific_encoding='ISO-8859-1')
        return super()._get_raw_html(url, force_encode=True)

    def _get_title(self, html_body_soup: BeautifulSoup):
        """
        Seems there might have some dirty content here
        """
        if self.domain_prefix == 'news':
            title_area = html_body_soup.find('div', {'class': 'title_area'})
            title = title_area.find('h1').text
        elif self.domain_prefix == 'm.news':
            title = html_body_soup.find('h1').text

        return clean_up(title).strip()

    def _get_author(self, html_body_soup: BeautifulSoup):
        """
        TODO: need some NLP method to refine or extract
        """
        if self.domain_prefix == 'news':
            author_info = html_body_soup.find('div', {'class': 'zebian'})
            author = author_info.text
        elif self.domain_prefix == 'm.news':
            function_info = html_body_soup.find('div', {'class': 'function'}).find(
                'span', {'class', 'info'})
            author = function_info.find('a').text

        return clean_up(author).strip()

    def _get_date(self, html_body_soup: BeautifulSoup):
        if self.domain_prefix == 'news':
            title_area = html_body_soup.find('div', {'class': 'title_area'})
            text_contain_date = title_area.find('div', {'class', 'info1'}).text
        elif self.domain_prefix == 'm.news':
            function_info = html_body_soup.find('div', {'class': 'function'}).find(
                'span', {'class', 'info'})
            text_contain_date = function_info.text

        article_info = html_body_soup.find('div', {'class': 'article-info'})
        return next(datefinder.find_dates(text_contain_date))

    def _get_content(self, html_body_soup: BeautifulSoup):
        if self.domain_prefix == 'news':
            content_area = html_body_soup.find(
                'div', {'class': 'content_area'})
            article = content_area.text
        elif self.domain_prefix == 'm.news':
            content_area = html_body_soup.find('div', {'class': 'cnt_bd'})
            paragraphs = content_area.find_all('p')
            article = '\n\n'.join((paragraph.text for paragraph in paragraphs))

        return clean_up(article)


if __name__ == "__main__":
    crawler = CCTVNewsCrawler()
    crawler.domain_prefix = 'news'
    crawler.crawl_single_url(
        'https://news.cctv.com/2020/08/19/ARTIJapDsvNdGtH0AF4k8yGf200819.shtml')  # success!!!
    crawler.domain_prefix = 'm.news'
    crawler.crawl_single_url(
        'http://m.news.cctv.com/2020/08/19/ARTIzpQnphaF1ZC0DFzMNxvd200819.shtml')  # success!!!

    domains_files = {
        'news': 'https://news.cctv.com/2020/08/19/ARTIJapDsvNdGtH0AF4k8yGf200819.shtml',
        'm.news': 'http://m.news.cctv.com/2020/08/19/ARTIzpQnphaF1ZC0DFzMNxvd200819.shtml'
    }

    # TODO: write Testcase by evaluate parse result with test_html_body/cctv.json
    for domain, url in domains_files.items():
        with open(f'test_html_body/cctv_{domain}.html', 'r') as fp:
            html = fp.read()

        _parsed_uri = urlparse(url)
        domain = '{uri.netloc}'.format(uri=_parsed_uri)
        domain = domain.replace('.cctv.com', '')
        crawler.domain_prefix = domain

        crawler.crawl_html(
            html, url=url)

    print(crawler.data)
    import ipdb
    ipdb.set_trace()
