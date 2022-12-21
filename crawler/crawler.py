from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from bs4.element import Comment

class Crawler:
    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def finvizCrawler(self):
        finvizURL = 'http://finviz.com/news.ashx'
        bloombergURL = 'http://www.bloomberg.com/markets/economics'
        req = Request(finvizURL, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser').body
        # print(bsObject.head.find('meta', {'name':'description'}).get('content'))
        [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]



if __name__ == '__main__':
    collector = Crawler.instance()
    collector.finvizCrawler()

