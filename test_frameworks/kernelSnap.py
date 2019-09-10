import snap
import os

DIRECT_GRAPH_PATH = "direct.graph"
UNDIRECT_GRAPH_PATH = "undirect.graph"
DATA_PATH = "../../data_smile/"

class Kernel:
    def __init__(self):
        if not os.path.exists(DIRECT_GRAPH_PATH):
            self._parse_from_raw_data()
        else:
            self.digraph = snap.TFIn(DIRECT_GRAPH_PATH)
            self.ugraph = snap.TFIn(UNDIRECT_GRAPH_PATH)


    def _parse_from_raw_data(self):
        train_path = DATA_PATH + 'train.txt'
        num_lines = sum(1 for line in open(train_path, "r"))
        trainFile = open(train_path, "r")
        self.digraph = snap.TNGraph.New()

        for i in range(num_lines):
            line = trainFile.readline()
            nodes = line.split("\t")
            base = int(nodes[0])
            if not self.digraph.IsNode(base):
                self.digraph.AddNode(base)
            for j in range(1, len(nodes)):
                node = int(nodes[j])
                if not self.digraph.IsNode(node):
                    self.digraph.AddNode(node)
                self.digraph.AddEdge(base, node)
        self.ugraph = snap.ConvertGraphMP(snap.PUNGraph, self.digraph)

        self.digraph.save(snap.TFOut(DIRECT_GRAPH_PATH))
        self.ugraph.save(snap.TFOut(UNDIRECT_GRAPH_PATH))

if __name__ == '__main__':
    kernel = Kernel()