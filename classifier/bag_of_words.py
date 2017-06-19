"""BOW implementation."""
import re
from collections import OrderedDict

import pandas


def bag_of_words(documents, vocabulary, normalization=True):
    """Perform Bag of Words algorithm.

    :param documents: iterable that contains all documents.
    :param normalization: if True vectors will contains relative frequencies.
    :return: pandas.Series
    """
    dimensions = len(vocabulary)
    vectors = []
    for text in documents:
        words = [w.lower() for w in re.findall(r"[a-zA-Z']+", text)]
        vector = [0] * dimensions
        for word in words:
            if word in vocabulary:
                vector[vocabulary[word]] += 1
        words_count = len(words) + 1
        if normalization:
            vectors.append([e / words_count * 100 for e in vector])
        else:
            vectors.append(vector)
    return pandas.Series(vectors)


def prepare_vocabulary(documents, low_bound=10, high_bound=500):
    """
    :param documents: iterable that contains all documents.
    :param low_bound: exclude words that appears less times then that number.
    :param high_bound: exclude words that appears more times then that number.
    :return: OrderedDict
    """
    vocabulary = OrderedDict()  # numbered words
    for text in documents:
        words = [w.lower() for w in re.findall(r"[a-zA-Z']+", text)]
        for word in words:
            vocabulary[word] = vocabulary.get(word, 0) + 1
    trimmed_vocabulary = OrderedDict()
    word_count = 0
    for word, frequency in vocabulary.items():
        if low_bound <= frequency <= high_bound:
            trimmed_vocabulary[word] = word_count
            word_count += 1
    return trimmed_vocabulary
