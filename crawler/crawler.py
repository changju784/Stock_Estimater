import pandas as pd
import requests
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

    def cnbc_crawler(self):
        # cnbcURL = 'https://www.cnbc.com/'
        # req = Request(cnbcURL, headers={'User-Agent': 'Mozilla/5.0'})
        # html = urlopen(req).read()
        # soup = BeautifulSoup(html, 'html.parser')

        url = 'http://finviz.com/news.ashx'

        # Make a request to the URL
        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the news articles on the page
        articles = soup.find_all('div', class_='news-content')

        # Create lists to store the data
        titles = []
        contents = []

        # Loop through each article and extract the data
        for article in articles:
            title = article.find('a', class_='nn-tab-link').get_text()
            link = article.find('a', class_='nn-tab-link')['href']
            content = ""
            # Make a request to the article URL and parse the content using BeautifulSoup
            article_response = requests.get(link)
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            # Find the article content and join the paragraphs into a single string
            article_paragraphs = article_soup.find('div', class_='news-container').find_all('p')
            content = "\n".join([p.get_text() for p in article_paragraphs])
            # Append the data to the lists
            titles.append(title)
            contents.append(content)

        # Create a dataframe from the data
        df = pd.DataFrame({'Title': title, 'Content': contents})

        # Print the dataframe
        print(df)


    def finviz_crawler(self):
        """
        Returns time & news title & pre-trained ratings dataframe crawled from finviz url.
        :return: dataframe
        """
        finviz_url = 'http://finviz.com/news.ashx'
        req = Request(finviz_url, headers={'User-Agent': 'Mozilla/5.0'})
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
        df = self.add_ratings(df)
        return df

    def add_ratings(self, df):
        """
        Pretrain text using sentiment intensity model
        :return: dataframe
        """
        df['Rate'] = ''
        sia = SentimentIntensityAnalyzer()
        for index, row in df.iterrows():
            row['Rate'] = sia.polarity_scores(row['Title'])['compound']
            print("Time: ", row['Time'])
            print("Title: ", row['Title'])
            print("Rate: ", row['Rate'])
            print("========================")
        return df

    def save_csv(self, df):
        file_path = "../docs/finviz_articles.csv"
        df.to_csv(file_path, mode='a', sep='\t', encoding='utf-8', index=False, header=False)
        return

if __name__ == '__main__':
    collector = Crawler.instance()
    df = collector.finviz_crawler()
    collector.save_csv(df)
    # collector.cnbc_crawler()


