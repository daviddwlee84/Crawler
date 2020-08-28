import os
import sys
curr_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(curr_dir))

# https://stackoverflow.com/questions/1944569/how-do-i-write-good-correct-package-init-py-files

__all__ = [
    'CCTVNewsCrawler',
    'NetEaseNewsCrawler',
    'SinaNewsCrawler',
    'SohuNewsCrawler',
    'TencentNewsCrawler',
    'TouTiaoNewsCrawler'
]

from .cctv import CCTVNewsCrawler
from .netease import NetEaseNewsCrawler
from .sina import SinaNewsCrawler
from .sohu import SohuNewsCrawler
from .tencent import TencentNewsCrawler
from .toutiao import TouTiaoNewsCrawler
