from news_crawler import NewsCrawler
from bs4 import BeautifulSoup
import datefinder
import re


def clean_up(text: str) -> str:
    tab = re.compile('#TAB#')
    rchar = re.compile('#R#')
    newline = re.compile('#N#')

    text = tab.sub('\t', text)
    text = rchar.sub('\r', text)
    text = newline.sub('\n', text)

    return text


class NetEaseNewsCrawler(NewsCrawler):
    def __init__(self, store_in_memory: bool = True, store_in_file: str = '../../../result/news/neteast_news.json'):
        super().__init__(store_in_memory, store_in_file)

    def _get_title(self, html_body_soup: BeautifulSoup):
        title = html_body_soup.find('h1').text
        return clean_up(title).strip()

    def _get_author(self, html_body_soup: BeautifulSoup):
        """
        TODO: Still need to refine this

        Information can be found in <head> <meta name="author">
        Information can be found in <head> <meta property="article:author">
        """
        author = html_body_soup.select_one('.ep-editor').text
        return clean_up(author).strip()

    def _get_date(self, html_body_soup: BeautifulSoup):
        """
        TODO: seems this need some NLP method to extract from content or something

        Information can be found in <head> <meta name="article:published_time">
        """
        post_time_source = html_body_soup.find(
            'div', {'class': 'post_time_source'})
        return next(datefinder.find_dates(post_time_source.text))

    def _get_content(self, html_body_soup: BeautifulSoup):
        article = html_body_soup.find('div', {'class': 'post_text'})
        if not article:
            article = html_body_soup.find('div', {'class': 'post_body'})
        return clean_up(article.text)


def test_post_time():
    test_str = '<div class="post_time_source">#N#                2018-01-16 17:44:59\u3000来源: <a id="ne_article_source" href="http://www.cqcb.com/headline/2018-01-16/640599_pc.html" target="_blank">重庆晨报上游新闻</a>#N#              #TAB##N#                <a href="http://jubao.aq.163.com/" target="_blank" class="post_jubao" title="举报">举报</a>#N#            </div>'
    post_time_source = BeautifulSoup(test_str, 'lxml').find(
        'div', {'class': 'post_time_source'})
    # for date in datefinder.find_dates(post_time_source.text):
    #     print(date)
    print(next(datefinder.find_dates(post_time_source.text)))


if __name__ == "__main__":
    # test_post_time()
    # import ipdb
    # ipdb.set_trace()

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
