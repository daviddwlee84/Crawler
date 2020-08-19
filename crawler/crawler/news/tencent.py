from news_crawler import NewsCrawler
from bs4 import BeautifulSoup
import datefinder


class TencentNewsCrawler(NewsCrawler):
    def __init__(self, store_in_memory: bool = True, store_in_file: str = '../../../result/news/tencent_news.json'):
        super().__init__(store_in_file, store_in_file)

    def _get_title(self, html_body: str):
        """
        https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class
        """
        soup = BeautifulSoup(html_body, 'lxml')
        return soup.find('h1').text

    def _get_author(self, html_body: str):
        """
        TODO: seems this need some NLP method to extract from content or something
        """
        return None

    def _get_date(self, html_body: str):
        """
        TODO: seems this need some NLP method to extract from content or something

        Information can be found in <head> <meta name="apub:time">
        """
        return None

    def _get_content(self, html_body: str):
        """
        Information can be found in <head> <meta name="description">
        """
        soup = BeautifulSoup(html_body, 'lxml')
        article = soup.find('div', {'class': 'content-article'}).text
        return article


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
