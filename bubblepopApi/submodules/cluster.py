from collections import Counter
import random

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def cluster(all_documents, algo='hac', verbose=False):
    """
    Clusters documents by HAC with cosine similarity.

    :param all_documents: List of strings, where each string is a normalized text.
    :param algo: Kind of algorithm which will be used.
    :param verbose: If verbose is true, then this function prints labels of each element in all_documents.
    :return: Dictionary, whose keys are cluster labels, and values are list of document index (index of all_documents).

    return example: {8: [0, 1, 2, 3, 4], 2: [5, 6, 7, 8], 1: [9, 10, 11], ...}
    """
    # Model initialization.
    tfidf = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=False,
                            sublinear_tf=True, tokenizer=lambda doc: doc.split(' '))
    X = tfidf.fit_transform(all_documents)
    cos_sim = cosine_similarity(X)
    num_expected_topic = int(len(all_documents) / 60 + 1)   # Hyper-parameter we should adjust.
    num_cluster = 3 * num_expected_topic

    # Algorithm selection.
    if algo == 'hac':
        cluster = AgglomerativeClustering(num_cluster, 'cosine', linkage='average')
    elif algo == 'k':
        cluster = KMeans(n_clusters=num_cluster, init='k-means++', max_iter=100, n_init=1)
    else:
        raise ValueError

    # Fit model to the data and get cluster labels.
    cluster.fit(X.toarray())
    cluster_labels = cluster.labels_

    # Drop out minor clusters.
    bincount = np.bincount(cluster_labels)
    argsort = np.argsort(bincount)
    id_mapping = {}
    for label, idx in enumerate(argsort[::-1]):
        if bincount[idx] > int(len(all_documents) * 0.03):
            id_mapping[idx] = label
        else:
            id_mapping[idx] = -1
    for idx, _ in enumerate(cluster_labels):
        cluster_labels[idx] = id_mapping[cluster_labels[idx]]

    # Verbose flag.
    if verbose:
        print(cluster_labels)

    # Make cluster dictionary, which is the return format of this function.
    cluster_dict = {}
    for idx, label in enumerate(cluster_labels):
        if label not in cluster_dict.keys():
            cluster_dict[label] = [idx]
        else:
            cluster_dict[label].append(idx)

    # Reassign each data point of the minor clusters to the major clusters.
    minors = cluster_dict.pop(-1, None)
    for minor_idx in minors:
        max_cluster_ids = []
        for neighbor in range(10):
            max_sim = -1
            cluster_id = -1
            for key in cluster_dict:
                major_idx = random.choice(cluster_dict[key])
                sim = cos_sim[major_idx][minor_idx]
                if sim > max_sim:
                    max_sim = sim
                    cluster_id = key
            max_cluster_ids.append(cluster_id)
        counter = Counter(max_cluster_ids)
        result_id = counter.most_common(1)[0][0]
        cluster_dict[result_id].append(minor_idx)

    return cluster_dict
