from urllib.parse import urlparse
from typing import Dict, List
import pandas as pd
import json
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm


class NewsCrawler(object):
    def __init__(self, store_in_memory: bool = True, store_in_file: str = '../../result/news.json'):
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

        return body

    def _get_title(self, html_body: str):
        raise NotImplementedError()

    def _get_author(self, html_body: str):
        raise NotImplementedError()

    def _get_date(self, html_body: str):
        raise NotImplementedError()

    def _get_content(self, html_body: str):
        raise NotImplementedError()

    def _crawl_html_body(self, html_body: str) -> Dict[str, str]:
        title = self._get_title(html_body)
        author = self._get_author(html_body)
        date = self._get_date(html_body)
        content = self._get_content(html_body)

        # https://stackoverflow.com/questions/9626535/get-protocol-host-name-from-url
        _parsed_uri = urlparse(url)
        domain = '{uri.netloc}'.format(uri=_parsed_uri)

        return {
            'url': url,
            'domain': domain,
            'html_body': html_body,
            'title': title,
            'author': author,
            'date': date,
            'content': content,
        }

    def crawl_html_body(self, html_body: str) -> Dict[str, str]:
        """
        Wrapper for _craw_html_body

        We store result to memory and file here, if specified.
        """
        result = self._crawl_html_body(html_body)

        if self._store_in_memory:
            # https://stackoverflow.com/questions/51774826/append-dictionary-to-data-frame
            self.data = self.data.append(result, ignore_index=True)

        if self._store_in_file:
            with open(self._store_in_file, 'a', encoding='utf8') as fp:
                json.dump(result, fp, ensure_ascii=False)
                fp.write('\n')

        return result

    def crawl_single_url(self, url: str) -> Dict[str, str]:
        """
        Crawl single news from an given URL.
        """
        raw_html = self._get_raw_html(url)
        if not raw_html:
            return None

        html_body = self._get_html_body(raw_html)
        result = self.crawl_html_body(html_body)

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
