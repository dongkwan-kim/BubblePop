from collections import Counter
import re

import numpy as np
from konlpy.tag import Hannanum
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

han = Hannanum()
hangul = re.compile('[^ 가-힣]+')
stop_file = open('stop_words.txt', 'r')
stop_words = stop_file.read().split(' ')
stop_file.close()


def normalize(doc, as_list=False):
    """
    Normalizes raw text, i.e., removes all punctuations, latin alphabets, numbers other than Hangul.
    This function does not merge the same words as one entity, because the occurrence of each word should be
    counted in order to calculate similarity using cosine or Jaccard coefficient.

    :param doc: Raw text whose type is string.
    :param as_list: If the flag is true, returns a list of normalized words. Otherwise, returns blank-joined string.
    :return: Normalized words with duplicates.
    """
    doc = hangul.sub('', doc)
    doc_words = han.nouns(doc)
    new_words = []
    for elem in doc_words:
        if elem not in stop_words:
            new_words.append(elem)
    if as_list:
        return new_words
    else:
        return ' '.join(new_words)


def cosine_sim(all_documents):
    """
    Computes the cosine similarities of some documents.

    :param all_documents: List of documents which are in string format.
    :return: Matrix of cosine similarities of each pair of documents.
    """
    tfidf = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=False,
                            sublinear_tf=True, tokenizer=lambda doc: doc.split(' '))
    return cosine_similarity(tfidf.fit_transform(all_documents))


def jaccard_sim(all_documents, domain_size=30):
    """
    Computes the Jaccard similarities of some documents.

    :param all_documents: List of documents which are in string format.
    :param domain_size: Number of words which are subject to the evaluation in each document.
    :return: Matrix of Jaccard similarities of each pair of documents.
    """
    list_of_wordset = []
    for idx in range(len(all_documents)):
        counter = Counter(all_documents[idx].split(' '))
        words = set()
        for elem in counter.most_common(domain_size):
            words.add(elem[0])
        list_of_wordset.append(words)

    result = np.ones((len(all_documents), len(all_documents)))
    for i in range(len(all_documents)):
        words1 = list_of_wordset[i]
        for j in range(i + 1, len(all_documents)):
            words2 = list_of_wordset[j]
            union = words1.union(words2)
            intersection = words1.intersection(words2)
            if len(union) == 0:
                result[i][j] = 1
            jaccard_val = len(intersection) / len(union)
            result[i][j] = jaccard_val
            result[j][i] = jaccard_val
    return result
