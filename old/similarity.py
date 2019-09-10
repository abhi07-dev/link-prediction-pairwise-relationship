from data.parser import get_in_out_dicts
from data.generator import data_path
import numpy as np

def jaccard(set1, set2):
    return len(set1 & set2) / len(set1 | set2)

def common_neighbours(set1, set2):
    return len(set1 & set2)

if __name__ == '__main__':
    inbound, outbound, peers = get_in_out_dicts(data_path)
    np.save("inbound", inbound)
    np.save("outbound", outbound)
    instances = list()

    with open('test-public.txt', 'r') as ins:
        ins.readline()
        for i in range(2000):
            instances.append([int(el) for el in ins.readline().split('\t')])

    undirected = dict()
    for key in inbound:
        undirected[key] = set(inbound[key])
        if key in outbound:
            undirected[key] = undirected[key] | set(outbound[key])



    res = list()
    for id, a, b in instances:
        # non_zero_sim = 0
        jaccard_2 = list()
        if b in inbound:
            for node in inbound[b]:
                jacc_val = jaccard(undirected[node], undirected[a])
                if jacc_val > 0:
                    # non_zero_sim += 1
                    jaccard_2.append(jacc_val)
        if len(jaccard_2) == 0:
            res.append((id, 0))
        else:
            res.append((id, np.max(jaccard_2)))
        # if a in undirected and b in undirected:
        #     common_neighbours = len(undirected[a] & undirected[b])
        #     union = len(undirected[a] | undirected[b])
        # res.append((id, float(common_neighbours) / union))

    _, max_jaccard = max(res, key=lambda x: x[1])
    res = [(id, jaccard_sim / max_jaccard) for id, jaccard_sim in res]

    with open('predict_jaccard_33.csv', 'w+') as pred_file:
        pred_file.write('Id,Prediction\n')
        for id, proba in res:
            pred_file.write(str(id) + ',' + str(proba) + '\n')