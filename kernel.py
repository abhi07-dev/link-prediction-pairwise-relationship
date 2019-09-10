import numpy as np
import pickle
from similarities import *
from scipy.sparse import csr_matrix
import pandas as pd

DATA_PATH = "data/"
INBOUND_FILENAME = DATA_PATH + "inbound.gpickle"
OUTBOUND_FILENAME = DATA_PATH + "outbound.gpickle"
TRAIN_FILE = DATA_PATH + 'train.txt'
TEST_FILE = DATA_PATH + 'test-public.txt'
TEST_SIZE = 2000
TEST_FEATURES = DATA_PATH + 'features.csv'


class Kernel:
    def __init__(self):
        if not np.DataSource().exists(INBOUND_FILENAME):
            self._parse_raw_data()
        else:
            with open(INBOUND_FILENAME, 'rb') as inbound_file:
                self.inbound = pickle.load(inbound_file)
            with open(OUTBOUND_FILENAME, 'rb') as outbound_file:
                self.outbound = pickle.load(outbound_file)

        # Building undirect dict
        self.undirect = dict()
        for key in self.inbound:
            self.undirect[key] = self.inbound[key]
            if key in self.outbound:
                self.undirect[key] |= self.outbound[key]


    def _parse_raw_data(self):
        print("Parsing from raw data")
        num_lines = sum(1 for line in open(TRAIN_FILE, "r"))
        trainFile = open(TRAIN_FILE, "r")
        self.inbound = dict()
        self.outbound = dict()

        for i in range(num_lines):
            line = trainFile.readline()
            nodes = line.split("\t")
            base = int(nodes[0])
            self.outbound[base] = set()

            for j in range(1, len(nodes)):
                outer = int(nodes[j])
                self.outbound[base].add(outer)
                self.inbound.setdefault(outer, set()).add(base)

        print("Start saving as files")
        with open(INBOUND_FILENAME, 'wb') as inbound_file:
            pickle.dump(self.inbound, inbound_file, pickle.HIGHEST_PROTOCOL)
        with open(OUTBOUND_FILENAME, 'wb') as outbound_file:
            pickle.dump(self.outbound, outbound_file, pickle.HIGHEST_PROTOCOL)

    def parse_test_instances(self):
        """
        Reads test file and returns list of instances
        :return: list of (Id, A, B)
        """
        instances = list()
        with open(TEST_FILE, 'r') as ins:
            ins.readline()
            for i in range(TEST_SIZE):
                id, a, b = [int(el) for el in ins.readline().split('\t')]

                instances.append((id, a, b))
        return instances

    def _find_index(self, long_list, el):
        low = 0
        high = len(long_list)-1
        while low <= high:
            mid = (low + high) // 2
            if el > long_list[mid]:
                low = mid + 1
            elif el < long_list[mid]:
                high = mid - 1
            else:
                return mid
        return -1

    def get_direct_adjacency_matrix(self, a_node, b_node):
        """
        Computes adjacency matrix for subgraph
        which includes only A, B and neighbours of them.
        Use it for Katz similarity
        :param a_node: node
        :param b_node: node
        :return: matrix, A_matrixId, B_matrixID
        """
        neighbours = {a_node, b_node}
        neighbours |= self.undirect[a_node] | self.undirect[b_node]
        neighbours = sorted(neighbours)
        sz = len(neighbours)
        if sz == 0:
            return None, None, None

        # result = np.zeros((sz, sz))
        row = list()
        col = list()
        data = list()

        for i in range(sz):
            nodex = neighbours[i]
            if nodex in self.outbound:
                for nodey in self.outbound[nodex]:
                    if nodey in neighbours:
                        j = self._find_index(neighbours, nodey)
                        data.append(1)
                        row.append(i)
                        col.append(j)
        result = csr_matrix((data, (row, col)), shape=(sz, sz))
        return result, self._find_index(neighbours, a_node), self._find_index(neighbours, b_node)

    def get_direct_weighted_matrix(self, a_node, b_node):
        """
        Computes weighted adjacency matrix for subgraph
        which includes only A, B and neighbours of them.
        Use it for Edgerank.
        :param a_node: node
        :param b_node: node
        :return: matrix, A_matrixId, B_matrixID
        """
        neighbours = {a_node, b_node}
        neighbours |= self.undirect[a_node] | self.undirect[b_node]
        neighbours = sorted(neighbours)
        sz = len(neighbours)
        if sz == 0:
            return None, None, None

        # result = np.zeros((sz, sz))
        row = list()
        col = list()
        data = list()

        for i in range(sz):
            nodex = neighbours[i]
            w = 0
            if nodex in self.outbound and len(self.outbound[nodex]) > 0:
                w = 1. / len(self.outbound[nodex])
                for nodey in self.outbound[nodex]:
                    if nodey in neighbours:
                        j = self._find_index(neighbours, nodey)
                        data.append(w)
                        row.append(i)
                        col.append(j)
        result = csr_matrix((data, (row, col)), shape=(sz, sz))
        return result, self._find_index(neighbours, a_node), self._find_index(neighbours, b_node)


    def apply_2(self, sim_function, a, b):
        sim_list = list()
        if a in self.outbound:
            for node in self.outbound[a]:
                sim_val = sim_function(node, b, self.undirect)
                if sim_val > 0:
                    sim_list.append(sim_val)
        if len(sim_list) == 0:
            return 0
        return np.mean(sim_list)

    def apply_3(self, sim_function, a, b):
        sim_list = list()
        if b in self.inbound:
            for node in self.inbound[b]:
                sim_val = sim_function(node, a, self.undirect)
                if sim_val > 0:
                    sim_list.append(sim_val)
        if len(sim_list) == 0:
            return 0
        return np.mean(sim_list)


if __name__ == '__main__':
    kernel = Kernel()
    instances = kernel.parse_test_instances()
    ins_feat = list()
    for id, a, b in instances:
        features = {
            'id': id,
            'common_neighbours_1': local_common_neighbours(a, b, kernel.undirect),
            'common_neighbours_2': kernel.apply_2(local_common_neighbours, a, b),
            'common_neighbours_3': kernel.apply_3(local_common_neighbours, a, b),
            'jaccard_1': local_jaccard(a, b, kernel.undirect),
            'jaccard_2': kernel.apply_2(local_jaccard, a, b),
            'jaccard_3': kernel.apply_3(local_jaccard, a, b),
            'cosine_1': local_cosine(a, b, kernel.undirect),
            'cosine_2': kernel.apply_2(local_cosine, a, b),
            'cosine_3': kernel.apply_3(local_cosine, a, b),
            'sorensen_1': local_sorensen(a, b, kernel.undirect),
            'sorensen_2': kernel.apply_2(local_sorensen, a, b),
            'sorensen_3': kernel.apply_3(local_sorensen, a, b),
            'hub_promoted_1': local_hub_promoted(a, b, kernel.undirect),
            'hub_promoted_2': kernel.apply_2(local_hub_promoted, a, b),
            'hub_promoted_3': kernel.apply_3(local_hub_promoted, a, b),
            'hub_depressed_1': local_hub_depressed(a, b, kernel.undirect),
            'hub_depressed_2': kernel.apply_2(local_hub_depressed, a, b),
            'hub_depressed_3': kernel.apply_3(local_hub_depressed, a, b),
            'preferential_attachment_1': local_preferential_attachment(a, b, kernel.undirect),
            'preferential_attachment_2': kernel.apply_2(local_preferential_attachment, a, b),
            'preferential_attachment_3': kernel.apply_3(local_preferential_attachment, a, b),
            'adamic_adar': local_adamic_adar(a, b, kernel.undirect),
            'resource_allocation': local_resource_allocation(a, b, kernel.undirect)
        }
        a_matrix, a_mat_id, b_mat_id = kernel.get_direct_adjacency_matrix(a, b)
        if a_matrix is not None:
            features['katz'] = global_katz(a_mat_id, b_mat_id, a_matrix)
        else:
            features['katz'] = 0

        w_matrix, a_mat_id, b_mat_id = kernel.get_direct_weighted_matrix(a, b)
        if w_matrix is not None:
            features['edgerank'] = global_edgerank(a_mat_id, b_mat_id, w_matrix)
        else:
            features['edgerank'] = 0
        ins_feat.append(features)
        print("Instance " + str(id) + " is done!")
    df = pd.DataFrame(ins_feat)
    df.to_csv(TEST_FEATURES)





