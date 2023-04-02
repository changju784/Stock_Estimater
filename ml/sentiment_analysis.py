import pandas as pd
from data_preprocessing import tokenize, numerize_tokens
from sklearn.model_selection import train_test_split
import ml.CNN as CNN

__all__ = ['sentiment_analysis']

def readCSV():
    '''
    Read crawled article data
    :return: dataframe
    '''
    filePath = "../docs/finviz_articles.csv"
    df = pd.read_csv(filePath, error_bad_lines=False, header=None, sep="\t", index_col=0)
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    return df

def train():
    '''
    Build sentiment analysis CNN model based on crawled data
    :return:
    '''
    # Load Data
    total_data = readCSV()

    # Data pre-processing
    total_data['Title'] = total_data['Title'].apply(tokenize)
    x = total_data['Title'].values
    y = total_data['Rate'].values
    sequence_matrix = numerize_tokens(x)
    x_train, x_test, y_train, y_test = train_test_split(sequence_matrix, y, test_size=0.2)

    result_model = CNN.build_model(x_train, y_train)
    evaluate(result_model, x_test, y_test)

def evaluate(model, x_test, y_test):
    '''
    Evaluate built model with test data
    '''
    test_sequence_matrix = numerize_tokens(x_test)
    loss, accuracy = model.evaluate(test_sequence_matrix, y_test)
    print(f'Test accuracy: {accuracy}')


if __name__ == '__main__':
    train()
