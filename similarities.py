import math
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve, inv

"""
Local similarity functions
"""


def local_common_neighbours(a, b, undirect):
    set1 = undirect[a]
    set2 = undirect[b]
    if len(set1) == 0 or len(set2) == 0:
        return 0
    return len(set1 & set2)


def local_jaccard(a, b, undirect):
    set1 = undirect[a]
    set2 = undirect[b]
    if len(set1) == 0 or len(set2) == 0:
        return 0
    return len(set1 & set2) / len(set1 | set2)


def local_cosine(a, b, undirect):
    set1 = undirect[a]
    set2 = undirect[b]
    if len(set1) == 0 or len(set2) == 0:
        return 0
    return len(set1 & set2) / math.sqrt(len(set1) * len(set2))


def local_sorensen(a, b, undirect):
    """
    This index is used mainly for ecological community data
    :param a:
    :param b:
    :param undirect:
    :return:
    """
    set1 = undirect[a]
    set2 = undirect[b]
    if len(set1) == 0 or len(set2) == 0:
        return 0
    return 2 * len(set1 & set2) / (len(set1) + len(set2))


def local_hub_promoted(a, b, undirect):
    """
    Under this measurement, the links adjacent to hubs are likely to be assigned
    high scores since the denominator is determined by the lower degree only.
    :param a:
    :param b:
    :param undirect:
    :return:
    """
    set1 = undirect[a]
    set2 = undirect[b]
    if len(set1) == 0 or len(set2) == 0:
        return 0
    return len(set1 & set2) / min(len(set1), len(set2))


def local_hub_depressed(a, b, undirect):
    """
    Under this measurement, the links adjacent to hubs are likely to be assigned
    high scores since the denominator is determined by the lower degree only.
    :param a:
    :param b:
    :param undirect:
    :return:
    """
    set1 = undirect[a]
    set2 = undirect[b]
    if len(set1) == 0 or len(set2) == 0:
        return 0
    return len(set1 & set2) / max(len(set1), len(set2))


def local_leight_holme_newman(a, b, undirect):
    """
    This index assigns high similarity to node pairs that have many common neighbors
    compared not to the possible maximum, but to the expected number of such neighbors.
    :param a:
    :param b:
    :param undirect:
    :return:
    """
    set1 = undirect[a]
    set2 = undirect[b]
    if len(set1) == 0 or len(set2) == 0:
        return 0
    return len(set1 & set2) / (len(set1) * len(set2))


def local_preferential_attachment(a, b, undirect):
    """
    The mechanism of preferential attachment can be used to generate evolving scale-free
    networks, where the probability that a new link is connected to the node x is proportional to neigh(x).size
    :param a:
    :param b:
    :param undirect:
    :return:
    """
    set1 = undirect[a]
    set2 = undirect[b]
    if len(set1) == 0 or len(set2) == 0:
        return 0
    return len(set1 & set2) / (len(set1) * len(set2))


def local_adamic_adar(a, b, undirect):
    """
    This index refines the simple counting of common neighbors by
    assigning the less-connected neighbors more weight
    :param a:
    :param b:
    :param undirect:
    :return:
    """
    set1 = undirect[a]
    set2 = undirect[b]
    if len(set1) == 0 or len(set2) == 0:
        return 0

    result = 0
    for node in set1 & set2:
        result += 1 / math.log2(len(undirect[node]))

    return result


def local_resource_allocation(a, b, undirect):
    """
    Consider a pair of nodes, x and y, which are not directly connected.
    The node x can send some resource to y, with their common neighbors
    playing the role of transmitters. In the simplest case, we assume
    that each transmitter has a unit of resource, and will equally
    distribute it to all its neighbors.
    :param a:
    :param b:
    :param undirect:
    :return:
    """
    set1 = undirect[a]
    set2 = undirect[b]
    if len(set1) == 0 or len(set2) == 0:
        return 0

    result = 0
    for node in set1 & set2:
        result += 1 / len(undirect[node])

    return result


# def local_triadic(node1, node2, inbound, outbound, undirected):
#     if len(undirected[node1]) == 0 or len(undirected[node1]) == 0:
#         return 0
#     xs = undirected[node1] | undirected[node2]
#     for x in xs:
#
# def get_triad_index(A, B, X, outbound):
#     if A in outbound and B in outbound and X in outbound and \
#             B in outbound[A] and X in outbound[A] and \
#             A in outbound[B] and X in outbound[B] and \
#             A in outbound[X] and B in outbound[X]:
#         return 13
#     elif is_one_way_connected(A, B, outbound) and is_two_way_connected(A, X, outbound) and is_two_way_connected(B, X, outbound) or \
#         is_two_way_connected(A, B, outbound) and is_one_way_connected(A, X, outbound) and is_two_way_connected(B, X, outbound) or \
#         is_two_way_connected(A, B, outbound) and is_two_way_connected(A, X, outbound) and is_one_way_connected(B, X, outbound):
#         return 12
#     elif
#
# def is_two_way_connected(A, B, outbound):
#     return A in outbound and B in outbound and A in outbound[B] and B in outbound[A]
#
# def is_one_way_connected(A, B, outbound):
#     if is_two_way_connected(A, B, outbound):
#         return False
#     if A in outbound and B in outbound[A]:
#         return True
#     if B in outbound and A in outbound[B]:
#         return True
#     return False

"""
Global similarity functions
"""


def global_katz(node1, node2, adj_matrix, beta=0.5, depth=2):
    """
    This index is based on the ensemble of all paths, which
    directly sums over the collection of paths and is exponentially damped by
    length to give the shorter paths more weights.
    :param node1:
    :param node2:
    :param adj_matrix:
    :param beta: beta coefficient in Katz similarity
    :param depth: how many times to iterate
    :return:
    """

    # 1st way
    # coef = beta
    # matrix = adj_matrix
    # result = coef * matrix[node1, node2]
    # np.dot(adj_matrix, adj_matrix)
    # for i in range(1, depth):
    #     coef *= beta
    #     matrix = np.dot(matrix, adj_matrix)
    #     result += coef * matrix[node1, node2]
    # return result

    # 2nd way
    I = csr_matrix(np.eye(adj_matrix.shape[0]))
    try:
        katz = inv(I - adj_matrix * beta) - I
        print("Katz is successfully calculated with matrix.shape =", adj_matrix.shape)
        return katz[node1, node2]
    except:
        print(adj_matrix)
        print("Quitting from Katz when matrix shape is", adj_matrix.shape)
        exit()


def global_edgerank(node1, node2, w_adj_matrix, d=0.5, w=1, depth=2):
    """
    The single highest-scoring feature found was termed
    EdgeRank and had an AUC of 0.926. This feature was
    a rooted PageRank (see [12]) over a weighted undirected
    adjacency matrix of the graph
    :param node1:
    :param node2:
    :param w_adj_matrix: weighted adjacency matrix
    :param d: random exploration probability
    :param w: weight to
    :param depth: how many times to iterate
    :return:
    """
    x = np.zeros(w_adj_matrix.shape[0])
    x[node1] = 1
    for i in range(depth):
        x = (1 - d) * x + d * (w_adj_matrix + csr_matrix.transpose(w_adj_matrix) * w) @ x
    print("Edgerank is successfully calculated with matrix.shape =", w_adj_matrix.shape)
    return x[node2]
