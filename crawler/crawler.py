import pandas as pd
from datetime import datetime
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer

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
        '''
        Returns time & news title dataframe crawled from finviz url.
        :return: dataframe
        '''
        finvizURL = 'http://finviz.com/news.ashx'
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

        # Preprocess Title
        df = df[df['Title'] != "Loading…"]

        # Format Time
        df = df[df['Time'].map(len) == 7]
        now = datetime.today().strftime('%Y-%m-%d')
        df['Time'] = now + ' ' + df['Time']
        df = self.usePreTrainedModel(df)
        return df

    def usePreTrainedModel(self, df):
        df['Rate'] = ''
        sia = SentimentIntensityAnalyzer()
        for index, row in df.iterrows():
            row['Rate'] = sia.polarity_scores(row['Title'])['compound']
        return df


    def saveCSV(self, df):
        filePath = "../docs/finviz_articles.csv"
        df.to_csv(filePath, sep='\t', encoding='utf-8', index=False)
        return

if __name__ == '__main__':
    collector = Crawler.instance()
    df = collector.finvizCrawler()
    collector.saveCSV(df)


