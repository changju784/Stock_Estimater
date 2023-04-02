from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

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
    """
    tokens = [t for t in tokens if not t in set(stopwords.words('english'))]
    return tokens

def numerize_tokens(tokens):
    """
    Numerize and pad tokens
    :return: numerized tokens
    """
    tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
    tokenizer.fit_on_texts(tokens)
    sequences = tokenizer.texts_to_sequences(tokens)
    padded_sequences = pad_sequences(sequences, maxlen=100, padding='post', truncating='post')
    return padded_sequences
