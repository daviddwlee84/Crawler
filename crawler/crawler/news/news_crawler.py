from urllib.parse import urlparse
from typing import Dict, List
import pandas as pd
import json
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from datetime import date, datetime


def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code

    https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable

    TODO: move this to utils
    """

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


class NewsCrawler(object):
    def __init__(self, store_in_memory: bool = True, store_in_file: str = '../../../result/news/news.json'):
        """

        TODO: anti-crawler mechanism e.g. delay


        TODO: customize parser

        https://rushter.com/blog/python-fast-html-parser/

        * selectolax
          * https://github.com/rushter/selectolax
        """
        self._store_in_memory = store_in_file
        self._store_in_file = store_in_file
        if self._store_in_memory:
            self.data = pd.DataFrame()

    def _get_raw_html(self, url: str) -> str:
        """
        Note that, you might need to customize this function,
        because the anti-crawler mechanism of each website are different.

        http://zetcode.com/python/requests/

        fake browser
        * https://stackoverflow.com/questions/27652543/how-to-use-python-requests-to-fake-a-browser-visit
        * https://pypi.org/project/fake-useragent/
        * https://github.com/hellysmile/fake-useragent

        TODO: retry on failure
        https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        raw_html = requests.get(url, headers=headers)

        if raw_html.status_code == 200:
            return raw_html.text
        else:
            return None

    def _get_html_body(self, raw_html: str) -> str:
        """
        get html body and do some clean up

        (maybe this step is not necessary, but will reduce
        the size of data to exclude some unnecessary code)
        """
        tree = BeautifulSoup(raw_html, 'lxml')

        body = tree.body
        if body is None:
            return None

        # clean up
        for tag in body.select('script'):
            tag.decompose()
        for tag in body.select('style'):
            tag.decompose()

        return str(body)

    def _get_html_title(self, html: str):
        soup = BeautifulSoup(html, 'lxml')
        return soup.title.string

    def _get_title(self, html_body: str):
        raise NotImplementedError()

    def _get_author(self, html_body: str):
        raise NotImplementedError()

    def _get_date(self, html_body: str):
        raise NotImplementedError()

    def _get_content(self, html_body: str):
        raise NotImplementedError()

    def _crawl_html_body(self, html_body: str) -> Dict[str, str]:
        """
        Crawl HTML Body and extract the information we interest in the webpage.
        Note that, you need to customize each function for the website.
        """
        title = self._get_title(html_body)
        author = self._get_author(html_body)
        date = self._get_date(html_body)
        content = self._get_content(html_body)

        return {
            'url': None,
            'domain': None,
            'html_title': None,
            'html_body': html_body,
            'title': title,
            'author': author,
            'date': date,
            'content': content,
        }

    def crawl_html(self, html: str, input_body_only: bool = False, url: str = None) -> Dict[str, str]:
        """
        Wrapper for _craw_html_body

        We store result to memory and file here, if specified.

        The input_body_only is used to support that the crawled result of
        RetroIndex only store HTML body
        """
        if input_body_only:
            html_body = html
        else:
            html_body = self._get_html_body(html)

        result = self._crawl_html_body(html_body)
        if not input_body_only:
            html_title = self._get_html_title(html)
            result['html_title'] = html_title

        if url:
            # https://stackoverflow.com/questions/9626535/get-protocol-host-name-from-url
            _parsed_uri = urlparse(url)
            domain = '{uri.netloc}'.format(uri=_parsed_uri)
            result['url'] = url
            result['domain'] = domain

        if self._store_in_memory:
            # https://stackoverflow.com/questions/51774826/append-dictionary-to-data-frame
            self.data = self.data.append(result, ignore_index=True)

        if self._store_in_file:
            with open(self._store_in_file, 'a', encoding='utf8') as fp:
                json.dump(result, fp, ensure_ascii=False, default=json_serial)
                fp.write('\n')

        return result

    def crawl_single_url(self, url: str) -> Dict[str, str]:
        """
        Crawl single news from an given URL.
        """
        raw_html = self._get_raw_html(url)
        if not raw_html:
            return None

        result = self.crawl_html(raw_html, input_body_only=False, url=url)

        return result

    def crawl_urls(self, urls: List[str]) -> List[Dict[str, str]]:
        results = []
        for url in tqdm(urls):
            result = self.crawl_single_url(url)
            if not result:
                print('Fail:', url)
                continue
            results.append(result)
        return results


test_html = """
<html>
    <head>
    </head>
    <body>
        <h1> This is a test. </h1>
    </body>
</html>
"""


def test_html_body():
    crawler = NewsCrawler(False, '')
    return crawler._get_html_body(test_html)


if __name__ == "__main__":
    print(test_html_body())