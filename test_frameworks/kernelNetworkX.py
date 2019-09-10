import networkx as nx
import os

DIRECT_GRAPH_PATH = "direct.gpickle"
UNDIRECT_GRAPH_PATH = "undirect.gpickle"
DATA_PATH = "../../data_smile/"

class Kernel:
    def __init__(self):
        if not os.path.exists(DIRECT_GRAPH_PATH):
            self._parse_from_raw_data()
        else:
            self.digraph = nx.read_gpickle(DIRECT_GRAPH_PATH)
            self.ugraph = nx.read_gpickle(UNDIRECT_GRAPH_PATH)


    def _parse_from_raw_data(self):
        train_path = DATA_PATH + 'train.txt'
        num_lines = sum(1 for line in open(train_path, "r"))
        trainFile = open(train_path, "r")
        self.digraph = nx.DiGraph()

        for i in range(num_lines):
            line = trainFile.readline()
            nodes = line.split("\t")
            base = int(nodes[0])
            for j in range(1, len(nodes)):
                self.digraph.add_edge(base, int(nodes[j]))
        self.ugraph = self.digraph.to_undirected()
        nx.write_gpickle(self.digraph, DIRECT_GRAPH_PATH)
        nx.write_gpickle(self.ugraph, UNDIRECT_GRAPH_PATH)

if __name__ == '__main__':
    kernel = Kernel()