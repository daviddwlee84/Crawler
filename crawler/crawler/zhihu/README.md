# Zhihu Crawler

## Base Classes

* `User`
* `Question`
* `Answer`
* `Post`

## Notes

Might have parsed failed problem.

For example:

```txt
https://zhuanlan.zhihu.com/p/260060450

该内容暂无法显示

文章被建议修改：违反知乎社区管理规定
作者修改内容通过后，文章会重新显示。
```

## TODO

* [ ] Deal with if getting html fail problem
* [X] Deal with single page too few "List-item" when using request parse html vs. using browser
* [ ] Parse Post with format (e.g. Markdown) or at least preserve paragraph (i.e. next lines)
  * Or this might good for test the "corrector"

## Resources

### Example

* [LiuRoy/zhihu_spider: 知乎爬虫](https://github.com/LiuRoy/zhihu_spider)
* [egrcc/zhihu-python: 获取知乎内容信息，包括问题，答案，用户，收藏夹信息](https://github.com/egrcc/zhihu-python)
* [shanelau/zhihu: 项目没有维护了， fork 吧](https://github.com/shanelau/zhihu)
* [lzjun567/zhihu-api: Zhihu API for Humans](https://github.com/lzjun567/zhihu-api)
* [ccforward/zhihu: ✨ 知乎日报 - 爬虫、数据分析、Node.js、Vue.js ...](https://github.com/ccforward/zhihu)
