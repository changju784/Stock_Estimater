from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

class Crawler:
    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

    def finvizCrawler(self):
        finvizURL = 'http://finviz.com/news.ashx'
        bloombergURL = 'http://www.bloomberg.com/markets/economics'
        req = Request(finvizURL, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        bsObject = BeautifulSoup(html, 'html.parser')
        print(bsObject)
        # for meta in bsObject.find_all('meta'):
        #     print(meta.get('content'))

if __name__ == '__main__':
    collector = Crawler.instance()
    collector.finvizCrawler()

