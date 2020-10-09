from typing import List
import os
import sys
import json

curr_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(curr_dir, '..'))

from crawler.crawler.zhihu.zhihu import User, Post

author_list = [
    'li_ge_notes',
    'wang-jia-48-31',
]


def __get_raw_post(posts: List[Post]) -> List[str]:
    """
    TODO: try to keep the format (e.g. `\n`)
    """
    return [post.content_raw_text for post in posts]


if __name__ == "__main__":
    result_dir = os.path.join(curr_dir, '../result/zhihu')
    for author in author_list:
        parse_file = os.path.join(result_dir, author + '.json')
        if not os.path.exists(parse_file):
            user = User(username=author)
            print('Parsing', user, '...')
            all_posts = list(user.get_posts())
            print('Parsed articles:', len(all_posts))
            with open(parse_file, 'w', encoding='utf8') as stream:
                json.dump(__get_raw_post(all_posts), stream,
                          indent=4, ensure_ascii=False)
        else:
            print(author, 'exist.')
