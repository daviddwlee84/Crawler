import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from functools import lru_cache
import time


@lru_cache()
def _get_html(url: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    raw_html = requests.get(url, headers=headers)

    if raw_html.status_code == 200:
        return raw_html.text

    return None


class User(object):
    def __init__(self, username: str = None, url: str = None):
        if url:
            self.base_url = url
            assert 'www.zhihu.com/people/' in url, 'Not a valid user url'
            self.username = url.rsplit('/', 1)[-1]
        elif username:
            self.username = username
            self.base_url = f'https://www.zhihu.com/people/{username}'
        else:
            assert False, 'Require either username or url'
        self.page_cache = {}

        self.get_profile()

    # https://www.geeksforgeeks.org/str-vs-repr-in-python/
    def __str__(self):
        return f'{self.name} ({self.username})'

    # ==== Base Function ==== #

    def _get_tab_base_url(self, tab: str) -> str:
        """
        Get tab base url by tab name (zhihu user page)
        """
        if tab == 'feed':
            url = self.base_url
        else:
            url = self.base_url + '/' + tab
        return url

    def _get_single_page(self, tab: str):
        """
        TODO: consider deprecate this method
        """
        if tab in self.page_cache:
            return self.page_cache[tab]

        url = self._get_tab_base_url(tab)

        html = _get_html(url)
        if not html:
            return None

        self.page_cache[tab] = html
        return self.page_cache[tab]

    # ==== Infos ==== #

    def get_profile(self):
        """
        TODO: there are some other more detail informations
        """

        html = self._get_single_page('feed')
        tree = BeautifulSoup(html, 'lxml')
        profile = tree.find(
            'div', {'class': 'ProfileHeader-main'})

        title = profile.select_one('.ProfileHeader-title')
        name = title.select_one('.ProfileHeader-name')

        self.name = name.text

    # ==== Helper ==== #

    def _get_multi_page_list_items(self, tab: str, method: str = 'get', max_pages: int = float('inf'), next_page_delay: float = 1):
        """
        next: keep click "next page"
        get: zhihu support `?page` get request
        """
        assert method in ['next', 'get']

        results = []

        base_url = self._get_tab_base_url(tab)

        if method == 'next':
            # TODO
            # while True:
            #     page_result = self._get_list_items(html)
            #     results.extend(page_result)
            #     next_button = tree.find('div', {'class': 'Pagination'}).find(
            #         'button', {'class': 'PaginationButton-next'})

            #     if not page_result or not next_button:
            #         break
            pass
        elif method == 'get':
            i = 1
            while True:
                html = _get_html(base_url + f'?page={i}')
                page_result = self._get_list_items(html)
                if not page_result or i >= max_pages:
                    break
                print('Parsed', base_url + f'?page={i}')
                results.extend(page_result)
                i += 1

        return results

    def _get_list_items(self, html: str) -> List[Dict[str, str]]:
        """
        Get list of item, collect its meta data (title, cover image, "link")
        TODO: next page
        """
        def fix_url(url: str):
            if url.startswith('//'):
                return 'https:' + url
            return url

        tree = BeautifulSoup(html, 'lxml')

        items = []
        for result in tree.find_all('div', {'class', 'List-item'}):
            item = {}

            article_meta_content = result.find('div', {'class', 'ContentItem'})
            # https://stackoverflow.com/questions/6287529/how-to-find-children-of-nodes-using-beautifulsoup
            for tag in article_meta_content.findChildren('meta', recursive=False):
                item[tag.get('itemprop')] = tag.get('content')

            # Somehow the "url" of "Post" will be "//url" so we have to fix it
            if 'url' in item:
                item['url'] = fix_url(item['url'])

            author_meta_content = article_meta_content.find(
                'div', {'class', 'ContentItem-meta'})
            for tag in author_meta_content.find_all('meta'):
                item['author_' + tag.get('itemprop')] = tag.get('content')

            rich_content = result.find('div', {'class', 'RichContent'})
            item['brief'] = rich_content.find(
                'div', 'RichContent-inner').find('span', {'class', 'RichText'}).text

            items.append(item)

        return items

    # ==== Tabs ==== #

    def get_answers(self):
        """
        TODO: switch to multi_page
        """
        html = self._get_single_page('answers')
        items = self._get_list_items(html)
        return items

    def get_zvideos(self):
        """
        TODO
        """
        pass

    def get_asks(self):
        """
        TODO
        """
        pass

    def get_posts(self, max_pages: int = float('inf')):
        """
        """
        items = self._get_multi_page_list_items('posts', max_pages=max_pages)
        return (
            Post(url=item['url']).parse() for item in items
        )

    def get_columns(self):
        """
        TODO
        """
        pass

    def get_pins(self):
        """
        TODO
        """
        pass

    def get_collections(self):
        """
        TODO
        """
        pass

    def get_following(self):
        """
        TODO: Directly return User objects
        """
        pass


class Post(object):

    __page = None
    parsed = False

    def __init__(self, id_num: str = None, url: str = None, init_parse: bool = False):
        if url:
            self.url = url
            assert 'zhuanlan.zhihu.com/p/' in url, 'Not a valid user url'
        elif id_num:
            self.url = f'https://zhuanlan.zhihu.com/p/{id_num}'
        else:
            assert False, 'Require either id_num or url'

        if init_parse:
            self.parse()

    def __str__(self):
        if not self.parsed:
            self.parse()
        return f'<<{self.title}>>'

    def __repr__(self):
        if not self.parsed:
            return '<<Unparsed Post object>>'
        return f'<<{self.title}>>'

    # ==== Parsing ==== #

    def _parse_header(self, header: BeautifulSoup):
        self.title = header.find('h1', {'calss', 'Post-Title'}).text
        author_info = header.find('div', {'class', 'AuthorInfo'})
        author_url = author_info.find(itemprop='url').get('content')
        self.author = User(url=author_url)

    def _parse_content(self, content: BeautifulSoup):
        self.content_html = str(content)
        self.content_raw_text = content.text
        # TODO: read detail paragraphs, figures as list
        # TODO: or read it as Markdown format

    def parse(self):
        """
        TODO: try lazy parse (only parse when it's used)
        """
        if not self.__page:
            self.__page = _get_html(self.url)
        self.parsed = True

        main = BeautifulSoup(self.__page, 'lxml').find('main')
        article = main.find('article')

        header = article.find('header')
        self._parse_header(header)

        content = article.find('div', {'class', 'RichText'})
        self._parse_content(content)

        return self


class Question(object):
    def __init__(self):
        pass

    def get_answers(self):
        """
        TODO: return Answer objects
        """
        pass


class Answer(object):
    def __init__(self):
        pass

# ====== Test ======


def __test_user():
    # user = User(url='https://www.zhihu.com/people/wang-jia-48-31')
    # print(user.name)
    # print(user.get_answers())

    user = User(username='li_ge_notes')
    print(user)
    print(user.get_answers())
    print(list(user.get_posts(max_pages=5)))


def __test_post():
    post = Post(url='https://zhuanlan.zhihu.com/p/257277844').parse()
    print(post.title)
    print(post.author)
    # print(post.author.get_answers())
    # print(post.content_html)
    print(post.content_raw_text)


if __name__ == "__main__":
    __test_user()
    # __test_post()
    import ipdb
    ipdb.set_trace()
