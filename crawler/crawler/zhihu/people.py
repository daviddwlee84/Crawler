import requests
from bs4 import BeautifulSoup
from functools import lru_cache


class User(object):
    def __init__(self, username: str = None, url: str = None):
        if url:
            self.base_url = url
            assert 'www.zhihu.com/people/' in url, 'Not a valid user url'
        elif username:
            self.base_url = f'https://www.zhihu.com/people/{username}'
        else:
            assert False, 'Require either username or url'
        self.page_cache = {}

    # ==== Base Function ==== #

    def _get_page(self, tab: str):
        if tab in self.page_cache:
            return self.page_cache[tab]

        if tab == 'feed':
            url = self.base_url
        else:
            url = self.base_url + '/' + tab

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        raw_html = requests.get(url, headers=headers)

        if raw_html.status_code == 200:
            self.page_cache[tab] = raw_html.text
            return self.page_cache[tab]

        return None

    # ==== Infos ==== #

    def get_profile(self):
        """
        TODO: there are some other more detail informations
        """

        html = self._get_page('feed')
        tree = BeautifulSoup(html, 'lxml')
        profile = tree.find(
            'div', {'class': 'ProfileHeader-main'})

        title = profile.select_one('.ProfileHeader-title')
        name = title.select_one('.ProfileHeader-name')

        return {
            'name': name.text
        }

    # ==== Helper ==== #

    def _get_list_item(self, tab: str):
        """
        Get list of item, collect its meta data (title, cover image, "link")
        TODO: next page
        """
        html = self._get_page(tab)
        tree = BeautifulSoup(html, 'lxml')

        items = []
        for result in tree.find_all('div', {'class', 'List-item'}):
            item = {}

            article_meta_content = result.find('div', {'class', 'ContentItem'})
            for tag in article_meta_content.findChildren('meta', recursive=False):
                item[tag.get('itemprop')] = tag.get('content')
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
        TODO
        """
        items = self._get_list_item('answers')
        import ipdb
        ipdb.set_trace()
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

    def get_posts(self):
        """
        TODO
        """
        pass

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


if __name__ == "__main__":
    user = User(url='https://www.zhihu.com/people/wang-jia-48-31')
    print(user.get_profile()['name'])
    print(user.get_answers())

    user = User(username='li_ge_notes')
    print(user.get_profile()['name'])
    print(user.get_answers())
    import ipdb
    ipdb.set_trace()
