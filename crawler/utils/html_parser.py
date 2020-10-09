import os
import requests
from cachetools import LRUCache
import time

curr_dir = os.path.dirname(os.path.abspath(__file__))


class HTMLParser(object):
    """
    Assign parsing task into it.

    It will mantain a queue and parse website in multithread with random switch proxy.

    Make headless an optional?!
    """

    def __init__(self, mode: str = 'requestium',
                 use_cache: bool = True, max_cache_size: int = 10000,
                 timeout: int = 15, browser: str = 'chrome',
                 loading_time: int = 3,  # delay to wait the webpage loading
                 webdriver_path: str = os.path.join(curr_dir, 'chromedriver')):
        assert mode in ['requests', 'selenium', 'requestium']
        assert browser in ['chrome']

        self.mode = mode
        self.loading_time = loading_time
        self.timeout = timeout
        self.use_cache = use_cache
        if use_cache:
            self.html_cache = LRUCache(maxsize=max_cache_size)

        if mode == 'requests':
            pass
        elif mode == 'selenium':
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(
                webdriver_path, chrome_options=chrome_options)
        elif mode == 'requestium':
            from requestium import Session, Keys
            self.session = Session(webdriver_path=webdriver_path,
                                   browser='chrome',
                                   default_timeout=timeout,
                                   webdriver_options={'arguments': ['headless']})
        else:
            assert False, '"mode" must be either requests, selenium, or requestium.'

    def _get_html(self, url: str, use_driver: bool = False, check_status: bool = False) -> str:
        """
        TODO: Add asynchronous queue

        use_driver only used for requestium
        TODO: check_status is used for, when using "driver", we don't know the html status code
        https://stackoverflow.com/questions/5799228/how-to-get-status-code-by-using-selenium-py-python-code
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        if self.mode == 'requests':
            raw_html = requests.get(url, headers=headers)
            if raw_html.status_code == 200:
                return raw_html.text

        elif self.mode == 'selenium':
            self.driver.get(url)
            # give some time for driver to load webpabe
            time.sleep(self.loading_time)
            return self.driver.page_source

        elif self.mode == 'requestium':
            if use_driver:
                self.session.driver.get(url)
                # give some time for driver to load webpabe
                time.sleep(self.loading_time)
                return self.session.driver.page_source
            else:
                raw_html = self.session.get(url, headers=headers)
                if raw_html.status_code == 200:
                    return raw_html.text

    def get_html_directly(self, url: str, use_driver: bool = False, check_status: bool = False) -> str:
        """
        Cache wrapper

        TODO: auto fix url schema (i.e. add http or https)
        (requests.exceptions.MissingSchem)
        """
        if self.use_cache:
            if url not in self.html_cache:
                html = self._get_html(url, use_driver, check_status)

                if not html:
                    return None

                self.html_cache[url] = html
            return self.html_cache[url]
        else:
            return self._get_html(url, use_driver, check_status)


if __name__ == "__main__":
    import timeit
    parser = HTMLParser(mode='requests')
    start = timeit.default_timer()
    parser.get_html_directly('https://www.google.com')
    print(timeit.default_timer() - start)

    parser = HTMLParser(mode='selenium')
    start = timeit.default_timer()
    parser.get_html_directly('https://www.google.com')
    print(timeit.default_timer() - start)

    parser = HTMLParser(mode='requestium', use_cache=False)
    start = timeit.default_timer()
    parser.get_html_directly('https://www.google.com', use_driver=False)
    print(timeit.default_timer() - start)
    start = timeit.default_timer()
    parser.get_html_directly('https://www.google.com', use_driver=True)
    print(timeit.default_timer() - start)
