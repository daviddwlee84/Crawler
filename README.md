# Crawler

## Requirements

```sh
# Install packages
pip3 install -r requirements.txt

# Setup driver for your system
cd crawler/utils
bash get_chromedriver_Linux.sh
bash get_chromedriver_WSL.sh
```

## Crawlers

### [News Crawler](crawler/crawler/news)

* Base class: `crawler/crawler/news/news_crawler.py`

### [Zhihu Crawler](crawler/crawler/zhihu)

## Todo

News Crawler

* [X] Passing soup object instead of HTML body string
* [ ] Anti-crawler
* [ ] Testcase
* [ ] Get keyword (during crawling (e.g. NER, html meta data) or after (e.g. TF-IDF))

## Resources

* [Crawler Traps: How to Identify and Avoid Them](https://www.contentkingapp.com/academy/crawler-traps/)

### Useful Tools

* [hellysmile/fake-useragent: up to date simple useragent faker with real world database](https://github.com/hellysmile/fake-useragent)
* [TheDevFromKer/Fake-Headers: Simple headers generator for requests lib](https://github.com/TheDevFromKer/Fake-Headers)
* [akoumjian/datefinder: Find dates inside text using Python and get back datetime objects](https://github.com/akoumjian/datefinder)
* [Decode or Encode Unicode Text - Online Toolz](https://www.online-toolz.com/tools/text-unicode-entities-convertor.php)

### Example

* [**clips/pattern: Web mining module for Python, with tools for scraping, natural language processing, machine learning, network analysis and visualization.**](https://github.com/clips/pattern)
* [iofu728/spider: 🕷some website spider application base on proxy pool (support http & websocket)](https://github.com/iofu728/spider)
