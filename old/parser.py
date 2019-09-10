def get_in_out_dicts(data_path):
    train_path = data_path + 'train.txt'
    trainFile = open(train_path, "r")
    num_lines = sum(1 for line in open(train_path, "r"))
    outerEdges = dict()
    innerEdges = dict()
    undirect = dict()
    peers = list()
    # numberOfEdges = 0

    for i in range(num_lines):
        line = trainFile.readline()
        nodes = line.split("\t")
        # print(nodes)
        # exit()
        base = int(nodes[0])
        outerEdges[base] = list()
        undirect[base] = set()
        for j in range(1, len(nodes)):
            # numberOfEdges += 1
            outer = int(nodes[j])
            outerEdges[base].append(outer)
            undirect[base].add(outer)

            innerEdges.setdefault(outer, []).append(base)
            peers.append((base, outer))
            undirect.setdefault(outer, set()).add(base)
    return (innerEdges, outerEdges, undirect)


if __name__ == '__main__':
    inbound, outbound, peers = get_in_out_dicts()
    print('Inbound:', len(inbound))
    print('Outbound:', len(outbound))
