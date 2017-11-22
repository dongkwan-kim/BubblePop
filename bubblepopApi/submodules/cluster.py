from sim_metrics import *
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans


def hac_cosine_cluster(all_documents, num_cluster=15):
    """
    Clusters documents by HAC with cosine similarity.

    :param all_documents: List of strings, where each string is a normalized text.
    :param num_cluster: Number of cluster labels.
    :return: Dictionary, whose keys are cluster labels, and values are list of document index (index of all_documents).

    return example: {8: [0, 1, 2, 3, 4], 2: [5, 6, 7, 8], 1: [9, 10, 11], ...}
    """
    tfidf = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=False,
                            sublinear_tf=True, tokenizer=lambda doc: doc.split(' '))
    X = tfidf.fit_transform(all_documents)
    hac = AgglomerativeClustering(num_cluster, 'cosine', linkage='average')
    hac.fit(X.toarray())

    cluster_dict = {}
    for idx, label in enumerate(hac.labels_):
        if label not in cluster_dict.keys():
            cluster_dict[label] = [idx]
        else:
            cluster_dict[label].append(idx)

    return cluster_dict


def kmeans_cluster(all_documents, num_cluster=15):
    tfidf = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=False,
                            sublinear_tf=True, tokenizer=lambda doc: doc.split(' '))
    X = tfidf.fit_transform(all_documents)
    km = KMeans(n_clusters=num_cluster, init='k-means++', max_iter=100, n_init=1)
    km.fit(X.toarray())

    cluster_dict = {}
    for idx, label in enumerate(km.labels_):
        if label not in cluster_dict.keys():
            cluster_dict[label] = [idx]
        else:
            cluster_dict[label].append(idx)

    return cluster_dict