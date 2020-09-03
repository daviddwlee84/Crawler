from news_crawler import NewsCrawler
from bs4 import BeautifulSoup
import datefinder


class TouTiaoNewsCrawler(NewsCrawler):
    def __init__(self, store_in_memory: bool = True, store_in_file: str = '../../../result/news/toutiao_news.json'):
        # https://stackoverflow.com/questions/576169/understanding-python-super-with-init-methods
        super().__init__(store_in_memory, store_in_file)

    def _get_raw_html(self, url: str, force_encode: bool = True, specific_encoding: str = '') -> str:
        """
        Deal with some anti-crawler mechanism
        """
        raise NotImplementedError()

    def _get_title(self, html_body_soup: BeautifulSoup):
        """
        https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class
        """
        return html_body_soup.select_one('.article-title').text

    def _get_author(self, html_body_soup: BeautifulSoup):
        article_sub = html_body_soup.find(
            'div', attrs={'class': 'article-sub'})
        # https://stackoverflow.com/questions/32063985/deleting-a-div-with-a-particlular-class-using-beautifulsoup
        # for span in article_sub.find_all('span', _class='original'):
        #     span.decompose()
        # return article_sub.find('span').text

        return article_sub.find_all('span')[1].text

    def _get_date(self, html_body_soup: BeautifulSoup):
        """
        https://github.com/akoumjian/datefinder
        """
        article_sub = html_body_soup.find(
            'div', attrs={'class': 'article-sub'})
        return next(datefinder.find_dates(article_sub.text))

    def _get_content(self, html_body_soup: BeautifulSoup):
        article = html_body_soup.find('article').text
        return article


if __name__ == "__main__":
    crawler = TouTiaoNewsCrawler()
    # TODO: deal with anti-crawler stuff
    # print(crawler.crawl_single_url('https://www.toutiao.com/a6862484901053071875/'))

    # TODO: write Testcase by evaluate parse result with test_html_body/toutiao.json
    with open('test_html_body/toutiao.html', 'r') as fp:
        html = fp.read()

    print(crawler.crawl_html(
        html, url='https://www.toutiao.com/a6862484901053071875/'))
    print(crawler.data)
    import ipdb
    ipdb.set_trace()
