from submodules.sim_metrics import *
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans


def cluster(all_documents, num_expected_topic=10, algo='hac', verbose=False):
    """
    Clusters documents by HAC with cosine similarity.

    :param all_documents: List of strings, where each string is a normalized text.
    :param num_cluster: Number of cluster labels.
    :param algo: Kind of algorithm which will be used.
    :param verbose: If verbose is true, then this function prints labels of each element in all_documents.
    :return: Dictionary, whose keys are cluster labels, and values are list of document index (index of all_documents).

    return example: {8: [0, 1, 2, 3, 4], 2: [5, 6, 7, 8], 1: [9, 10, 11], ...}
    """
    tfidf = TfidfVectorizer(norm='l2', min_df=0, use_idf=True, smooth_idf=False,
                            sublinear_tf=True, tokenizer=lambda doc: doc.split(' '))
    X = tfidf.fit_transform(all_documents)
    num_cluster = 3 * num_expected_topic

    if algo == 'hac':
        cluster = AgglomerativeClustering(num_cluster, 'cosine', linkage='average')
    elif algo == 'k':
        cluster = KMeans(n_clusters=num_cluster, init='k-means++', max_iter=100, n_init=1)
    else:
        raise ValueError
    cluster.fit(X.toarray())

    if verbose:
        print(cluster.labels_)

    cluster_dict = {}
    for idx, label in enumerate(cluster.labels_):
        if label not in cluster_dict.keys():
            cluster_dict[label] = [idx]
        else:
            cluster_dict[label].append(idx)
    return cluster_dict
