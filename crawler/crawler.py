from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd

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
        # Returns time & news title dataframe crawled from finviz url.
        finvizURL = 'http://finviz.com/news.ashx'
        # bloombergURL = 'http://www.bloomberg.com/markets/economics'
        req = Request(finvizURL, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        tables = []
        for table in soup.find_all('table'):
            for tr in table.find_all('tr'):
                tableData = [td.get_text(strip=True) for td in tr.find_all('td')]
                if len(tableData) == 3:
                    tables.append(tableData)
        df = pd.DataFrame(tables[1:], columns=['', 'Time', 'Title'])
        df = df.iloc[:, 1:]
        df = df[df['Time'].map(len) == 7]
        return df




if __name__ == '__main__':
    collector = Crawler.instance()
    collector.finvizCrawler()

