from news_crawler import NewsCrawler
from bs4 import BeautifulSoup
import datefinder


class NetEaseNewsCrawler(NewsCrawler):
    def __init__(self, store_in_memory: bool = True, store_in_file: str = '../../../result/news/neteast_news.json'):
        super().__init__(store_in_file, store_in_file)

    def _get_title(self, html_body: str):
        soup = BeautifulSoup(html_body, 'lxml')
        return soup.find('h1').text

    def _get_author(self, html_body: str):
        """
        TODO: Still need to refine this

        Information can be found in <head> <meta name="author">
        Information can be found in <head> <meta property="article:author">
        """
        soup = BeautifulSoup(html_body, 'lxml')
        return soup.select_one('.ep-editor').text

    def _get_date(self, html_body: str):
        """
        TODO: seems this need some NLP method to extract from content or something

        Information can be found in <head> <meta name="article:published_time">
        """
        soup = BeautifulSoup(html_body, 'lxml')
        post_time_source = soup.find('div', {'class': 'post_time_source'})
        return list(datefinder.find_dates(post_time_source.text))[0]

    def _get_content(self, html_body: str):
        soup = BeautifulSoup(html_body, 'lxml')
        article = soup.find('div', {'class': 'post_body'}).text
        return article


if __name__ == "__main__":
    crawler = NetEaseNewsCrawler()
    crawler.crawl_single_url(
        'https://money.163.com/20/0819/13/FKD7UNN100258105.html')  # success!!!

    # TODO: write Testcase by evaluate parse result with test_html_body/tencent.json
    with open('test_html_body/netease.html', 'r') as fp:
        html = fp.read()

    crawler.crawl_html(
        html, url='https://tech.163.com/20/0819/07/FKCKGHRO00097U7S.html')
    print(crawler.data)
    import ipdb
    ipdb.set_trace()
