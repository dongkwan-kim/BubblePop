from collections import Counter
import re

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
    Computes the cosine similarity of some documents.

    :param all_documents: List of documents which are in string format.
    :return: Matrix of cosine similarities of each pair of documents.
    """
    tfidf = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=False,
                            sublinear_tf=True, tokenizer=lambda doc: doc.split(' '))
    return cosine_similarity(tfidf.fit_transform(all_documents))


def jaccard(doc1, doc2, domain_size=20):
    """
    Computes the Jaccard coefficient of two documents. The number of words which are subject to the calculation is
    determined by cutting 'domain_size' number of words from most-used one to the least-used.

    :param doc1: Whole paragraph of the first document as str type.
    :param doc2: Whole paragraph of the second document as str type.
    :param domain_size: Number of words which are subject to the evaluation in each document.
    :return: list(Jaccard coefficient, union of morphemes of two documents).
    """
    result = []
    counter1 = Counter(normalize(doc1, as_list=True))
    counter2 = Counter(normalize(doc2, as_list=True))
    words1 = set()
    words2 = set()
    for elem in counter1.most_common(domain_size):
        words1.add(elem[0])
    for elem in counter2.most_common(domain_size):
        words2.add(elem[0])
    union = words1.union(words2)
    intersection = words1.intersection(words2)
    result.append(len(intersection) / len(union))
    result.append(union)
    return result
