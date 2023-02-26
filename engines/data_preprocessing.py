from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

__all__ = ['tokenize']

def tokenize(text):
    """
    returns tokens of texts
    :return: tokens list
    """
    tokens = word_tokenize(text)
    tokens = [t.lower() for t in tokens if t.isalnum()]
    tokens = remove_stopwords(tokens)
    return tokens


def remove_stopwords(tokens):
    """
    Remove stopwords from tokens
    :return: tokens list
    :param tokens:
    :return:
    """
    tokens = [t for t in tokens if not t in set(stopwords.words('english'))]
    return tokens
