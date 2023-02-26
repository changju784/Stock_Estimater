import pandas as pd
from data_preprocessing import tokenize

__all__ = ['sentiment_analysis']

def readCSV():
    filePath = "../docs/finviz_articles.csv"
    df = pd.read_csv(filePath, error_bad_lines=False, header=None, sep="\t", index_col=0)
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    return df

def train():
    total_data = readCSV()
    total_data['Title'] = total_data['Title'].apply(tokenize)
    X = total_data['Title'].values
    y = total_data['Rate'].values



if __name__ == '__main__':
    train()
