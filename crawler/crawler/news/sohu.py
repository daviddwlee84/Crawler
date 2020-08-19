from news_crawler import NewsCrawler
from bs4 import BeautifulSoup
import datefinder


class NetEaseNewsCrawler(NewsCrawler):
    def __init__(self, store_in_memory: bool = True, store_in_file: str = '../../../result/news/sohu_news.json'):
        super().__init__(store_in_memory, store_in_file)

    def _get_title(self, html_body_soup: BeautifulSoup):
        """
        Seems there might have some dirty content here
        """
        title = html_body_soup.find('div', {'class': 'text-title'}).text
        return title.strip().split('\n')[0]

    def _get_author(self, html_body_soup: BeautifulSoup):
        article_info = html_body_soup.find('div', {'class': 'article-info'})
        return article_info.find_all('span')[-1].find('a').text

    def _get_date(self, html_body_soup: BeautifulSoup):
        article_info = html_body_soup.find('div', {'class': 'article-info'})
        return list(datefinder.find_dates(article_info.text))[0]

    def _get_content(self, html_body_soup: BeautifulSoup):
        article = html_body_soup.find('article', {'class': 'article'}).text
        return article


if __name__ == "__main__":
    crawler = NetEaseNewsCrawler()
    crawler.crawl_single_url(
        'https://www.sohu.com/a/413813393_267106')  # success!!!

    # TODO: write Testcase by evaluate parse result with test_html_body/tencent.json
    with open('test_html_body/sohu.html', 'r') as fp:
        html = fp.read()

    crawler.crawl_html(
        html, url='https://www.sohu.com/a/413838286_115565')
    print(crawler.data)
    import ipdb
    ipdb.set_trace()
